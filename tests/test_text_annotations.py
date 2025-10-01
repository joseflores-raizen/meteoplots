#!/usr/bin/env python3
"""
Test script to demonstrate the text annotation functionality in meteoplots.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np
import xarray as xr
from meteoplots.plots import plot_contourf_from_xarray

# Create sample data
lon = np.linspace(-10, 10, 20)
lat = np.linspace(30, 50, 15)
lon_grid, lat_grid = np.meshgrid(lon, lat)

# Create a temperature-like field
temperature = 15 + 10 * np.sin(lon_grid * np.pi / 10) * np.cos(lat_grid * np.pi / 20) + np.random.normal(0, 2, lon_grid.shape)

# Create xarray dataset
ds = xr.Dataset({
    'temperature': (['latitude', 'longitude'], temperature)
}, coords={
    'longitude': lon,
    'latitude': lat
})

# Define text annotations
texts = [
    {'text': 'High Temp Zone', 'lon': 5, 'lat': 40, 'fontsize': 14, 'color': 'red', 'weight': 'bold'},
    {'text': 'Low Temp Zone', 'lon': -5, 'lat': 35, 'fontsize': 12, 'color': 'blue'},
    {'text': 'Center', 'lon': 0, 'lat': 40, 'bbox': {'boxstyle': 'round', 'facecolor': 'white', 'alpha': 0.8}}
]

print("Testing text annotation functionality...")

try:
    # Test the contourf function with text annotations
    fig, ax = plot_contourf_from_xarray(
        ds['temperature'],
        plot_var_colorbar='temperature',  # Use predefined colorbar
        title='Temperature with Text Annotations',
        colorbar_title='Temperature (°C)',
        texts=texts,
        savefigure={'save': True, 'format': 'png', 'filename': 'test_text_annotations'},
        path_save='./tmp/plots/'
    )
    
    print("✓ Text annotation functionality is working correctly!")
    print("✓ Plot saved successfully with text annotations")
    
except Exception as e:
    print(f"✗ Error testing text annotations: {e}")
    import traceback
    traceback.print_exc()

print("Test completed.")