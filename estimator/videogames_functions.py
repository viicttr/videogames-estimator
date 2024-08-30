from datetime import datetime
import pandas as pd 
import numpy as np 

def dic_dates(mi_dict): 
    
    fecha = datetime.strptime(mi_dict['released'], '%d-%m-%Y')
    
    dia = fecha.day
    mes = fecha.month
    año = fecha.year
    
    # Calcular el trimestre, cuatrimestre, semestre, lustro, década y estación
    trimestre = (mes - 1) // 4 + 1
    cuatrimestre = (mes - 1) // 4 + 1
    semestre = mes // 7 + 1
    lustro = año // 5 * 5 
    decada = año // 10 * 10 
    
    primavera_inicio = pd.Timestamp(f'{año}-03-21')
    primavera_fin = pd.Timestamp(f'{año}-06-20')
    verano_inicio = pd.Timestamp(f'{año}-06-21')
    verano_fin = pd.Timestamp(f'{año}-09-22')
    otoño_inicio = pd.Timestamp(f'{año}-09-23')
    otoño_fin = pd.Timestamp(f'{año}-12-20')
    
    if primavera_inicio <= fecha <= primavera_fin:
        estacion = '1' #Spring 
    elif verano_inicio <= fecha <= verano_fin:
        estacion = '2' #Summer 
    elif otoño_inicio <= fecha <= otoño_fin:
        estacion = '3' #Autumn 
    else:
        estacion = '4' #Winter 
    
    # Agregar los nuevos valores al diccionario
    mi_dict['released_año'] = año
    mi_dict['released_mes'] = mes
    mi_dict['released_dia'] = dia
    mi_dict['released_trimestre'] = trimestre
    mi_dict['released_cuatrimestre'] = cuatrimestre
    mi_dict['released_semestre'] = semestre
    mi_dict['released_lustro'] = lustro
    mi_dict['released_decada'] = decada
    mi_dict['released_estacion'] = estacion
    
    # Eliminar la clave original 'released'
    del mi_dict['released']
    
    # Mostrar el resultado final
    return mi_dict 

def prediction(new_data_dic_ini, sc, pca, tree_reg): 
    
    order_list = ['id', 'slug', 'rating', 'reviews_text_count', 'added', 'playtime', 'suggestions_count', 'reviews_count', 'exceptional', 'meh', 'recommended', 'skip', 'exceptional_percent', 'meh_percent', 'recommended_percent', 'skip_percent', 'beaten', 'dropped', 'owned', 'playing', 'toplay', 'yet', 'apple-appstore', 'epic-games', 'gog', 'google-play', 'itch', 'nintendo', 'playstation-store', 'steam', 'xbox-store', 'xbox360', '3do_parent', 'android_parent', 'atari_parent', 'commodore-amiga_parent', 'ios_parent', 'linux_parent', 'mac_parent', 'neo-geo_parent', 'nintendo_parent', 'pc_parent', 'playstation_parent', 'sega_parent', 'web_parent', 'xbox_parent', 'action', 'adventure', 'arcade', 'board-games', 'card', 'casual', 'educational', 'family', 'fighting', 'indie', 'massively-multiplayer', 'platformer', 'puzzle', 'racing', 'role-playing-games-rpg', 'shooter', 'simulation', 'sports', 'strategy', 'released_año', 'released_mes', 'released_dia', 'released_trimestre', 'released_cuatrimestre', 'released_semestre', 'released_lustro', 'released_decada', 'released_estacion', '3do_released_at_mes', '3do_released_at_estacion', 'android_released_at_mes', 'android_released_at_estacion', 'apple-ii_released_at_mes', 'apple-ii_released_at_estacion', 'atari-2600_released_at_mes', 'atari-2600_released_at_estacion', 'atari-5200_released_at_mes', 'atari-5200_released_at_estacion', 'atari-7800_released_at_mes', 'atari-7800_released_at_estacion', 'atari-8-bit_released_at_mes', 'atari-8-bit_released_at_estacion', 'atari-flashback_released_at_mes', 'atari-flashback_released_at_estacion', 'atari-lynx_released_at_mes', 'atari-lynx_released_at_estacion', 'atari-st_released_at_mes', 'atari-st_released_at_estacion', 'atari-xegs_released_at_mes', 'atari-xegs_released_at_estacion', 'commodore-amiga_released_at_mes', 'commodore-amiga_released_at_estacion', 'dreamcast_released_at_mes', 'dreamcast_released_at_estacion', 'game-boy_released_at_mes', 'game-boy_released_at_estacion', 'game-boy-advance_released_at_mes', 'game-boy-advance_released_at_estacion', 'game-boy-color_released_at_mes', 'game-boy-color_released_at_estacion', 'game-gear_released_at_mes', 'game-gear_released_at_estacion', 'gamecube_released_at_mes', 'gamecube_released_at_estacion', 'genesis_released_at_mes', 'genesis_released_at_estacion', 'ios_released_at_mes', 'ios_released_at_estacion', 'jaguar_released_at_mes', 'jaguar_released_at_estacion', 'linux_released_at_mes', 'linux_released_at_estacion', 'macintosh_released_at_mes', 'macintosh_released_at_estacion', 'macos_released_at_mes', 'macos_released_at_estacion', 'neogeo_released_at_mes', 'neogeo_released_at_estacion', 'nes_released_at_mes', 'nes_released_at_estacion', 'nintendo-3ds_released_at_mes', 'nintendo-3ds_released_at_estacion', 'nintendo-64_released_at_mes', 'nintendo-64_released_at_estacion', 'nintendo-ds_released_at_mes', 'nintendo-ds_released_at_estacion', 'nintendo-dsi_released_at_mes', 'nintendo-dsi_released_at_estacion', 'nintendo-switch_released_at_mes', 'nintendo-switch_released_at_estacion', 'pc_released_at_mes', 'pc_released_at_estacion', 'playstation1_released_at_mes', 'playstation1_released_at_estacion', 'playstation2_released_at_mes', 'playstation2_released_at_estacion', 'playstation3_released_at_mes', 'playstation3_released_at_estacion', 'playstation4_released_at_mes', 'playstation4_released_at_estacion', 'playstation5_released_at_mes', 'playstation5_released_at_estacion', 'ps-vita_released_at_mes', 'ps-vita_released_at_estacion', 'psp_released_at_mes', 'psp_released_at_estacion', 'sega-32x_released_at_mes', 'sega-32x_released_at_estacion', 'sega-cd_released_at_mes', 'sega-cd_released_at_estacion', 'sega-master-system_released_at_mes', 'sega-master-system_released_at_estacion', 'sega-saturn_released_at_mes', 'sega-saturn_released_at_estacion', 'snes_released_at_mes', 'snes_released_at_estacion', 'web_released_at_mes', 'web_released_at_estacion', 'wii_released_at_mes', 'wii_released_at_estacion', 'wii-u_released_at_mes', 'wii-u_released_at_estacion', 'xbox-old_released_at_mes', 'xbox-old_released_at_estacion', 'xbox-one_released_at_mes', 'xbox-one_released_at_estacion', 'xbox-series-x_released_at_mes', 'xbox-series-x_released_at_estacion', 'xbox360_released_at_mes', 'xbox360_released_at_estacion', 'exito']
    order_list_2 = ['rating', 'reviews_text_count', 'added', 'playtime', 'suggestions_count', 'reviews_count', 'exceptional', 'meh', 'recommended', 'skip', 'exceptional_percent', 'meh_percent', 'recommended_percent', 'skip_percent', 'beaten', 'dropped', 'owned', 'playing', 'toplay', 'yet', 'apple-appstore', 'epic-games', 'gog', 'google-play', 'itch', 'nintendo', 'playstation-store', 'steam', 'xbox-store', 'xbox360', '3do_parent', 'android_parent', 'atari_parent', 'commodore-amiga_parent', 'ios_parent', 'linux_parent', 'mac_parent', 'neo-geo_parent', 'nintendo_parent', 'pc_parent', 'playstation_parent', 'sega_parent', 'web_parent', 'xbox_parent', 'action', 'adventure', 'arcade', 'board-games', 'card', 'casual', 'educational', 'family', 'fighting', 'indie', 'massively-multiplayer', 'platformer', 'puzzle', 'racing', 'role-playing-games-rpg', 'shooter', 'simulation', 'sports', 'strategy', 'released_año', 'released_mes', 'released_dia', 'released_trimestre', 'released_cuatrimestre', 'released_semestre', 'released_lustro', 'released_decada', 'released_estacion', '3do_released_at_mes', '3do_released_at_estacion', 'android_released_at_mes', 'android_released_at_estacion', 'apple-ii_released_at_mes', 'apple-ii_released_at_estacion', 'atari-2600_released_at_mes', 'atari-2600_released_at_estacion', 'atari-5200_released_at_mes', 'atari-5200_released_at_estacion', 'atari-7800_released_at_mes', 'atari-7800_released_at_estacion', 'atari-8-bit_released_at_mes', 'atari-8-bit_released_at_estacion', 'atari-flashback_released_at_mes', 'atari-flashback_released_at_estacion', 'atari-lynx_released_at_mes', 'atari-lynx_released_at_estacion', 'atari-st_released_at_mes', 'atari-st_released_at_estacion', 'atari-xegs_released_at_mes', 'atari-xegs_released_at_estacion', 'commodore-amiga_released_at_mes', 'commodore-amiga_released_at_estacion', 'dreamcast_released_at_mes', 'dreamcast_released_at_estacion', 'game-boy_released_at_mes', 'game-boy_released_at_estacion', 'game-boy-advance_released_at_mes', 'game-boy-advance_released_at_estacion', 'game-boy-color_released_at_mes', 'game-boy-color_released_at_estacion', 'game-gear_released_at_mes', 'game-gear_released_at_estacion', 'gamecube_released_at_mes', 'gamecube_released_at_estacion', 'genesis_released_at_mes', 'genesis_released_at_estacion', 'ios_released_at_mes', 'ios_released_at_estacion', 'jaguar_released_at_mes', 'jaguar_released_at_estacion', 'linux_released_at_mes', 'linux_released_at_estacion', 'macintosh_released_at_mes', 'macintosh_released_at_estacion', 'macos_released_at_mes', 'macos_released_at_estacion', 'neogeo_released_at_mes', 'neogeo_released_at_estacion', 'nes_released_at_mes', 'nes_released_at_estacion', 'nintendo-3ds_released_at_mes', 'nintendo-3ds_released_at_estacion', 'nintendo-64_released_at_mes', 'nintendo-64_released_at_estacion', 'nintendo-ds_released_at_mes', 'nintendo-ds_released_at_estacion', 'nintendo-dsi_released_at_mes', 'nintendo-dsi_released_at_estacion', 'nintendo-switch_released_at_mes', 'nintendo-switch_released_at_estacion', 'pc_released_at_mes', 'pc_released_at_estacion', 'playstation1_released_at_mes', 'playstation1_released_at_estacion', 'playstation2_released_at_mes', 'playstation2_released_at_estacion', 'playstation3_released_at_mes', 'playstation3_released_at_estacion', 'playstation4_released_at_mes', 'playstation4_released_at_estacion', 'playstation5_released_at_mes', 'playstation5_released_at_estacion', 'ps-vita_released_at_mes', 'ps-vita_released_at_estacion', 'psp_released_at_mes', 'psp_released_at_estacion', 'sega-32x_released_at_mes', 'sega-32x_released_at_estacion', 'sega-cd_released_at_mes', 'sega-cd_released_at_estacion', 'sega-master-system_released_at_mes', 'sega-master-system_released_at_estacion', 'sega-saturn_released_at_mes', 'sega-saturn_released_at_estacion', 'snes_released_at_mes', 'snes_released_at_estacion', 'web_released_at_mes', 'web_released_at_estacion', 'wii_released_at_mes', 'wii_released_at_estacion', 'wii-u_released_at_mes', 'wii-u_released_at_estacion', 'xbox-old_released_at_mes', 'xbox-old_released_at_estacion', 'xbox-one_released_at_mes', 'xbox-one_released_at_estacion', 'xbox-series-x_released_at_mes', 'xbox-series-x_released_at_estacion', 'xbox360_released_at_mes', 'xbox360_released_at_estacion']
    variable_names = ['rating', 'reviews_text_count', 'added', 'playtime', 'suggestions_count', 'reviews_count', 'exceptional', 'meh', 'recommended', 'skip', 'exceptional_percent', 'meh_percent', 'recommended_percent', 'skip_percent', 'beaten', 'dropped', 'owned', 'playing', 'toplay', 'yet', 'apple-appstore', 'epic-games', 'gog', 'google-play', 'itch', 'nintendo', 'playstation-store', 'steam', 'xbox-store', 'xbox360', '3do_released_at_mes', '3do_released_at_estacion', 'android_released_at_mes', 'android_released_at_estacion', 'apple-ii_released_at_mes', 'apple-ii_released_at_estacion', 'atari-2600_released_at_mes', 'atari-2600_released_at_estacion', 'atari-5200_released_at_mes', 'atari-5200_released_at_estacion', 'atari-7800_released_at_mes', 'atari-7800_released_at_estacion', 'atari-8-bit_released_at_mes', 'atari-8-bit_released_at_estacion', 'atari-flashback_released_at_mes', 'atari-flashback_released_at_estacion', 'atari-lynx_released_at_mes', 'atari-lynx_released_at_estacion', 'atari-st_released_at_mes', 'atari-st_released_at_estacion', 'atari-xegs_released_at_mes', 'atari-xegs_released_at_estacion', 'commodore-amiga_released_at_mes', 'commodore-amiga_released_at_estacion', 'dreamcast_released_at_mes', 'dreamcast_released_at_estacion', 'game-boy_released_at_mes', 'game-boy_released_at_estacion', 'game-boy-advance_released_at_mes', 'game-boy-advance_released_at_estacion', 'game-boy-color_released_at_mes', 'game-boy-color_released_at_estacion', 'game-gear_released_at_mes', 'game-gear_released_at_estacion', 'gamecube_released_at_mes', 'gamecube_released_at_estacion', 'genesis_released_at_mes', 'genesis_released_at_estacion', 'ios_released_at_mes', 'ios_released_at_estacion', 'jaguar_released_at_mes', 'jaguar_released_at_estacion', 'linux_released_at_mes', 'linux_released_at_estacion', 'macintosh_released_at_mes', 'macintosh_released_at_estacion', 'macos_released_at_mes', 'macos_released_at_estacion', 'neogeo_released_at_mes', 'neogeo_released_at_estacion', 'nes_released_at_mes', 'nes_released_at_estacion', 'nintendo-3ds_released_at_mes', 'nintendo-3ds_released_at_estacion', 'nintendo-64_released_at_mes', 'nintendo-64_released_at_estacion', 'nintendo-ds_released_at_mes', 'nintendo-ds_released_at_estacion', 'nintendo-dsi_released_at_mes', 'nintendo-dsi_released_at_estacion', 'nintendo-switch_released_at_mes', 'nintendo-switch_released_at_estacion', 'pc_released_at_mes', 'pc_released_at_estacion', 'playstation1_released_at_mes', 'playstation1_released_at_estacion', 'playstation2_released_at_mes', 'playstation2_released_at_estacion', 'playstation3_released_at_mes', 'playstation3_released_at_estacion', 'playstation4_released_at_mes', 'playstation4_released_at_estacion', 'playstation5_released_at_mes', 'playstation5_released_at_estacion', 'ps-vita_released_at_mes', 'ps-vita_released_at_estacion', 'psp_released_at_mes', 'psp_released_at_estacion', 'sega-32x_released_at_mes', 'sega-32x_released_at_estacion', 'sega-cd_released_at_mes', 'sega-cd_released_at_estacion', 'sega-master-system_released_at_mes', 'sega-master-system_released_at_estacion', 'sega-saturn_released_at_mes', 'sega-saturn_released_at_estacion', 'snes_released_at_mes', 'snes_released_at_estacion', 'web_released_at_mes', 'web_released_at_estacion', 'wii_released_at_mes', 'wii_released_at_estacion', 'wii-u_released_at_mes', 'wii-u_released_at_estacion', 'xbox-old_released_at_mes', 'xbox-old_released_at_estacion', 'xbox-one_released_at_mes', 'xbox-one_released_at_estacion', 'xbox-series-x_released_at_mes', 'xbox-series-x_released_at_estacion', 'xbox360_released_at_mes', 'xbox360_released_at_estacion']
    
    new_data_dic = dic_dates(new_data_dic_ini) 
    
    # Añadir las nuevas variables al diccionario con valor 0 
    for var in variable_names:
        new_data_dic[var] = 0
    
    ordered_dict = {key: new_data_dic[key] for key in order_list if key in new_data_dic}
    
    # Convertir el diccionario a una lista
    new_data = list(ordered_dict.values())
    new_data_array = np.array(new_data).reshape(1, -1)
    
    # Se aplica la scala MixMax que se aplicó para el modelo 
    new_data_scaled = sc.transform(new_data_array)
    df = pd.DataFrame(new_data_scaled, columns=order_list_2)
    
    new_data_scaled_2 = df.drop(variable_names, axis=1)
    
    # Aplicar PCA al nuevo registro
    new_data_pca = pca.transform(new_data_scaled_2)
    
    # Hacer la predicción
    prediction = tree_reg.predict(new_data_pca) 
    
    return prediction 