import numpy as np
import pyvista as pv
from scipy.spatial import Voronoi

# Parameters
cube_size = 1.0       # Side length of the cube
num_grains = 100       # Number of grains (random seeds)

# Generate random seed points within the cube
np.random.seed(42)  # For reproducibility
seed_points = np.random.rand(num_grains, 3) * cube_size

# Compute Voronoi tessellation for the seeds
vor = Voronoi(seed_points)

# Define the cube boundary
cube = pv.Cube(bounds=(0, cube_size, 0, cube_size, 0, cube_size))

# Create a PyVista MultiBlock to store grains
grains = pv.MultiBlock()

# Loop through Voronoi regions
for region_idx, region in enumerate(vor.regions):
    if not -1 in region and len(region) > 0:  # Skip invalid or open regions
        vertices = vor.vertices[region]  # Vertices of the grain boundary
        try:
            # Create a PyVista PolyData for the Voronoi cell
            grain = pv.PolyData(vertices).convex_hull()
            # Clip the grain to the cube boundaries
            grain = grain.clip_box(bounds=(0, cube_size, 0, cube_size, 0, cube_size), invert=False)
            # Add the clipped grain to the MultiBlock dataset
            grains.append(grain)
        except:
            continue  # Skip problematic regions

# Assign random colors to each grain
colors = np.random.randint(0, 255, (len(grains), 3))

# Create a PyVista plotter
plotter = pv.Plotter()
#for idx, grain in enumerate(grains):
#    plotter.add_mesh(grain, color=colors[idx] / 255, show_edges=True)
#plotter.add_points(seed_points, color='black', point_size=8, render_points_as_spheres=True, label='Seeds')
#plotter.show()
for grain, color in zip(grains, colors):
    plotter.add_mesh(grain, color=color / 255, show_edges=True)
plotter.add_points(seed_points, color='black', point_size=8, render_points_as_spheres=True, label='Seeds')
plotter.show()

