"""
Tests for meteoplots.colorbar.colorbars module.
"""

import unittest
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap, LinearSegmentedColormap

from meteoplots.colorbar.colorbars import custom_colorbar


class TestCustomColorbar(unittest.TestCase):
    """Tests for the custom_colorbar function."""
    
    def test_help_functionality(self):
        """Test that help=True displays available variables."""
        # Capture the behavior of help=True (returns None after printing)
        result = custom_colorbar(help=True)
        
        # Should return None when help=True
        self.assertIsNone(result)
        
    def test_valid_temperature_variables(self):
        """Test valid temperature colorbar configurations."""
        # Test the existing temp850 configuration
        levels, colors, cmap, cbar_ticks = custom_colorbar(variavel_plotagem='temp850')
        
        self.assertIsNotNone(levels)
        self.assertIsNotNone(colors)
        self.assertIsNotNone(cmap)
        # cbar_ticks can be None
        
        # Test our new temperature alias
        levels, colors, cmap, cbar_ticks = custom_colorbar(variavel_plotagem='temperature')
        
        self.assertIsNotNone(levels)
        self.assertIsNotNone(colors)
        self.assertIsNotNone(cmap)
        
    def test_precipitation_variables(self):
        """Test precipitation-related colorbar configurations."""
        # Test our new precipitation alias
        levels, colors, cmap, cbar_ticks = custom_colorbar(variavel_plotagem='precipitation')
        
        self.assertIsNotNone(levels)
        self.assertIsNotNone(colors)
        # cmap can be None for this configuration
        
        # Test an existing precipitation config
        levels, colors, cmap, cbar_ticks = custom_colorbar(variavel_plotagem='tp')
        
        self.assertIsNotNone(levels)
        self.assertIsNotNone(colors)
        
    def test_invalid_variable(self):
        """Test behavior with invalid/unknown variable."""
        with self.assertRaises(ValueError) as context:
            custom_colorbar(variavel_plotagem='nonexistent_variable')
        
        self.assertIn("não configurada", str(context.exception))
        
    def test_none_variable(self):
        """Test behavior when no variable is specified."""
        levels, colors, cmap, cbar_ticks = custom_colorbar(variavel_plotagem=None)
        
        # Should return all None when no variable specified
        self.assertIsNone(levels)
        self.assertIsNone(colors)
        self.assertIsNone(cmap)
        self.assertIsNone(cbar_ticks)
        
    def test_custom_parameter(self):
        """Test custom parameter functionality."""
        custom_config = {
            'levels': [0, 10, 20, 30],
            'colors': ['blue', 'green', 'red'],
            'cmap': None,
            'cbar_ticks': [0, 15, 30]
        }
        
        levels, colors, cmap, cbar_ticks = custom_colorbar(custom=custom_config)
        
        self.assertEqual(levels, [0, 10, 20, 30])
        self.assertEqual(colors, ['blue', 'green', 'red'])
        self.assertIsNone(cmap)
        self.assertEqual(cbar_ticks, [0, 15, 30])
        
    def test_colorbar_structure_consistency(self):
        """Test that all colorbar configurations have consistent structure."""
        test_vars = ['temperature', 'precipitation', 'temp850', 'tp']
        
        for var in test_vars:
            with self.subTest(variable=var):
                levels, colors, cmap, cbar_ticks = custom_colorbar(variavel_plotagem=var)
                
                # Check that we get valid returns
                self.assertIsNotNone(levels)
                self.assertIsNotNone(colors)
                # cmap and cbar_ticks can be None depending on configuration
                
                # Check levels format
                self.assertTrue(hasattr(levels, '__len__') or callable(levels))
                
                # Check colors format
                self.assertIsInstance(colors, list)
        
    def test_functional_levels(self):
        """Test that lambda levels are properly resolved."""
        # Test a variable with lambda levels
        levels, colors, cmap, cbar_ticks = custom_colorbar(variavel_plotagem='temp_anomalia')
        
        self.assertIsNotNone(levels)
        # Should be resolved to actual array/list, not a function
        self.assertFalse(callable(levels))
        self.assertTrue(hasattr(levels, '__len__'))
        
    def test_colormap_generation(self):
        """Test that colormaps are properly generated from functions."""
        # Test a variable with string cmap (should be string)
        levels, colors, cmap, cbar_ticks = custom_colorbar(variavel_plotagem='temp_anomalia')
        
        self.assertIsNotNone(cmap)
        # Should be a string colormap name
        self.assertIsInstance(cmap, str)
        self.assertEqual(cmap, 'RdBu_r')


if __name__ == '__main__':
    unittest.main()