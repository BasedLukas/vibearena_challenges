#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from datetime import timedelta
from pathlib import Path
from typing import Any

from sentry.runner import configure

configure()

from django.utils import timezone

from sentry import roles
from sentry.models import (
    Group,
    Organization,
    OrganizationMember,
    OrganizationMemberTeam,
    Project,
    SavedSearch,
    Team,
)
from sentry.models.savedsearch import SortOptions, Visibility
from sentry.models.search_common import SearchType
from sentry.services.organization import organization_provisioning_service
from sentry.users.models.user import User


@dataclass
class SeedContext:
    primary_org: Organization
    secondary_org: Organization
    users: dict[str, User]
    teams: dict[str, Team]
    projects: dict[str, Project]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Seed Sentry interview challenge data.")
    parser.add_argument(
        "--seed-file",
        type=Path,
        required=True,
        help="Path to challenge seed JSON file.",
    )
    return parser.parse_args()


def load_seed(seed_file: Path) -> dict[str, Any]:
    with seed_file.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def ensure_organization(slug: str, name: str) -> Organization:
    organization, created = Organization.objects.get_or_create(slug=slug, defaults={"name": name})
    if organization.name != name:
        organization.name = name
        organization.save(update_fields=["name"])
    if created:
        # Keep control silo organization mapping in sync when org is created directly.
        organization_provisioning_service.change_organization_slug(
            organization_id=organization.id, slug=organization.slug
        )
        organization.handle_async_replication(organization.id)
    return organization


def ensure_user(username: str, email: str, password: str, is_superuser: bool = False) -> User:
    user = User.objects.filter(username=username).first()
    if user is None:
        user = User.objects.create_user(username=username, email=email, password=password)
    else:
        changed = False
        if user.email != email:
            user.email = email
            changed = True
        user.set_password(password)
        changed = True
        if changed:
            user.save()

    if is_superuser and not user.is_superuser:
        user.is_superuser = True
        user.is_staff = True
        user.save(update_fields=["is_superuser", "is_staff"])

    return user


def ensure_member(
    organization: Organization,
    user: User,
    role_id: str,
    team_slugs: list[str],
    all_teams: dict[str, Team],
) -> OrganizationMember:
    member, _ = OrganizationMember.objects.get_or_create(
        organization=organization,
        user_id=user.id,
        defaults={"role": role_id, "has_global_access": False},
    )

    updates: list[str] = []
    if member.role != role_id:
        member.role = role_id
        updates.append("role")
    if member.has_global_access:
        member.has_global_access = False
        updates.append("has_global_access")
    if updates:
        member.save(update_fields=updates)

    allowed_teams = [all_teams[slug] for slug in team_slugs]
    for team in allowed_teams:
        omt, _ = OrganizationMemberTeam.objects.get_or_create(
            organizationmember=member,
            team=team,
            defaults={"is_active": True},
        )
        if not omt.is_active:
            omt.is_active = True
            omt.save(update_fields=["is_active"])

    OrganizationMemberTeam.objects.filter(
        organizationmember=member, team__organization=organization
    ).exclude(team__in=allowed_teams).update(is_active=False)

    return member


def create_groups(projects: dict[str, Project], groups: list[dict[str, Any]]) -> int:
    now = timezone.now()
    created_or_updated = 0

    for entry in groups:
        project = projects[entry["project"]]
        message = entry["message"]
        first_seen = now - timedelta(minutes=int(entry.get("first_seen_minutes_ago", 120)))
        last_seen = now - timedelta(minutes=int(entry.get("last_seen_minutes_ago", 15)))
        times_seen = int(entry.get("times_seen", 1))

        group, created = Group.objects.get_or_create(
            project=project,
            message=message,
            defaults={
                "culprit": entry.get("culprit"),
                "first_seen": first_seen,
                "last_seen": last_seen,
                "active_at": first_seen,
                "times_seen": times_seen,
                "platform": entry.get("platform", "python"),
                "substatus": None,
            },
        )
        if not created:
            group.first_seen = first_seen
            group.last_seen = last_seen
            group.active_at = first_seen
            group.times_seen = times_seen
            group.platform = entry.get("platform", "python")
            group.substatus = None
            group.save(
                update_fields=[
                    "first_seen",
                    "last_seen",
                    "active_at",
                    "times_seen",
                    "platform",
                    "substatus",
                ]
            )
        created_or_updated += 1

    return created_or_updated


def create_saved_searches(
    organization: Organization, owner: User, searches: list[dict[str, str]]
) -> int:
    SavedSearch.objects.filter(
        organization=organization,
        owner_id=owner.id,
        name__startswith="[Challenge]",
        type=SearchType.ISSUE.value,
    ).delete()

    for entry in searches:
        SavedSearch.objects.create(
            organization=organization,
            owner_id=owner.id,
            type=SearchType.ISSUE.value,
            name=entry["name"],
            query=entry["query"],
            sort=entry.get("sort", SortOptions.DATE),
            visibility=Visibility.OWNER,
        )

    return len(searches)


def build_context(seed: dict[str, Any]) -> SeedContext:
    primary_org = ensure_organization(
        slug=seed["primary_org"]["slug"], name=seed["primary_org"]["name"]
    )
    secondary_org = ensure_organization(
        slug=seed["secondary_org"]["slug"], name=seed["secondary_org"]["name"]
    )

    users: dict[str, User] = {
        "admin@sentry.io": ensure_user(
            username="admin@sentry.io",
            email="admin@sentry.io",
            password="admin",
            is_superuser=True,
        )
    }
    for user_def in seed["users"]:
        users[user_def["username"]] = ensure_user(
            username=user_def["username"],
            email=user_def["email"],
            password=user_def["password"],
            is_superuser=bool(user_def.get("is_superuser", False)),
        )

    teams: dict[str, Team] = {}
    for team_def in seed["teams"]:
        team, _ = Team.objects.get_or_create(
            organization=primary_org,
            slug=team_def["slug"],
            defaults={"name": team_def["name"]},
        )
        if team.name != team_def["name"]:
            team.name = team_def["name"]
            team.save(update_fields=["name"])
        teams[team.slug] = team

    projects: dict[str, Project] = {}
    for project_def in seed["projects"]:
        project, _ = Project.objects.get_or_create(
            organization=primary_org,
            slug=project_def["slug"],
            defaults={"name": project_def["name"]},
        )
        if project.name != project_def["name"]:
            project.name = project_def["name"]
            project.save(update_fields=["name"])

        team = teams[project_def["team"]]
        project.add_team(team)
        projects[project.slug] = project

    shadow_team, _ = Team.objects.get_or_create(
        organization=secondary_org,
        slug=seed["secondary_project"]["team_slug"],
        defaults={"name": seed["secondary_project"]["team_name"]},
    )
    shadow_project, _ = Project.objects.get_or_create(
        organization=secondary_org,
        slug=seed["secondary_project"]["slug"],
        defaults={"name": seed["secondary_project"]["name"]},
    )
    shadow_project.add_team(shadow_team)
    projects[shadow_project.slug] = shadow_project

    owner_user = User.objects.filter(is_superuser=True).first()
    if owner_user is not None:
        ensure_member(
            organization=primary_org,
            user=owner_user,
            role_id=roles.get_top_dog().id,
            team_slugs=list(teams.keys()),
            all_teams=teams,
        )

    for member_def in seed["memberships"]:
        ensure_member(
            organization=primary_org,
            user=users[member_def["username"]],
            role_id=member_def.get("role", roles.get_default().id),
            team_slugs=member_def["teams"],
            all_teams=teams,
        )

    return SeedContext(
        primary_org=primary_org,
        secondary_org=secondary_org,
        users=users,
        teams=teams,
        projects=projects,
    )


def main() -> None:
    args = parse_args()
    seed = load_seed(args.seed_file)

    context = build_context(seed)
    group_count = create_groups(context.projects, seed["groups"])
    search_count = create_saved_searches(
        organization=context.primary_org,
        owner=context.users["candidate_user"],
        searches=seed["saved_searches"],
    )

    print("Challenge seed complete:")
    print(f"  - Primary org: {context.primary_org.slug}")
    print(f"  - Secondary org: {context.secondary_org.slug}")
    print(f"  - Projects seeded: {len(context.projects)}")
    print(f"  - Groups created/updated: {group_count}")
    print(f"  - Candidate saved searches: {search_count}")


if __name__ == "__main__":
    main()
    import os
    import sys

    sys.stdout.flush()
    sys.stderr.flush()
    os._exit(0)
