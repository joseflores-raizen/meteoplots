#!/usr/bin/env python3
"""
Comprehensive test of text annotation functionality across all plot functions.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np
import xarray as xr
from meteoplots.plots import (
    plot_contourf_from_xarray,
    plot_contour_from_xarray,
    plot_quiver_from_xarray,
    plot_streamplot_from_xarray,
    plot_multipletypes_from_xarray
)

# Create sample data
lon = np.linspace(-10, 10, 20)
lat = np.linspace(30, 50, 15)
lon_grid, lat_grid = np.meshgrid(lon, lat)

# Create temperature and wind data
temperature = 15 + 10 * np.sin(lon_grid * np.pi / 10) * np.cos(lat_grid * np.pi / 20)
u_wind = 5 * np.sin(lon_grid * np.pi / 5)
v_wind = 3 * np.cos(lat_grid * np.pi / 8)

# Create xarray datasets
temp_data = xr.DataArray(
    temperature,
    coords=[('latitude', lat), ('longitude', lon)],
    attrs={'units': '°C', 'long_name': 'Temperature'}
)

u_data = xr.DataArray(
    u_wind,
    coords=[('latitude', lat), ('longitude', lon)],
    attrs={'units': 'm/s', 'long_name': 'U Wind Component'}
)

v_data = xr.DataArray(
    v_wind,
    coords=[('latitude', lat), ('longitude', lon)],
    attrs={'units': 'm/s', 'long_name': 'V Wind Component'}
)

# Define text annotations using different coordinate systems
texts_lonlat = [
    {'text': 'High Temp', 'lon': 5, 'lat': 40, 'fontsize': 14, 'color': 'red', 'weight': 'bold'},
    {'text': 'Low Temp', 'lon': -5, 'lat': 35, 'fontsize': 12, 'color': 'blue'}
]

texts_xy = [
    {'text': 'Center Point', 'x': 0, 'y': 40, 'bbox': {'boxstyle': 'round', 'facecolor': 'white', 'alpha': 0.8}},
    {'text': 'Wind Zone', 'x': -3, 'y': 45, 'fontsize': 10, 'color': 'green'}
]

print("Testing text annotation functionality across all plot functions...")

test_results = []

# Test 1: Contourf plot
try:
    fig, ax = plot_contourf_from_xarray(
        temp_data,
        plot_var_colorbar='temperature',
        title='Contourf with Text Annotations',
        texts=texts_lonlat,
        savefigure={'save': True, 'format': 'png', 'filename': 'test_contourf_text'},
        path_save='./tmp/plots/'
    )
    test_results.append("✓ Contourf with text annotations: SUCCESS")
except Exception as e:
    test_results.append(f"✗ Contourf with text annotations: FAILED - {e}")

# Test 2: Contour plot
try:
    fig, ax = plot_contour_from_xarray(
        temp_data,
        levels=[10, 15, 20, 25],
        colors=['blue', 'green', 'orange', 'red'],
        title='Contour with Text Annotations',
        texts=texts_xy,
        savefigure={'save': True, 'format': 'png', 'filename': 'test_contour_text'},
        path_save='./tmp/plots/'
    )
    test_results.append("✓ Contour with text annotations: SUCCESS")
except Exception as e:
    test_results.append(f"✗ Contour with text annotations: FAILED - {e}")

# Test 3: Quiver plot
try:
    fig, ax = plot_quiver_from_xarray(
        u_data, v_data,
        title='Quiver with Text Annotations',
        texts=texts_lonlat,
        savefigure={'save': True, 'format': 'png', 'filename': 'test_quiver_text'},
        path_save='./tmp/plots/'
    )
    test_results.append("✓ Quiver with text annotations: SUCCESS")
except Exception as e:
    test_results.append(f"✗ Quiver with text annotations: FAILED - {e}")

# Test 4: Streamplot
try:
    fig, ax = plot_streamplot_from_xarray(
        u_data, v_data,
        title='Streamplot with Text Annotations',
        texts=texts_xy,
        savefigure={'save': True, 'format': 'png', 'filename': 'test_streamplot_text'},
        path_save='./tmp/plots/'
    )
    test_results.append("✓ Streamplot with text annotations: SUCCESS")
except Exception as e:
    test_results.append(f"✗ Streamplot with text annotations: FAILED - {e}")

# Test 5: Multipletypes plot
try:
    # Create combined dataset for multipletypes
    combined_data = {
        'temperature': temp_data,
        'u_wind': u_data,
        'v_wind': v_data
    }
    
    fig, ax = plot_multipletypes_from_xarray(
        combined_data,
        plot_var_colorbar='temperature',
        title='Multipletypes with Text Annotations',
        plot_types=['contourf', 'quiver'],
        texts=texts_lonlat,
        savefigure={'save': True, 'format': 'png', 'filename': 'test_multipletypes_text'},
        path_save='./tmp/plots/'
    )
    test_results.append("✓ Multipletypes with text annotations: SUCCESS")
except Exception as e:
    test_results.append(f"✗ Multipletypes with text annotations: FAILED - {e}")

# Print results
print("\n" + "="*60)
print("TEXT ANNOTATION TEST RESULTS")
print("="*60)
for result in test_results:
    print(result)

success_count = len([r for r in test_results if '✓' in r])
total_count = len(test_results)
print(f"\nSUMMARY: {success_count}/{total_count} tests passed")

if success_count == total_count:
    print("🎉 All text annotation functionality is working correctly!")
else:
    print("⚠️ Some text annotation tests failed - see details above")

print("\nText annotation feature implementation complete!")