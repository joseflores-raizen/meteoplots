def calcula_media_bacia(dataset, lat, lon, bacia, codigo, shp):

    import regionmask
    import pandas as pd
    import numpy as np

    if shp[shp['nome'] == bacia].geometry.values[0] is None:
        # print(f'Não há pontos na bacia {bacia}. Código {codigo}. Pegando o mais próximo')
        media = dataset.sel(latitude=lat, longitude=lon, method='nearest')
        media = media.drop_vars(['latitude', 'longitude'])
    else:
        bacia_mask = regionmask.Regions(shp[shp['nome'] == bacia].geometry)
        mask = bacia_mask.mask(dataset.longitude, dataset.latitude)
        chuva_mask = dataset.where(mask == 0)
        media = chuva_mask.mean(('latitude', 'longitude'))

        if pd.isna(media['tp'].values.mean()):
            # print(f'Não há pontos na bacia {bacia}. Código {codigo}. Pegando o mais próximo')
            media = dataset.sel(latitude=lat, longitude=lon, method='nearest')
            media = media.drop_vars(['latitude', 'longitude'])

    return media.expand_dims({'id': [codigo]})

def figures_panel(path_figs: str | list, output_file='panel.png', path_to_save='./tmp/paineis/', img_size=(6,6), ncols=None, nrows=None):

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
