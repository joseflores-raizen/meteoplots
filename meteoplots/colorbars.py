def custom_colorbar(variavel_plotagem):

    import numpy as np
    import matplotlib.pyplot as plt
    from matplotlib.colors import ListedColormap, LinearSegmentedColormap

    if variavel_plotagem in ['chuva_ons', 'tp', 'chuva_pnmm']:
        levels = [0, 1 ,5, 10, 15, 20, 25, 30, 40, 50, 75, 100, 150, 200]
        colors = ['#ffffff', '#e1ffff', '#b3f0fb','#95d2f9','#2585f0','#0c68ce','#73fd8b','#39d52b','#3ba933','#ffe67b','#ffbd4a','#fd5c22','#b91d22','#f7596f','#a9a9a9']
        cmap = None
        cbar_ticks = None

    elif variavel_plotagem in ['chuva_ons_geodataframe']:
        levels = [0, 1 ,5, 10, 15, 20, 25, 30, 40, 50, 75, 100, 150, 200]
        colors = ['#ffffff', '#e1ffff', '#b3f0fb','#95d2f9','#2585f0','#0c68ce','#73fd8b','#39d52b','#3ba933','#ffe67b','#ffbd4a','#fd5c22','#b91d22','#f7596f','#a9a9a9']  
        custom_cmap = LinearSegmentedColormap.from_list("CustomCmap", colors)
        cmap = ListedColormap(colors)
        cbar_ticks = None

    elif variavel_plotagem in ['chuva_boletim_consumidores']:
        levels = range(-300, 305, 5)
        colors = ['purple', 'white', 'green']
        custom_cmap = LinearSegmentedColormap.from_list("CustomCmap", colors)
        cmap = plt.get_cmap(custom_cmap, len(levels)  + 1) 
        cbar_ticks = range(-300, 350, 50)

    elif variavel_plotagem == 'acumulado_total_geodataframe':
        levels = range(0, 420, 20)
        colors = [
            '#FFFFFF',
            '#B1EDCF',
            '#97D8B7',
            '#7DC19E',
            '#62AA85',
            '#48936D',
            '#2E7E54',
            '#14673C',
            '#14678C',
            '#337E9F',
            '#5094B5',
            '#6DACC8',
            '#8BC4DE',
            '#A9DBF2',
            '#EBD5EB',
            '#D9BED8',
            '#C5A7C5',
            '#B38FB2',
            '#A0779F',
            '#8E5F8D',
        ]
        custom_cmap = LinearSegmentedColormap.from_list("CustomCmap", colors)
        cmap = plt.get_cmap(custom_cmap, len(levels)  + 1) 
        cbar_ticks = None

    elif variavel_plotagem in ['tp_anomalia']:
        colors = ['mediumvioletred', 'maroon', 'firebrick', 'red', 'chocolate', 'orange', 'gold', 'yellow', 'white', 'aquamarine', 'mediumturquoise', 'cyan', 'lightblue', 'blue', 'purple', 'mediumpurple', 'blueviolet']
        levels = range(-150, 155, 5)
        custom_cmap = LinearSegmentedColormap.from_list("CustomCmap", colors)
        cmap = plt.get_cmap(custom_cmap, len(levels)  + 1) 
        cbar_ticks = [-150, -125, -100, -75, -50, -25, 0, 25, 50, 75, 100, 125, 150]

    elif variavel_plotagem in ['tp_anomalia_mensal']:
        colors = ['mediumvioletred', 'maroon', 'firebrick', 'red', 'chocolate', 'orange', 'gold', 'yellow', 'white', 'aquamarine', 'mediumturquoise', 'cyan', 'lightblue', 'blue', 'purple', 'mediumpurple', 'blueviolet']
        levels = range(-300, 305, 5)
        custom_cmap = LinearSegmentedColormap.from_list("CustomCmap", colors)
        cmap = plt.get_cmap(custom_cmap, len(levels)  + 1) 
        cbar_ticks = range(-300, 350, 50)

    elif variavel_plotagem in ['chuva_acumualada_merge']:
        colors = ["#ffffff", "#e6e6e6", "#bebebe", "#969696", 
                  "#6e6e6e", "#c8ffbe", "#96f58c", "#50f050", 
                  "#1eb41e", "#057805", "#0a50aa", "#1464d2", 
                  "#2882f0", "#50a5f5", "#96d2fa", "#e1ffff", 
                  "#fffaaa", "#ffe878", "#ffc03c", "#ffa000", 
                  "#ff6000", "#ff3200", "#e11400", "#a50000",
                  "#c83c3c", "#e67070", "#f8a0a0", "#ffe6e6", 
                  "#cdcdff", "#b4a0ff", "#8c78ff", "#6455dc",
                  "#3c28b4"]
        levels = [0, 1, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 24, 28, 32, 36, 40, 50, 60, 80, 100, 120, 140, 160, 180, 200, 220, 240, 260, 280, 300]
        cmap = None 
        cbar_ticks = None

    elif variavel_plotagem in ['chuva_acumualada_merge_anomalia']:
        colors = ['#FF0000', '#Ffa500', '#FFFFFF', '#0000ff', '#800080']
        levels = np.arange(-200, 210, 10)
        custom_cmap = LinearSegmentedColormap.from_list("CustomCmap", colors)
        cmap = plt.get_cmap(custom_cmap, len(levels)  + 1) 
        cbar_ticks = [-200, -175, -150, -125, -100, -75, -50, -25, 0, 25, 50, 75, 100, 125, 150, 175, 200]

    elif variavel_plotagem in ['dif_prev']:
        colors = ['#FF0000', '#Ffa500', '#FFFFFF', '#0000ff', '#800080']
        levels = np.arange(-50, 55, 5)
        custom_cmap = LinearSegmentedColormap.from_list("CustomCmap", colors)
        cmap = plt.get_cmap(custom_cmap, len(levels)  + 1) 
        cbar_ticks = None

    elif variavel_plotagem in ['pct_climatologia']:
        colors = ['firebrick', 'red', 'orange', 'yellow', 'white', 'aquamarine', 'mediumturquoise', 'cyan', 'lightblue', 'blue', 'purple', 'mediumpurple', 'blueviolet']
        levels = range(0, 305, 5)
        custom_cmap = LinearSegmentedColormap.from_list("CustomCmap", colors)
        cmap = plt.get_cmap(custom_cmap, len(levels)  + 1) 
        cbar_ticks = levels[::4]   

    elif variavel_plotagem in ['psi']:
        levels = np.arange(-30, 30.2, 0.2)
        colors = ['maroon', 'darkred', 'red', 'orange', 'yellow', 'white', 'cyan', 'dodgerblue', 'blue', 'darkblue', 'indigo']
        custom_cmap = LinearSegmentedColormap.from_list("CustomCmap", colors)
        cmap = plt.get_cmap(custom_cmap, len(levels)  + 1) 
        cbar_ticks = np.arange(-30, 35, 5)

    elif variavel_plotagem in ['chi']:
        levels = np.arange(-10, 10.5, 0.5)
        colors = ['green', 'white', 'brown']
        custom_cmap = LinearSegmentedColormap.from_list("CustomCmap", colors)
        cmap = plt.get_cmap(custom_cmap, len(levels)  + 1) 
        cbar_ticks = np.arange(-10, 11, 1)

    elif variavel_plotagem in ['geop_500_anomalia']:
        levels = range(-40, 42, 2)
        colors = ['darkblue', 'blue', 'white', 'red', 'darkred']
        cmap = LinearSegmentedColormap.from_list("CustomCmap", colors)
        cmap = plt.get_cmap(cmap, len(levels))    
        cbar_ticks = None     

    elif variavel_plotagem in ['pnmm_vento']:
        levels = [
        900, 950, 976, 986, 995, 1002, 1007, 1011,
        1013, 1015, 1019, 1024, 1030, 1038, 1046, 1080
        ]
        colors = [
        "#2b2e52", "#2a4d91", "#3e66c5", "#5498c6", "#54b3bc",
        "#56bfb7", "#87c2b6", "#c1ccc6", "#d7c6c8", "#dcc1a5",
        "#dfcd9b", "#dfba7a", "#d68856", "#c0575b", "#8f2c53"
        ]
        cmap = ListedColormap(colors)
        cbar_ticks = None     

    elif variavel_plotagem == 'frentes':
        levels = list(range(0, 6))
        colors = [
            "#ffffff",  # 0 - branco
            "#fee391",  # 1 - amarelo claro
            "#fec44f",  # 2 - laranja claro
            "#fe9929",  # 3 - laranja médio
            "#ec7014",  # 4 - laranja escuro
            "#cc4c02",  # 5 - vermelho-laranja
        ]
        cmap = None       
        cbar_ticks = None 

    elif variavel_plotagem == 'frentes_anomalia':
        levels = [-3, -2, -1, 0, 1, 2, 3]
        colors = [
            "#b2182b",  # -3 - vermelho escuro
            "#ef8a62",  # -2 - vermelho claro
            "#ffffff",  # -1 - bege rosado
            "#ffffff",  #  0 - branco
            "#d1e5f0",  # +1 - azul claro
            "#67a9cf",  # +2 - azul médio
            "#2166ac",  # +3 - azul escuro
        ]
        cmap = None   
        cbar_ticks = None

    elif variavel_plotagem == 'acumulado_total':
        levels = range(0, 420, 20)
        colors = [
            '#FFFFFF',
            '#B1EDCF',
            '#97D8B7',
            '#7DC19E',
            '#62AA85',
            '#48936D',
            '#2E7E54',
            '#14673C',
            '#14678C',
            '#337E9F',
            '#5094B5',
            '#6DACC8',
            '#8BC4DE',
            '#A9DBF2',
            '#EBD5EB',
            '#D9BED8',
            '#C5A7C5',
            '#B38FB2',
            '#A0779F',
            '#8E5F8D',
            '#682F67',
            '#6C0033',
            '#631C2A',
            '#A54945',
            '#C16E4E',
            '#DE9357',
            '#FAC66C',
            '#FBD479',
            '#FDE385',
            '#FEF192',
            '#FFFF9F',
        ]
        cmap = None
        cbar_ticks = None

    elif variavel_plotagem == 'wind200':
        colors = ['#FFFFFF','#FFFFC1','#EBFF51','#ACFE53','#5AFD5B','#54FCD2','#54DBF5','#54ACFC', '#4364FC','#2F29ED','#3304BC','#440499']
        levels = np.arange(40, 85, 2)
        custom_cmap = LinearSegmentedColormap.from_list("CustomCmap", colors)
        cmap = plt.get_cmap(custom_cmap, len(levels)  + 1)
        cbar_ticks = None

    elif variavel_plotagem == 'geop_500':
        levels = range(450, 605, 5)
        colors = ['#303030', '#585858', '#7A7A7A', '#C9E2F6', '#C6DAF3', '#A0B4CC', '#6A7384', '#E0DCFF',
                '#C6BBFF', '#836FEC', '#7467D1', '#4230C0', '#3020A5', '#2877ED', '#2D88F1', '#3897F3',
                '#6CA0D0', '#5EA4EC', '#A1DFDE', '#C1EDBC', '#9EFA95', '#7DE17F', '#24A727', '#069F09',
                '#FAF6AF', '#F5DD6F', '#E8C96E', '#FBA103', '#E9610D', '#EB3D18', '#DF1507', '#BC0005',
                '#A50102', '#614338', '#75524C', '#806762', '#886760', '#917571', '#AE867E', '#C3A09A',
                '#E0C5BE', '#DFABAD', '#E26863', '#C83A36', '#8F1E1A', '#6A0606']
        custom_cmap = LinearSegmentedColormap.from_list("CustomCmap", colors)
        cmap = plt.get_cmap(custom_cmap, len(levels)  + 1) 
        cbar_ticks = None

    elif variavel_plotagem == 'vorticidade':
        levels = range(-100, 110, 10)
        colors = None
        cmap = plt.get_cmap('RdBu_r', len(levels)  + 1)
        cbar_ticks = None

    elif variavel_plotagem == 'temp850':
        levels = np.arange(-14, 34, 1)
        colors = ['#8E27BA','#432A98','#1953A8','#148BC1','#15B3A4', '#16C597','#77DE75','#C5DD47','#F5BB1A','#F0933A','#EF753D',
        '#F23B39', '#C41111', '#8D0A0A']
        custom_cmap = LinearSegmentedColormap.from_list("CustomCmap", colors)
        cmap = plt.get_cmap(custom_cmap, len(levels)  + 1)
        cbar_ticks = None

    elif variavel_plotagem == 'temp_anomalia':
        levels = np.arange(-5, 5.1, 0.1)
        colors = None
        cmap = 'RdBu_r'
        cbar_ticks = np.arange(-5, 5.5, 0.5)

    elif variavel_plotagem == 'divergencia850':
        levels = np.arange(-5, 6, 1)
        colors = None
        cmap = plt.get_cmap('RdBu_r', len(levels)  + 1)
        cbar_ticks = None

    elif variavel_plotagem == 'ivt':
        colors = ['white', 'yellow', 'orange', 'red', 'gray']
        levels = np.arange(250, 1650, 50)
        custom_cmap = LinearSegmentedColormap.from_list("CustomCmap", colors)
        cmap = plt.get_cmap(custom_cmap, len(levels)  + 1) 
        cbar_ticks = None

    elif variavel_plotagem == 'wind_prec_geop':
        levels = [2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 35]
        colors = ["#ffffff", '#00004C', '#003862',
                '#001D7E', '#004C98', '#0066AD', 
                '#009BDB', '#77BAE8', '#9ED7FF',
                '#F6E5BD', '#F1E3A0', '#F3D98B',
                '#F5C96C', '#EFB73F', '#EA7B32',
                '#D75C12', '#BF0411']
        cmap = None
        cbar_ticks = None

    elif variavel_plotagem == 'diferenca':
        levels = range(-100, 110, 10)
        colors = ['mediumvioletred', 'maroon', 'firebrick', 
                  'red', 'chocolate', 'orange', 'gold', 
                  'yellow', 'white', 'white', 'aquamarine', 
                  'mediumturquoise', 'cyan', 'lightblue', 'blue', 
                  'purple', 'mediumpurple', 'blueviolet']
        custom_cmap = LinearSegmentedColormap.from_list("CustomCmap", colors)
        cmap = plt.get_cmap(custom_cmap, len(levels)  + 1) 
        cbar_ticks = None

    elif variavel_plotagem in ['probabilidade', 'desvpad']:
        levels = range(0, 110, 10)
        colors = ['white', 'yellow', 'lightgreen', 'green', 'blue', 'purple']
        custom_cmap = LinearSegmentedColormap.from_list("CustomCmap", colors)
        cmap = plt.get_cmap(custom_cmap, len(levels)  + 1) 
        cbar_ticks = None

    elif variavel_plotagem == 'geada-inmet':
        levels = [-100, -8, -3, -1, 100]
        colors = ['#FFFFFF','#D2CBEB','#6D55BF','#343396']
        cmap = None
        cbar_ticks = None

    elif variavel_plotagem == 'geada-cana':
        levels = [-100, -5, -3.5, -2, 100]
        colors = ['#FFFFFF','#D2CBEB','#6D55BF','#343396']
        cmap = None
        cbar_ticks = None

    elif variavel_plotagem == 'olr':
        levels = range(200, 410, 10)
        colors = None
        cmap = 'plasma' 
        cbar_ticks = None       

    elif variavel_plotagem == 'mag_vento100':
        levels = np.arange(1, 20, 1)
        colors = ['#FFFFFF','#FFFFC1','#EBFF51','#ACFE53','#5AFD5B','#54FCD2','#54DBF5','#54ACFC', '#4364FC','#2F29ED','#3304BC','#440499']
        custom_cmap = LinearSegmentedColormap.from_list("CustomCmap", colors)
        cmap = plt.get_cmap(custom_cmap, len(levels)  + 1)
        cbar_ticks = None

    elif variavel_plotagem == 'mag_vento100_anomalia':
        levels = np.arange(-3, 3.5, 0.5)
        colors = None
        cmap = 'RdBu'
        cbar_ticks = np.arange(-3, 3.5, 0.5)

    elif variavel_plotagem in ['sst_anomalia']:
        levels = np.arange(-3, 3.05, 0.05)
        colors = ['indigo', 'darkblue', 'blue', 'dodgerblue', 'cyan', 'white', 'white', 'yellow', 'orange', 'red', 'darkred', 'maroon']
        custom_cmap = LinearSegmentedColormap.from_list("CustomCmap", colors)
        cmap = plt.get_cmap(custom_cmap, len(levels)  + 1) 
        cbar_ticks = np.arange(-3, 3.5, 0.5)

    return levels, colors, cmap, cbar_ticks