"""
Pytest configuration and shared fixtures for meteoplots tests.
"""

import pytest
import numpy as np
import xarray as xr
import tempfile
import os
from pathlib import Path
import geopandas as gpd
from shapely.geometry import Polygon


@pytest.fixture
def sample_temperature_data():
    """Create sample temperature data as xarray DataArray."""
    # Create sample lat/lon grid
    lat = np.arange(-35, 10, 0.5)
    lon = np.arange(-75, -30, 0.5)
    
    # Generate synthetic temperature data
    temp_data = 20 + 10 * np.random.random((len(lat), len(lon)))
    
    # Create xarray DataArray
    temperature = xr.DataArray(
        temp_data,
        coords=[('latitude', lat), ('longitude', lon)],
        attrs={'units': '°C', 'long_name': 'Temperature at 2m'}
    )
    
    return temperature


@pytest.fixture
def sample_precipitation_data():
    """Create sample precipitation data as xarray DataArray."""
    lat = np.arange(-35, 10, 0.5)
    lon = np.arange(-75, -30, 0.5)
    
    # Generate synthetic precipitation data (positive values only)
    precip_data = np.random.exponential(5, (len(lat), len(lon)))
    
    precipitation = xr.DataArray(
        precip_data,
        coords=[('latitude', lat), ('longitude', lon)],
        attrs={'units': 'mm', 'long_name': 'Total Precipitation'}
    )
    
    return precipitation


@pytest.fixture
def sample_pressure_data():
    """Create sample pressure data as xarray DataArray."""
    lat = np.arange(-35, 10, 0.5)
    lon = np.arange(-75, -30, 0.5)
    
    # Generate synthetic pressure data around 1013 hPa
    pressure_data = 1013 + 20 * np.random.random((len(lat), len(lon))) - 10
    
    pressure = xr.DataArray(
        pressure_data,
        coords=[('latitude', lat), ('longitude', lon)],
        attrs={'units': 'hPa', 'long_name': 'Sea Level Pressure'}
    )
    
    return pressure


@pytest.fixture
def sample_wind_components():
    """Create sample U and V wind components as xarray DataArrays."""
    lat = np.arange(-35, 10, 0.5)
    lon = np.arange(-75, -30, 0.5)
    
    # Generate synthetic wind components
    u_data = 10 * np.random.random((len(lat), len(lon))) - 5
    v_data = 10 * np.random.random((len(lat), len(lon))) - 5
    
    u_component = xr.DataArray(
        u_data,
        coords=[('latitude', lat), ('longitude', lon)],
        attrs={'units': 'm/s', 'long_name': 'U-component of wind'}
    )
    
    v_component = xr.DataArray(
        v_data,
        coords=[('latitude', lat), ('longitude', lon)],
        attrs={'units': 'm/s', 'long_name': 'V-component of wind'}
    )
    
    return u_component, v_component


@pytest.fixture
def sample_extent():
    """Standard extent for Brazil region."""
    return [-60, -30, -35, 5]  # [lon_min, lon_max, lat_min, lat_max]


@pytest.fixture
def sample_shapefile(tmp_path):
    """Create a temporary shapefile for testing basin analysis."""
    # Create simple polygon geometries
    polygons = [
        Polygon([(-55, -20), (-50, -20), (-50, -15), (-55, -15)]),  # Basin 1
        Polygon([(-50, -25), (-45, -25), (-45, -20), (-50, -20)]),  # Basin 2
    ]
    
    # Create GeoDataFrame
    gdf = gpd.GeoDataFrame({
        'Nome_Bacia': ['Bacia_Norte', 'Bacia_Sul'],
        'Area_km2': [50000, 60000],
        'geometry': polygons
    }, crs='EPSG:4326')
    
    # Save to temporary shapefile
    shapefile_path = tmp_path / "test_bacias.shp"
    gdf.to_file(shapefile_path)
    
    return str(shapefile_path)


@pytest.fixture
def test_output_dir(tmp_path):
    """Create temporary directory for test outputs."""
    output_dir = tmp_path / "test_outputs"
    output_dir.mkdir()
    return str(output_dir)


@pytest.fixture(scope="session")
def matplotlib_backend():
    """Set matplotlib to use Agg backend for testing (no display)."""
    import matplotlib
    matplotlib.use('Agg')
    return matplotlib


class TestDataGenerator:
    """Utility class for generating additional test data."""
    
    @staticmethod
    def create_xarray_with_custom_dims(lat_name='latitude', lon_name='longitude'):
        """Create xarray data with custom dimension names."""
        lat = np.arange(-35, 10, 1.0)
        lon = np.arange(-75, -30, 1.0)
        data = np.random.random((len(lat), len(lon)))
        
        return xr.DataArray(
            data,
            coords=[(lat_name, lat), (lon_name, lon)],
            attrs={'units': 'test_units', 'long_name': 'Test Data'}
        )
    
    @staticmethod
    def create_invalid_colorbar_data():
        """Create data that should trigger colorbar validation errors."""
        lat = np.arange(-35, 10, 1.0)
        lon = np.arange(-75, -30, 1.0)
        data = np.random.random((len(lat), len(lon)))
        
        return xr.DataArray(
            data,
            coords=[('latitude', lat), ('longitude', lon)],
            attrs={'units': 'invalid_units', 'long_name': 'Invalid Test Data'}
        )


@pytest.fixture
def data_generator():
    """Provide TestDataGenerator instance."""
    return TestDataGenerator()


# Utility function for tests
def assert_figure_created(fig):
    """Assert that a matplotlib figure was created properly."""
    assert fig is not None
    assert hasattr(fig, 'axes')
    assert len(fig.axes) > 0


def assert_plot_has_data(ax):
    """Assert that a plot axis contains some data."""
    assert ax is not None
    # Check if there are any collections (for contourf) or lines (for contour)
    has_collections = len(ax.collections) > 0
    has_lines = len(ax.lines) > 0
    has_patches = len(ax.patches) > 0
    
    assert has_collections or has_lines or has_patches, "Plot should contain some visual elements"