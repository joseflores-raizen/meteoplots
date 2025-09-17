
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

    fig, ax = None, None

    if 'shaded' in plot_types:

        print('Plotting shaded...')

        fig, ax = plot_shaded_from_xarray(
            xarray_data=xarray_data['shaded'],
            plot_var=plot_var,
            dim_lat=dim_lat,
            dim_lon=dim_lon,
            shapefiles=shapefiles,
            fig=fig,
            ax=ax,
            savefigure=kwargs.get('savefigure_shaded', False),
            **kwargs
        )

    if 'contour' in plot_types:

        print('Plotting contour...')

        fig, ax = plot_contour_from_xarray(
            xarray_data=xarray_data['contour'],
            plot_var=plot_var,
            dim_lat=dim_lat,
            dim_lon=dim_lon,
            shapefiles=shapefiles,
            fig=fig,
            ax=ax,
            savefigure=kwargs.get('savefigure_contour', False),
            **kwargs
        )

    return


