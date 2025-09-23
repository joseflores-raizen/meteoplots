"""
Tests for meteoplots.plots module.
"""

import pytest
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import xarray as xr
from unittest.mock import patch, MagicMock

from meteoplots.plots import (
    add_box_to_plot,
    plot_contourf_from_xarray,
    plot_contour_from_xarray,
    plot_quiver_from_xarray,
    plot_streamplot_from_xarray,
    plot_multipletypes_from_xarray,
    get_base_ax
)
from tests.conftest import assert_figure_created, assert_plot_has_data


class TestAddBoxToPlot:
    """Tests for add_box_to_plot function."""
    
    def test_add_single_box(self, matplotlib_backend):
        """Test adding a single box to a plot."""
        fig, ax = get_base_ax(extent=[-60, -40, -30, -10], figsize=(8, 6))
        
        # Define box extent
        extent_boxes = [[-55, -45, -25, -15]]  # [lon_min, lon_max, lat_min, lat_max]
        
        add_box_to_plot(ax, extent_boxes)
        
        # Check that a patch was added
        assert len(ax.patches) == 1
        assert isinstance(ax.patches[0], mpatches.Rectangle)
        
        plt.close(fig)
        
    def test_add_multiple_boxes(self, matplotlib_backend):
        """Test adding multiple boxes to a plot."""
        fig, ax = get_base_ax(extent=[-60, -35, -35, -15], figsize=(8, 6))
        
        # Define multiple box extents
        extent_boxes = [
            [-55, -45, -25, -15],
            [-50, -40, -30, -20]
        ]
        
        add_box_to_plot(ax, extent_boxes)
        
        # Check that two patches were added
        assert len(ax.patches) == 2
        
        plt.close(fig)
        
    def test_box_styling_parameters(self, matplotlib_backend):
        """Test that styling parameters are applied correctly."""
        fig, ax = get_base_ax(extent=[-60, -40, -30, -10], figsize=(8, 6))
        
        extent_boxes = [[-55, -45, -25, -15]]
        
        add_box_to_plot(
            ax, 
            extent_boxes,
            edgecolor_box='red',
            facecolor_box='blue',
            linewidth_box=3,
            linestyle_box='--',
            alpha_box=0.5
        )
        
        # Check that patch was added with correct properties
        assert len(ax.patches) == 1
        patch = ax.patches[0]
        
        import matplotlib.colors as mcolors
        assert patch.get_edgecolor()[0:3] == mcolors.to_rgb('red')  # Check RGB components
        assert patch.get_facecolor()[0:3] == mcolors.to_rgb('blue')
        assert patch.get_linewidth() == 3
        assert patch.get_linestyle() == '--'
        assert patch.get_alpha() == 0.5
        
        plt.close(fig)
        
    def test_empty_box_list(self, matplotlib_backend):
        """Test behavior with empty box list."""
        fig, ax = plt.subplots()
        
        extent_boxes = []
        
        # Should not raise an error
        add_box_to_plot(ax, extent_boxes)
        
        # No patches should be added
        assert len(ax.patches) == 0
        
        plt.close(fig)


class TestPlotContourfFromXarray:
    """Tests for plot_contourf_from_xarray function."""
    
    def test_basic_contourf_plot(self, sample_temperature_data, matplotlib_backend):
        """Test basic contourf plotting functionality."""
        fig, ax = plot_contourf_from_xarray(
            xarray_data=sample_temperature_data,
            plot_var_colorbar='temperature'
        )
        
        assert_figure_created(fig)
        assert_plot_has_data(ax)
        
        plt.close(fig)
        
    def test_contourf_with_custom_extent(self, sample_temperature_data, matplotlib_backend):
        """Test contourf plotting with custom extent."""
        custom_extent = [-60, -30, -35, 5]
        
        fig, ax = plot_contourf_from_xarray(
            xarray_data=sample_temperature_data,
            plot_var_colorbar='temperature',
            extent=custom_extent
        )
        
        assert_figure_created(fig)
        
        # Check that extent was applied (approximately)
        xlim = ax.get_xlim()
        ylim = ax.get_ylim()
        
        # Extents might be slightly adjusted by cartopy/matplotlib
        assert xlim[0] <= custom_extent[0] + 5
        assert xlim[1] >= custom_extent[1] - 5
        assert ylim[0] <= custom_extent[2] + 5
        assert ylim[1] >= custom_extent[3] - 5
        
        plt.close(fig)
        
    def test_contourf_with_manual_levels(self, sample_temperature_data, matplotlib_backend):
        """Test contourf plotting with manual levels and colors."""
        fig, ax = plot_contourf_from_xarray(
            xarray_data=sample_temperature_data,
            levels=[10, 15, 20, 25, 30],
            colors=['blue', 'green', 'yellow', 'red']
        )
        
        assert_figure_created(fig)
        assert_plot_has_data(ax)
        
        plt.close(fig)
        
    def test_contourf_with_manual_cmap(self, sample_temperature_data, matplotlib_backend):
        """Test contourf plotting with manual colormap."""
        fig, ax = plot_contourf_from_xarray(
            xarray_data=sample_temperature_data,
            levels=[10, 15, 20, 25, 30],
            cmap='viridis'
        )
        
        assert_figure_created(fig)
        assert_plot_has_data(ax)
        
        plt.close(fig)
        
    def test_contourf_missing_colorbar_params_raises_error(self, sample_temperature_data):
        """Test that missing colorbar parameters raise ValueError."""
        with pytest.raises(ValueError, match="When plot_var_colorbar is None"):
            plot_contourf_from_xarray(
                xarray_data=sample_temperature_data
                # Missing both plot_var_colorbar and manual config
            )
            
    def test_contourf_with_title(self, sample_temperature_data, matplotlib_backend):
        """Test contourf plotting with title."""
        title = "Test Temperature Plot"
        
        fig, ax = plot_contourf_from_xarray(
            xarray_data=sample_temperature_data,
            plot_var_colorbar='temperature',
            title=title
        )
        
        assert_figure_created(fig)
        assert ax.get_title() == title
        
        plt.close(fig)
        
    def test_contourf_with_basin_analysis(self, sample_temperature_data, sample_shapefile, matplotlib_backend):
        """Test contourf plotting with basin analysis."""
        with patch('meteoplots.utils.utils.calculate_mean_basin_value_from_shapefile') as mock_basin:
            # Mock the basin analysis function
            mock_basin.return_value = [
                {'Nome_Bacia': 'Bacia_Norte', 'value': 25.5, 'centroid_lon': -52.5, 'centroid_lat': -17.5},
                {'Nome_Bacia': 'Bacia_Sul', 'value': 23.2, 'centroid_lon': -47.5, 'centroid_lat': -22.5}
            ]
            
            fig, ax = plot_contourf_from_xarray(
                xarray_data=sample_temperature_data,
                plot_var_colorbar='temperature',
                shp_path_bacias=sample_shapefile,
                add_values_from_shapefile=True
            )
            
            assert_figure_created(fig)
            mock_basin.assert_called_once()
            
            plt.close(fig)


class TestPlotContourFromXarray:
    """Tests for plot_contour_from_xarray function."""
    
    def test_basic_contour_plot(self, sample_pressure_data, matplotlib_backend):
        """Test basic contour plotting functionality."""
        fig, ax = plot_contour_from_xarray(
            xarray_data=sample_pressure_data,
            contour_levels=[np.arange(1000, 1030, 5)],
            colors_levels=['black']
        )
        
        assert_figure_created(fig)
        assert len(ax.collections) > 0  # Contour lines create collections
        
        plt.close(fig)
        
    def test_contour_multiple_levels(self, sample_pressure_data, matplotlib_backend):
        """Test contour plotting with multiple level sets."""
        fig, ax = plot_contour_from_xarray(
            xarray_data=sample_pressure_data,
            contour_levels=[
                np.arange(1000, 1020, 5),
                np.arange(1020, 1030, 2)
            ],
            colors_levels=['black', 'red']
        )
        
        assert_figure_created(fig)
        assert len(ax.collections) > 0
        
        plt.close(fig)


class TestPlotQuiverFromXarray:
    """Tests for plot_quiver_from_xarray function."""
    
    def test_basic_quiver_plot(self, sample_wind_components, matplotlib_backend):
        """Test basic quiver plotting functionality."""
        u_component, v_component = sample_wind_components
        
        fig, ax = plot_quiver_from_xarray(
            xarray_u=u_component,
            xarray_v=v_component
        )
        
        assert_figure_created(fig)
        # Quiver plots don't create collections, but they do modify the axes
        assert ax is not None
        
        plt.close(fig)
        
    def test_quiver_with_skip(self, sample_wind_components, matplotlib_backend):
        """Test quiver plotting with point skipping."""
        u_component, v_component = sample_wind_components
        
        fig, ax = plot_quiver_from_xarray(
            xarray_u=u_component,
            xarray_v=v_component,
            quiver_skip=3
        )
        
        assert_figure_created(fig)
        
        plt.close(fig)
        
    def test_quiver_with_key(self, sample_wind_components, matplotlib_backend):
        """Test quiver plotting with scale key."""
        u_component, v_component = sample_wind_components
        
        fig, ax = plot_quiver_from_xarray(
            xarray_u=u_component,
            xarray_v=v_component,
            quiver_key={'length': 10, 'label': '10 m/s'}
        )
        
        assert_figure_created(fig)
        
        plt.close(fig)


class TestPlotStreamplotFromXarray:
    """Tests for plot_streamplot_from_xarray function."""
    
    def test_basic_streamplot(self, sample_wind_components, matplotlib_backend):
        """Test basic streamplot functionality."""
        u_component, v_component = sample_wind_components
        
        fig, ax = plot_streamplot_from_xarray(
            xarray_u=u_component,
            xarray_v=v_component
        )
        
        assert_figure_created(fig)
        
        plt.close(fig)
        
    def test_streamplot_with_color_by_magnitude(self, sample_wind_components, matplotlib_backend):
        """Test streamplot with color by magnitude."""
        u_component, v_component = sample_wind_components
        
        fig, ax = plot_streamplot_from_xarray(
            xarray_u=u_component,
            xarray_v=v_component,
            stream_color_by_magnitude=True,
            stream_cmap='viridis'
        )
        
        assert_figure_created(fig)
        
        plt.close(fig)


class TestPlotMultipletypesFromXarray:
    """Tests for plot_multipletypes_from_xarray function."""
    
    def test_contourf_only(self, sample_temperature_data, matplotlib_backend):
        """Test multipletypes with contourf only."""
        fig, ax = plot_multipletypes_from_xarray(
            xarray_data={'contourf': sample_temperature_data},
            plot_var_colorbar='temperature',
            plot_types=['contourf']
        )
        
        assert_figure_created(fig)
        assert_plot_has_data(ax)
        
        plt.close(fig)
        
    def test_contourf_and_contour(self, sample_temperature_data, sample_pressure_data, matplotlib_backend):
        """Test multipletypes with both contourf and contour."""
        fig, ax = plot_multipletypes_from_xarray(
            xarray_data={
                'contourf': sample_temperature_data,
                'contour': sample_pressure_data
            },
            plot_var_colorbar='temperature',
            plot_types=['contourf', 'contour'],
            contour_levels=[np.arange(1000, 1030, 5)],
            colors_levels=['black']
        )
        
        assert_figure_created(fig)
        assert_plot_has_data(ax)
        
        plt.close(fig)
        
    def test_quiver_and_streamplot(self, sample_wind_components, matplotlib_backend):
        """Test multipletypes with quiver and streamplot."""
        u_component, v_component = sample_wind_components
        
        fig, ax = plot_multipletypes_from_xarray(
            xarray_data={
                'u_quiver': u_component,
                'v_quiver': v_component
            },
            plot_types=['quiver', 'streamplot']
        )
        
        assert_figure_created(fig)
        
        plt.close(fig)
        
    def test_all_plot_types(self, sample_temperature_data, sample_pressure_data, sample_wind_components, matplotlib_backend):
        """Test multipletypes with all plot types combined."""
        u_component, v_component = sample_wind_components
        
        fig, ax = plot_multipletypes_from_xarray(
            xarray_data={
                'contourf': sample_temperature_data,
                'contour': sample_pressure_data,
                'u_quiver': u_component,
                'v_quiver': v_component
            },
            plot_var_colorbar='temperature',
            plot_types=['contourf', 'contour', 'quiver', 'streamplot'],
            contour_levels=[np.arange(1000, 1030, 5)],
            colors_levels=['black']
        )
        
        assert_figure_created(fig)
        assert_plot_has_data(ax)
        
        plt.close(fig)
        
    def test_multipletypes_missing_colorbar_raises_error(self, sample_temperature_data):
        """Test that missing colorbar parameters raise ValueError in multipletypes."""
        with pytest.raises(ValueError, match="When plot_var_colorbar is None"):
            plot_multipletypes_from_xarray(
                xarray_data={'contourf': sample_temperature_data},
                plot_types=['contourf']
                # Missing plot_var_colorbar and manual config
            )
            
    def test_multipletypes_with_boxes(self, sample_temperature_data, matplotlib_backend):
        """Test multipletypes with box patches."""
        box_patches = [[-55, -45, -25, -15]]
        
        fig, ax = plot_multipletypes_from_xarray(
            xarray_data={'contourf': sample_temperature_data},
            plot_var_colorbar='temperature',
            plot_types=['contourf'],
            box_patches=box_patches
        )
        
        assert_figure_created(fig)
        assert len(ax.patches) >= 1  # Should have box patches
        
        plt.close(fig)


class TestPlotsUtilities:
    """Tests for utility functions and common functionality."""
    
    def test_coordinate_dimension_handling(self, data_generator, matplotlib_backend):
        """Test handling of different coordinate dimension names."""
        # Test with custom dimension names
        data = data_generator.create_xarray_with_custom_dims('lat', 'lon')
        
        fig, ax = plot_contourf_from_xarray(
            xarray_data=data,
            plot_var_colorbar='temperature',
            dim_lat='lat',
            dim_lon='lon'
        )
        
        assert_figure_created(fig)
        
        plt.close(fig)
        
    def test_longitude_conversion(self, matplotlib_backend):
        """Test longitude conversion from 0-360 to -180-180."""
        # Create data with 0-360 longitude
        lat = np.arange(-35, 10, 2)
        lon = np.arange(280, 330, 2)  # 0-360 format
        data = np.random.random((len(lat), len(lon)))
        
        temperature_360 = xr.DataArray(
            data,
            coords=[('latitude', lat), ('longitude', lon)],
            attrs={'units': '°C', 'long_name': 'Temperature'}
        )
        
        fig, ax = plot_contourf_from_xarray(
            xarray_data=temperature_360,
            plot_var_colorbar='temperature'
        )
        
        assert_figure_created(fig)
        
        plt.close(fig)
        
    def test_savefigure_functionality(self, sample_temperature_data, test_output_dir, matplotlib_backend):
        """Test figure saving functionality."""
        output_filename = "test_temperature_plot"
        
        fig, ax = plot_contourf_from_xarray(
            xarray_data=sample_temperature_data,
            plot_var_colorbar='temperature',
            savefigure=True,
            path_save=test_output_dir,
            output_filename=output_filename
        )
        
        assert_figure_created(fig)
        
        # Check that file was saved
        import os
        expected_file = os.path.join(test_output_dir, f"{output_filename}.png")
        assert os.path.exists(expected_file)
        
        plt.close(fig)


class TestErrorHandling:
    """Tests for error handling in plots module."""
    
    def test_invalid_xarray_data(self, matplotlib_backend):
        """Test error handling with invalid xarray data."""
        # This should raise an appropriate error
        with pytest.raises((AttributeError, ValueError, TypeError)):
            plot_contourf_from_xarray(
                xarray_data="not_an_xarray",
                plot_var_colorbar='temperature'
            )
            
    def test_missing_coordinates(self, matplotlib_backend):
        """Test error handling with missing coordinate dimensions."""
        # Create data without proper coordinates
        bad_data = xr.DataArray(
            np.random.random((10, 10)),
            dims=['x', 'y']  # Wrong dimension names
        )
        
        with pytest.raises((KeyError, ValueError)):
            plot_contourf_from_xarray(
                xarray_data=bad_data,
                plot_var_colorbar='temperature'
            )
            
    def test_inconsistent_wind_components(self, sample_wind_components, matplotlib_backend):
        """Test error handling with inconsistent wind component shapes."""
        u_component, v_component = sample_wind_components
        
        # Create mismatched v component
        v_bad = v_component.isel(latitude=slice(0, 5))  # Different shape
        
        with pytest.raises((ValueError, IndexError)):
            plot_quiver_from_xarray(
                xarray_u=u_component,
                xarray_v=v_bad
            )