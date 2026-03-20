import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
from calendar import monthrange
from datetime import datetime

sns.set_theme(style="whitegrid")

def seleccionar_archivo():
    carpeta = "entrada"
    archivos = [f for f in os.listdir(carpeta) if f.endswith(('.xlsx', '.xls', '.csv'))]
    
    if not archivos:
        print("⚠️ No hay archivos en la carpeta entrada.")
        return None
    
    print("\n📥 Archivos disponibles:")
    for i, f in enumerate(archivos, 1):
        print(f"{i}. {f}")
    
    while True:
        try:
            opc = int(input("\nSelecciona el número del archivo: "))
            if 1 <= opc <= len(archivos):
                return os.path.join(carpeta, archivos[opc-1])
            print("❌ Número fuera de rango.")
        except ValueError:
            print("❌ Debes ingresar un número.")

def configurar_campos_tendencia(df):
    print("\n=== CONFIGURACIÓN DE TENDENCIAS ===")
    
    cols_todas = df.columns.tolist()
    cols_numericas = df.select_dtypes(include=['int64', 'float64']).columns.tolist()
    cols_categoricas = df.select_dtypes(include=['object']).columns.tolist()
    cols_fechas = [c for c in cols_todas if 'fecha' in c.lower() or 'date' in c.lower()]
    
    config = {}
    
    # Seleccionar campo fecha
    print("\n¿Cuál es la columna de FECHA?")
    if cols_fechas:
        print("Sugeridas:")
        for i, col in enumerate(cols_fechas, 1):
            print(f"{i}. {col}")
        print(f"{len(cols_fechas)+1}. Otra columna")
    else:
        print("No se detectaron columnas de fecha.")
        cols_fechas = cols_todas
        for i, col in enumerate(cols_fechas, 1):
            print(f"{i}. {col}")
    
    while True:
        try:
            opc = int(input("→ ")) - 1
            if 0 <= opc < len(cols_fechas):
                config['fecha'] = cols_fechas[opc]
                break
            print("❌ Número fuera de rango.")
        except ValueError:
            print("❌ Debes ingresar un número.")
    
    # Seleccionar campo valor
    print("\n¿Cuál es la columna de VALOR a medir?")
    for i, col in enumerate(cols_numericas, 1):
        print(f"{i}. {col}")
    
    while True:
        try:
            opc = int(input("→ ")) - 1
            if 0 <= opc < len(cols_numericas):
                config['valor'] = cols_numericas[opc]
                break
            print("❌ Número fuera de rango.")
        except ValueError:
            print("❌ Debes ingresar un número.")
    
    # Seleccionar campos de drill-down
    print("\n¿Cuáles columnas quieres usar para drill-down?")
    print("(Puedes seleccionar varias separadas por coma, ej: 1,3,4)")
    for i, col in enumerate(cols_categoricas, 1):
        print(f"{i}. {col}")
    
    while True:
        try:
            seleccion = input("→ ").strip()
            indices = [int(x.strip())-1 for x in seleccion.split(',')]
            cols_drill = [cols_categoricas[i] for i in indices if 0 <= i < len(cols_categoricas)]
            if cols_drill:
                config['drill'] = cols_drill
                break
            print("❌ Selección inválida.")
        except:
            print("❌ Debes ingresar números separados por coma.")
    
    print("\n✅ Configuración guardada:")
    print(f"   FECHA  → {config['fecha']}")
    print(f"   VALOR  → {config['valor']}")
    print(f"   DRILL  → {config['drill']}")
    
    return config

def graficar_tendencia(datos, titulo, col_x, col_y, num_figura):
    fig, ax = plt.subplots(figsize=(14, 6), num=num_figura)
    
    ax.plot(range(len(datos)), datos.values,
            marker='o', linewidth=2, color='steelblue', label=col_y)
    
    # Línea de tendencia
    z = np.polyfit(range(len(datos)), datos.values, 1)
    p = np.poly1d(z)
    ax.plot(range(len(datos)), p(range(len(datos))),
            linestyle='--', color='red', linewidth=1.5, label='Tendencia')
    
    # Etiquetas en puntos
    for i, v in enumerate(datos.values):
        ax.annotate(f'${v:,.0f}', (i, v),
                   textcoords="offset points",
                   xytext=(0, 10), ha='center', fontsize=8)
    
    ax.set_xticks(range(len(datos)))
    ax.set_xticklabels(datos.index.astype(str), rotation=45, ha='right')
    ax.set_title(titulo, fontsize=14, fontweight='bold')
    ax.set_xlabel(col_x)
    ax.set_ylabel(col_y)
    ax.legend()
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()
    plt.pause(0.1)

def graficar_barras(datos, titulo, col_cat, col_num, num_figura):
    fig, ax = plt.subplots(figsize=(12, 6), num=num_figura)
    sns.barplot(x=datos.values, y=datos.index.astype(str),
               hue=datos.index.astype(str), palette='Blues_r', ax=ax, legend=False)
    ax.set_title(titulo, fontsize=14, fontweight='bold')
    ax.set_xlabel(col_num)
    ax.set_ylabel(col_cat)
    for i, v in enumerate(datos.values):
        ax.text(v, i, f' ${v:,.2f}', va='center')
    plt.tight_layout()
    plt.show()
    plt.pause(0.1)

def analisis_tendencias(df, config):
    plt.ion()
    
    col_fecha = config['fecha']
    col_valor = config['valor']
    cols_drill = config['drill']
    
    df[col_fecha] = pd.to_datetime(df[col_fecha], errors='coerce')
    
    hoy = datetime.now()
    año_actual = hoy.year
    mes_actual = hoy.month
    dia_actual = hoy.day
    dias_mes_actual = monthrange(hoy.year, hoy.month)[1]
    
    fig_num = 1
    
    # =====================
    # NIVEL 1 — ANUAL
    # =====================
    print("\n=== NIVEL 1 — RESUMEN ANUAL ===")
    
    tendencia_anual = df.groupby(df[col_fecha].dt.year)[col_valor].sum().round(2)
    tendencia_anual.index = tendencia_anual.index.astype(int)
    
    # Calcular proyección año actual
    ventas_año_actual = tendencia_anual.get(año_actual, 0)
    meses_completos_año = mes_actual - 1  # meses completos antes del mes actual
    ventas_mes_actual = df[
        (df[col_fecha].dt.year == año_actual) & 
        (df[col_fecha].dt.month == mes_actual)
    ][col_valor].sum().round(2)
    
    # Proyección mes actual
    promedio_diario = ventas_mes_actual / dia_actual
    proyeccion_mes = (promedio_diario * dias_mes_actual).round(2)
    
    # Proyección año completo
    ventas_meses_completos = df[
        (df[col_fecha].dt.year == año_actual) & 
        (df[col_fecha].dt.month < mes_actual)
    ][col_valor].sum().round(2)
    
    proyeccion_año = (ventas_meses_completos + proyeccion_mes) / mes_actual * 12
    proyeccion_año = round(proyeccion_año, 2)
    
    # Mostrar en pantalla
    for año, valor in tendencia_anual.items():
        if año == año_actual:
            print(f"• {año}: ${valor:,.2f} ({mes_actual} meses, {dia_actual} días en curso)")
            print(f"  → Proyección {hoy.strftime('%B')} completo: ${proyeccion_mes:,.2f}")
            print(f"  → Proyección {año_actual} completo:   ${proyeccion_año:,.2f}")
            # Comparar proyección vs año anterior
            if año_actual - 1 in tendencia_anual.index:
                año_anterior = tendencia_anual[año_actual - 1]
                var = ((proyeccion_año - año_anterior) / año_anterior * 100).round(1)
                direccion = "crecimiento 📈" if var > 0 else "decrecimiento 📉"
                print(f"  → vs {año_actual-1}: {direccion} ({var:+.1f}%) proyectado")
        else:
            print(f"• {año}: ${valor:,.2f}")
    
    # Comparación entre años anteriores completos
    años_completos = tendencia_anual[tendencia_anual.index < año_actual]
    if len(años_completos) > 1:
        print("\nComportamiento años anteriores:")
        for i in range(len(años_completos)-1):
            año_a = int(años_completos.index[i])
            año_b = int(años_completos.index[i+1])
            var = ((años_completos.iloc[i+1] - años_completos.iloc[i]) / años_completos.iloc[i] * 100).round(1)
            direccion = "crecimiento 📈" if var > 0 else "decrecimiento 📉"
            print(f"• {año_a} vs {año_b}: {direccion} ({var:+.1f}%)")
    
    # Gráfica anual con proyección
    fig, ax = plt.subplots(figsize=(14, 6), num=fig_num)
    
    # Datos reales
    ax.plot(tendencia_anual.index.astype(str), tendencia_anual.values,
            marker='o', linewidth=2, color='steelblue', label='Real')
    
    # Punto proyección año actual
    ax.plot(str(año_actual), proyeccion_año,
            marker='o', markersize=10, color='orange',
            linestyle='none', label=f'Proyección {año_actual}')
    
    # Línea punteada del real al proyectado
    ax.plot([str(año_actual), str(año_actual)],
            [ventas_año_actual, proyeccion_año],
            linestyle='--', color='orange', linewidth=1.5)
    
    # Etiquetas
    for i, (año, valor) in enumerate(tendencia_anual.items()):
        ax.annotate(f'${valor:,.0f}', (str(año), valor),
                   textcoords="offset points",
                   xytext=(0, 10), ha='center', fontsize=9)
    
    ax.annotate(f'Proy: ${proyeccion_año:,.0f}',
               (str(año_actual), proyeccion_año),
               textcoords="offset points",
               xytext=(0, 10), ha='center', fontsize=9, color='orange')
    
    ax.set_title(f"Tendencia Anual de {col_valor}", fontsize=14, fontweight='bold')
    ax.set_xlabel("Año")
    ax.set_ylabel(col_valor)
    ax.legend()
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()
    plt.pause(0.1)
    fig_num += 1
    
    # =====================
    # NIVEL 2 — MENSUAL
    # =====================
    if input("\n¿Quieres profundizar en un año específico? (s/n): ").lower() == 's':
        años = tendencia_anual.index.tolist()
        print("\n¿Qué año quieres analizar?")
        for i, año in enumerate(años, 1):
            print(f"{i}. {año}")
        
        while True:
            try:
                opc = int(input("→ ")) - 1
                if 0 <= opc < len(años):
                    año_sel = años[opc]
                    break
                print("❌ Número fuera de rango.")
            except ValueError:
                print("❌ Debes ingresar un número.")
        
        df_año = df[df[col_fecha].dt.year == año_sel]
        orden_meses = {1:'Ene', 2:'Feb', 3:'Mar', 4:'Abr', 5:'May', 6:'Jun',
                      7:'Jul', 8:'Ago', 9:'Sep', 10:'Oct', 11:'Nov', 12:'Dic'}
        
        tendencia_mensual = df_año.groupby(df_año[col_fecha].dt.month)[col_valor].sum().round(2)
        
        print(f"\n=== NIVEL 2 — TENDENCIA MENSUAL {año_sel} ===")
        
        labels_meses = []
        valores_meses = []
        proyeccion_mes_label = None
        proyeccion_mes_valor = None
        
        for mes_num, valor in tendencia_mensual.items():
            mes_nom = orden_meses[mes_num]
            if año_sel == año_actual and mes_num == mes_actual:
                promedio_diario_m = valor / dia_actual
                proy_mes = round(promedio_diario_m * dias_mes_actual, 2)
                print(f"• {mes_nom}: ${valor:,.2f} ({dia_actual} días) → Proyección: ${proy_mes:,.2f}")
                labels_meses.append(mes_nom)
                valores_meses.append(valor)
                proyeccion_mes_label = mes_nom
                proyeccion_mes_valor = proy_mes
            else:
                print(f"• {mes_nom}: ${valor:,.2f}")
                labels_meses.append(mes_nom)
                valores_meses.append(valor)
        
        # Gráfica mensual con proyección si es año actual
        fig, ax = plt.subplots(figsize=(14, 6), num=fig_num)
        ax.plot(labels_meses, valores_meses,
                marker='o', linewidth=2, color='steelblue', label='Real')
        
        if proyeccion_mes_label and año_sel == año_actual:
            idx = labels_meses.index(proyeccion_mes_label)
            ax.plot(proyeccion_mes_label, proyeccion_mes_valor,
                    marker='o', markersize=10, color='orange',
                    linestyle='none', label=f'Proyección {proyeccion_mes_label}')
            ax.plot([labels_meses[idx], proyeccion_mes_label],
                    [valores_meses[idx], proyeccion_mes_valor],
                    linestyle='--', color='orange', linewidth=1.5)
            ax.annotate(f'Proy: ${proyeccion_mes_valor:,.0f}',
                       (proyeccion_mes_label, proyeccion_mes_valor),
                       textcoords="offset points",
                       xytext=(0, 10), ha='center', fontsize=9, color='orange')
        
        for i, (label, valor) in enumerate(zip(labels_meses, valores_meses)):
            ax.annotate(f'${valor:,.0f}', (label, valor),
                       textcoords="offset points",
                       xytext=(0, 10), ha='center', fontsize=8)
        
        ax.set_title(f"Tendencia Mensual {año_sel} — {col_valor}", 
                    fontsize=14, fontweight='bold')
        ax.set_xlabel("Mes")
        ax.set_ylabel(col_valor)
        ax.legend()
        ax.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.show()
        plt.pause(0.1)
        fig_num += 1
        
        # =====================
        # NIVEL 3 — POR MES
        # =====================
        if input("\n¿Quieres profundizar en un mes específico? (s/n): ").lower() == 's':
            meses_disp = list(tendencia_mensual.index)
            print("\n¿Qué mes quieres analizar?")
            for i, mes_num in enumerate(meses_disp, 1):
                print(f"{i}. {orden_meses[mes_num]}")
            
            while True:
                try:
                    opc = int(input("→ ")) - 1
                    if 0 <= opc < len(meses_disp):
                        mes_sel_num = meses_disp[opc]
                        mes_sel_nom = orden_meses[mes_sel_num]
                        break
                    print("❌ Número fuera de rango.")
                except ValueError:
                    print("❌ Debes ingresar un número.")
            
            df_mes = df_año[df_año[col_fecha].dt.month == mes_sel_num]
            
            print(f"\n¿Por qué campo quieres ver el detalle de {mes_sel_nom} {año_sel}?")
            for i, col in enumerate(cols_drill, 1):
                print(f"{i}. {col}")
            
            while True:
                try:
                    opc = int(input("→ ")) - 1
                    if 0 <= opc < len(cols_drill):
                        col_detalle = cols_drill[opc]
                        break
                    print("❌ Número fuera de rango.")
                except ValueError:
                    print("❌ Debes ingresar un número.")
            
            resultado = df_mes.groupby(col_detalle)[col_valor].sum().round(2).sort_values(ascending=False)
            
            print(f"\n{col_valor} por {col_detalle} — {mes_sel_nom} {año_sel}:")
            print(resultado.to_string())
            
            graficar_barras(resultado,
                           f"{col_valor} por {col_detalle} — {mes_sel_nom} {año_sel}",
                           col_detalle, col_valor, fig_num)
            fig_num += 1
            
            # NIVEL 4
            cols_restantes = [c for c in cols_drill if c != col_detalle]
            if cols_restantes and input("\n¿Quieres profundizar un nivel más? (s/n): ").lower() == 's':
                valores = resultado.index.tolist()
                print(f"\n¿Sobre qué valor de [{col_detalle}] quieres profundizar?")
                for i, val in enumerate(valores, 1):
                    print(f"{i}. {val}")
                
                while True:
                    try:
                        opc = int(input("→ ")) - 1
                        if 0 <= opc < len(valores):
                            valor_sel = valores[opc]
                            break
                        print("❌ Número fuera de rango.")
                    except ValueError:
                        print("❌ Debes ingresar un número.")
                
                df_detalle = df_mes[df_mes[col_detalle] == valor_sel]
                
                print(f"\n¿Por qué campo quieres ver el detalle de [{valor_sel}]?")
                for i, col in enumerate(cols_restantes, 1):
                    print(f"{i}. {col}")
                
                while True:
                    try:
                        opc = int(input("→ ")) - 1
                        if 0 <= opc < len(cols_restantes):
                            col_detalle2 = cols_restantes[opc]
                            break
                        print("❌ Número fuera de rango.")
                    except ValueError:
                        print("❌ Debes ingresar un número.")
                
                resultado2 = df_detalle.groupby(col_detalle2)[col_valor].sum().round(2).sort_values(ascending=False)
                
                print(f"\n{col_valor} por {col_detalle2} — {valor_sel} en {mes_sel_nom} {año_sel}:")
                print(resultado2.to_string())
                
                graficar_barras(resultado2,
                               f"{col_valor} por {col_detalle2} — {valor_sel} {mes_sel_nom} {año_sel}",
                               col_detalle2, col_valor, fig_num)

    if input("\n¿Deseas hacer otro análisis de tendencias? (s/n): ").lower() == 's':
        analisis_tendencias(df, config)
    else:
        plt.ioff()

def main():
    print("=== ANÁLISIS DE TENDENCIAS ===")
    
    ruta = seleccionar_archivo()
    if ruta is None:
        return
    
    if ruta.endswith('.csv'):
        df = pd.read_csv(ruta)
    else:
        df = pd.read_excel(ruta)
    
    print(f"\n✅ Archivo cargado: {os.path.basename(ruta)}")
    print(f"   Registros: {len(df)}")
    print(f"   Columnas: {len(df.columns)}")
    
    config = configurar_campos_tendencia(df)
    analisis_tendencias(df, config)

if __name__ == "__main__":
    main()