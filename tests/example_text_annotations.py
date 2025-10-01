"""
Example usage of text annotations in meteoplots functions.
"""

import numpy as np
import xarray as xr
from meteoplots.plots import plot_contourf_from_xarray, plot_quiver_from_xarray

def test_text_annotations():
    """Demonstrate text annotation functionality."""
    
    # Create sample data
    lons = np.linspace(-60, -40, 20)
    lats = np.linspace(-30, -10, 15)
    temp_data = 20 + 10 * np.random.random((15, 20))
    
    # Create xarray DataArray
    temperature = xr.DataArray(
        temp_data,
        coords={'latitude': lats, 'longitude': lons},
        dims=['latitude', 'longitude'],
        name='temperature'
    )
    
    # Example 1: Simple text annotations
    simple_texts = [
        {'x': -55, 'y': -25, 'text': 'City A'},
        {'x': -45, 'y': -20, 'text': 'City B'},
        {'x': -50, 'y': -15, 'text': 'City C'}
    ]
    
    # Example 2: Styled text annotations
    styled_texts = [
        {
            'x': -55, 'y': -25, 'text': 'High Temp Zone',
            'fontsize': 14, 'color': 'red', 'fontweight': 'bold'
        },
        {
            'x': -45, 'y': -20, 'text': 'Medium Zone',
            'fontsize': 12, 'color': 'orange', 'rotation': 45
        },
        {
            'x': -50, 'y': -15, 'text': 'Low Zone',
            'fontsize': 10, 'color': 'blue', 'ha': 'left',
            'bbox': {'boxstyle': 'round', 'facecolor': 'yellow', 'alpha': 0.5}
        }
    ]
    
    print("Creating plot with simple text annotations...")
    fig, ax = plot_contourf_from_xarray(
        xarray_data=temperature,
        plot_var_colorbar='temperature',
        title='Temperature with Simple Text Labels',
        texts=simple_texts,
        extent=[-60, -40, -30, -10],
        figsize=(10, 8),
        path_save='./tmp/plots',
        output_filename='temperature_with_simple_texts.png'
    )
    
    print("Creating plot with styled text annotations...")
    fig, ax = plot_contourf_from_xarray(
        xarray_data=temperature,
        plot_var_colorbar='temperature',
        title='Temperature with Styled Text Labels',
        texts=styled_texts,
        extent=[-60, -40, -30, -10],
        figsize=(10, 8),
        # Global text styling defaults
        text_fontsize=11,
        text_color='darkblue',
        text_fontweight='normal',
        path_save='./tmp/plots',
        output_filename='temperature_with_styled_texts.png'
    )
    
    print("Text annotation examples completed!")

if __name__ == "__main__":
    test_text_annotations()