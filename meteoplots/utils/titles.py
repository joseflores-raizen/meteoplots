

def generate_title(titulo_principal=None, subtitulo=None, data=None, nivel=None, 
                 unidade=None, modelo=None, fonte=None, bold_subtitle=True, 
                 include_datetime=False):
    """
    Generate a comprehensive title for meteorological plots
    
    Parameters:
    -----------
    titulo_principal : str, optional
        Main title text (e.g., "Temperatura do Ar", "Precipitação")
    subtitulo : str, optional  
        Subtitle with additional information
    data : str or datetime, optional
        Date/time information to display
    nivel : str, optional
        Atmospheric level (e.g., "850 hPa", "Superfície", "2m")
    unidade : str, optional
        Units of measurement (e.g., "°C", "mm", "m/s")
    modelo : str, optional
        Model name (e.g., "GFS", "ERA5", "WRF")
    fonte : str, optional
        Data source information
    bold_subtitle : bool, default True
        Whether to make subtitle bold using LaTeX formatting
    include_datetime : bool, default True
        Whether to include current datetime in title
    **kwargs : dict
        Additional parameters for future extensions
        
    Returns:
    --------
    str : Formatted title string with LaTeX formatting
    
    Examples:
    ---------
    >>> gerar_titulo("Temperatura", "Análise", data="2024-01-15", nivel="2m", unidade="°C")
    >>> gerar_titulo("Precipitação", modelo="GFS", unidade="mm/h")
    """
    import datetime
    
    # Build title components
    title_parts = []
    
    # Main title
    if titulo_principal:
        title_parts.append(titulo_principal)
    
    # Add level information
    if nivel:
        if title_parts:
            title_parts[-1] += f" - {nivel}"
        else:
            title_parts.append(nivel)
    
    # Add units
    if unidade:
        if title_parts:
            title_parts[-1] += f" ({unidade})"
        else:
            title_parts.append(f"({unidade})")
    
    # Subtitle with model/source information
    subtitle_parts = []
    
    if subtitulo:
        subtitle_parts.append(subtitulo)
    
    if modelo:
        subtitle_parts.append(f"Modelo: {modelo}")
    
    if fonte:
        subtitle_parts.append(f"Fonte: {fonte}")
    
    # Date information
    if data:
        if isinstance(data, datetime.datetime):
            data_str = data.strftime("%d/%m/%Y %H:%M UTC")
        elif isinstance(data, str):
            data_str = data
        else:
            data_str = str(data)
        subtitle_parts.append(f"Data: {data_str}")
    
    # Current generation timestamp
    if include_datetime:
        now = datetime.datetime.now()
        timestamp = now.strftime("%d/%m/%Y %H:%M")
        subtitle_parts.append(f"Gerado em: {timestamp}")
    
    # Combine subtitle parts
    if subtitle_parts:
        subtitle_text = " | ".join(subtitle_parts)
        # Escape spaces for LaTeX if using bold formatting
        if bold_subtitle:
            subtitle_text = subtitle_text.replace(' ', '\\ ')
            subtitle_formatted = f'$\\mathbf{{{subtitle_text}}}$'
        else:
            subtitle_formatted = subtitle_text
        title_parts.append(subtitle_formatted)
    
    # Join all parts with newlines
    if title_parts:
        titulo_final = '\n'.join(title_parts)
    else:
        titulo_final = "Gráfico Meteorológico"
    
    return titulo_final
