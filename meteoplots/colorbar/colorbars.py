def custom_colorbar(variavel_plotagem=None, help=False, custom=False):
    
    import numpy as np
    import matplotlib.pyplot as plt
    from matplotlib.colors import ListedColormap, LinearSegmentedColormap, BoundaryNorm

    # Initialize return variables
    levels = None
    colors = None
    cmap = None
    cbar_ticks = None
    
    configs = {
        "chuva_ons": {
            "levels": [0, 1, 5, 10, 15, 20, 25, 30, 40, 50, 75, 100, 150, 200],
            "colors": ['#ffffff', '#e1ffff', '#b3f0fb', '#95d2f9', '#2585f0', '#0c68ce',
                       '#73fd8b', '#39d52b', '#3ba933', '#ffe67b', '#ffbd4a', '#fd5c22',
                       '#b91d22', '#f7596f', '#a9a9a9'],
            "cmap": None,
            "cbar_ticks": None,
        },
        "tp": {
            "levels": [0, 1, 5, 10, 15, 20, 25, 30, 40, 50, 75, 100, 150, 200],
            "colors": ['#ffffff', '#e1ffff', '#b3f0fb', '#95d2f9', '#2585f0', '#0c68ce',
                       '#73fd8b', '#39d52b', '#3ba933', '#ffe67b', '#ffbd4a', '#fd5c22',
                       '#b91d22', '#f7596f', '#a9a9a9'],
            "cmap": None,
            "cbar_ticks": None,
        },
        "chuva_pnmm": {
            "levels": [0, 1, 5, 10, 15, 20, 25, 30, 40, 50, 75, 100, 150, 200],
            "colors": ['#ffffff', '#e1ffff', '#b3f0fb', '#95d2f9', '#2585f0', '#0c68ce',
                       '#73fd8b', '#39d52b', '#3ba933', '#ffe67b', '#ffbd4a', '#fd5c22',
                       '#b91d22', '#f7596f', '#a9a9a9'],
            "cmap": None,
            "cbar_ticks": None,
        },
        "chuva_ons_geodataframe": {
            "levels": [0, 1, 5, 10, 15, 20, 25, 30, 40, 50, 75, 100, 150, 200],
            "colors": ['#ffffff', '#e1ffff', '#b3f0fb', '#95d2f9', '#2585f0', '#0c68ce',
                       '#73fd8b', '#39d52b', '#3ba933', '#ffe67b', '#ffbd4a', '#fd5c22',
                       '#b91d22', '#f7596f', '#a9a9a9'],
            "cmap": lambda colors: ListedColormap(colors),
            "cbar_ticks": None,
        },
        "chuva_boletim_consumidores": {
            "levels": range(-300, 305, 5),
            "colors": ['purple', 'white', 'green'],
            "cmap": lambda colors, levels: plt.get_cmap(
                LinearSegmentedColormap.from_list("CustomCmap", colors),
                len(levels) + 1
            ),
            "cbar_ticks": range(-300, 350, 50),
        },
        "acumulado_total_geodataframe": {
            "levels": range(0, 420, 20),
            "colors": [
                '#FFFFFF', '#B1EDCF', '#97D8B7', '#7DC19E', '#62AA85', '#48936D',
                '#2E7E54', '#14673C', '#14678C', '#337E9F', '#5094B5', '#6DACC8',
                '#8BC4DE', '#A9DBF2', '#EBD5EB', '#D9BED8', '#C5A7C5', '#B38FB2',
                '#A0779F', '#8E5F8D',
            ],
            "cmap": lambda colors, levels: plt.get_cmap(
                LinearSegmentedColormap.from_list("CustomCmap", colors),
                len(levels) + 1
            ),
            "cbar_ticks": None,
        },
        "tp_anomalia": {
            "levels": range(-150, 155, 5),
            "colors": ['mediumvioletred', 'maroon', 'firebrick', 'red', 'chocolate', 'orange',
                       'gold', 'yellow', 'white', 'aquamarine', 'mediumturquoise', 'cyan',
                       'lightblue', 'blue', 'purple', 'mediumpurple', 'blueviolet'],
            "cmap": lambda colors, levels: plt.get_cmap(
                LinearSegmentedColormap.from_list("CustomCmap", colors),
                len(levels) + 1
            ),
            "cbar_ticks": [-150, -125, -100, -75, -50, -25, 0, 25, 50, 75, 100, 125, 150],
        },
        "tp_anomalia_mensal": {
            "levels": range(-300, 305, 5),
            "colors": ['mediumvioletred', 'maroon', 'firebrick', 'red', 'chocolate', 'orange',
                       'gold', 'yellow', 'white', 'aquamarine', 'mediumturquoise', 'cyan',
                       'lightblue', 'blue', 'purple', 'mediumpurple', 'blueviolet'],
            "cmap": lambda colors, levels: plt.get_cmap(
                LinearSegmentedColormap.from_list("CustomCmap", colors),
                len(levels) + 1
            ),
            "cbar_ticks": range(-300, 350, 50),
        },
        "chuva_acumualada_merge": {
            "levels": [0, 1, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 24, 28, 32, 36, 40, 50, 60, 80,
                       100, 120, 140, 160, 180, 200, 220, 240, 260, 280, 300],
            "colors": ["#ffffff", "#e6e6e6", "#bebebe", "#969696", "#6e6e6e", "#c8ffbe",
                       "#96f58c", "#50f050", "#1eb41e", "#057805", "#0a50aa", "#1464d2",
                       "#2882f0", "#50a5f5", "#96d2fa", "#e1ffff", "#fffaaa", "#ffe878",
                       "#ffc03c", "#ffa000", "#ff6000", "#ff3200", "#e11400", "#a50000",
                       "#c83c3c", "#e67070", "#f8a0a0", "#ffe6e6", "#cdcdff", "#b4a0ff",
                       "#8c78ff", "#6455dc", "#3c28b4"],
            "cmap": None,
            "cbar_ticks": None,
        },
        "chuva_acumualada_merge_anomalia": {
            "levels": lambda: np.arange(-200, 210, 10),
            "colors": ['#FF0000', '#Ffa500', '#FFFFFF', '#0000ff', '#800080'],
            "cmap": lambda colors, levels: plt.get_cmap(
                LinearSegmentedColormap.from_list("CustomCmap", colors),
                len(levels) + 1
            ),
            "cbar_ticks": [-200, -175, -150, -125, -100, -75, -50, -25, 0, 25, 50, 75, 100, 125, 150, 175, 200],
        },
        "dif_prev": {
            "levels": lambda: np.arange(-50, 55, 5),
            "colors": ['#FF0000', '#Ffa500', '#FFFFFF', '#0000ff', '#800080'],
            "cmap": lambda colors, levels: plt.get_cmap(
                LinearSegmentedColormap.from_list("CustomCmap", colors),
                len(levels) + 1
            ),
            "cbar_ticks": None,
        },
        "pct_climatologia": {
            "levels": range(0, 305, 5),
            "colors": ['firebrick', 'red', 'orange', 'yellow', 'white', 'aquamarine',
                       'mediumturquoise', 'cyan', 'lightblue', 'blue', 'purple',
                       'mediumpurple', 'blueviolet'],
            "cmap": lambda colors, levels: plt.get_cmap(
                LinearSegmentedColormap.from_list("CustomCmap", colors),
                len(levels) + 1
            ),
            "cbar_ticks": lambda levels: list(levels)[::4],
        },
        "psi": {
            "levels": lambda: np.arange(-30, 30.2, 0.2),
            "colors": ['maroon', 'darkred', 'red', 'orange', 'yellow', 'white', 'cyan',
                       'dodgerblue', 'blue', 'darkblue', 'indigo'],
            "cmap": lambda colors, levels: plt.get_cmap(
                LinearSegmentedColormap.from_list("CustomCmap", colors),
                len(levels) + 1
            ),
            "cbar_ticks": lambda: np.arange(-30, 35, 5),
        },
        "chi": {
            "levels": lambda: np.arange(-10, 10.5, 0.5),
            "colors": ['green', 'white', 'brown'],
            "cmap": lambda colors, levels: plt.get_cmap(
                LinearSegmentedColormap.from_list("CustomCmap", colors),
                len(levels) + 1
            ),
            "cbar_ticks": lambda: np.arange(-10, 11, 1),
        },
        "geop_500_anomalia": {
            "levels": range(-40, 42, 2),
            "colors": ['darkblue', 'blue', 'white', 'red', 'darkred'],
            "cmap": lambda colors, levels: plt.get_cmap(
                LinearSegmentedColormap.from_list("CustomCmap", colors),
                len(levels)
            ),
            "cbar_ticks": None,
        },
        "pnmm_vento": {
            "levels": [900, 950, 976, 986, 995, 1002, 1007, 1011, 1013, 1015, 1019, 1024, 1030, 1038, 1046, 1080],
            "colors": ["#2b2e52", "#2a4d91", "#3e66c5", "#5498c6", "#54b3bc", "#56bfb7",
                       "#87c2b6", "#c1ccc6", "#d7c6c8", "#dcc1a5", "#dfcd9b", "#dfba7a",
                       "#d68856", "#c0575b", "#8f2c53"],
            "cmap": lambda colors: ListedColormap(colors),
            "cbar_ticks": None,
        },
        "frentes": {
            "levels": list(range(0, 6)),
            "colors": ["#ffffff", "#fee391", "#fec44f", "#fe9929", "#ec7014", "#cc4c02"],
            "cmap": None,
            "cbar_ticks": None,
        },
        "frentes_anomalia": {
            "levels": [-3, -2, -1, 0, 1, 2, 3],
            "colors": ["#b2182b", "#ef8a62", "#ffffff", "#ffffff", "#d1e5f0", "#67a9cf", "#2166ac"],
            "cmap": None,
            "cbar_ticks": None,
        },
        "acumulado_total": {
            "levels": range(0, 420, 20),
            "colors": [
                '#FFFFFF', '#B1EDCF', '#97D8B7', '#7DC19E', '#62AA85', '#48936D',
                '#2E7E54', '#14673C', '#14678C', '#337E9F', '#5094B5', '#6DACC8',
                '#8BC4DE', '#A9DBF2', '#EBD5EB', '#D9BED8', '#C5A7C5', '#B38FB2',
                '#A0779F', '#8E5F8D', '#682F67', '#6C0033', '#631C2A', '#A54945',
                '#C16E4E', '#DE9357', '#FAC66C', '#FBD479', '#FDE385', '#FEF192',
                '#FFFF9F',
            ],
            "cmap": None,
            "cbar_ticks": None,
        },
        "wind200": {
            "levels": lambda: np.arange(40, 85, 2),
            "colors": ['#FFFFFF', '#FFFFC1', '#EBFF51', '#ACFE53', '#5AFD5B', '#54FCD2',
                       '#54DBF5', '#54ACFC', '#4364FC', '#2F29ED', '#3304BC', '#440499'],
            "cmap": lambda colors, levels: plt.get_cmap(
                LinearSegmentedColormap.from_list("CustomCmap", colors),
                len(levels) + 1
            ),
            "cbar_ticks": None,
        },
        "geop_500": {
            "levels": range(450, 605, 5),
            "colors": ['#303030', '#585858', '#7A7A7A', '#C9E2F6', '#C6DAF3', '#A0B4CC',
                       '#6A7384', '#E0DCFF', '#C6BBFF', '#836FEC', '#7467D1', '#4230C0',
                       '#3020A5', '#2877ED', '#2D88F1', '#3897F3', '#6CA0D0', '#5EA4EC',
                       '#A1DFDE', '#C1EDBC', '#9EFA95', '#7DE17F', '#24A727', '#069F09',
                       '#FAF6AF', '#F5DD6F', '#E8C96E', '#FBA103', '#E9610D', '#EB3D18',
                       '#DF1507', '#BC0005', '#A50102', '#614338', '#75524C', '#806762',
                       '#886760', '#917571', '#AE867E', '#C3A09A', '#E0C5BE', '#DFABAD',
                       '#E26863', '#C83A36', '#8F1E1A', '#6A0606'],
            "cmap": lambda colors, levels: plt.get_cmap(
                LinearSegmentedColormap.from_list("CustomCmap", colors),
                len(levels) + 1
            ),
            "cbar_ticks": None,
        },
        "vorticidade": {
            "levels": range(-100, 110, 10),
            "colors": None,
            "cmap": lambda colors, levels: plt.get_cmap('RdBu_r', len(levels) + 1),
            "cbar_ticks": None,
        },
        "temp850": {
            "levels": lambda: np.arange(-14, 34, 1),
            "colors": ['#8E27BA', '#432A98', '#1953A8', '#148BC1', '#15B3A4', '#16C597',
                       '#77DE75', '#C5DD47', '#F5BB1A', '#F0933A', '#EF753D', '#F23B39',
                       '#C41111', '#8D0A0A'],
            "cmap": lambda colors, levels: plt.get_cmap(
                LinearSegmentedColormap.from_list("CustomCmap", colors),
                len(levels) + 1
            ),
            "cbar_ticks": None,
        },
        "temperature": {  # Alias for temp850
            "levels": lambda: np.arange(-14, 34, 1),
            "colors": ['#8E27BA', '#432A98', '#1953A8', '#148BC1', '#15B3A4', '#16C597',
                       '#77DE75', '#C5DD47', '#F5BB1A', '#F0933A', '#EF753D', '#F23B39',
                       '#C41111', '#8D0A0A'],
            "cmap": lambda colors, levels: plt.get_cmap(
                LinearSegmentedColormap.from_list("CustomCmap", colors),
                len(levels) + 1
            ),
            "cbar_ticks": None,
        },
        "precipitation": {  # Alias for tp_acumulada
            "levels": [0, 1, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 24, 28, 32, 36, 40, 50, 60, 80,
                       100, 120, 140, 160, 180, 200, 220, 240, 260, 280, 300],
            "colors": ["#ffffff", "#e6e6e6", "#bebebe", "#969696", "#6e6e6e", "#c8ffbe",
                       "#96f58c", "#50f050", "#1eb41e", "#057805", "#0a50aa", "#1464d2",
                       "#2882f0", "#50a5f5", "#96d2fa", "#e1ffff", "#fffaaa", "#ffe878",
                       "#ffc03c", "#ffa000", "#ff6000", "#ff3200", "#e11400", "#a50000",
                       "#c83c3c", "#e67070", "#f8a0a0", "#ffe6e6", "#cdcdff", "#b4a0ff",
                       "#8c78ff", "#6455dc", "#3c28b4"],
            "cmap": None,
            "cbar_ticks": None,
        },
        "slp": {  # Sea level pressure
            "levels": [900, 950, 976, 986, 995, 1002, 1007, 1011, 1013, 1015, 1019, 1024, 1030, 1038, 1046, 1080],
            "colors": ["#2b2e52", "#2a4d91", "#3e66c5", "#5498c6", "#54b3bc", "#56bfb7",
                       "#87c2b6", "#c1ccc6", "#d7c6c8", "#dcc1a5", "#dfcd9b", "#dfba7a",
                       "#d68856", "#c0575b", "#8f2c53"],
            "cmap": lambda colors: ListedColormap(colors),
            "cbar_ticks": None,
        },
        "temp_anomalia": {
            "levels": lambda: np.arange(-5, 5.1, 0.1),
            "colors": None,
            "cmap": 'RdBu_r',
            "cbar_ticks": lambda: np.arange(-5, 5.5, 0.5),
        },
        "divergencia850": {
            "levels": lambda: np.arange(-5, 6, 1),
            "colors": None,
            "cmap": lambda colors, levels: plt.get_cmap('RdBu_r', len(levels) + 1),
            "cbar_ticks": None,
        },
        "ivt": {
            "levels": lambda: np.arange(250, 1650, 50),
            "colors": ['white', 'yellow', 'orange', 'red', 'gray'],
            "cmap": lambda colors, levels: plt.get_cmap(
                LinearSegmentedColormap.from_list("CustomCmap", colors),
                len(levels) + 1
            ),
            "cbar_ticks": None,
        },
        "wind_prec_geop": {
            "levels": [2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 35],
            "colors": ["#ffffff", '#00004C', '#003862', '#001D7E', '#004C98', '#0066AD',
                       '#009BDB', '#77BAE8', '#9ED7FF', '#F6E5BD', '#F1E3A0', '#F3D98B',
                       '#F5C96C', '#EFB73F', '#EA7B32', '#D75C12', '#BF0411'],
            "cmap": None,
            "cbar_ticks": None,
        },
        "diferenca": {
            "levels": range(-100, 110, 10),
            "colors": ['mediumvioletred', 'maroon', 'firebrick', 'red', 'chocolate', 'orange',
                       'gold', 'yellow', 'white', 'white', 'aquamarine', 'mediumturquoise',
                       'cyan', 'lightblue', 'blue', 'purple', 'mediumpurple', 'blueviolet'],
            "cmap": lambda colors, levels: plt.get_cmap(
                LinearSegmentedColormap.from_list("CustomCmap", colors),
                len(levels) + 1
            ),
            "cbar_ticks": None,
        },
        "probabilidade": {
            "levels": range(0, 110, 10),
            "colors": ['white', 'yellow', 'lightgreen', 'green', 'blue', 'purple'],
            "cmap": lambda colors, levels: plt.get_cmap(
                LinearSegmentedColormap.from_list("CustomCmap", colors),
                len(levels) + 1
            ),
            "cbar_ticks": None,
        },
        "desvpad": {
            "levels": range(0, 110, 10),
            "colors": ['white', 'yellow', 'lightgreen', 'green', 'blue', 'purple'],
            "cmap": lambda colors, levels: plt.get_cmap(
                LinearSegmentedColormap.from_list("CustomCmap", colors),
                len(levels) + 1
            ),
            "cbar_ticks": None,
        },
        "geada-inmet": {
            "levels": [-100, -8, -3, -1, 100],
            "colors": ['#FFFFFF', '#D2CBEB', '#6D55BF', '#343396'],
            "cmap": None,
            "cbar_ticks": None,
        },
        "geada-cana": {
            "levels": [-100, -5, -3.5, -2, 100],
            "colors": ['#FFFFFF', '#D2CBEB', '#6D55BF', '#343396'],
            "cmap": None,
            "cbar_ticks": None,
        },
        "olr": {
            "levels": range(200, 410, 10),
            "colors": None,
            "cmap": 'plasma',
            "cbar_ticks": None,
        },
        "mag_vento100": {
            "levels": lambda: np.arange(1, 20, 1),
            "colors": ['#FFFFFF', '#FFFFC1', '#EBFF51', '#ACFE53', '#5AFD5B', '#54FCD2',
                       '#54DBF5', '#54ACFC', '#4364FC', '#2F29ED', '#3304BC', '#440499'],
            "cmap": lambda colors, levels: plt.get_cmap(
                LinearSegmentedColormap.from_list("CustomCmap", colors),
                len(levels) + 1
            ),
            "cbar_ticks": None,
        },
        "mag_vento100_anomalia": {
            "levels": lambda: np.arange(-3, 3.5, 0.5),
            "colors": None,
            "cmap": 'RdBu',
            "cbar_ticks": lambda: np.arange(-3, 3.5, 0.5),
        },
        "sst_anomalia": {
            "levels": lambda: np.arange(-3, 3.05, 0.05),
            "colors": ['indigo', 'darkblue', 'blue', 'dodgerblue', 'cyan', 'white', 'white',
                       'yellow', 'orange', 'red', 'darkred', 'maroon'],
            "cmap": lambda colors, levels: plt.get_cmap(
                LinearSegmentedColormap.from_list("CustomCmap", colors),
                len(levels) + 1
            ),
            "cbar_ticks": lambda: np.arange(-3, 3.5, 0.5),
        },

    }

    if help:
        print("Variáveis configuradas:")
        
        # Create a figure with subplots for each variable showing only colorbars
        import math
        num_vars = len(configs)
        cols = 3
        rows = math.ceil(num_vars / cols)
        
        fig, axes = plt.subplots(rows, cols, figsize=(18, 3 * rows))
        if rows == 1:
            axes = axes.reshape(1, -1)
        
        for i, var in enumerate(configs.keys()):
            row = i // cols
            col = i % cols
            ax = axes[row, col]
            
            print(f"- {var}")
            
            try:
                # Get configuration for this variable
                cfg = configs[var]
                
                # Resolve levels if it's a function
                levels = cfg["levels"]() if callable(cfg["levels"]) else cfg["levels"]
                colors = cfg["colors"]
                
                # Resolve cbar_ticks if it's a function
                cbar_ticks = cfg["cbar_ticks"]
                if callable(cbar_ticks):
                    if cbar_ticks.__code__.co_argcount == 0:
                        cbar_ticks = cbar_ticks()
                    else:
                        cbar_ticks = cbar_ticks(list(levels))
                
                # Generate cmap
                cmap_config = cfg["cmap"]
                if callable(cmap_config):
                    arg_count = cmap_config.__code__.co_argcount
                    if arg_count == 1:
                        cmap = cmap_config(colors)
                    elif arg_count == 2:
                        cmap = cmap_config(colors, list(levels))
                    else:
                        cmap = cmap_config()
                elif isinstance(cmap_config, str):
                    cmap = cmap_config
                else:
                    cmap = cmap_config
                
                # Create colorbar only (no image)
                if colors and cmap is None:
                    # Create a custom colormap from discrete colors
                    if hasattr(levels, '__len__'):
                        levels_list = list(levels)
                    else:
                        levels_list = list(levels)
                    
                    cmap_preview = ListedColormap(colors[:len(levels_list)-1] if len(colors) >= len(levels_list) else colors)
                    norm = BoundaryNorm(levels_list, cmap_preview.N)
                elif cmap:
                    if hasattr(levels, '__len__'):
                        levels_list = list(levels)
                    else:
                        levels_list = list(levels)
                    cmap_preview = cmap
                    norm = plt.Normalize(vmin=min(levels_list), vmax=max(levels_list))
                else:
                    # Fallback to viridis if no colormap available
                    if hasattr(levels, '__len__'):
                        levels_list = list(levels)
                    else:
                        levels_list = list(levels)
                    cmap_preview = 'viridis'
                    norm = plt.Normalize(vmin=min(levels_list), vmax=max(levels_list))
                
                # Create a colorbar without an image in horizontal orientation
                sm = plt.cm.ScalarMappable(cmap=cmap_preview, norm=norm)
                sm.set_array([])
                
                # Remove axes and just show colorbar horizontally
                ax.set_visible(False)
                cbar = plt.colorbar(sm, ax=ax, orientation='horizontal', fraction=1.0, aspect=30, pad=0.1)
                cbar.set_label(var, fontsize=10, fontweight='bold')
                
                # Set ticks if available
                if cbar_ticks is not None:
                    if hasattr(cbar_ticks, '__len__') and len(cbar_ticks) <= 10:
                        cbar.set_ticks(list(cbar_ticks))
                
            except Exception as e:
                # If there's an error, just show the variable name
                ax.text(0.5, 0.5, var, ha='center', va='center', transform=ax.transAxes, 
                       fontsize=10, fontweight='bold')
                ax.text(0.5, 0.3, f"Error: {str(e)[:30]}...", ha='center', va='center', 
                       transform=ax.transAxes, fontsize=8, color='red')
                ax.set_xticks([])
                ax.set_yticks([])
        
        # Hide empty subplots
        for i in range(num_vars, rows * cols):
            row = i // cols
            col = i % cols
            axes[row, col].set_visible(False)
        
        plt.tight_layout()
        plt.show()
        return

    if variavel_plotagem is not None:

        if variavel_plotagem not in configs:
            raise ValueError(f"Variável {variavel_plotagem} não configurada!")

        cfg = configs[variavel_plotagem]

        # Resolve levels if it's a function
        levels = cfg["levels"]() if callable(cfg["levels"]) else cfg["levels"]
        
        colors = cfg["colors"]
        
        # Resolve cbar_ticks if it's a function
        cbar_ticks = cfg["cbar_ticks"]
        if callable(cbar_ticks):
            if cbar_ticks.__code__.co_argcount == 0:
                cbar_ticks = cbar_ticks()
            else:
                cbar_ticks = cbar_ticks(levels)

        # Generate cmap
        cmap_config = cfg["cmap"]
        if callable(cmap_config):
            # Check function signature to determine how to call it
            arg_count = cmap_config.__code__.co_argcount
            if arg_count == 1:
                cmap = cmap_config(colors)
            elif arg_count == 2:
                cmap = cmap_config(colors, levels)
            else:
                cmap = cmap_config()
        elif isinstance(cmap_config, str):
            cmap = cmap_config
        else:
            cmap = cmap_config

    if custom:
        levels = custom.get("levels")
        colors = custom.get("colors")
        cmap = custom.get("cmap")
        cbar_ticks = custom.get("cbar_ticks")

    return levels, colors, cmap, cbar_ticks