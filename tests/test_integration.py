"""
Integration tests for meteoplots library.

These tests verify that different components work together correctly
and test complete workflows that users would typically perform.
"""

import pytest
import numpy as np
import matplotlib.pyplot as plt
import xarray as xr
import os
from unittest.mock import patch

from meteoplots.plots import (
    plot_contourf_from_xarray,
    plot_multipletypes_from_xarray,
    add_box_to_plot
)
from meteoplots.colorbar.colorbars import custom_colorbar
from meteoplots.utils.titles import generate_title
from meteoplots.utils.utils import figures_panel
from tests.conftest import assert_figure_created


class TestCompleteWorkflows:
    """Test complete end-to-end workflows."""
    
    def test_complete_meteorological_analysis(self, sample_temperature_data, sample_pressure_data, 
                                           sample_wind_components, test_output_dir, matplotlib_backend):
        """Test complete meteorological analysis workflow."""
        u_component, v_component = sample_wind_components
        
        # Step 1: Create multipletypes plot with all data
        fig, ax = plot_multipletypes_from_xarray(
            xarray_data={
                'contourf': sample_temperature_data,
                'contour': sample_pressure_data,
                'u_quiver': u_component,
                'v_quiver': v_component
            },
            plot_var_colorbar='temperature',
            plot_types=['contourf', 'contour', 'quiver'],
            title='Complete Meteorological Analysis',
            extent=[-60, -30, -35, 5],
            figsize=(12, 8),
            
            # Contour parameters
            contour_levels=[np.arange(1000, 1030, 5)],
            colors_levels=['black'],
            
            # Quiver parameters
            quiver_skip=3,
            
            # Save parameters
            savefigure=True,
            path_save=test_output_dir,
            output_filename='complete_analysis'
        )
        
        assert_figure_created(fig)
        
        # Verify file was saved
        expected_file = os.path.join(test_output_dir, 'complete_analysis.png')
        assert os.path.exists(expected_file)
        
        plt.close(fig)
        
    def test_basin_analysis_workflow(self, sample_precipitation_data, sample_shapefile, 
                                   test_output_dir, matplotlib_backend):
        """Test complete basin analysis workflow."""
        # Mock the basin calculation to avoid complex geospatial operations
        with patch('meteoplots.utils.utils.calculate_mean_basin_value_from_shapefile') as mock_basin:
            mock_basin.return_value = [
                {
                    'Nome_Bacia': 'Bacia_Norte',
                    'value': 15.5,
                    'centroid_lon': -52.5,
                    'centroid_lat': -17.5
                },
                {
                    'Nome_Bacia': 'Bacia_Sul', 
                    'value': 12.3,
                    'centroid_lon': -47.5,
                    'centroid_lat': -22.5
                }
            ]
            
            # Create plot with basin analysis
            fig, ax = plot_contourf_from_xarray(
                xarray_data=sample_precipitation_data,
                plot_var_colorbar='tp',
                title='Precipitation Analysis by Basin',
                extent=[-60, -30, -35, 5],
                
                # Basin analysis parameters
                shp_path_bacias=sample_shapefile,
                add_values_from_shapefile=True,
                basin_column_name='Nome_Bacia',
                
                # Save parameters
                savefigure=True,
                path_save=test_output_dir,
                output_filename='basin_analysis'
            )
            
            assert_figure_created(fig)
            
            # Verify basin function was called
            mock_basin.assert_called()
            
            plt.close(fig)
            
    def test_custom_colorbar_integration(self, sample_temperature_data, matplotlib_backend):
        """Test integration between custom colorbar and plotting functions."""
        # Get colorbar configuration
        colorbar_config = custom_colorbar(variavel_plotagem='temperature')
        
        assert colorbar_config is not None
        
        # Use the colorbar in a plot
        fig, ax = plot_contourf_from_xarray(
            xarray_data=sample_temperature_data,
            plot_var_colorbar='temperature'
        )
        
        assert_figure_created(fig)
        
        # The plot should have used the colorbar configuration
        assert len(ax.collections) > 0  # Should have contourf collections
        
        plt.close(fig)
        
    def test_title_generation_integration(self, sample_temperature_data, matplotlib_backend):
        """Test integration of title generation with plotting."""
        from datetime import datetime
        
        # Generate professional title
        title = generate_title(
            titulo_principal="Temperatura do Ar",
            subtitulo="Análise Sinótica",
            data=datetime(2024, 1, 15, 12, 0),
            nivel="2m",
            unidade="°C",
            modelo="GFS",
            fonte="NCEP"
        )
        
        # Use title in plot
        fig, ax = plot_contourf_from_xarray(
            xarray_data=sample_temperature_data,
            plot_var_colorbar='temperature',
            title=title,
            title_size=14
        )
        
        assert_figure_created(fig)
        assert ax.get_title() == title
        
        plt.close(fig)
        
    def test_box_overlay_workflow(self, sample_temperature_data, matplotlib_backend):
        """Test workflow with box overlays for region highlighting."""
        # Create base plot
        fig, ax = plot_contourf_from_xarray(
            xarray_data=sample_temperature_data,
            plot_var_colorbar='temperature',
            title='Temperature with Regions of Interest'
        )
        
        # Add multiple boxes for different regions
        region_boxes = [
            [-55, -45, -25, -15],  # Region 1
            [-50, -40, -30, -20],  # Region 2
            [-60, -50, -35, -25]   # Region 3
        ]
        
        add_box_to_plot(
            ax=ax,
            extent_boxes=region_boxes,
            edgecolor_box='red',
            linewidth_box=2,
            linestyle_box='--'
        )
        
        assert_figure_created(fig)
        assert len(ax.patches) == len(region_boxes)
        
        plt.close(fig)
        
    def test_panel_creation_workflow(self, sample_temperature_data, sample_precipitation_data,
                                   sample_pressure_data, test_output_dir, matplotlib_backend):
        """Test complete workflow creating multiple plots and combining into panel."""
        plot_files = []
        
        # Create multiple individual plots
        datasets = [
            (sample_temperature_data, 'temperature', 'Temperature Analysis'),
            (sample_precipitation_data, 'tp', 'Precipitation Analysis'),
            (sample_pressure_data, 'slp', 'Pressure Analysis')
        ]
        
        for i, (data, colorbar_var, title) in enumerate(datasets):
            fig, ax = plot_contourf_from_xarray(
                xarray_data=data,
                plot_var_colorbar=colorbar_var,
                title=title,
                figsize=(8, 6),
                savefigure=True,
                path_save=test_output_dir,
                output_filename=f'individual_plot_{i+1}'
            )
            
            plot_files.append(os.path.join(test_output_dir, f'individual_plot_{i+1}.png'))
            plt.close(fig)
            
        # Verify individual plots were created
        assert all(os.path.exists(f) for f in plot_files)
        
        # Create panel from individual plots
        panel_path = figures_panel(
            path_figs=plot_files,
            output_file='analysis_panel.png',
            path_to_save=test_output_dir,
            img_size=(6, 4),
            ncols=2,
            nrows=2
        )
        
        # Verify panel was created
        assert os.path.exists(panel_path)
        
    def test_error_recovery_workflow(self, sample_temperature_data, matplotlib_backend):
        """Test workflow error recovery scenarios."""
        # Test 1: Invalid colorbar should fall back to manual configuration
        try:
            fig, ax = plot_contourf_from_xarray(
                xarray_data=sample_temperature_data,
                plot_var_colorbar='nonexistent_colorbar',
                levels=[10, 15, 20, 25, 30],
                colors=['blue', 'green', 'yellow', 'red']
            )
            # If no error, the fallback worked
            assert_figure_created(fig)
            plt.close(fig)
        except ValueError:
            # Expected behavior if no fallback
            pass
            
        # Test 2: Missing colorbar configuration should raise clear error
        with pytest.raises(ValueError):
            plot_contourf_from_xarray(
                xarray_data=sample_temperature_data
                # Missing all colorbar configuration
            )


class TestPerformanceIntegration:
    """Test performance aspects of integrated workflows."""
    
    def test_large_dataset_handling(self, matplotlib_backend):
        """Test handling of larger datasets (within reason for tests)."""
        # Create larger dataset
        lat = np.arange(-35, 10, 0.25)  # Higher resolution
        lon = np.arange(-75, -30, 0.25)
        temp_data = 20 + 10 * np.random.random((len(lat), len(lon)))
        
        large_temperature = xr.DataArray(
            temp_data,
            coords=[('latitude', lat), ('longitude', lon)],
            attrs={'units': '°C', 'long_name': 'Temperature'}
        )
        
        # Should handle without memory issues
        fig, ax = plot_contourf_from_xarray(
            xarray_data=large_temperature,
            plot_var_colorbar='temperature',
            title='Large Dataset Test'
        )
        
        assert_figure_created(fig)
        plt.close(fig)
        
    def test_multiple_plot_types_performance(self, matplotlib_backend):
        """Test performance with multiple simultaneous plot types."""
        # Create datasets
        lat = np.arange(-35, 10, 1.0)
        lon = np.arange(-75, -30, 1.0)
        
        temp_data = 20 + 10 * np.random.random((len(lat), len(lon)))
        pressure_data = 1013 + 20 * np.random.random((len(lat), len(lon))) - 10
        u_data = 10 * np.random.random((len(lat), len(lon))) - 5
        v_data = 10 * np.random.random((len(lat), len(lon))) - 5
        
        temperature = xr.DataArray(temp_data, coords=[('latitude', lat), ('longitude', lon)])
        pressure = xr.DataArray(pressure_data, coords=[('latitude', lat), ('longitude', lon)])
        u_component = xr.DataArray(u_data, coords=[('latitude', lat), ('longitude', lon)])
        v_component = xr.DataArray(v_data, coords=[('latitude', lat), ('longitude', lon)])
        
        # Complex plot with all types
        fig, ax = plot_multipletypes_from_xarray(
            xarray_data={
                'contourf': temperature,
                'contour': pressure,
                'u_quiver': u_component,
                'v_quiver': v_component
            },
            plot_var_colorbar='temperature',
            plot_types=['contourf', 'contour', 'quiver', 'streamplot'],
            contour_levels=[np.arange(1000, 1030, 5)],
            colors_levels=['black'],
            quiver_skip=2
        )
        
        assert_figure_created(fig)
        plt.close(fig)


class TestRealWorldScenarios:
    """Test scenarios that mimic real-world usage patterns."""
    
    def test_weather_forecast_scenario(self, sample_temperature_data, sample_wind_components,
                                     test_output_dir, matplotlib_backend):
        """Test typical weather forecast visualization scenario."""
        u_component, v_component = sample_wind_components
        
        # Generate professional title
        title = generate_title(
            titulo_principal="Previsão Meteorológica",
            subtitulo="Temperatura + Vento",
            data="2024-01-15 12Z",
            modelo="GFS",
            fonte="NCEP"
        )
        
        # Create forecast plot
        fig, ax = plot_multipletypes_from_xarray(
            xarray_data={
                'contourf': sample_temperature_data,
                'u_quiver': u_component,
                'v_quiver': v_component
            },
            plot_var_colorbar='temperature',
            plot_types=['contourf', 'quiver'],
            title=title,
            extent=[-60, -30, -35, 5],  # Brazil focus
            quiver_skip=4,
            quiver_key={'length': 10, 'label': '10 m/s'},
            
            # Professional output
            figsize=(12, 8),
            savefigure=True,
            path_save=test_output_dir,
            output_filename='weather_forecast'
        )
        
        assert_figure_created(fig)
        
        # Add region of interest
        add_box_to_plot(
            ax=ax,
            extent_boxes=[[-50, -40, -25, -15]],  # Southeast Brazil
            edgecolor_box='red',
            linewidth_box=2,
            linestyle_box='-'
        )
        
        plt.close(fig)
        
    def test_climate_monitoring_scenario(self, sample_precipitation_data, sample_shapefile,
                                       test_output_dir, matplotlib_backend):
        """Test climate monitoring with basin analysis scenario."""
        with patch('meteoplots.utils.utils.calculate_mean_basin_value_from_shapefile') as mock_basin:
            mock_basin.return_value = [
                {'Nome_Bacia': 'Bacia_Norte', 'value': 150.2, 'centroid_lon': -52.5, 'centroid_lat': -17.5},
                {'Nome_Bacia': 'Bacia_Sul', 'value': 89.7, 'centroid_lon': -47.5, 'centroid_lat': -22.5}
            ]
            
            # Create monitoring plot with basin analysis
            title = generate_title(
                titulo_principal="Monitoramento Climático",
                subtitulo="Precipitação Acumulada por Bacia",
                unidade="mm/mês",
                fonte="Observações + Sensoriamento Remoto"
            )
            
            fig, ax = plot_contourf_from_xarray(
                xarray_data=sample_precipitation_data,
                plot_var_colorbar='tp',
                title=title,
                extent=[-60, -30, -35, 5],
                
                # Basin analysis
                shp_path_bacias=sample_shapefile,
                add_values_from_shapefile=True,
                basin_column_name='Nome_Bacia',
                
                # Professional styling
                colorbar_position='horizontal',
                label_colorbar='Precipitação (mm/mês)',
                figsize=(14, 8),
                
                # Output
                savefigure=True,
                path_save=test_output_dir,
                output_filename='climate_monitoring'
            )
            
            assert_figure_created(fig)
            plt.close(fig)
            
    def test_research_publication_scenario(self, sample_temperature_data, sample_pressure_data,
                                         test_output_dir, matplotlib_backend):
        """Test scenario for research publication quality figures."""
        # Create high-quality figure for publication
        fig, ax = plot_multipletypes_from_xarray(
            xarray_data={
                'contourf': sample_temperature_data,
                'contour': sample_pressure_data
            },
            plot_var_colorbar='temperature',
            plot_types=['contourf', 'contour'],
            
            # Publication-quality title
            title=generate_title(
                titulo_principal="Surface Temperature and Sea Level Pressure",
                subtitulo="January 2024 Mean",
                unidade="°C / hPa"
            ),
            
            # High resolution and quality
            figsize=(10, 8),
            extent=[-60, -30, -35, 5],
            
            # Contour styling
            contour_levels=[np.arange(1005, 1025, 2)],
            colors_levels=['black'],
            
            # Professional colorbar
            colorbar_position='vertical',
            label_colorbar='Temperature (°C)',
            
            # High-quality output
            savefigure=True,
            path_save=test_output_dir,
            output_filename='publication_figure',
            dpi=300
        )
        
        assert_figure_created(fig)
        plt.close(fig)
        
        # Verify high-quality output was created
        output_file = os.path.join(test_output_dir, 'publication_figure.png')
        assert os.path.exists(output_file)


class TestEdgeCases:
    """Test edge cases and boundary conditions."""
    
    def test_minimal_data_extent(self, matplotlib_backend):
        """Test with minimal data extent."""
        # Very small dataset
        lat = np.array([-25, -20])
        lon = np.array([-50, -45])
        temp_data = np.array([[20, 22], [21, 23]])
        
        minimal_data = xr.DataArray(
            temp_data,
            coords=[('latitude', lat), ('longitude', lon)],
            attrs={'units': '°C'}
        )
        
        fig, ax = plot_contourf_from_xarray(
            xarray_data=minimal_data,
            plot_var_colorbar='temperature'
        )
        
        assert_figure_created(fig)
        plt.close(fig)
        
    def test_single_point_data(self, matplotlib_backend):
        """Test with single data point."""
        # Single point dataset
        single_data = xr.DataArray(
            [[25.0]],
            coords=[('latitude', [-25]), ('longitude', [-50])],
            attrs={'units': '°C'}
        )
        
        # This might raise an error or handle gracefully
        try:
            fig, ax = plot_contourf_from_xarray(
                xarray_data=single_data,
                plot_var_colorbar='temperature'
            )
            assert_figure_created(fig)
            plt.close(fig)
        except (ValueError, IndexError):
            # Expected for single point data
            pass
            
    def test_global_longitude_wraparound(self, matplotlib_backend):
        """Test with longitude data that wraps around globe."""
        # Data spanning longitude wraparound
        lat = np.arange(-10, 11, 5)
        lon = np.arange(350, 370, 5)  # Crosses 360° boundary
        temp_data = 20 + 5 * np.random.random((len(lat), len(lon)))
        
        global_data = xr.DataArray(
            temp_data,
            coords=[('latitude', lat), ('longitude', lon)],
            attrs={'units': '°C'}
        )
        
        fig, ax = plot_contourf_from_xarray(
            xarray_data=global_data,
            plot_var_colorbar='temperature'
        )
        
        assert_figure_created(fig)
        plt.close(fig)