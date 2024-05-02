#WFC

This script demonstrates the Wave Function Collapse (WFC) algorithm implemented in Python. WFC is a technique used for procedural generation, particularly in generating tile-based patterns while adhering to certain local constraints. 

The script defines a class `WaveFunctionCollapse` which encapsulates the WFC algorithm. It takes in a set of tiles and corresponding adjacency rules as input and generates a tile map based on those rules.

Usage:

1. Define tiles and adjacency rules:
    - `tiles`: Dictionary mapping integer values to symbols representing different tile types.
    - `tiles_rule`: Dictionary mapping relative positions to sets of compatible tiles based on adjacency rules.

2. Initialize the `WaveFunctionCollapse` object:
    - `a = WaveFunctionCollapse(tiles, tiles_rule, map_size=(10, 10))`: Create an instance of the `WaveFunctionCollapse` class with specified tiles, adjacency rules, and map size.

3. Run the WFC algorithm:
    - `a.run()`: Execute the WFC algorithm to generate the tile map.

4. Visualize the generated tile map:
    - `a.plot_tile()`: Print the generated tile map.