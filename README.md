# meteoplots

Biblioteca para geração de gráficos meteorológicos (chuva, vento, SST, etc.) em Python.

---

## 📦 Instalação

Você pode instalar diretamente a partir do GitHub:

```bash
pip install git+https://github.com/joseflores-raizen/meteoplots.git
```

---

## 🎯 Funções Principais

### 📊 **Funções de Plotagem**

#### `plot_contourf_from_xarray()`
Cria gráficos preenchidos (contourf) a partir de dados xarray.

```python
from meteoplots.plots import plot_contourf_from_xarray

# Exemplo básico
fig, ax = plot_contourf_from_xarray(
    xarray_data=temperatura_data,
    plot_var='temperature',
    title='Temperatura do Ar - 2m',
    extent=[-60, -30, -35, 5],  # [lon_min, lon_max, lat_min, lat_max]
    figsize=(12, 8)
)
```

**Parâmetros principais:**
- `xarray_data`: Dados em formato xarray DataArray
- `plot_var`: Variável meteorológica para colorbar automática
- `dim_lat/dim_lon`: Nomes das dimensões de latitude/longitude
- `extent`: Extensão geográfica [lon_min, lon_max, lat_min, lat_max]
- `normalize_colorbar`: Normalização da barra de cores
- `shapefiles`: Lista de shapefiles para sobreposição

#### `plot_contour_from_xarray()`
Cria linhas de contorno a partir de dados xarray.

```python
from meteoplots.plots import plot_contour_from_xarray

# Linhas de contorno para pressão
fig, ax = plot_contour_from_xarray(
    xarray_data=pressao_data,
    contour_levels=[np.arange(1000, 1020, 2)],
    colors_levels=['red'],
    title='Linhas de Pressão (hPa)'
)
```

**Parâmetros específicos:**
- `contour_levels`: Lista de níveis para contorno
- `colors_levels`: Cores das linhas de contorno
- `styles_levels`: Estilos das linhas

#### `plot_quiver_from_xarray()`
Cria gráficos de vetores de vento (quiver plots).

```python
from meteoplots.plots import plot_quiver_from_xarray

# Vetores de vento
fig, ax = plot_quiver_from_xarray(
    xarray_u=u_component,
    xarray_v=v_component,
    quiver_skip=3,  # Skip pontos para visualização mais limpa
    quiver_kwargs={'scale': 400, 'headwidth': 3},
    quiver_key={'length': 10, 'label': '10 m/s'}
)
```

**Parâmetros específicos:**
- `xarray_u/xarray_v`: Componentes U e V do vento
- `quiver_skip`: Subsampling para visualização mais limpa
- `quiver_kwargs`: Parâmetros do matplotlib quiver
- `quiver_key`: Configuração da legenda de escala

#### `plot_streamplot_from_xarray()`
Cria linhas de fluxo (streamlines) para campos de vento.

```python
from meteoplots.plots import plot_streamplot_from_xarray

# Linhas de fluxo
fig, ax = plot_streamplot_from_xarray(
    xarray_u=u_component,
    xarray_v=v_component,
    stream_kwargs={'density': 2, 'color': 'blue', 'linewidth': 1.5},
    stream_color_by_magnitude=True,  # Cor baseada na magnitude
    stream_cmap='viridis'
)
```

**Parâmetros específicos:**
- `stream_kwargs`: Parâmetros do matplotlib streamplot
- `stream_color_by_magnitude`: Colorir por magnitude do vento
- `stream_cmap`: Colormap para magnitude
- `stream_colorbar`: Mostrar barra de cores

#### `plot_multipletypes_from_xarray()`
**🌟 Função principal** - Combina múltiplos tipos de plot em um único gráfico.

```python
from meteoplots.plots import plot_multipletypes_from_xarray

# Exemplo completo combinando múltiplos plots
fig, ax = plot_multipletypes_from_xarray(
    xarray_data={
        'contourf': temperatura_data,
        'contour': pressao_data,
        'u_quiver': u_component,
        'v_quiver': v_component
    },
    plot_var='temperature',
    plot_types=['contourf', 'contour', 'quiver', 'streamplot'],
    title='Análise Meteorológica Completa',
    extent=[-60, -30, -35, 5],
    figsize=(15, 10),
    
    # Parâmetros específicos para cada tipo
    contour_levels=[np.arange(1010, 1025, 2)],
    colors_levels=['black'],
    quiver_skip=4,
    streamplot_kwargs={'density': 1.5, 'color': 'white', 'alpha': 0.7}
)
```

**Tipos de plot disponíveis:**
- `'contourf'`: Dados preenchidos com cores
- `'contour'`: Linhas de contorno
- `'quiver'`: Vetores de vento
- `'streamplot'`: Linhas de fluxo

---

## ⚙️ **Parâmetros Comuns**

### 🗺️ **Configuração Geográfica**
```python
# Configurações de mapa
extent = [-60, -30, -35, 5]  # Brasil: [lon_min, lon_max, lat_min, lat_max]
central_longitude = 0  # Longitude central da projeção
figsize = (12, 8)  # Tamanho da figura
```

### 🎨 **Personalização Visual**
```python
# Títulos e labels
title = 'Meu Gráfico Meteorológico'
title_size = 16
label_colorbar = 'Temperatura (°C)'
colorbar_position = 'horizontal'  # ou 'vertical'

# Salvamento
savefigure = True
path_save = './figuras'
output_filename = 'meu_grafico.png'
```

### 📂 **Shapefiles**
```python
# Adicionar contornos de países/estados
shapefiles = [
    'path/to/brazil_states.shp',
    'path/to/south_america.shp'
]
```

---

## 💡 **Exemplos Práticos**

### Exemplo 1: Temperatura com Contornos de Pressão
```python
import xarray as xr
from meteoplots.plots import plot_multipletypes_from_xarray

# Carregar dados
temp_data = xr.open_dataarray('temperatura.nc')
pres_data = xr.open_dataarray('pressao.nc')

# Plotar
plot_multipletypes_from_xarray(
    xarray_data={'contourf': temp_data, 'contour': pres_data},
    plot_var='temperature',
    plot_types=['contourf', 'contour'],
    title='Temperatura + Pressão',
    extent=[-75, -30, -35, 10],
    contour_levels=[np.arange(1000, 1030, 4)],
    colors_levels=['black']
)
```

### Exemplo 2: Campo de Vento Completo
```python
# Dados de vento
u_wind = xr.open_dataarray('u_component.nc')
v_wind = xr.open_dataarray('v_component.nc')

# Plotar vetores e linhas de fluxo
plot_multipletypes_from_xarray(
    xarray_data={'u_quiver': u_wind, 'v_quiver': v_wind},
    plot_types=['quiver', 'streamplot'],
    title='Campo de Vento - 850 hPa',
    quiver_skip=5,
    streamplot_kwargs={'density': 2, 'color': 'red', 'alpha': 0.6}
)
```

---

## 🎨 **Colorbars Automáticas**

A biblioteca inclui colorbars pré-configuradas para variáveis meteorológicas:

- `temperature`: Temperaturas do ar
- `precipitation`: Precipitação
- `wind_speed`: Velocidade do vento
- `pressure`: Pressão atmosférica
- `humidity`: Umidade relativa
- E muitas outras...

---

## 📚 **Dependências**

- `matplotlib` >= 3.0
- `cartopy` >= 0.18
- `xarray` >= 0.16
- `numpy` >= 1.18
- `geopandas` >= 0.8 (opcional, para shapefiles)

---

## 🤝 **Contribuições**

Contribuições são bem-vindas! Por favor, abra issues ou pull requests no repositório do GitHub.

---

## 📄 **Licença**

Este projeto está licenciado sob a licença MIT.
