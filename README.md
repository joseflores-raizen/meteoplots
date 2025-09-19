# meteoplots

Biblioteca para geração de gráficos meteorológicos (chuva, vento, SST, etc.) em Python.

---

## 📦 Instalação

Você pode instalar diretamente a partir do GitHub:

```bash
pip install git+https://github.com/joseflores-raizen/meteoplots.git
pip install --upgrade --force-reinstall --no-cache-dir git+https://github.com/joseflores-raizen/meteoplots.git@main
```

---

## 📊 **Trabalhando com Dados xarray**

A biblioteca meteoplots trabalha exclusivamente com objetos **`xarray.DataArray`** para dados meteorológicos. O xarray é a biblioteca padrão para manipulação de dados científicos multidimensionais em Python.

### O que é xarray.DataArray?
Um `xarray.DataArray` é uma estrutura de dados que combina:
- **Valores numéricos** (dados meteorológicos)
- **Coordenadas** (latitude, longitude, tempo, níveis)
- **Metadados** (atributos, unidades, descrições)

### Carregando Dados Meteorológicos
```python
import xarray as xr
import numpy as np

# Método 1: Carregar de arquivo NetCDF
temperatura = xr.open_dataarray('temperatura_2m.nc')
precipitacao = xr.open_dataset('precipitacao.nc')['tp']  # Extrair variável específica

# Método 2: Criar dados sintéticos para testes
lat = np.arange(-35, 10, 0.5)
lon = np.arange(-75, -30, 0.5)
temp_data = 20 + 10 * np.random.random((len(lat), len(lon)))

temperatura = xr.DataArray(
    temp_data,
    coords=[('latitude', lat), ('longitude', lon)],
    attrs={'units': '°C', 'long_name': 'Temperatura do Ar 2m'}
)

# Método 3: Converter de outros formatos
import pandas as pd
# De pandas DataFrame para xarray
df = pd.read_csv('dados_estacoes.csv')
data_xr = df.set_index(['lat', 'lon']).to_xarray()
```

### Estrutura Típica de Dados Meteorológicos
```python
# Visualizar estrutura do DataArray
print(temperatura)
# Output:
# <xarray.DataArray 'temperature' (latitude: 90, longitude: 90)>
# array([[15.2, 15.4, ...],
#        [16.1, 16.3, ...], ...])
# Coordinates:
#   * latitude   (latitude) float64 -35.0 -34.5 ... 9.0 9.5
#   * longitude  (longitude) float64 -75.0 -74.5 ... -30.5 -30.0
# Attributes:
#     units:      °C
#     long_name:  Temperatura do Ar 2m
```

### Verificando Dimensões e Coordenadas
```python
# Verificar dimensões necessárias para meteoplots
print("Dimensões:", list(temperatura.dims))  # Deve incluir 'latitude' e 'longitude'
print("Coordenadas:", list(temperatura.coords))
print("Shape:", temperatura.shape)

# Renomear dimensões se necessário
if 'lat' in temperatura.dims:
    temperatura = temperatura.rename({'lat': 'latitude', 'lon': 'longitude'})
```

### Preparando Dados para Múltiplos Plots
```python
# Para plot_multipletypes_from_xarray, organize como dicionário
dados_multiplos = {
    'contourf': temperatura,      # Para plot preenchido
    'contour': pressao,           # Para linhas de contorno  
    'u_quiver': componente_u,     # Componente U do vento
    'v_quiver': componente_v      # Componente V do vento
}
```

### Dicas Importantes
- **Coordenadas obrigatórias**: `latitude/lat` e `longitude/lon` ou 
- **Ordem das dimensões**: Não importa, o xarray gerencia automaticamente
- **Sistemas de coordenadas**: A biblioteca aceita lon 0-360° ou -180-180°

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
    plot_var_colorbar='temperature',
    title='Temperatura do Ar - 2m',
    extent=[-60, -30, -35, 5],  # [lon_min, lon_max, lat_min, lat_max]
    figsize=(12, 8)
)
```

**Parâmetros principais:**
- `xarray_data`: Dados em formato xarray DataArray
- `plot_var_colorbar`: Variável meteorológica para colorbar automática
- `dim_lat/dim_lon`: Nomes das dimensões de latitude/longitude
- `extent`: Extensão geográfica [lon_min, lon_max, lat_min, lat_max]
- `normalize_colorbar`: Normalização da barra de cores
- `shapefiles`: Lista de shapefiles para sobreposição

**Parâmetros para análise de bacias:**
- `shp_path_bacias`: Caminho para shapefile de bacias hidrográficas
- `add_values_from_shapefile`: Se `True`, adiciona valores médios das bacias no mapa
- `basin_column_name`: Nome da coluna com identificação das bacias (padrão: 'Nome_Bacia')

#### Exemplo com Análise de Bacias
```python
# Exemplo com cálculo de valores médios por bacia
fig, ax = plot_contourf_from_xarray(
    xarray_data=precipitacao_data,
    plot_var_colorbar='tp',
    title='Precipitação por Bacia Hidrográfica',
    extent=[-60, -30, -35, 5],
    
    # Parâmetros para análise de bacias
    shp_path_bacias='path/to/bacias_hidrograficas.shp',
    add_values_from_shapefile=True,
    basin_column_name='Nome_Bacia',  # Nome da coluna com ID das bacias
    
    figsize=(12, 8)
)
```

**Funcionalidade de Bacias:**
- Calcula automaticamente o valor médio de cada bacia
- Adiciona anotações no centróide de cada bacia
- Útil para análise hidrológica e climatológica regional

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
    plot_var_colorbar='temperature',
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

### 🛡️ **Configuração de Colorbars**
```python
# Método 1: Usar colorbar pré-configurada (recomendado)
plot_contourf_from_xarray(data, plot_var_colorbar='tp')

# Método 2: Configuração manual com levels e colors
plot_contourf_from_xarray(
    data, 
    levels=[0, 5, 10, 15, 20], 
    colors=['blue', 'green', 'yellow', 'red']
)

# Método 3: Configuração manual com levels e cmap
plot_contourf_from_xarray(
    data, 
    levels=[0, 5, 10, 15, 20], 
    cmap='viridis'
)

# ❌ Erro: sem plot_var_colorbar nem configuração manual
# plot_contourf_from_xarray(data)  # Gerará ValueError
```

**Importante:** Se `plot_var_colorbar=None`, você **deve** fornecer:
- `levels` **E** `colors`, ou
- `levels` **E** `cmap`

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
    plot_var_colorbar='temperature',
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

### Exemplo 3: Análise de Bacias Hidrográficas
```python
from meteoplots.plots import plot_contourf_from_xarray
import xarray as xr

# Carregar dados de precipitação
precip_data = xr.open_dataarray('precipitacao_mensal.nc')

# Análise por bacias com valores médios
fig, ax = plot_contourf_from_xarray(
    xarray_data=precip_data,
    plot_var_colorbar='tp',  # Colorbar de precipitação
    title='Precipitação Média por Bacia Hidrográfica',
    extent=[-75, -30, -35, 10],  # Brasil
    
    # Configuração de bacias
    shp_path_bacias='data/bacias_hidrograficas_brasil.shp',
    add_values_from_shapefile=True,
    basin_column_name='Nome_Bacia',
    
    # Sobreposição de estados
    shapefiles=['data/estados_brasil.shp'],
    
    # Configurações visuais
    colorbar_position='horizontal',
    label_colorbar='Precipitação (mm/mês)',
    figsize=(15, 10)
)
```

### Exemplo 4: Usando Funções Utilitárias
```python
from meteoplots.plots import plot_contourf_from_xarray
from meteoplots.colorbars import custom_colorbar
from meteoplots.utils.titles import gerar_titulo
import datetime

# Carregar dados
temp_data = xr.open_dataarray('temperatura.nc')

# Gerar título profissional
titulo = gerar_titulo(
    titulo_principal="Temperatura do Ar",
    nivel="850 hPa",
    unidade="°C",
    modelo="GFS",
    data=datetime.datetime(2024, 1, 15, 12, 0),
    subtitulo="Análise"
)

# Verificar colorbars disponíveis
custom_colorbar(help=True)

# Plotar com colorbar automática
plot_contourf_from_xarray(
    xarray_data=temp_data,
    plot_var_colorbar='temp850',  # Usar colorbar pré-configurada
    title=titulo,
    extent=[-60, -30, -35, 5],
    label_colorbar='Temperatura (°C)'
)
```

---

## �️ **Análise de Bacias Hidrográficas**

A função `plot_contourf_from_xarray()` inclui funcionalidade especial para análise de bacias hidrográficas, calculando automaticamente valores médios por bacia e exibindo-os no mapa.

### Como Funciona
```python
# Ativar análise de bacias
plot_contourf_from_xarray(
    xarray_data=data,
    plot_var_colorbar='tp',
    
    # Parâmetros para bacias
    shp_path_bacias='caminho/para/bacias.shp',
    add_values_from_shapefile=True,
    basin_column_name='Nome_Bacia'  # Coluna com ID das bacias
)
```

### Funcionalidades da Análise de Bacias
- **Cálculo automático**: Valor médio espacial para cada bacia
- **Anotações no mapa**: Valores exibidos no centróide de cada bacia
- **Flexibilidade**: Funciona com qualquer shapefile de polígonos
- **Precisão**: Considera apenas pixels dentro de cada bacia

### Requisitos do Shapefile
- **Geometria**: Polígonos representando as bacias
- **Coluna de identificação**: Nome ou código único para cada bacia
- **Sistema de coordenadas**: Preferencialmente EPSG:4326 (lat/lon)

### Exemplo Prático
```python
# Análise de precipitação por sub-bacias do São Francisco
plot_contourf_from_xarray(
    xarray_data=precipitacao_mensal,
    plot_var_colorbar='tp',
    title='Precipitação - Sub-bacias do Rio São Francisco',
    
    # Configuração das bacias
    shp_path_bacias='dados/sub_bacias_sao_francisco.shp',
    add_values_from_shapefile=True,
    basin_column_name='CODIGO_BACIA',
    
    # Região de interesse
    extent=[-50, -37, -18, -8],
    label_colorbar='Precipitação (mm/mês)'
)
```

### Casos de Uso
- **Hidrologia**: Análise de precipitação por bacia
- **Planejamento hídrico**: Distribuição de recursos
- **Climatologia regional**: Padrões por região
- **Agricultura**: Monitoramento de chuva por fazenda/região

---

## �🎨 **Colorbars Automáticas**

A biblioteca inclui colorbars pré-configuradas para variáveis meteorológicas através da função `custom_colorbar()`.

### `custom_colorbar()`
Gera automaticamente níveis, cores e colormaps para variáveis meteorológicas específicas.

```python
from meteoplots.colorbars import custom_colorbar

# Obter configuração de colorbar para precipitação
levels, colors, cmap, cbar_ticks = custom_colorbar('tp')

# Ver todas as variáveis disponíveis
custom_colorbar(help=True)
```

**Variáveis disponíveis incluem:**
- **Precipitação**: `tp`, `chuva_ons`, `chuva_pnmm`, `tp_anomalia`, `tp_anomalia_mensal`
- **Temperatura**: `temp850`, `temp_anomalia`
- **Vento**: `wind200`, `mag_vento100`, `mag_vento100_anomalia`
- **Pressão**: `pnmm_vento`, `geop_500`, `geop_500_anomalia`
- **Oceanografia**: `sst_anomalia`
- **Campos dinâmicos**: `psi`, `chi`, `vorticidade`, `divergencia850`
- **Outros**: `olr`, `ivt`, `frentes`, `probabilidade`, `geada-inmet`

**Parâmetros:**
- `variavel_plotagem`: Nome da variável meteorológica
- `help`: Se `True`, mostra todas as variáveis disponíveis com preview visual

**Retorna:**
- `levels`: Níveis para contorno/colorbar
- `colors`: Lista de cores (se aplicável)
- `cmap`: Colormap do matplotlib
- `cbar_ticks`: Posições dos ticks na colorbar

---

## 📝 **Geração de Títulos**

### `gerar_titulo()`
Gera títulos formatados e informativos para gráficos meteorológicos.

```python
from meteoplots.utils.titles import gerar_titulo

# Título simples
titulo = gerar_titulo(
    titulo_principal="Temperatura do Ar",
    nivel="2m",
    unidade="°C"
)

# Título completo com metadados
titulo = gerar_titulo(
    titulo_principal="Precipitação Acumulada",
    subtitulo="Previsão 24h",
    data="15/01/2024 12:00",
    nivel="Superfície", 
    unidade="mm",
    modelo="GFS",
    fonte="NOAA"
)
```

**Parâmetros principais:**
- `titulo_principal`: Título principal (ex: "Temperatura do Ar")
- `subtitulo`: Informação adicional
- `data`: Data/hora (string ou datetime)
- `nivel`: Nível atmosférico (ex: "850 hPa", "Superfície")
- `unidade`: Unidade de medida (ex: "°C", "mm/h")
- `modelo`: Nome do modelo (ex: "GFS", "ERA5")
- `fonte`: Fonte dos dados
- `bold_subtitle`: Formatação em negrito (LaTeX)
- `include_datetime`: Incluir timestamp de geração

**Exemplo de saída:**
```
Temperatura do Ar - 2m (°C)
𝐀𝐧á𝐥𝐢𝐬𝐞\ |\ 𝐌𝐨𝐝𝐞𝐥𝐨:\ 𝐆𝐅𝐒\ |\ 𝐃𝐚𝐭𝐚:\ 𝟏𝟓/𝟎𝟏/𝟐𝟎𝟐𝟒\ |\ 𝐆𝐞𝐫𝐚𝐝𝐨\ 𝐞𝐦:\ 𝟏𝟖/𝟎𝟗/𝟐𝟎𝟐𝟓
```

**Características:**
- **Formatação automática**: LaTeX para texto em negrito
- **Timestamp automático**: Data/hora de geração
- **Flexível**: Combine apenas os parâmetros necessários
- **Padrão profissional**: Adequado para relatórios científicos

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
