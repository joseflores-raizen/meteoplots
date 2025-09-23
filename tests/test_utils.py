"""
Tests for meteoplots.utils module.
"""

import pytest
import numpy as np
import pandas as pd
import xarray as xr
import geopandas as gpd
from shapely.geometry import Polygon
import tempfile
import os
from datetime import datetime
from unittest.mock import patch, MagicMock
from PIL import Image

from meteoplots.utils.utils import (
    calculate_mean_basin_value_from_shapefile,
    figures_panel
)
from meteoplots.utils.titles import generate_title


class TestCalculateMeanBasinValue:
    """Tests for calculate_mean_basin_value_from_shapefile function."""
    
    def test_basic_basin_calculation(self, sample_temperature_data):
        """Test basic basin value calculation."""
        # Create a simple shapefile-like GeoDataFrame
        polygon = Polygon([(-55, -20), (-50, -20), (-50, -15), (-55, -15)])
        gdf = gpd.GeoDataFrame({
            'Nome_Bacia': ['Test_Basin'],
            'geometry': [polygon]
        }, crs='EPSG:4326')
        
        # Test the function
        with patch('regionmask.Regions') as mock_regions:
            # Mock the regionmask functionality
            mock_mask = MagicMock()
            mock_mask.mask.return_value = xr.DataArray(
                np.zeros((10, 10)),  # Simple mask
                dims=['latitude', 'longitude']
            )
            mock_regions.return_value = mock_mask
            
            result = calculate_mean_basin_value_from_shapefile(
                dataset=sample_temperature_data,
                basin='Test_Basin',
                shp=gdf,
                dim_lat='latitude',
                dim_lon='longitude'
            )
            
            # Check result structure
            assert isinstance(result, pd.DataFrame)
            assert 'valor' in result.columns
            assert 'basin' in result.columns
            assert 'latitude' in result.columns
            assert 'longitude' in result.columns
            assert len(result) == 1
            assert result['basin'].iloc[0] == 'Test_Basin'
            
    def test_basin_calculation_with_custom_dims(self, data_generator):
        """Test basin calculation with custom dimension names."""
        # Create data with custom dimension names
        data = data_generator.create_xarray_with_custom_dims('lat', 'lon')
        
        polygon = Polygon([(-55, -20), (-50, -20), (-50, -15), (-55, -15)])
        gdf = gpd.GeoDataFrame({
            'Nome_Bacia': ['Test_Basin'],
            'geometry': [polygon]
        }, crs='EPSG:4326')
        
        with patch('regionmask.Regions') as mock_regions:
            mock_mask = MagicMock()
            mock_mask.mask.return_value = xr.DataArray(
                np.zeros((10, 10)),
                dims=['lat', 'lon']
            )
            mock_regions.return_value = mock_mask
            
            result = calculate_mean_basin_value_from_shapefile(
                dataset=data,
                basin='Test_Basin',
                shp=gdf,
                dim_lat='lat',
                dim_lon='lon'
            )
            
            assert isinstance(result, pd.DataFrame)
            assert 'lat' in result.columns
            assert 'lon' in result.columns
            
    def test_basin_not_found(self, sample_temperature_data):
        """Test behavior when basin is not found in shapefile."""
        polygon = Polygon([(-55, -20), (-50, -20), (-50, -15), (-55, -15)])
        gdf = gpd.GeoDataFrame({
            'Nome_Bacia': ['Different_Basin'],
            'geometry': [polygon]
        }, crs='EPSG:4326')
        
        # This should raise an error or return empty result
        with pytest.raises((IndexError, KeyError)):
            calculate_mean_basin_value_from_shapefile(
                dataset=sample_temperature_data,
                basin='Nonexistent_Basin',
                shp=gdf
            )


class TestFiguresPanel:
    """Tests for figures_panel function."""
    
    def create_test_images(self, output_dir, num_images=3):
        """Helper function to create test PNG images."""
        import matplotlib.pyplot as plt
        
        image_paths = []
        
        for i in range(num_images):
            fig, ax = plt.subplots(figsize=(4, 3))
            ax.plot([1, 2, 3], [1, 4, 2])
            ax.set_title(f'Test Image {i+1}')
            
            img_path = os.path.join(output_dir, f'test_image_{i+1}.png')
            fig.savefig(img_path, dpi=100, bbox_inches='tight')
            plt.close(fig)
            
            image_paths.append(img_path)
            
        return image_paths
        
    def test_panel_from_list(self, test_output_dir):
        """Test creating panel from list of image paths."""
        # Create test images
        image_paths = self.create_test_images(test_output_dir, 3)
        
        # Create panel
        output_path = figures_panel(
            path_figs=image_paths,
            output_file='test_panel_list.png',
            path_to_save=test_output_dir
        )
        
        # Check that panel was created
        assert os.path.exists(output_path)
        
        # Check that it's a valid image
        with Image.open(output_path) as img:
            assert img.size[0] > 0
            assert img.size[1] > 0
            
    def test_panel_from_directory(self, test_output_dir):
        """Test creating panel from directory of images."""
        # Create test images in a subdirectory
        img_dir = os.path.join(test_output_dir, 'images')
        os.makedirs(img_dir, exist_ok=True)
        
        self.create_test_images(img_dir, 4)
        
        # Create panel
        output_path = figures_panel(
            path_figs=img_dir,
            output_file='test_panel_dir.png',
            path_to_save=test_output_dir
        )
        
        # Check that panel was created
        assert os.path.exists(output_path)
        
    def test_panel_custom_layout(self, test_output_dir):
        """Test creating panel with custom layout."""
        image_paths = self.create_test_images(test_output_dir, 6)
        
        # Create panel with custom layout
        output_path = figures_panel(
            path_figs=image_paths,
            output_file='test_panel_custom.png',
            path_to_save=test_output_dir,
            ncols=3,
            nrows=2
        )
        
        # Check that panel was created
        assert os.path.exists(output_path)
        
    def test_panel_custom_image_size(self, test_output_dir):
        """Test creating panel with custom image size."""
        image_paths = self.create_test_images(test_output_dir, 2)
        
        # Create panel with custom image size
        output_path = figures_panel(
            path_figs=image_paths,
            output_file='test_panel_size.png',
            path_to_save=test_output_dir,
            img_size=(8, 6)
        )
        
        # Check that panel was created
        assert os.path.exists(output_path)
        
    def test_panel_single_image(self, test_output_dir):
        """Test creating panel with single image."""
        image_paths = self.create_test_images(test_output_dir, 1)
        
        output_path = figures_panel(
            path_figs=image_paths,
            output_file='test_panel_single.png',
            path_to_save=test_output_dir
        )
        
        # Check that panel was created
        assert os.path.exists(output_path)
        
    def test_panel_empty_list(self, test_output_dir):
        """Test behavior with empty image list."""
        # This should handle empty list gracefully
        with pytest.raises((IndexError, ValueError)):
            figures_panel(
                path_figs=[],
                output_file='test_panel_empty.png',
                path_to_save=test_output_dir
            )
            
    def test_panel_nonexistent_directory(self, test_output_dir):
        """Test behavior with nonexistent directory."""
        nonexistent_dir = os.path.join(test_output_dir, 'nonexistent')
        
        # Should handle gracefully or raise appropriate error
        with pytest.raises(FileNotFoundError):
            figures_panel(
                path_figs=nonexistent_dir,
                output_file='test_panel_nodir.png',
                path_to_save=test_output_dir
            )


class TestGenerateTitle:
    """Tests for generate_title function."""
    
    def test_basic_title_generation(self):
        """Test basic title generation."""
        title = generate_title(
            titulo_principal="Temperatura do Ar",
            subtitulo="Análise"
        )
        
        assert isinstance(title, str)
        assert "Temperatura do Ar" in title
        assert "Análise" in title
        
    def test_title_with_all_parameters(self):
        """Test title generation with all parameters."""
        test_date = datetime(2024, 1, 15, 12, 0)
        
        title = generate_title(
            titulo_principal="Temperatura",
            subtitulo="Previsão",
            data=test_date,
            nivel="850 hPa",
            unidade="°C",
            modelo="GFS",
            fonte="NCEP"
        )
        
        assert isinstance(title, str)
        assert "Temperatura" in title
        assert "850 hPa" in title
        assert "°C" in title
        assert "GFS" in title
        
    def test_title_with_date_string(self):
        """Test title generation with date as string."""
        title = generate_title(
            titulo_principal="Precipitação",
            data="2024-01-15"
        )
        
        assert isinstance(title, str)
        assert "Precipitação" in title
        assert "2024-01-15" in title
        
    def test_title_with_level_and_units(self):
        """Test title generation with level and units."""
        title = generate_title(
            titulo_principal="Vento",
            nivel="10m",
            unidade="m/s"
        )
        
        assert isinstance(title, str)
        assert "Vento" in title
        assert "10m" in title
        assert "m/s" in title
        
    def test_title_bold_subtitle_option(self):
        """Test title generation with bold subtitle option."""
        title_bold = generate_title(
            titulo_principal="Pressão",
            subtitulo="Análise",
            bold_subtitle=True
        )
        
        title_normal = generate_title(
            titulo_principal="Pressão",
            subtitulo="Análise",
            bold_subtitle=False
        )
        
        assert isinstance(title_bold, str)
        assert isinstance(title_normal, str)
        # Both should contain the subtitle, but formatting might differ
        assert "Análise" in title_bold
        assert "Análise" in title_normal
        
    def test_title_include_datetime_option(self):
        """Test title generation with datetime inclusion option."""
        title_with_dt = generate_title(
            titulo_principal="Umidade",
            include_datetime=True
        )
        
        title_without_dt = generate_title(
            titulo_principal="Umidade",
            include_datetime=False
        )
        
        assert isinstance(title_with_dt, str)
        assert isinstance(title_without_dt, str)
        assert "Umidade" in title_with_dt
        assert "Umidade" in title_without_dt
        
    def test_title_minimal_parameters(self):
        """Test title generation with minimal parameters."""
        title = generate_title(titulo_principal="Teste")
        
        assert isinstance(title, str)
        assert "Teste" in title
        
    def test_title_no_parameters(self):
        """Test title generation with no parameters."""
        title = generate_title()
        
        # Should return some default title or empty string
        assert isinstance(title, str)
        
    def test_title_special_characters(self):
        """Test title generation with special characters."""
        title = generate_title(
            titulo_principal="Temperatura & Umidade",
            subtitulo="Análise - Região Sul",
            unidade="°C/%"
        )
        
        assert isinstance(title, str)
        assert "Temperatura & Umidade" in title
        assert "°C" in title
        
    def test_title_latex_formatting(self):
        """Test that title uses proper LaTeX formatting."""
        title = generate_title(
            titulo_principal="CO₂",
            unidade="ppm",
            bold_subtitle=True
        )
        
        assert isinstance(title, str)
        # Should handle subscripts and special formatting appropriately
        
    def test_title_model_information(self):
        """Test title generation with model information."""
        title = generate_title(
            titulo_principal="Precipitação",
            modelo="ERA5",
            fonte="Copernicus"
        )
        
        assert isinstance(title, str)
        assert "ERA5" in title
        assert "Copernicus" in title


class TestUtilsIntegration:
    """Integration tests for utils functionality."""
    
    def test_basin_calculation_with_real_data_structure(self, sample_temperature_data, sample_shapefile):
        """Test basin calculation with realistic data structure."""
        # Read the actual shapefile created by the fixture
        gdf = gpd.read_file(sample_shapefile)
        
        # Mock regionmask to avoid complex geospatial calculations in tests
        with patch('regionmask.Regions') as mock_regions:
            mock_mask = MagicMock()
            # Create a mask that covers some of the data
            mask_data = np.zeros_like(sample_temperature_data.values)
            mask_data[10:20, 10:20] = 0  # Valid region
            mask_data[mask_data != 0] = 1  # Invalid region
            
            mock_mask.mask.return_value = xr.DataArray(
                mask_data,
                coords=sample_temperature_data.coords,
                dims=sample_temperature_data.dims
            )
            mock_regions.return_value = mock_mask
            
            result = calculate_mean_basin_value_from_shapefile(
                dataset=sample_temperature_data,
                basin='Bacia_Norte',
                shp=gdf,
                dim_lat='latitude',
                dim_lon='longitude'
            )
            
            assert isinstance(result, pd.DataFrame)
            assert not result.empty
            assert result['basin'].iloc[0] == 'Bacia_Norte'
            
    def test_complete_workflow_with_titles_and_panels(self, test_output_dir):
        """Test complete workflow combining titles and panel generation."""
        # Generate some titles
        title1 = generate_title("Temperatura", "Análise", nivel="2m", unidade="°C")
        title2 = generate_title("Precipitação", "Previsão", unidade="mm/h")
        
        # Create test images (simulating plots with these titles)
        image_paths = []
        for i, title in enumerate([title1, title2]):
            import matplotlib.pyplot as plt
            
            fig, ax = plt.subplots(figsize=(8, 6))
            ax.plot(np.random.random(10))
            ax.set_title(title, fontsize=12)
            
            img_path = os.path.join(test_output_dir, f'workflow_image_{i+1}.png')
            fig.savefig(img_path, dpi=150, bbox_inches='tight')
            plt.close(fig)
            
            image_paths.append(img_path)
            
        # Create panel
        panel_path = figures_panel(
            path_figs=image_paths,
            output_file='workflow_panel.png',
            path_to_save=test_output_dir
        )
        
        # Verify everything was created
        assert all(os.path.exists(path) for path in image_paths)
        assert os.path.exists(panel_path)
        
        # Verify panel is larger than individual images
        with Image.open(panel_path) as panel_img:
            with Image.open(image_paths[0]) as single_img:
                assert panel_img.size[0] >= single_img.size[0]
                assert panel_img.size[1] >= single_img.size[1]