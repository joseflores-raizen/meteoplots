
def calculate_mean_basin_value_from_shapefile(dataset, basin, shp, dim_lat='lat', dim_lon='lon'):

    import regionmask
    import pandas as pd

    mask = regionmask.Regions(shp[shp['Nome_Bacia'] == basin].geometry)
    mask = mask.mask(dataset[dim_lon], dataset[dim_lat])
    mask_var = dataset.where(mask==0)
    mean_mask = mask_var.mean(dim=[dim_lat, dim_lon], skipna=True)
    valor = mean_mask.item()
    mean_mask = pd.DataFrame({"valor": [valor], "basin": [basin], dim_lat: [shp[shp['Nome_Bacia'] == basin].centroid.y.values[0]], dim_lon: [shp[shp['Nome_Bacia'] == basin].centroid.x.values[0]]})

    return mean_mask

def figures_panel(path_figs, output_file='panel.png', path_to_save='./tmp/paineis/', img_size=(6,6), ncols=None, nrows=None):

    import matplotlib.pyplot as plt 
    from PIL import Image
    import os, math

    if isinstance(path_figs, list):
        lista_png = path_figs
        lista_png = [x for x in lista_png if x.endswith('.png')]
    
    elif isinstance(path_figs, str):
        lista_png = os.listdir(path_figs)
        lista_png = [f'{path_figs}/{x}' for x in lista_png if x.endswith('.png')]

    n_imgs = len(lista_png)

    if ncols is not None and nrows is not None:
        pass

    else:
        ncols = 2 if n_imgs > 3 else n_imgs
        nrows = math.ceil(n_imgs / ncols)

    # ajusta dinamicamente o tamanho da figura
    figsize = (img_size[0]*ncols, img_size[1]*nrows)

    fig, axs = plt.subplots(nrows=nrows, ncols=ncols, figsize=figsize, constrained_layout=True)

    if isinstance(axs, plt.Axes):
        axs = [axs]
    else:
        axs = axs.flatten()

    for i, img_path in enumerate(lista_png):
        img = Image.open(img_path)
        axs[i].imshow(img)
        axs[i].axis("off")

    for j in range(n_imgs, len(axs)):
        axs[j].axis("off")

    if output_file:
        os.makedirs(path_to_save, exist_ok=True)
        fig.savefig(f'{path_to_save}/{output_file}', dpi=300, bbox_inches="tight", pad_inches=0)
        print(f"✅ Painel salvo em: {output_file}")
        return f'{path_to_save}/{output_file}'


