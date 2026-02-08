"""
Your solution: a permutation of 0-96.

Each position in the list represents the layer position in the reconstructed model.
The value at that position is which piece (piece_N.pth) goes there.

Example: If SOLUTION[0] = 42, then piece_42.pth is the first layer.

The model structure:
- 48 Block modules (each has inp: 48->96 and out: 96->48 layers)
- 1 LastLayer (48->1) - this is piece_85.pth

Total: 97 pieces to arrange in the correct order.
"""

SOLUTION = [
    # Fill in your 97 numbers here (0-96), comma-separated
    # Example: 0, 1, 2, 3, ..., 96
]
