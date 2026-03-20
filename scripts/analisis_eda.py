import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns

from datetime import datetime



# DEFINICION DE CAMPOS PARA REPORTE AUTOMATICO

def configurar_campos(df):
    print("\n=== CONFIGURACIÓN DEL DATASET ===")
    print("Vamos a identificar los campos clave para el reporte ejecutivo.")
    
    cols_todas = df.columns.tolist()
    cols_numericas = df.select_dtypes(include=['int64', 'float64']).columns.tolist()
    cols_categoricas = df.select_dtypes(include=['object']).columns.tolist()
    cols_fechas = [c for c in cols_todas if 'fecha' in c.lower() or 'date' in c.lower()]
    
    # ── NUEVO BLOQUE ──
    print("\n¿Hay columnas numéricas que son realmente categorías?")
    print("Columnas numéricas detectadas:")
    for i, col in enumerate(cols_numericas, 1):
        print(f"{i}. {col}")
    print("(Puedes seleccionar varias separadas por coma, Enter para omitir)")
    
    seleccion = input("→ ").strip()
    if seleccion != '':
        try:
            indices = [int(x.strip())-1 for x in seleccion.split(',')]
            cols_convertir = [cols_numericas[i] for i in indices if 0 <= i < len(cols_numericas)]
            for col in cols_convertir:
                df[col] = df[col].astype(str)
                cols_categoricas.append(col)
                cols_numericas.remove(col)
                print(f"✅ [{col}] convertida a categoría.")
        except:
            print("❌ Selección inválida, continuando sin cambios.")
    # ── FIN NUEVO BLOQUE ──

    config = {}
    
    # Detectar sugerencias automáticas
    sugerencias = {
        'valor':   [c for c in cols_numericas],
        'geo':     [c for c in cols_categoricas if any(x in c.lower() for x in ['region','ciudad','zona','pais','estado','departamento'])],
        'agente':  [c for c in cols_categoricas if any(x in c.lower() for x in ['vendedor','empleado','agente','responsable','ejecutivo'])],
        'categoria':[c for c in cols_categoricas if any(x in c.lower() for x in ['categoria','tipo','clase','grupo','producto'])],
        'pventa':  [c for c in cols_categoricas if any(x in c.lower() for x in ['tienda','sucursal','local','sede','punto'])],
        'fecha':   cols_fechas
    }
    
    preguntas = {
        'valor':    '¿Cuál es la columna de VALOR PRINCIPAL a medir?',
        'geo':      '¿Cuál es la columna GEOGRÁFICA?',
        'agente':   '¿Cuál es la columna de AGENTE?',
        'categoria':'¿Cuál es la columna de CATEGORÍA?',
        'pventa':   '¿Cuál es la columna de PUNTO DE VENTA?',
        'fecha':    '¿Cuál es la columna de FECHA?'
    }
    
    for clave, pregunta in preguntas.items():
        print(f"\n{pregunta}")
        sug = sugerencias[clave]
        
        if sug:
            print("Sugeridas:")
            for i, col in enumerate(sug, 1):
                print(f"{i}. {col}")
            print(f"{len(sug)+1}. Otra columna")
            print(f"{len(sug)+2}. Omitir")
            
            while True:
                try:
                    opc = int(input("→ "))
                    if 1 <= opc <= len(sug):
                        config[clave] = sug[opc-1]
                        break
                    elif opc == len(sug)+1:
                        # Mostrar todas las columnas disponibles
                        print("\nColumnas disponibles:")
                        for i, col in enumerate(cols_todas, 1):
                            print(f"{i}. {col}")
                        while True:
                            try:
                                opc2 = int(input("→ ")) - 1
                                if 0 <= opc2 < len(cols_todas):
                                    config[clave] = cols_todas[opc2]
                                    break
                                print("❌ Número fuera de rango.")
                            except ValueError:
                                print("❌ Debes ingresar un número.")
                        break
                    elif opc == len(sug)+2:
                        config[clave] = None
                        break
                    else:
                        print("❌ Número fuera de rango.")
                except ValueError:
                    print("❌ Debes ingresar un número.")
        else:
            # No hay sugeridas, mostrar todas las columnas
            print("No se detectaron columnas sugeridas.")
            print("Columnas disponibles:")
            for i, col in enumerate(cols_todas, 1):
                print(f"{i}. {col}")
            print(f"{len(cols_todas)+1}. Omitir")
            
            while True:
                try:
                    opc = int(input("→ "))
                    if 1 <= opc <= len(cols_todas):
                        config[clave] = cols_todas[opc-1]
                        break
                    elif opc == len(cols_todas)+1:
                        config[clave] = None
                        break
                    else:
                        print("❌ Número fuera de rango.")
                except ValueError:
                    print("❌ Debes ingresar un número.")
    
    print("\n✅ Configuración guardada:")
    for clave, valor in config.items():
        print(f"   {clave.upper():12} → {valor if valor else 'No definido'}")
    
    return config, cols_numericas, cols_categoricas

# FIN DE DEFINICION DE CAMPOS

# REPORTE EJECUTIVO AUTOMÁTICO

def generar_reporte_ejecutivo(df, config, nombre_archivo):
    print("\n📝 GENERANDO REPORTE EJECUTIVO...")
    
    reporte = []
    reporte.append("=" * 60)
    reporte.append("REPORTE EJECUTIVO AUTOMÁTICO")
    reporte.append(f"Archivo: {nombre_archivo}")
    reporte.append(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    reporte.append(f"Registros analizados: {len(df)}")
    reporte.append("=" * 60)
    
    col_valor    = config.get('valor')
    col_geo      = config.get('geo')
    col_agente   = config.get('agente')
    col_categoria= config.get('categoria')
    col_pventa   = config.get('pventa')
    col_fecha    = config.get('fecha')
    
    # RESUMEN GENERAL
    if col_valor:
        # Verificar que el campo valor sea numérico
        try:
            df[col_valor] = pd.to_numeric(df[col_valor], errors='coerce')
            reporte.append("\nRESUMEN GENERAL:")
            total = df[col_valor].sum()
            promedio = df[col_valor].mean()
            maximo = df[col_valor].max()
            minimo = df[col_valor].min()
            reporte.append(f"• Total {col_valor}: {total:,.2f}")
            reporte.append(f"• Promedio por registro: {promedio:,.2f}")
            reporte.append(f"• Valor máximo: {maximo:,.2f}")
            reporte.append(f"• Valor mínimo: {minimo:,.2f}")
        except:
            reporte.append(f"\n⚠️ [{col_valor}] no es numérico, resumen omitido.")
    
    # HALLAZGOS PRINCIPALES
    reporte.append("\nHALLAZGOS PRINCIPALES:")
    
    if col_geo and col_valor:
        resumen_geo = df.groupby(col_geo)[col_valor].sum().round(2).sort_values(ascending=False)
        mejor_geo = resumen_geo.index[0]
        peor_geo = resumen_geo.index[-1]
        reporte.append(f"• {col_geo} con mejor resultado: {mejor_geo} (${resumen_geo[mejor_geo]:,.2f})")
        reporte.append(f"• {col_geo} con menor resultado: {peor_geo} (${resumen_geo[peor_geo]:,.2f})")
    
    if col_agente and col_valor:
        resumen_agente = df.groupby(col_agente)[col_valor].sum().round(2).sort_values(ascending=False)
        mejor_agente = resumen_agente.index[0]
        peor_agente = resumen_agente.index[-1]
        reporte.append(f"• {col_agente} estrella: {mejor_agente} (${resumen_agente[mejor_agente]:,.2f})")
        reporte.append(f"• {col_agente} crítico: {peor_agente} (${resumen_agente[peor_agente]:,.2f})")
    
    if col_categoria and col_valor:
        resumen_cat = df.groupby(col_categoria)[col_valor].sum().round(2).sort_values(ascending=False)
        mejor_cat = resumen_cat.index[0]
        peor_cat = resumen_cat.index[-1]
        reporte.append(f"• {col_categoria} líder: {mejor_cat} (${resumen_cat[mejor_cat]:,.2f})")
        reporte.append(f"• {col_categoria} crítica: {peor_cat} (${resumen_cat[peor_cat]:,.2f})")
    
    if col_pventa and col_valor:
        resumen_pventa = df.groupby(col_pventa)[col_valor].sum().round(2).sort_values(ascending=False)
        mejor_pventa = resumen_pventa.index[0]
        peor_pventa = resumen_pventa.index[-1]
        reporte.append(f"• {col_pventa} top: {mejor_pventa} (${resumen_pventa[mejor_pventa]:,.2f})")
        reporte.append(f"• {col_pventa} más baja: {peor_pventa} (${resumen_pventa[peor_pventa]:,.2f})")
    
    # PUNTOS CRÍTICOS CON DRILL-DOWN
    reporte.append("\nPUNTOS CRÍTICOS:")
    
    if col_geo and col_valor:
        # Drill-down del peor geográfico
        df_peor_geo = df[df[col_geo] == peor_geo]
        reporte.append(f"\n• {col_geo} crítico: {peor_geo} (${resumen_geo[peor_geo]:,.2f})")
        reporte.append(f"  Representa {resumen_geo[peor_geo]/resumen_geo.sum()*100:.1f}% del total")
        
        if col_categoria:
            drill_cat = df_peor_geo.groupby(col_categoria)[col_valor].sum().round(2).sort_values()
            peor_cat_geo = drill_cat.index[0]
            reporte.append(f"  → {col_categoria} más débil en {peor_geo}: {peor_cat_geo} (${drill_cat[peor_cat_geo]:,.2f})")
        
        if col_agente:
            drill_agente = df_peor_geo.groupby(col_agente)[col_valor].sum().round(2).sort_values()
            peor_agente_geo = drill_agente.index[0]
            reporte.append(f"  → {col_agente} crítico en {peor_geo}: {peor_agente_geo} (${drill_agente[peor_agente_geo]:,.2f})")
        
        if col_pventa:
            drill_pventa = df_peor_geo.groupby(col_pventa)[col_valor].sum().round(2).sort_values()
            peor_pventa_geo = drill_pventa.index[0]
            reporte.append(f"  → {col_pventa} más baja en {peor_geo}: {peor_pventa_geo} (${drill_pventa[peor_pventa_geo]:,.2f})")
        
        reporte.append(f"  → Recomendación: Investigar estrategia de {peor_geo}")
        reporte.append(f"    con foco en {col_categoria if col_categoria else ''} y {col_agente if col_agente else ''}.")
    
    # TENDENCIA
    # RESUMEN ANUAL
    if col_fecha and col_valor:
        df[col_fecha] = pd.to_datetime(df[col_fecha], errors='coerce')
        año_actual = datetime.now().year
        resumen_anual = df.groupby(df[col_fecha].dt.year)[col_valor].sum().round(2)
        
        reporte.append(f"\nRESUMEN ANUAL DE {col_valor}:")
        for año, valor in resumen_anual.items():
            año = int(año)
            if año == año_actual:
                # Calcular cuántos meses hay en el año actual
                meses = df[df[col_fecha].dt.year == año_actual][col_fecha].dt.month.nunique()
                reporte.append(f"• {año}: ${valor:,.2f} ({meses} meses calculados)")
            else:
                reporte.append(f"• {año}: ${valor:,.2f}")
        
        # Comparar solo años completos
        años_completos = resumen_anual[resumen_anual.index != año_actual]
        if len(años_completos) > 1:
            variacion = ((años_completos.iloc[-1] - años_completos.iloc[0]) / años_completos.iloc[0] * 100).round(1)
            direccion = "crecimiento 📈" if variacion > 0 else "decrecimiento 📉"
            # Comparación entre cada año consecutivo
        for i in range(len(años_completos)-1):
            año_a = int(años_completos.index[i])
            año_b = int(años_completos.index[i+1])
            val_a = años_completos.iloc[i]
            val_b = años_completos.iloc[i+1]
            var = ((val_b - val_a) / val_a * 100).round(1)
            direccion = "crecimiento 📈" if var > 0 else "decrecimiento 📉"
            reporte.append(f"• {año_a} vs {año_b}: {direccion} ({var:+.1f}%)")
        
        # Proyección año actual
        if año_actual in resumen_anual.index.astype(int).tolist():
            meses_transcurridos = df[df[col_fecha].dt.year == año_actual][col_fecha].dt.month.nunique()
            valor_actual = resumen_anual[año_actual]
            proyeccion = (valor_actual / meses_transcurridos * 12).round(2)
            ultimo_año_completo = años_completos.iloc[-1]
            var_proyeccion = ((proyeccion - ultimo_año_completo) / ultimo_año_completo * 100).round(1)
            direccion_proy = "positivo 📈" if var_proyeccion > 0 else "negativo 📉"
            reporte.append(f"\n• Proyección {año_actual} (base {meses_transcurridos} meses): ${proyeccion:,.2f}")
            reporte.append(f"• Resultado proyectado vs {int(años_completos.index[-1])}: {direccion_proy} ({var_proyeccion:+.1f}%)")
    
    # Guardar reporte
    if not os.path.exists("salida"):
        os.makedirs("salida")
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    nombre_reporte = os.path.join("salida", f"REPORTE_EJECUTIVO_{timestamp}.txt")
    
    with open(nombre_reporte, "w", encoding="utf-8") as f:
        for linea in reporte:
            f.write(linea + "\n")
    
    # Mostrar en pantalla también
    print("\n")
    for linea in reporte:
        print(linea)
    
    print(f"\n✅ Reporte guardado en: {nombre_reporte}")

# FIN DE REPORTE EJECUTIVO AUTOMÁTICO

def seleccionar_archivo():
    carpeta = "entrada"
    archivos = [f for f in os.listdir(carpeta) if f.endswith(('.xlsx', '.xls', '.csv'))]
    
    if not archivos:
        print("⚠️ No hay archivos en la carpeta entrada.")
        return None
    
    print("\n📥 Archivos disponibles:")
    for i, f in enumerate(archivos, 1):
        print(f"{i}. {f}")
    
    try:
        opc = int(input("\nSelecciona el número del archivo: "))
        if 1 <= opc <= len(archivos):
            return os.path.join(carpeta, archivos[opc-1])
        else:
            print("❌ Número fuera de rango.")
            return None
    except ValueError:
        print("❌ Debes ingresar un número.")
        return None

def analisis_estadistico(df, cols_numericas):
    print("\n=== ANÁLISIS ESTADÍSTICO ===")
    
    # Detectar columnas numéricas automáticamente
    # cols_numericas = df.select_dtypes(include=['int64', 'float64']).columns.tolist()
    
    if not cols_numericas:
        print("⚠️ No se encontraron columnas numéricas.")
        return
    
    print("\nColumnas numéricas disponibles:")
    for i, col in enumerate(cols_numericas, 1):
        print(f"{i}. {col}")
    print(f"{len(cols_numericas)+1}. Todas")
    
    print("\nPuedes seleccionar una o varias separadas por coma.")
    print(f"Ejemplo: 1,3 o {len(cols_numericas)+1} para todas")
    
    seleccion = input("\nSelecciona: ").strip()
    
    # Procesar selección
    if seleccion == str(len(cols_numericas)+1):
        cols_seleccionadas = cols_numericas
    else:
        try:
            indices = [int(x.strip())-1 for x in seleccion.split(',')]
            cols_seleccionadas = [cols_numericas[i] for i in indices if 0 <= i < len(cols_numericas)]
        except:
            print("❌ Selección inválida.")
            return
    
    if not cols_seleccionadas:
        print("❌ No se seleccionaron columnas válidas.")
        return
    
    print(f"\n📊 Estadísticos para: {cols_seleccionadas}")
    print("="*60)
    print(df[cols_seleccionadas].describe().round(2).to_string())
    
    # Información adicional
    print("\n📋 INFORMACIÓN ADICIONAL:")
    for col in cols_seleccionadas:
        print(f"\n[{col}]")
        print(f"  Suma total:    {df[col].sum():,.2f}")
        print(f"  Mediana:       {df[col].median():,.2f}")
        print(f"  Moda:          {df[col].mode()[0]:,.2f}")
        print(f"  Rango:         {df[col].max() - df[col].min():,.2f}")
        print(f"  Valores nulos: {df[col].isna().sum()}")

# ANALISIS CRUZADO
def analisis_cruzado(df, cols_numericas, cols_categoricas):
    print("\n=== ANÁLISIS CRUZADO ===")
    
    # Detectar columnas categóricas y numéricas
    #cols_categoricas = df.select_dtypes(include=['object']).columns.tolist()
    #cols_numericas = df.select_dtypes(include=['int64', 'float64']).columns.tolist()

    if not cols_categoricas or not cols_numericas:
        print("⚠️ Se necesitan columnas categóricas y numéricas.")
        return
    
    # Seleccionar columna categórica
    print("\n¿Por qué categoría quieres agrupar?")
    for i, col in enumerate(cols_categoricas, 1):
        print(f"{i}. {col}")
    
    while True:
        try:
            opc_cat = int(input("\nSelecciona: ")) - 1
            if 0 <= opc_cat < len(cols_categoricas):
                col_categoria = cols_categoricas[opc_cat]
                break
            print("❌ Número fuera de rango.")
        except ValueError:
            print("❌ Debes ingresar un número.")
    
    # Seleccionar columna numérica
    print(f"\n¿Qué campo numérico quieres medir?")
    for i, col in enumerate(cols_numericas, 1):
        print(f"{i}. {col}")
    
    while True:
        try:
            opc_num = int(input("\nSelecciona: ")) - 1
            if 0 <= opc_num < len(cols_numericas):
                col_numerica = cols_numericas[opc_num]
                break
            print("❌ Número fuera de rango.")
        except ValueError:
            print("❌ Debes ingresar un número.")
    
    # Seleccionar métrica
    print(f"\n¿Qué métrica quieres aplicar a [{col_numerica}]?")
    print("1. Suma total")
    print("2. Promedio")
    print("3. Conteo")
    print("4. Máximo")
    print("5. Mínimo")
    print("6. Top N")
    
    while True:
        metrica = input("\nSelecciona: ")
        if metrica in ['1','2','3','4','5','6']:
            break
        print("❌ Elige solo 1, 2, 3, 4, 5 o 6.")
    
    # Aplicar métrica
    if metrica == '1':
        resultado = df.groupby(col_categoria)[col_numerica].sum().round(2).sort_values(ascending=False)
        nombre_metrica = "Suma Total"
    elif metrica == '2':
        resultado = df.groupby(col_categoria)[col_numerica].mean().round(2).sort_values(ascending=False)
        nombre_metrica = "Promedio"
    elif metrica == '3':
        resultado = df.groupby(col_categoria)[col_numerica].count().sort_values(ascending=False)
        nombre_metrica = "Conteo"
    elif metrica == '4':
        resultado = df.groupby(col_categoria)[col_numerica].max().round(2).sort_values(ascending=False)
        nombre_metrica = "Máximo"
    elif metrica == '5':
        resultado = df.groupby(col_categoria)[col_numerica].min().round(2).sort_values(ascending=False)
        nombre_metrica = "Mínimo"
    elif metrica == '6':
        while True:
            try:
                n = int(input("¿Cuántos registros quieres ver? (Top N): "))
                if n > 0:
                    break
                print("❌ Debe ser mayor a 0.")
            except ValueError:
                print("❌ Debes ingresar un número.")
        resultado = df.groupby(col_categoria)[col_numerica].sum().round(2).sort_values(ascending=False).head(n)
        nombre_metrica = f"Top {n}"

    print(f"\n📊 {nombre_metrica} de [{col_numerica}] por [{col_categoria}]:")
    print("="*50)
    print(resultado.to_string())
    
    # Preguntar si quiere otro análisis cruzado
    if input("\n¿Deseas hacer otro análisis cruzado? (s/n): ").lower() == 's':
        analisis_cruzado(df, cols_numericas, cols_categoricas)
# FIN DE ANALISIS CRUZADO

# ANALISIS DRILL-DOWN
def analisis_drill_down(df, cols_numericas, cols_categoricas):
    print("\n=== ANÁLISIS DRILL-DOWN ===")
    
    plt.ion()  # Modo interactivo ON - mantiene gráficas abiertas
    
    # cols_categoricas = df.select_dtypes(include=['object']).columns.tolist()
    # cols_numericas = df.select_dtypes(include=['int64', 'float64']).columns.tolist()
    
    
    # Seleccionar campo numérico a medir
    print("\n¿Qué campo numérico quieres medir?")
    for i, col in enumerate(cols_numericas, 1):
        print(f"{i}. {col}")
    
    while True:
        try:
            opc = int(input("\nSelecciona: ")) - 1
            if 0 <= opc < len(cols_numericas):
                col_numerica = cols_numericas[opc]
                break
            print("❌ Número fuera de rango.")
        except ValueError:
            print("❌ Debes ingresar un número.")

    def graficar_nivel(datos, titulo, col_cat, col_num, num_figura):
        fig, ax = plt.subplots(figsize=(12, 6), num=num_figura)
        sns.barplot(x=datos.values, y=datos.index,
                   hue=datos.index, palette='Blues_r', ax=ax, legend=False)
        ax.set_title(titulo, fontsize=14, fontweight='bold')
        ax.set_xlabel(f'{col_num}')
        ax.set_ylabel(col_cat)
        for i, v in enumerate(datos.values):
            ax.text(v, i, f' ${v:,.2f}', va='center')
        plt.tight_layout()
        plt.show()
        plt.pause(0.1)  # Pausa breve para renderizar

    # NIVEL 1
    print(f"\n¿Por qué categoría quieres agrupar primero?")
    for i, col in enumerate(cols_categoricas, 1):
        print(f"{i}. {col}")
    
    while True:
        try:
            opc = int(input("\nSelecciona: ")) - 1
            if 0 <= opc < len(cols_categoricas):
                col_nivel1 = cols_categoricas[opc]
                break
            print("❌ Número fuera de rango.")
        except ValueError:
            print("❌ Debes ingresar un número.")

    resultado_nivel1 = df.groupby(col_nivel1)[col_numerica].sum().round(2).sort_values(ascending=False)
    titulo1 = f"{col_numerica} por {col_nivel1}"
    graficar_nivel(resultado_nivel1, titulo1, col_nivel1, col_numerica, 1)
    
    print(f"\n📊 {titulo1}:")
    print(resultado_nivel1.to_string())

    # NIVEL 2
    if input("\n¿Quieres hacer drill-down? (s/n): ").lower() == 's':
        
        valores = resultado_nivel1.index.tolist()
        print(f"\n¿Sobre qué valor de [{col_nivel1}] quieres profundizar?")
        for i, val in enumerate(valores, 1):
            print(f"{i}. {val}")
        
        while True:
            try:
                opc = int(input("\nSelecciona: ")) - 1
                if 0 <= opc < len(valores):
                    valor_filtro = valores[opc]
                    break
                print("❌ Número fuera de rango.")
            except ValueError:
                print("❌ Debes ingresar un número.")

        df_filtrado = df[df[col_nivel1] == valor_filtro]
        cols_restantes = [c for c in cols_categoricas if c != col_nivel1]

        print(f"\n¿Por qué categoría quieres agrupar dentro de [{valor_filtro}]?")
        for i, col in enumerate(cols_restantes, 1):
            print(f"{i}. {col}")
        
        while True:
            try:
                opc = int(input("\nSelecciona: ")) - 1
                if 0 <= opc < len(cols_restantes):
                    col_nivel2 = cols_restantes[opc]
                    break
                print("❌ Número fuera de rango.")
            except ValueError:
                print("❌ Debes ingresar un número.")

        resultado_nivel2 = df_filtrado.groupby(col_nivel2)[col_numerica].sum().round(2).sort_values(ascending=False)
        titulo2 = f"{col_numerica} por {col_nivel2} — dentro de {valor_filtro}"
        graficar_nivel(resultado_nivel2, titulo2, col_nivel2, col_numerica, 2)
        
        print(f"\n📊 {titulo2}:")
        print(resultado_nivel2.to_string())

        # NIVEL 3
        if input("\n¿Quieres profundizar un nivel más? (s/n): ").lower() == 's':
            
            valores_nivel2 = resultado_nivel2.index.tolist()
            print(f"\n¿Sobre qué valor de [{col_nivel2}] quieres profundizar?")
            for i, val in enumerate(valores_nivel2, 1):
                print(f"{i}. {val}")
            
            while True:
                try:
                    opc = int(input("\nSelecciona: ")) - 1
                    if 0 <= opc < len(valores_nivel2):
                        valor_filtro2 = valores_nivel2[opc]
                        break
                    print("❌ Número fuera de rango.")
                except ValueError:
                    print("❌ Debes ingresar un número.")

            df_filtrado2 = df_filtrado[df_filtrado[col_nivel2] == valor_filtro2]
            cols_restantes2 = [c for c in cols_categoricas if c not in [col_nivel1, col_nivel2]]

            if cols_restantes2:
                print(f"\n¿Por qué categoría quieres agrupar dentro de [{valor_filtro2}]?")
                for i, col in enumerate(cols_restantes2, 1):
                    print(f"{i}. {col}")
                
                while True:
                    try:
                        opc = int(input("\nSelecciona: ")) - 1
                        if 0 <= opc < len(cols_restantes2):
                            col_nivel3 = cols_restantes2[opc]
                            break
                        print("❌ Número fuera de rango.")
                    except ValueError:
                        print("❌ Debes ingresar un número.")

                resultado_nivel3 = df_filtrado2.groupby(col_nivel3)[col_numerica].sum().round(2).sort_values(ascending=False)
                titulo3 = f"{col_numerica} por {col_nivel3} — {col_nivel2} {valor_filtro2} en {valor_filtro}"
                graficar_nivel(resultado_nivel3, titulo3, col_nivel3, col_numerica, 3)
                
                print(f"\n📊 {titulo3}:")
                print(resultado_nivel3.to_string())
            else:
                print("⚠️ No hay más niveles disponibles.")

    if input("\n¿Deseas hacer otro drill-down? (s/n): ").lower() == 's':
        analisis_drill_down(df, cols_numericas, cols_categoricas)
    else:
        plt.ioff()  # Modo interactivo OFF al terminar
# FIN DE ANALISIS DRILL-DOWN

# VISUALIZACIONES
def visualizaciones(df, cols_numericas, cols_categoricas):
    import matplotlib.pyplot as plt
    import seaborn as sns
    
    print("\n=== VISUALIZACIONES ===")
    
    # cols_categoricas = df.select_dtypes(include=['object']).columns.tolist()
    # cols_numericas = df.select_dtypes(include=['int64', 'float64']).columns.tolist()
    
    
    print("\n¿Qué tipo de gráfica quieres generar?")
    print("1. Barras — categoría vs numérico")
    print("2. Línea — tendencia por fecha")
    print("3. Dispersión — relación entre dos numéricos")
    print("4. Mapa de calor — correlación entre numéricos")
    print("5. Distribución — histograma de un numérico")
    
    while True:
        tipo = input("\nSelecciona: ")
        if tipo in ['1','2','3','4','5']: break
        print("❌ Elige solo 1, 2, 3, 4 o 5.")

    if tipo == '1':
        # Barras
        print("\n¿Qué categoría quieres en el eje Y?")
        for i, col in enumerate(cols_categoricas, 1):
            print(f"{i}. {col}")
        while True:
            try:
                opc = int(input("\nSelecciona: ")) - 1
                if 0 <= opc < len(cols_categoricas):
                    col_cat = cols_categoricas[opc]
                    break
                print("❌ Número fuera de rango.")
            except ValueError:
                print("❌ Debes ingresar un número.")

        print(f"\n¿Qué campo numérico quieres medir?")
        for i, col in enumerate(cols_numericas, 1):
            print(f"{i}. {col}")
        while True:
            try:
                opc = int(input("\nSelecciona: ")) - 1
                if 0 <= opc < len(cols_numericas):
                    col_num = cols_numericas[opc]
                    break
                print("❌ Número fuera de rango.")
            except ValueError:
                print("❌ Debes ingresar un número.")

        print("\n¿Qué métrica aplicar?")
        print("1. Suma | 2. Promedio | 3. Conteo")
        while True:
            met = input("Selecciona: ")
            if met in ['1','2','3']: break
            print("❌ Elige solo 1, 2 o 3.")

        if met == '1':
            datos = df.groupby(col_cat)[col_num].sum().round(2).sort_values(ascending=False)
            metrica = "Suma"
        elif met == '2':
            datos = df.groupby(col_cat)[col_num].mean().round(2).sort_values(ascending=False)
            metrica = "Promedio"
        else:
            datos = df.groupby(col_cat)[col_num].count().sort_values(ascending=False)
            metrica = "Conteo"

        fig, ax = plt.subplots(figsize=(12, 6))
        sns.barplot(x=datos.values, y=datos.index, 
                   hue=datos.index, palette='Blues_r', ax=ax, legend=False)
        ax.set_title(f'{metrica} de {col_num} por {col_cat}', 
                    fontsize=14, fontweight='bold')
        ax.set_xlabel(f'{metrica} ({col_num})')
        ax.set_ylabel(col_cat)
        for i, v in enumerate(datos.values):
            ax.text(v, i, f' {v:,.2f}', va='center')
        plt.tight_layout()
        plt.show()

    elif tipo == '2':
        # Línea de tendencia
        cols_fecha = [col for col in df.columns if 'fecha' in col.lower() or 'date' in col.lower()]
        
        if not cols_fecha:
            print("⚠️ No se detectaron columnas de fecha.")
            return
        
        print("\n¿Qué columna de fecha quieres usar?")
        for i, col in enumerate(cols_fecha, 1):
            print(f"{i}. {col}")
        while True:
            try:
                opc = int(input("\nSelecciona: ")) - 1
                if 0 <= opc < len(cols_fecha):
                    col_fecha = cols_fecha[opc]
                    break
                print("❌ Número fuera de rango.")
            except ValueError:
                print("❌ Debes ingresar un número.")

        print(f"\n¿Qué campo numérico quieres ver en el tiempo?")
        for i, col in enumerate(cols_numericas, 1):
            print(f"{i}. {col}")
        while True:
            try:
                opc = int(input("\nSelecciona: ")) - 1
                if 0 <= opc < len(cols_numericas):
                    col_num = cols_numericas[opc]
                    break
                print("❌ Número fuera de rango.")
            except ValueError:
                print("❌ Debes ingresar un número.")

        df[col_fecha] = pd.to_datetime(df[col_fecha], errors='coerce')

        print("\n¿Cómo quieres agrupar la fecha?")
        print("1. Por Año")
        print("2. Por Mes")
        print("3. Por Día")
        print("4. Por Año y Mes")

        while True:
            agrupacion = input("\nSelecciona: ")
            if agrupacion in ['1','2','3','4']: break
            print("❌ Elige solo 1, 2, 3 o 4.")

        if agrupacion == '1':
            df['Periodo'] = df[col_fecha].dt.year.astype(str)
            titulo_periodo = "Año"
        elif agrupacion == '2':
            df['Periodo'] = df[col_fecha].dt.month.map({
                1:'Ene', 2:'Feb', 3:'Mar', 4:'Abr', 5:'May', 6:'Jun',
                7:'Jul', 8:'Ago', 9:'Sep', 10:'Oct', 11:'Nov', 12:'Dic'
            })
            titulo_periodo = "Mes"
        elif agrupacion == '3':
            df['Periodo'] = df[col_fecha].dt.date.astype(str)
            titulo_periodo = "Día"
        else:
            df['Periodo'] = df[col_fecha].dt.to_period('M').astype(str)
            titulo_periodo = "Año-Mes"

        # tendencia va FUERA de todos los if, al mismo nivel
        if agrupacion == '2':
            orden_meses = ['Ene','Feb','Mar','Abr','May','Jun',
                        'Jul','Ago','Sep','Oct','Nov','Dic']
            tendencia = df.groupby('Periodo')[col_num].sum().reset_index()
            tendencia['Periodo'] = pd.Categorical(tendencia['Periodo'],
                                                categories=orden_meses,
                                                ordered=True)
            tendencia = tendencia.sort_values('Periodo')
        else:
            tendencia = df.groupby('Periodo')[col_num].sum().reset_index()
            tendencia = tendencia.sort_values('Periodo')

        tendencia['Periodo'] = tendencia['Periodo'].astype(str)

        # fig y ax van aquí, al mismo nivel que tendencia
        fig, ax = plt.subplots(figsize=(14, 6))
        ax.plot(tendencia['Periodo'], tendencia[col_num],
        marker='o', linewidth=2, color='steelblue')
        
        # Línea de tendencia
        import numpy as np
        z = np.polyfit(range(len(tendencia)), tendencia[col_num], 1)
        p = np.poly1d(z)
        ax.plot(tendencia['Periodo'], p(range(len(tendencia))),
                linestyle='--', color='red', linewidth=1.5, label='Tendencia')
        
        ax.set_title(f'Tendencia de {col_num} por {titulo_periodo}', 
                    fontsize=14, fontweight='bold')
        ax.set_xlabel('Período')
        ax.set_ylabel(col_num)
        ax.tick_params(axis='x', rotation=90)
        ax.legend()
        ax.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.show()

    elif tipo == '3':
        # Dispersión
        print("\n¿Qué campo numérico va en el eje X?")
        for i, col in enumerate(cols_numericas, 1):
            print(f"{i}. {col}")
        while True:
            try:
                opc = int(input("\nSelecciona: ")) - 1
                if 0 <= opc < len(cols_numericas):
                    col_x = cols_numericas[opc]
                    break
                print("❌ Número fuera de rango.")
            except ValueError:
                print("❌ Debes ingresar un número.")

        print(f"\n¿Qué campo numérico va en el eje Y?")
        cols_y = [c for c in cols_numericas if c != col_x]
        for i, col in enumerate(cols_y, 1):
            print(f"{i}. {col}")
        while True:
            try:
                opc = int(input("\nSelecciona: ")) - 1
                if 0 <= opc < len(cols_y):
                    col_y = cols_y[opc]
                    break
                print("❌ Número fuera de rango.")
            except ValueError:
                print("❌ Debes ingresar un número.")

        # Color por categoría opcional
        col_color = None
        if cols_categoricas and input("\n¿Colorear por categoría? (s/n): ").lower() == 's':
            print("¿Qué categoría usar para el color?")
            for i, col in enumerate(cols_categoricas, 1):
                print(f"{i}. {col}")
            while True:
                try:
                    opc = int(input("\nSelecciona: ")) - 1
                    if 0 <= opc < len(cols_categoricas):
                        col_color = cols_categoricas[opc]
                        break
                    print("❌ Número fuera de rango.")
                except ValueError:
                    print("❌ Debes ingresar un número.")

        fig, ax = plt.subplots(figsize=(12, 6))
        if col_color:
            sns.scatterplot(data=df, x=col_x, y=col_y, 
                          hue=col_color, ax=ax, alpha=0.7)
        else:
            sns.scatterplot(data=df, x=col_x, y=col_y, ax=ax, alpha=0.7)
        ax.set_title(f'Relación entre {col_x} y {col_y}', 
                    fontsize=14, fontweight='bold')
        plt.tight_layout()
        plt.show()

    elif tipo == '4':
        # Mapa de calor de correlación
        fig, ax = plt.subplots(figsize=(10, 8))
        correlacion = df[cols_numericas].corr().round(2)
        sns.heatmap(correlacion, annot=True, cmap='Blues', 
                   fmt='.2f', ax=ax)
        ax.set_title('Mapa de Calor — Correlación entre Variables', 
                    fontsize=14, fontweight='bold')
        plt.tight_layout()
        plt.show()

    elif tipo == '5':
        # Histograma
        print("\n¿Qué campo numérico quieres ver?")
        for i, col in enumerate(cols_numericas, 1):
            print(f"{i}. {col}")
        while True:
            try:
                opc = int(input("\nSelecciona: ")) - 1
                if 0 <= opc < len(cols_numericas):
                    col_num = cols_numericas[opc]
                    break
                print("❌ Número fuera de rango.")
            except ValueError:
                print("❌ Debes ingresar un número.")

        fig, ax = plt.subplots(figsize=(12, 6))
        sns.histplot(df[col_num], bins=30, kde=True, 
                    color='steelblue', ax=ax)
        ax.set_title(f'Distribución de {col_num}', 
                    fontsize=14, fontweight='bold')
        ax.set_xlabel(col_num)
        ax.set_ylabel('Frecuencia')
        plt.tight_layout()
        plt.show()

    if input("\n¿Deseas generar otra visualización? (s/n): ").lower() == 's':
        visualizaciones(df, cols_numericas, cols_categoricas)
# FIN DE VISUALIZACIONES

def main():
    print("=== ANALIZADOR EDA GENÉRICO ===")
    
    ruta = seleccionar_archivo()
    if ruta is None:
        return
    
    if ruta.endswith('.csv'):
        df = pd.read_csv(ruta)
    else:
        df = pd.read_excel(ruta)
    
    nombre_archivo = os.path.basename(ruta)
    print(f"\n✅ Archivo cargado: {ruta}")
    print(f"   Registros: {len(df)}")
    print(f"   Columnas: {len(df.columns)}")
    
    # Configurar campos clave y columnas
    config, cols_numericas, cols_categoricas = configurar_campos(df)
    
    while True:
        print("\n¿Qué análisis deseas hacer?")
        print("1. Estadísticos descriptivos")
        print("2. Análisis cruzado")
        print("3. Drill-down multidimensional")
        print("4. Visualizaciones")
        print("5. Reporte ejecutivo automático")
        print("6. Salir")
        
        opc = input("\nSelecciona: ")
        if opc == '1':
            analisis_estadistico(df, cols_numericas)
        elif opc == '2':
            analisis_cruzado(df, cols_numericas, cols_categoricas)
        elif opc == '3':
            analisis_drill_down(df, cols_numericas, cols_categoricas)
        elif opc == '4':
            visualizaciones(df, cols_numericas, cols_categoricas)
        elif opc == '5':
            generar_reporte_ejecutivo(df, config, nombre_archivo)
        elif opc == '6':
            print("👋 ¡Hasta luego!")
            break
        else:
            print("❌ Elige solo 1, 2, 3, 4, 5 o 6.")

if __name__ == "__main__":
    main()