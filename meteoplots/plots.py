
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

def add_box_to_plot(ax, extent_boxes:list, **kwargs):

    import matplotlib.patches as mpatches

    '''Add a rectangular box to an existing plot'''

    # Default parameters
    edgecolor = kwargs.get('edgecolor_box', 'black')
    facecolor = kwargs.get('facecolor_box', 'none')
    linewidth = kwargs.get('linewidth_box', 1)
    linestyle = kwargs.get('linestyle_box', '-')
    alpha = kwargs.get('alpha_box', 1.0)

    # Create a rectangle patch
    for extent_box in extent_boxes:
        rect = mpatches.Rectangle((extent_box[0], extent_box[2]), extent_box[1]-extent_box[0], extent_box[3]-extent_box[2],
                                linewidth=linewidth, edgecolor=edgecolor, facecolor=facecolor, linestyle=linestyle, alpha=alpha,
                                transform=ccrs.PlateCarree())

        # Add the rectangle to the axes
        ax.add_patch(rect)

    return

def plot_contourf_from_xarray(xarray_data, plot_var_colorbar=None, dim_lat='latitude', dim_lon='longitude', shapefiles=None, normalize_colorbar=False, **kwargs):

    from meteoplots.colorbar.colorbars import custom_colorbar
    from meteoplots.utils.utils import calculate_mean_basin_value_from_shapefile
    from matplotlib.colors import BoundaryNorm
    from mpl_toolkits.axes_grid1.inset_locator import inset_axes
    import geopandas as gpd
    import numpy as np
    import os

    '''Plot contourf data from an xarray DataArray'''

    # Default parameters
    extent = kwargs.get('extent', [280, 330, -35, 10])
    figsize = kwargs.get('figsize', (12, 12))
    central_longitude = kwargs.get('central_longitude', 0)
    title_size = kwargs.get('title_size', 16)
    title = kwargs.get('title', '')
    title_loc = kwargs.get('title_loc', 'left')
    colorbar_position = kwargs.get('colorbar_position', 'horizontal')
    label_colorbar = kwargs.get('label_colorbar', '')
    path_save = kwargs.get('path_save', './tmp/plots')
    output_filename = kwargs.get('output_filename', 'contourf_plot.png')

    # Colormap and levels
    if plot_var_colorbar is None:
        # If no plot_var_colorbar provided, user must provide colorbar parameters manually
        levels = kwargs.get('levels', None)
        colors = kwargs.get('colors', None)
        cmap = kwargs.get('cmap', None)
        cbar_ticks = kwargs.get('cbar_ticks', None)
        
        # Check if required colorbar parameters are provided
        if levels is None or (colors is None and cmap is None):
            raise ValueError(
                "When plot_var_colorbar is None, you must provide either:\n"
                "1. 'levels' and 'colors' parameters, or\n"
                "2. 'levels' and 'cmap' parameters\n"
                "Example: plot_contourf_from_xarray(data, levels=[0,5,10], colors=['blue','red'])\n"
                "Or use: plot_contourf_from_xarray(data, plot_var_colorbar='tp')"
            )
    else:
        levels, colors, cmap, cbar_ticks = custom_colorbar(variavel_plotagem=plot_var_colorbar)

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

    # Plot contourf data
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
    ax.set_title(title, fontsize=title_size, loc=title_loc)

    # add mean values from shapefile whit geometry centroids
    shp_path_bacias = kwargs.get('shp_path_bacias', None)
    add_values_from_shapefile = kwargs.get('add_values_from_shapefile', False)
    basin_column_name = kwargs.get('basin_column_name', 'Nome_Bacia')
    
    if shp_path_bacias is not None and add_values_from_shapefile:

        print("Calculating mean values for each basin...")

        import pandas as pd

        # criando a var para tp no dataset se nao existir, o valor será o mesmo
        shp = gpd.read_file(shp_path_bacias).to_crs(epsg=4326)
        shp['centroid'] = shp['geometry'].centroid
        shp['lat'] = shp['centroid'].y
        shp['lon'] = shp['centroid'].x

        mean_values = []
        for basin in shp[basin_column_name].unique():
            mean_value = calculate_mean_basin_value_from_shapefile(dataset=xarray_data, shp=shp, basin=basin, dim_lat=dim_lat, dim_lon=dim_lon)
            mean_values.append(mean_value)

        media_bacia = pd.concat(mean_values, ignore_index=True)

        # Itera sobre as bacias e adiciona as anotações no mapa
        for _, row in media_bacia.iterrows():

            lon, lat = row[dim_lon], row[dim_lat]  # Extrai coordenadas do centroide
            lon = lon+360
            ax.text(lon, lat, f"{row['valor']:.0f}", fontsize=13, color='black', fontweight='bold', ha='center', va='center', transform=ccrs.PlateCarree())

    # Add box if extent_box is provided
    box_patches = kwargs.get('box_patches', None)
    if box_patches is not None:
        add_box_to_plot(ax, box_patches, **kwargs)

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

    # Default parameters
    extent = kwargs.get('extent', [240, 360, -60, 20])
    figsize = kwargs.get('figsize', (12, 12))
    central_longitude = kwargs.get('central_longitude', 0)
    title_size = kwargs.get('title_size', 16)
    title_loc = kwargs.get('title_loc', 'left')
    title = kwargs.get('title', '')
    path_save = kwargs.get('path_save', './tmp/plots')
    output_filename = kwargs.get('output_filename', 'contour_plot.png')

    # Create figure and axis
    extent = tuple(extent)
    figsize = tuple(figsize)
    fig, ax = kwargs.get('fig', None), kwargs.get('ax', None)
    if fig is None or ax is None:
        fig, ax = get_base_ax(extent=extent, figsize=figsize, central_longitude=central_longitude)

    # Plot contour data
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
    ax.set_title(title, fontsize=title_size, loc=title_loc)

    # Add box if extent_box is provided
    box_patches = kwargs.get('box_patches', None)
    if box_patches is not None:
        add_box_to_plot(ax, box_patches, **kwargs)

    savefigure_kwargs = kwargs.get('savefigure', True)
    if savefigure_kwargs:
        os.makedirs(path_save, exist_ok=True)
        plt.savefig(f'{path_save}/{output_filename}', bbox_inches='tight')
        plt.close(fig)
        print(f'✅ Plot saved as {path_save}/{output_filename}')

    return fig, ax

def plot_quiver_from_xarray(xarray_u, xarray_v, dim_lat='latitude', dim_lon='longitude', shapefiles=None, **kwargs):

    '''Plot quiver (wind vectors) from xarray DataArrays for u and v components'''

    import geopandas as gpd
    import numpy as np
    import os

    # Default parameters
    extent = kwargs.get('extent', [240, 360, -60, 20])
    figsize = kwargs.get('figsize', (12, 12))
    central_longitude = kwargs.get('central_longitude', 0)
    title_size = kwargs.get('title_size', 16)
    title_loc = kwargs.get('title_loc', 'left')
    title = kwargs.get('title', '')
    path_save = kwargs.get('path_save', './tmp/plots')
    output_filename = kwargs.get('output_filename', 'quiver_plot.png')

    # Quiver parameters
    quiver_skip = kwargs.get('quiver_skip', 2)  # Skip every N points for cleaner display

    # Create figure and axis
    extent = tuple(extent)
    figsize = tuple(figsize)
    fig, ax = kwargs.get('fig', None), kwargs.get('ax', None)
    if fig is None or ax is None:
        fig, ax = get_base_ax(extent=extent, figsize=figsize, central_longitude=central_longitude)

    # Create coordinate grids
    lon, lat = np.meshgrid(xarray_u[dim_lon], xarray_u[dim_lat])
    
    # Subsample for cleaner display
    lon_sub = lon[::quiver_skip, ::quiver_skip]
    lat_sub = lat[::quiver_skip, ::quiver_skip]
    u_sub = xarray_u[::quiver_skip, ::quiver_skip]
    v_sub = xarray_v[::quiver_skip, ::quiver_skip]

    # Plot quiver
    quiver_kwargs= kwargs.get('quiver_kwargs', {'headlength': 4, 'headwidth': 3,'angles': 'uv', 'scale':400})
    qv = ax.quiver(lon_sub, lat_sub, u_sub, v_sub,
                  transform=ccrs.PlateCarree(), zorder=5,
                  **quiver_kwargs)

    # Add quiver key if requested
    quiver_key = kwargs.get('quiver_key', None)
    if quiver_key:
        key_length = quiver_key.get('length', 10)
        key_label = quiver_key.get('label', f'{key_length} m/s')
        key_position = quiver_key.get('position', (0.9, 0.95))
        
        ax.quiverkey(qv, key_position[0], key_position[1], key_length, key_label,
                    labelpos='E', coordinates='axes', fontproperties={'size': 12})

    # Shapefiles if provided
    if shapefiles is not None:
        for shapefile in shapefiles:
            gdf = gpd.read_file(shapefile)
            gdf.plot(ax=ax, facecolor='none', edgecolor='black', linewidths=1, alpha=0.5, transform=ccrs.PlateCarree())

    # Title
    ax.set_title(title, fontsize=title_size, loc=title_loc)

    # Add box if extent_box is provided
    box_patches = kwargs.get('box_patches', None)
    if box_patches is not None:
        add_box_to_plot(ax, box_patches, **kwargs)

    savefigure_kwargs = kwargs.get('savefigure', True)
    if savefigure_kwargs:
        os.makedirs(path_save, exist_ok=True)
        plt.savefig(f'{path_save}/{output_filename}', bbox_inches='tight')
        plt.close(fig)
        print(f'✅ Plot saved as {path_save}/{output_filename}')

    return fig, ax

def plot_streamplot_from_xarray(xarray_u, xarray_v, dim_lat='latitude', dim_lon='longitude', shapefiles=None, **kwargs):

    '''Plot streamlines from xarray DataArrays for u and v components'''

    import geopandas as gpd
    import numpy as np
    import os

    # Default parameters
    extent = kwargs.get('extent', [240, 360, -60, 20])
    figsize = kwargs.get('figsize', (12, 12))
    central_longitude = kwargs.get('central_longitude', 0)
    title_size = kwargs.get('title_size', 16)
    title_loc = kwargs.get('title_loc', 'left')
    title = kwargs.get('title', '')
    path_save = kwargs.get('path_save', './tmp/plots')
    output_filename = kwargs.get('output_filename', 'streamplot.png')

    # Streamplot parameters
    stream_kwargs = kwargs.get('stream_kwargs', {
        'density': 2,
        'color': 'black',
        'linewidth': 1.0,
        'arrowsize': 1.0,
        'arrowstyle': '->',
    })

    # Create figure and axis
    extent = tuple(extent)
    figsize = tuple(figsize)
    fig, ax = kwargs.get('fig', None), kwargs.get('ax', None)
    if fig is None or ax is None:
        fig, ax = get_base_ax(extent=extent, figsize=figsize, central_longitude=central_longitude)

    # Get coordinate arrays
    lon_data = xarray_u[dim_lon].values
    lat_data = xarray_u[dim_lat].values
    u_data = xarray_u.values
    v_data = xarray_v.values

    # Check and convert longitude dimension if needed (0-360 to -180-180)
    if lon_data.max() > 180:
        print("Converting longitude from 0-360 to -180-180 degrees...")
        # Convert longitude values
        lon_data = np.where(lon_data > 180, lon_data - 360, lon_data)
        
        # Sort indices for proper ordering
        sort_idx = np.argsort(lon_data)
        lon_data = lon_data[sort_idx]
        u_data = u_data[:, sort_idx]
        v_data = v_data[:, sort_idx]

    # Create coordinate grids
    lon_grid, lat_grid = np.meshgrid(lon_data, lat_data)

    # Create streamplot
    stream = ax.streamplot(lon_grid, lat_grid, u_data, v_data,
                          transform=ccrs.PlateCarree(),
                          **stream_kwargs
                          )

    # Add magnitude-based coloring if requested
    stream_color_by_magnitude = kwargs.get('stream_color_by_magnitude', False)
    if stream_color_by_magnitude:
        # remove color from stream_kwargs to avoid conflict
        if 'color' in stream_kwargs:
            del stream_kwargs['color']
        magnitude = np.sqrt(u_data**2 + v_data**2)
        stream = ax.streamplot(lon_grid, lat_grid, u_data, v_data,
                               color=magnitude, transform=ccrs.PlateCarree(), cmap=kwargs.get('stream_cmap', 'viridis'), **stream_kwargs)
        
        # Add colorbar for magnitude
        if kwargs.get('stream_colorbar', True):
            from mpl_toolkits.axes_grid1.inset_locator import inset_axes
            axins = inset_axes(ax, width="95%", height="2%", loc='lower center', borderpad=-3.6)
            cb = fig.colorbar(stream.lines, cax=axins, orientation='horizontal', 
                            label=kwargs.get('stream_colorbar_label', 'Wind Speed (m/s)'))

    # Shapefiles if provided
    if shapefiles is not None:
        for shapefile in shapefiles:
            gdf = gpd.read_file(shapefile)
            gdf.plot(ax=ax, facecolor='none', edgecolor='black', linewidths=1, alpha=0.5, transform=ccrs.PlateCarree())

    # Title
    ax.set_title(title, fontsize=title_size, loc=title_loc)

    # Add box if extent_box is provided
    box_patches = kwargs.get('box_patches', None)
    if box_patches is not None:
        add_box_to_plot(ax, box_patches, **kwargs)


    savefigure_kwargs = kwargs.get('savefigure', True)
    if savefigure_kwargs:
        os.makedirs(path_save, exist_ok=True)
        plt.savefig(f'{path_save}/{output_filename}', bbox_inches='tight')
        plt.close(fig)
        print(f'✅ Plot saved as {path_save}/{output_filename}')

    return fig, ax

def plot_multipletypes_from_xarray(xarray_data, plot_var_colorbar=None, dim_lat='latitude', dim_lon='longitude', shapefiles=None, plot_types=['contourf', 'contour', 'quiver', 'streamplot'], **kwargs):

    '''Plot multiple types of data (contourf, contour lines, wind vectors, streamlines) from an xarray Dataset'''
    
    from meteoplots.colorbar.colorbars import custom_colorbar
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
    title_loc = kwargs.get('title_loc', 'left')
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
    
    # Pre-process wind data coordinates if quiver or streamplot are requested
    wind_lon_data = None
    wind_lat_data = None
    wind_lon_grid = None
    wind_lat_grid = None
    u_wind_data = None
    v_wind_data = None
    
    if ('quiver' in plot_types or 'streamplot' in plot_types) and 'u_quiver' in xarray_data and 'v_quiver' in xarray_data:
        print('Pre-processing wind data coordinates...')
        u_data = xarray_data['u_quiver']
        v_data = xarray_data['v_quiver']
        
        wind_lon_data = u_data[dim_lon].values
        wind_lat_data = u_data[dim_lat].values
        u_wind_data = u_data.values
        v_wind_data = v_data.values
        
        # Check and convert longitude dimension if needed (0-360 to -180-180)
        if wind_lon_data.max() > 180:
            print("Converting longitude from 0-360 to -180-180 degrees for wind data...")
            wind_lon_data = np.where(wind_lon_data > 180, wind_lon_data - 360, wind_lon_data)
            sort_idx = np.argsort(wind_lon_data)
            wind_lon_data = wind_lon_data[sort_idx]
            u_wind_data = u_wind_data[:, sort_idx]
            v_wind_data = v_wind_data[:, sort_idx]
        
        wind_lon_grid, wind_lat_grid = np.meshgrid(wind_lon_data, wind_lat_data)
    
    if 'contourf' in plot_types or 'contour' in plot_types:
        # Get coordinate data from the first available dataset
        if 'contourf' in plot_types and 'contourf' in xarray_data:
            lon_data = xarray_data['contourf'][dim_lon]
            lat_data = xarray_data['contourf'][dim_lat]
        elif 'contour' in plot_types and 'contour' in xarray_data:
            lon_data = xarray_data['contour'][dim_lon]
            lat_data = xarray_data['contour'][dim_lat]
        
        if lon_data is not None and lat_data is not None:
            lon_grid, lat_grid = np.meshgrid(lon_data, lat_data)

    # Plot contourf data
    if 'contourf' in plot_types and 'contourf' in xarray_data:
        print('Plotting contourf...')
        
        # Colormap and levels
        if plot_var_colorbar is None:
            # If no plot_var_colorbar provided, user must provide colorbar parameters manually
            levels = kwargs.get('levels', None)
            colors = kwargs.get('colors', None)
            cmap = kwargs.get('cmap', None)
            cbar_ticks = kwargs.get('cbar_ticks', None)
            
            # Check if required colorbar parameters are provided
            if levels is None or (colors is None and cmap is None):
                raise ValueError(
                    "When plot_var_colorbar is None, you must provide either:\n"
                    "1. 'levels' and 'colors' parameters, or\n"
                    "2. 'levels' and 'cmap' parameters\n"
                    "Example: plot_multipletypes_from_xarray(data, levels=[0,5,10], colors=['blue','red'])\n"
                    "Or use: plot_multipletypes_from_xarray(data, plot_var_colorbar='tp')"
                )
        else:
            levels, colors, cmap, cbar_ticks = custom_colorbar(variavel_plotagem=plot_var_colorbar)
        
        if colors is not None and cmap is not None:
            colors = None

        if normalize_colorbar:
            norm = BoundaryNorm(levels, len(colors) if colors else len(levels))
        else:
            norm = None
        
        # Plot using pre-computed coordinates
        cf = ax.contourf(lon_grid, lat_grid, xarray_data['contourf'], 
                        transform=ccrs.PlateCarree(), transform_first=True, 
                        origin='upper', levels=levels, colors=colors, 
                        extend='both', cmap=cmap, norm=norm)
        
        # Add colorbar
        colorbar_position = kwargs.get('colorbar_position', 'horizontal')
        label_colorbar = kwargs.get('label_colorbar', '[units]')
        
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
        
        contour_levels = kwargs.get('contour_levels', [np.arange(np.nanmin(xarray_data['contour']), np.nanmax(xarray_data['contour']), 1)])
        colors_levels = kwargs.get('colors_levels', ['red'])
        styles_levels = kwargs.get('styles_levels', ['solid'])

        # Plot all contour levels efficiently
        for color, level, style in zip(colors_levels, contour_levels, styles_levels):

            cf = ax.contour(lon_grid, lat_grid, xarray_data['contour'], levels=level, 
                          colors=color, linestyles=style, linewidths=1.5, 
                          transform=ccrs.PlateCarree(), transform_first=True)
            plt.clabel(cf, inline=True, fmt='%.0f', fontsize=15, colors=color)

    # Plot quiver (wind vectors)
    if 'quiver' in plot_types and 'u_quiver' in xarray_data and 'v_quiver' in xarray_data:
        print('Plotting quiver...')
        
        # Get quiver parameters
        quiver_skip = kwargs.get('quiver_skip', 2)  # Skip every N points for cleaner display
        
        # Use pre-processed wind data
        quiv_lon_grid = wind_lon_grid
        quiv_lat_grid = wind_lat_grid
        u_data = u_wind_data
        v_data = v_wind_data
        
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

    # Plot streamlines
    if 'streamplot' in plot_types and 'u_quiver' in xarray_data and 'v_quiver' in xarray_data:
        print('Plotting streamlines...')
        
        # Get streamplot parameters
        streamplot_kwargs = kwargs.get('streamplot_kwargs', {
            'density': 2,
            'color': 'blue',
            'linewidth': 1.0,
            'arrowsize': 1.0,
            'arrowstyle': '->',
        })
        
        # Use pre-processed wind data
        stream_lon_grid = wind_lon_grid
        stream_lat_grid = wind_lat_grid
        u_stream_data = u_wind_data
        v_stream_data = v_wind_data
        
        # Create streamplot
        stream_color_by_magnitude = kwargs.get('stream_color_by_magnitude', False)
        if stream_color_by_magnitude:
            magnitude = np.sqrt(u_stream_data**2 + v_stream_data**2)
            # For magnitude coloring, remove 'color' from streamplot_kwargs to avoid conflict
            streamplot_kwargs_mag = streamplot_kwargs.copy()
            if 'color' in streamplot_kwargs_mag:
                del streamplot_kwargs_mag['color']
            stream = ax.streamplot(stream_lon_grid, stream_lat_grid, u_stream_data, v_stream_data,
                                  transform=ccrs.PlateCarree(),
                                  color=magnitude,
                                  cmap=kwargs.get('stream_cmap', 'viridis'),
                                  **streamplot_kwargs_mag)
            
            # Add colorbar for magnitude if not already present
            if kwargs.get('stream_colorbar', True) and 'contourf' not in plot_types:
                axins = inset_axes(ax, width="95%", height="2%", loc='lower center', borderpad=-3.6)
                cb = fig.colorbar(stream.lines, cax=axins, orientation='horizontal', 
                                label=kwargs.get('stream_colorbar_label', 'Wind Speed (m/s)'))
        else:
            stream = ax.streamplot(stream_lon_grid, stream_lat_grid, u_stream_data, v_stream_data,
                                  transform=ccrs.PlateCarree(),
                                  **streamplot_kwargs)

    # Add shapefiles once at the end
    if gdfs:
        print('Adding shapefiles...')
        for gdf in gdfs:
            gdf.plot(ax=ax, facecolor='none', edgecolor='black', linewidths=1, 
                    alpha=0.5, transform=ccrs.PlateCarree())

    # Set title
    ax.set_title(title, fontsize=title_size, loc=title_loc)

    # Add box if extent_box is provided
    box_patches = kwargs.get('box_patches', None)
    if box_patches is not None:
        add_box_to_plot(ax, box_patches, **kwargs)

    # Handle saving
    savefigure = kwargs.get('savefigure', True)
    if savefigure:
        os.makedirs(path_save, exist_ok=True)
        output_filename = kwargs.get('output_filename', 'multiple_plot.png')
        plt.savefig(f'{path_save}/{output_filename}', bbox_inches='tight')
        print(f'✅ Plot saved as {path_save}/{output_filename}')
        if not kwargs.get('keep_open', False):
            plt.close(fig)
    
    return fig, ax