
import cartopy.crs as ccrs
import matplotlib.pyplot as plt

def get_base_ax(extent, figsize, central_longitude=0):

    import cartopy.feature as cfeature

    fig = plt.figure(figsize=figsize)
    ax = plt.axes(projection=ccrs.PlateCarree(central_longitude=central_longitude))
    ax.set_extent(list(extent), crs=ccrs.PlateCarree())

    ax.coastlines(resolution='110m', color='black')
    ax.add_feature(cfeature.BORDERS, edgecolor='black')

    # Labels dos ticks de lat e lon
    gl = ax.gridlines(draw_labels=True, alpha=0.2, linestyle='--')
    gl.top_labels = False
    gl.right_labels = False

    return fig, ax

def plot_shaded_from_xarray(xarray_data, plot_var: str, dim_lat='latitude', dim_lon='longitude', shapefiles=None, normalize_colorbar=False, **kwargs):

    from meteoplots.colorbars import custom_colorbar
    from matplotlib.colors import BoundaryNorm
    from mpl_toolkits.axes_grid1.inset_locator import inset_axes
    import geopandas as gpd
    import numpy as np
    import os

    '''Plot shaded data from an xarray DataArray'''

    # Default parameters
    extent = kwargs.get('extent', [240, 360, -60, 20])
    figsize = kwargs.get('figsize', (12, 12))
    central_longitude = kwargs.get('central_longitude', 0)
    title_size = kwargs.get('title_size', 16)
    title = kwargs.get('title', '')
    colorbar_position = kwargs.get('colorbar_position', 'horizontal')
    label_colorbar = kwargs.get('label_colorbar', '')
    path_save = kwargs.get('path_save', './tmp/plots')
    output_filename = kwargs.get('output_filename', 'shaded_plot.png')

    # Colormap and levels
    levels, colors, cmap, cbar_ticks = custom_colorbar(plot_var)

    if colors is not None and cmap is not None:
        colors = None

    if normalize_colorbar:
        norm = BoundaryNorm(levels, len(colors))

    else:
        norm = None

    # Create figure and axis
    extent = tuple(extent)
    figsize = tuple(figsize)
    fig, ax = kwargs.get('fig', None), kwargs.get('ax', None)
    if fig is None or ax is None:
        fig, ax = get_base_ax(extent=extent, figsize=figsize, central_longitude=central_longitude)

    # Plot shaded data
    lon, lat = np.meshgrid(xarray_data[dim_lon], xarray_data[dim_lat])
    cf = ax.contourf(lon, lat, xarray_data, transform=ccrs.PlateCarree(), transform_first=True, origin='upper', levels=levels, colors=colors, extend='both', cmap=cmap, norm=norm)

    # Colorbar
    if colorbar_position == 'vertical':
        axins = inset_axes(ax, width="3%", height="100%", loc='right', borderpad=-2.7)
        cb = fig.colorbar(cf, cax=axins, orientation='vertical', label=label_colorbar, ticks=levels, extendrect=True)

    elif colorbar_position == 'horizontal':
        axins = inset_axes(ax, width="95%", height="2%", loc='lower center', borderpad=-3.6)
        cb = fig.colorbar(cf, cax=axins, orientation='horizontal', ticks=levels if len(levels)<=26 else levels[::2], extendrect=True, label=label_colorbar)

    if cbar_ticks is not None:
        cb.set_ticks(cbar_ticks)

    # Shapefiles if provided
    if shapefiles is not None:
        for shapefile in shapefiles:
            gdf = gpd.read_file(shapefile)
            gdf.plot(ax=ax, facecolor='none', edgecolor='black', linewidths=1, alpha=0.5, transform=ccrs.PlateCarree())

    # Title
    ax.set_title(title, fontsize=title_size)

    savefigure_kwargs = kwargs.get('savefigure', True)
    if savefigure_kwargs:
        os.makedirs(path_save, exist_ok=True)
        plt.savefig(f'{path_save}/{output_filename}', bbox_inches='tight')
        plt.close(fig)
        print(f'✅ Plot saved as {path_save}/{output_filename}')
    return fig, ax

def plot_contour_from_xarray(xarray_data, dim_lat='latitude', dim_lon='longitude', shapefiles=None, **kwargs):

    '''Plot contour lines from an xarray Dataset'''

    import geopandas as gpd
    import numpy as np
    import os

    '''Plot shaded data from an xarray DataArray'''

    # Default parameters
    extent = kwargs.get('extent', [240, 360, -60, 20])
    figsize = kwargs.get('figsize', (12, 12))
    central_longitude = kwargs.get('central_longitude', 0)
    title_size = kwargs.get('title_size', 16)
    title = kwargs.get('title', '')
    path_save = kwargs.get('path_save', './tmp/plots')
    output_filename = kwargs.get('output_filename', 'shaded_plot.png')

    # Create figure and axis
    extent = tuple(extent)
    figsize = tuple(figsize)
    fig, ax = kwargs.get('fig', None), kwargs.get('ax', None)
    if fig is None or ax is None:
        fig, ax = get_base_ax(extent=extent, figsize=figsize, central_longitude=central_longitude)

    # Plot shaded data
    lon, lat = np.meshgrid(xarray_data[dim_lon], xarray_data[dim_lat])
    contour_levels = kwargs.get('contour_levels', [np.arange(np.nanmin(xarray_data), np.nanmax(xarray_data), 5)])
    colors_levels = kwargs.get('colors_levels', ['red'])

    for color, level in zip(colors_levels, contour_levels):
        cf = ax.contour(lon, lat, xarray_data, levels=level, colors=color, linestyles='solid', linewidths=1.5, transform=ccrs.PlateCarree(), transform_first=True)
        plt.clabel(cf, inline=True, fmt='%.0f', fontsize=15, colors=color)

    # Shapefiles if provided
    if shapefiles is not None:
        for shapefile in shapefiles:
            gdf = gpd.read_file(shapefile)
            gdf.plot(ax=ax, facecolor='none', edgecolor='black', linewidths=1, alpha=0.5, transform=ccrs.PlateCarree())

    # Title
    ax.set_title(title, fontsize=title_size)

    savefigure_kwargs = kwargs.get('savefigure', True)
    if savefigure_kwargs:
        os.makedirs(path_save, exist_ok=True)
        plt.savefig(f'{path_save}/{output_filename}', bbox_inches='tight')
        plt.close(fig)
        print(f'✅ Plot saved as {path_save}/{output_filename}')

    return fig, ax

def plot_multipletypes_from_xarray(xarray_data, plot_var: str, dim_lat='latitude', dim_lon='longitude', shapefiles=None, plot_types=['shaded', 'contour', 'quiver'], **kwargs):

    '''Plot multiple types of data (shaded, contour lines, wind barbs) from an xarray Dataset'''
    
    from meteoplots.colorbars import custom_colorbar
    from matplotlib.colors import BoundaryNorm
    from mpl_toolkits.axes_grid1.inset_locator import inset_axes
    import geopandas as gpd
    import numpy as np
    import os

    # Pre-extract common parameters to avoid repeated kwargs.get() calls
    extent = kwargs.get('extent', [240, 360, -60, 20])
    figsize = kwargs.get('figsize', (12, 12))
    central_longitude = kwargs.get('central_longitude', 0)
    title_size = kwargs.get('title_size', 16)
    title = kwargs.get('title', '')
    path_save = kwargs.get('path_save', './tmp/plots')
    normalize_colorbar = kwargs.get('normalize_colorbar', False)
    
    # Create figure and axis once
    extent = tuple(extent)
    figsize = tuple(figsize)
    fig, ax = get_base_ax(extent=extent, figsize=figsize, central_longitude=central_longitude)
    
    # Pre-load and cache shapefiles to avoid repeated file I/O
    gdfs = []
    if shapefiles is not None:
        print('Loading shapefiles...')
        for shapefile in shapefiles:
            gdfs.append(gpd.read_file(shapefile))
    
    # Pre-compute coordinate grids if any plotting will be done
    lon_data = None
    lat_data = None
    lon_grid = None
    lat_grid = None
    
    if 'shaded' in plot_types or 'contour' in plot_types:
        # Get coordinate data from the first available dataset
        if 'shaded' in plot_types and 'shaded' in xarray_data:
            lon_data = xarray_data['shaded'][dim_lon]
            lat_data = xarray_data['shaded'][dim_lat]
        elif 'contour' in plot_types and 'contour' in xarray_data:
            lon_data = xarray_data['contour'][dim_lon]
            lat_data = xarray_data['contour'][dim_lat]
        
        if lon_data is not None and lat_data is not None:
            lon_grid, lat_grid = np.meshgrid(lon_data, lat_data)

    # Plot shaded data
    if 'shaded' in plot_types and 'shaded' in xarray_data:
        print('Plotting shaded...')
        
        # Get colorbar configuration
        levels, colors, cmap, cbar_ticks = custom_colorbar(plot_var)
        
        if colors is not None and cmap is not None:
            colors = None

        if normalize_colorbar:
            norm = BoundaryNorm(levels, len(colors) if colors else len(levels))
        else:
            norm = None
        
        # Plot using pre-computed coordinates
        cf = ax.contourf(lon_grid, lat_grid, xarray_data['shaded'], 
                        transform=ccrs.PlateCarree(), transform_first=True, 
                        origin='upper', levels=levels, colors=colors, 
                        extend='both', cmap=cmap, norm=norm)
        
        # Add colorbar
        colorbar_position = kwargs.get('colorbar_position', 'horizontal')
        label_colorbar = kwargs.get('label_colorbar', '')
        
        if colorbar_position == 'vertical':
            axins = inset_axes(ax, width="3%", height="100%", loc='right', borderpad=-2.7)
            cb = fig.colorbar(cf, cax=axins, orientation='vertical', label=label_colorbar, 
                            ticks=levels, extendrect=True)
        elif colorbar_position == 'horizontal':
            axins = inset_axes(ax, width="95%", height="2%", loc='lower center', borderpad=-3.6)
            cb = fig.colorbar(cf, cax=axins, orientation='horizontal', 
                            ticks=levels if len(levels)<=26 else levels[::2], 
                            extendrect=True, label=label_colorbar)

        if cbar_ticks is not None:
            cb.set_ticks(cbar_ticks)

    # Plot contour lines
    if 'contour' in plot_types and 'contour' in xarray_data:
        print('Plotting contour...')
        
        contour_levels = kwargs.get('contour_levels', [np.arange(np.nanmin(xarray_data['contour']), 
                                                                np.nanmax(xarray_data['contour']), 5)])
        colors_levels = kwargs.get('colors_levels', ['red'])

        # Plot all contour levels efficiently
        for color, level in zip(colors_levels, contour_levels):
            cf = ax.contour(lon_grid, lat_grid, xarray_data['contour'], levels=level, 
                          colors=color, linestyles='solid', linewidths=1.5, 
                          transform=ccrs.PlateCarree(), transform_first=True)
            plt.clabel(cf, inline=True, fmt='%.0f', fontsize=15, colors=color)

    # Plot quiver (wind vectors)
    if 'quiver' in plot_types and 'quiver' in xarray_data:
        print('Plotting quiver...')
        
        # Get quiver parameters
        quiver_skip = kwargs.get('quiver_skip', 2)  # Skip every N points for cleaner display
        
        # Expect quiver data to have 'u_quiver' and 'v_quiver' components
        u_data = xarray_data['u_quiver']
        v_data = xarray_data['v_quiver']
        
        # Get coordinate data for quiver (might be different resolution than shaded/contour)
        if lon_grid is None or lat_grid is None:
            quiv_lon_data = u_data[dim_lon]
            quiv_lat_data = u_data[dim_lat]
            quiv_lon_grid, quiv_lat_grid = np.meshgrid(quiv_lon_data, quiv_lat_data)
        else:
            quiv_lon_grid, quiv_lat_grid = lon_grid, lat_grid
        
        # Subsample for cleaner display
        quiv_lon_sub = quiv_lon_grid[::quiver_skip, ::quiver_skip]
        quiv_lat_sub = quiv_lat_grid[::quiver_skip, ::quiver_skip]
        u_sub = u_data[::quiver_skip, ::quiver_skip]
        v_sub = v_data[::quiver_skip, ::quiver_skip]
        
        # Plot quiver
        quiver_kwargs= kwargs.get('quiver_kwargs', {'headlength': 4, 'headwidth': 3,'angles': 'uv', 'scale':400})
        qv = ax.quiver(quiv_lon_sub, quiv_lat_sub, u_sub, v_sub, zorder=5,
                      transform=ccrs.PlateCarree(), **quiver_kwargs)

        # Add quiver key if requested
        quiver_key = kwargs.get('quiver_key', None)
        if quiver_key:
            key_length = quiver_key.get('length', 10)
            key_label = quiver_key.get('label', f'{key_length} m/s')
            key_position = quiver_key.get('position', (0.9, 0.95))
            
            ax.quiverkey(qv, key_position[0], key_position[1], key_length, key_label,
                        labelpos='E', coordinates='axes', fontproperties={'size': 12})

    # Add shapefiles once at the end
    if gdfs:
        print('Adding shapefiles...')
        for gdf in gdfs:
            gdf.plot(ax=ax, facecolor='none', edgecolor='black', linewidths=1, 
                    alpha=0.5, transform=ccrs.PlateCarree())

    # Set title
    ax.set_title(title, fontsize=title_size)

    # Handle saving
    savefigure = kwargs.get('savefigure', True)
    
    if savefigure:
        os.makedirs(path_save, exist_ok=True)
        output_filename = kwargs.get('output_filename', 'multiple_plot.png')
        plt.savefig(f'{path_save}/{output_filename}', bbox_inches='tight')
        plt.close(fig)
        print(f'✅ Plot saved as {path_save}/{output_filename}')
    
    return fig, ax


