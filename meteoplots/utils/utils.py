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
