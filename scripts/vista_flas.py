import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# ==========================
# CONFIGURACIÓN INICIAL
# ==========================

# Ajusta esta parte a tu archivo
def cargar_dataframe():
    ruta = input("Ingresa la ruta del archivo (CSV o Excel): ").strip()
    if not ruta:
        print("No se ingresó ninguna ruta.")
        input("Presiona Enter para salir...")
        return None

    ruta_lower = ruta.lower()

    try:
        if ruta_lower.endswith((".xlsx", ".xls")):
            xl = pd.ExcelFile(ruta)
            hojas = xl.sheet_names
            if len(hojas) == 1:
                df = pd.read_excel(ruta)
            else:
                print("Hojas disponibles:", ", ".join(hojas))
                num = input("Número de hoja (0 = primera) [0]: ").strip() or "0"
                idx = int(num)
                df = pd.read_excel(ruta, sheet_name=hojas[idx])
        else:
            df = pd.read_csv(ruta, encoding="utf-8")

        print("\n✅ DataFrame cargado correctamente.")
        input("Presiona Enter para continuar...")
        return df

    except Exception as e:
        print("\n❌ Error al cargar el archivo:", e)
        input("Presiona Enter para salir...")
        return None


def limpiar_pantalla():
    os.system("cls" if os.name == "nt" else "clear")


def pausar():
    input("\nPresiona Enter para volver al menú...")

# ==========================
# DICCIONARIO EXPLICACIONES
# ==========================
EXPLICACIONES = {
    "corr_num": """📌 Correlación numérica
Mide qué tan relacionada está una variable numérica con otra (relación lineal).

Interpretación aproximada de la fuerza (valor absoluto):
- 0.00–0.30 → débil
- 0.30–0.60 → moderada
- 0.60–0.80 → fuerte
- 0.80–1.00 → muy fuerte

Signo:
- Positivo → cuando una sube, la otra tiende a subir.
- Negativo → cuando una sube, la otra tiende a bajar.
""",

    "describe_num": """📌 describe() numérico
Resumen estadístico de columnas numéricas:
- count → cuántos datos hay
- unique → cuántos valores únicos hay
- top → el valor más frecuente
- freq → cuántas veces aparece el valor más frecuente
- mean → promedio
- std → qué tanto se dispersan los datos
- min / max → valores mínimo y máximo
- 25% / 50% / 75% → percentiles (mediana en 50%)
""",

    "distrib_num": """📌 Distribución numérica- 
- Histograma → forma de la distribución (simétrica, sesgada, etc.)- 
- Boxplot → mediana, rangos y posibles outliers.
- Interpretación → si la distribución es normal, sesgada, con outliers, etc.

""",

    "distrib_cat": """📌 Distribución categórica
- value_counts → cuántas veces aparece cada categoría.
- Gráfico de barras → visualización de las categorías más frecuentes.
""",

    "nulos": """📌 Nulos
- isnull().sum() → cuántos datos faltan por columna.
- % de nulos → qué tan grave es el problema de datos faltantes.
""",

    "rel_cat_num": """📌 Categórica vs numérica
Compara una variable numérica entre grupos (categorías):
- Promedio por categoría → qué grupo tiene mayor/menor valor medio.
- Boxplot → distribución de la variable numérica en cada grupo.
- Interpretación → si hay diferencias entre grupos, si algún grupo tiene mucha variabilidad, etc.
""",

    "rel_cat_cat": """📌 Categórica vs categórica
Compara dos variables categóricas:
- Contingencia → cuántas veces aparece cada combinación de categorías.
- Gráfico de barras agrupadas → visualización de las combinaciones más frecuentes.
- Interpretación → si hay asociación entre las categorías, si alguna combinación es especialmente común o rara, etc.

""",
    "rel_num_num": """📌 Numérica vs numérica
Compara dos variables numéricas:
- Correlación → qué tan relacionadas están.
- Gráfico de dispersión → visualización de la relación entre las variables.
- Interpretación → si hay una relación lineal, si hay outliers, etc.
""",
    "histograma": """📌 Histograma
Muestra la distribución de una variable numérica.
- Eje X → valores de la variable.(Agrupados en intervalos Pequeños-Medios-Grandes).
- Eje Y → frecuencia (cuántas veces aparece cada valor).
- Interpretación → forma de la distribución (simétrica, sesgada, etc.)
- La línea azul es como una lomita suave que te dice dónde están la mayoría de las cosas. 
    Si la línea sube, es porque hay muchas cosas ahí. Si baja, es porque casi no hay.
""",
    "frecuencias": """📌 Frecuencias
- value_counts() → cuántas veces aparece cada valor en una columna.
- Gráfico de barras → visualización de las frecuencias.
- Interpretación → qué categorías son más comunes, si hay categorías raras, etc.
"""

}

def mostrar_explicacion(clave: str):
    texto = EXPLICACIONES.get(clave)
    if texto:
        print(texto)

# FIN DE DICCIONARIO EXPLICACIONES


def elegir_columnas_por_numero(lista_columnas, mensaje, permitir_multiples=True):
    if not lista_columnas:
        print("No hay columnas disponibles para esta selección.")
        return None
    print("\nColumnas disponibles:")
    for i, col in enumerate(lista_columnas):
        print(f"{i}) {col}")
    # Texto del prompt según si se permite una o varias columnas
    if permitir_multiples:
        prompt = f"\n{mensaje} (puedes escribir varios números separados por coma): "
    else:
        prompt = f"\n{mensaje} (escribe SOLO un número): "
    entrada = input(prompt).strip()
    if not entrada:
        print("No se seleccionó ninguna columna.")
        return None
    try:
        indices = [int(x.strip()) for x in entrada.split(",") if x.strip()]
    except ValueError:
        print("Error: solo se permiten números.")
        return None
    if not permitir_multiples and len(indices) != 1:
        print("Debes elegir exactamente una columna.")
        return None
    if any(i < 0 or i >= len(lista_columnas) for i in indices):
        print("Algún número está fuera de rango.")
        return None
    columnas = [lista_columnas[i] for i in indices]
    return columnas

# ==========================
# GUARDAR TABLA 
def guardar_tabla(df_resultado: pd.DataFrame, nombre_base: str):
    """
    df_resultado: DataFrame o Series convertido a DataFrame
    nombre_base: nombre sugerido para el archivo (sin extensión)
    """
    print("\n¿Quieres guardar este resultado?")
    print("1) Sí, en CSV")
    print("2) Sí, en Excel")
    print("0) No guardar")

    op = input("Elige una opción: ").strip()

    if op == "0":
        return

    ruta = input(f"Nombre/ruta del archivo (sin extensión) [{nombre_base}]: ").strip()
    if not ruta:
        ruta = nombre_base

    try:
        if op == "1":
            ruta_completa = ruta + ".csv"
            df_resultado.to_csv(ruta_completa, index=True)
            print(f"\n✅ Guardado en {ruta_completa}")
        elif op == "2":
            ruta_completa = ruta + ".xlsx"
            df_resultado.to_excel(ruta_completa, index=True)
            print(f"\n✅ Guardado en {ruta_completa}")
        else:
            print("Opción de guardado inválida. No se guardó nada.")
    except Exception as e:
        print("\n❌ Error al guardar el archivo:", e)

# FIN DE GUARDAR TABLA

# ==========================
# MODO REPORTE RÁPIDO
# ==========================

def modo_reporte(df: pd.DataFrame):
    """
    Genera un reporte básico en un solo archivo Excel con varias hojas.
    """
    limpiar_pantalla()
    print("=== MODO REPORTE RÁPIDO ===")
    ruta = input("Ruta\\nombre de reporte (sin extensión) x omision --> [reporte_resumen]: ").strip()
    if not ruta:
        ruta = "salida\\reporte_resumen"

    ruta_xlsx = ruta + ".xlsx"

    desc_all = df.describe(include="all").T
    nulos = df.isnull().sum().to_frame(name="n_nulos")
    nulos_pct = (df.isnull().mean() * 100).round(2).to_frame(name="%_nulos")
    nunique = df.nunique().to_frame(name="nunique")
    corr = df.select_dtypes(include=["number"]).corr().round(3)

    try:
        with pd.ExcelWriter(ruta_xlsx) as writer:
            desc_all.to_excel(writer, sheet_name="describe_all")
            nulos.to_excel(writer, sheet_name="nulos_abs")
            nulos_pct.to_excel(writer, sheet_name="nulos_pct")
            nunique.to_excel(writer, sheet_name="nunique")
            corr.to_excel(writer, sheet_name="correlacion_num")
        print(f"\n✅ Reporte guardado en {ruta_xlsx}")
    except Exception as e:
        print("\n❌ Error al generar el reporte:", e)

    pausar()

# ==========================
# MÓDULO 1: VISIÓN GENERAL
# ==========================

def menu_vision_general(df: pd.DataFrame):
    while True:
        limpiar_pantalla()
        print("=== VISIÓN GENERAL ===")
        print("1) Shape --> filas y columnas")
        print("2) tolist() --> lista de columnas")
        print("3) dtypes --> tipos de datos")
        print("4) head() --> primeras filas")
        print("5) sample() --> muestra aleatoria")
        print("6) describe(include='all') --> resumen general")
        print("7) nunique() --> cantidad de valores únicos por columna")
        print("0) Volver al menú principal")

        op = input("\nElige una opción: ").strip()
        limpiar_pantalla()

        if op == "1":
            print("Shape --> (filas, columnas)")
            print(df.shape)
            pausar()
        elif op == "2":
            print("tolist() --> lista de columnas")
            print(df.columns.tolist())
            pausar()    
        elif op == "3":
            print("dtypes --> tipos de datos")
            print(df.dtypes)
            pausar()

        elif op == "4":
            print("head() --> primeras 5 filas")
            print(df.head())
            pausar()

        elif op == "5":
            print("sample(5) --> 5 filas aleatorias")            
            print(df.sample(n=min(5, len(df)), random_state=0))
            pausar()

        elif op == "6":
            print("describe(include='all') --> resumen general")
            mostrar_explicacion("describe_num")   # <<--- NUEVO
            print(df.describe(include="all").T)
            pausar()

        elif op == "7":
            print("nunique() --> cantidad de valores únicos por columna")
            print(df.nunique())
            pausar()

        elif op == "0":
            break

        else:
            print("Opción inválida.")
            pausar()


# ==========================
# MÓDULO 2: CALIDAD DE DATOS
# ==========================

def menu_calidad_datos(df: pd.DataFrame):
    while True:
        limpiar_pantalla()
        print("=== CALIDAD DE DATOS ===")
        print("1) Nulos por columna (isnull().sum())")
        print("2) Porcentaje de nulos por columna")
        print("3) Filas duplicadas (duplicated().sum())")
        print("4) Top 5 columnas con más nulos")
        print("0) Volver al menú principal")

        op = input("\nElige una opción: ").strip()
        limpiar_pantalla()

        if op == "1":
            print("Nulos por columna:")
            print(df.isnull().sum())
            pausar()

        elif op == "2":
            print("Porcentaje de nulos por columna:")
            porcentaje = (df.isnull().mean() * 100).round(2)
            print(porcentaje)
            pausar()

        elif op == "3":
            print("Número de filas duplicadas:")
            print(df.duplicated().sum())
            pausar()

        elif op == "4":
            print("Top 5 columnas con más nulos:")
            nulos = df.isnull().sum().sort_values(ascending=False)
            print(nulos.head(5))
            pausar()

        elif op == "0":
            break

        else:
            print("Opción inválida.")
            pausar()


# ==========================
# MÓDULO 3: DISTRIBUCIONES
# ==========================

def menu_distribuciones(df: pd.DataFrame):
    while True:
        limpiar_pantalla()
        print("=== DISTRIBUCIONES (UNIVARIADO) ===")
        print("1) Variable numérica --> histograma + boxplot + resumen")
        print("2) Variable categórica --> tabla de frecuencias + gráfico de barras")
        print("0) Volver al menú principal")

        op = input("\nElige una opción: ").strip()
        limpiar_pantalla()

        if op == "1":
            distribucion_numerica(df)
        elif op == "2":
            distribucion_categorica(df)
        elif op == "0":
            break
        else:
            print("Opción inválida.")
            pausar()


def distribucion_numerica(df: pd.DataFrame):
    mostrar_explicacion("distrib_num")   # <<--- NUEVO
    cols_num = df.select_dtypes(include=["number"]).columns.tolist()
    col_sel = elegir_columnas_por_numero(cols_num, "Elige UNA columna numérica", permitir_multiples=False)
    if not col_sel:
        pausar()
        return

    col = col_sel[0]
    serie = df[col].dropna()

    print(f"📊 Resumen numérico para '{col}':")
    print(serie.describe().round(2))

    print("\nGenerando histograma y boxplot...")
    sns.set(style="whitegrid")

    plt.figure(figsize=(10, 4))

    plt.subplot(1, 2, 1)
    sns.histplot(serie, kde=True)
    plt.title(f"Histograma de {col}")

    plt.subplot(1, 2, 2)
    sns.boxplot(x=serie)
    plt.title(f"Boxplot de {col}")

    plt.tight_layout()
    plt.show()
    resumen = serie.describe().round(2).to_frame(name=col)

    #guardar el resumen numérico en un archivo Excel o CSV
    guardar_tabla(resumen, f"resumen_univar_{col}")
    pausar()
    

def distribucion_categorica(df: pd.DataFrame):
    mostrar_explicacion("distrib_cat")   # <<--- NUEVO
    cols_cat = df.select_dtypes(include=["object", "string", "category"]).columns.tolist()
    col_sel = elegir_columnas_por_numero(cols_cat, "Elige UNA columna categórica", permitir_multiples=False)
    if not col_sel:
        pausar()
        return

    col = col_sel[0]
    serie = df[col].astype("category")

    print(f"📊 Frecuencias para '{col}':")
    print(serie.value_counts(dropna=False))

    print("\nGenerando gráfico de barras...")
    plt.figure(figsize=(8, 4))
    serie.value_counts(dropna=False).plot(kind="bar")
    plt.title(f"Frecuencias de {col}")
    plt.xlabel(col)
    plt.ylabel("Conteo")
    plt.tight_layout()
    plt.show()
    pausar()


# ==========================
# MÓDULO 4: RELACIONES ENTRE VARIABLES
# ==========================

def menu_relaciones(df: pd.DataFrame):
    while True:
        limpiar_pantalla()
        print("=== RELACIONES ENTRE VARIABLES ===")
        print("1) Numérica vs numérica --> scatterplot + correlación")
        print("2) Categórica vs numérica --> boxplot + promedio por categoría")
        print("3) Categórica vs categórica --> crosstab + heatmap")
        print("0) Volver al menú principal")

        op = input("\nElige una opción: ").strip()
        limpiar_pantalla()

        if op == "1":
            relacion_num_vs_num(df)
        elif op == "2":
            relacion_cat_vs_num(df)
        elif op == "3":
            relacion_cat_vs_cat(df)
        elif op == "0":
            break
        else:
            print("Opción inválida.")
            pausar()


def relacion_num_vs_num(df: pd.DataFrame):
    mostrar_explicacion("corr_num")   # <<--- NUEVO
    cols_num = df.select_dtypes(include=["number"]).columns.tolist()
    if len(cols_num) < 2:
        print("Se necesitan al menos 2 columnas numéricas.")
        pausar()
        return

    print("Elige la variable en el eje X:")
    col_x = elegir_columnas_por_numero(cols_num, "Columna X", permitir_multiples=False)
    if not col_x:
        pausar()
        return

    print("\nElige la variable en el eje Y:")
    col_y = elegir_columnas_por_numero(cols_num, "Columna Y", permitir_multiples=False)
    if not col_y:
        pausar()
        return

    x, y = col_x[0], col_y[0]
    print(f"Correlación entre {x} y {y}:")
    print(df[[x, y]].corr().round(3))

    print("\nGenerando scatterplot...")
    plt.figure(figsize=(6, 5))
    sns.scatterplot(data=df, x=x, y=y)
    plt.title(f"{y} vs {x}")
    plt.tight_layout()
    plt.show()
    pausar()


def relacion_cat_vs_num(df: pd.DataFrame):
    mostrar_explicacion("rel_cat_num")   # <<--- NUEVO
    cols_cat = df.select_dtypes(include=["object", "string", "category"]).columns.tolist()
    cols_num = df.select_dtypes(include=["number"]).columns.tolist()

    if not cols_cat or not cols_num:
        print("Se necesita al menos una columna categórica y una numérica.")
        pausar()
        return

    print("Elige la columna CATEGÓRICA:")
    col_cat = elegir_columnas_por_numero(cols_cat, "Categórica", permitir_multiples=False)
    if not col_cat:
        pausar()
        return

    print("\nElige la columna NUMÉRICA:")
    col_num = elegir_columnas_por_numero(cols_num, "Numérica", permitir_multiples=False)
    if not col_num:
        pausar()
        return

    c, n = col_cat[0], col_num[0]

    print(f"Promedio de '{n}' por categoría de '{c}':")
    tabla = df.groupby(c)[n].mean().round(2)
    print(tabla)

    # NUEVO: ofrecer guardar esa tabla
    guardar_tabla(tabla.to_frame(name=f"mean_{n}"), f"mean_{n}_por_{c}")

    print("\nGenerando boxplot...")
    plt.figure(figsize=(8, 5))
    sns.boxplot(data=df, x=c, y=n)
    plt.title(f"{n} por {c}")
    plt.tight_layout()
    plt.show()
    pausar()


def relacion_cat_vs_cat(df: pd.DataFrame):
    mostrar_explicacion("rel_cat_cat")   # <<--- NUEVO
    cols_cat = df.select_dtypes(include=["object", "string", "category"]).columns.tolist()
    if len(cols_cat) < 2:
        print("Se necesitan al menos 2 columnas categóricas.")
        pausar()
        return

    print("Elige la PRIMERA columna categórica:")
    col1 = elegir_columnas_por_numero(cols_cat, "Primera categórica", permitir_multiples=False)
    if not col1:
        pausar()
        return

    print("\nElige la SEGUNDA columna categórica:")
    col2 = elegir_columnas_por_numero(cols_cat, "Segunda categórica", permitir_multiples=False)
    if not col2:
        pausar()
        return

    c1, c2 = col1[0], col2[0]
    tabla = pd.crosstab(df[c1], df[c2])
    print(f"Tabla de contingencia entre {c1} y {c2}:")
    print(tabla)

    print("\nGenerando heatmap...")
    plt.figure(figsize=(8, 6))
    sns.heatmap(tabla, annot=False, cmap="Blues")
    plt.title(f"Heatmap: {c1} vs {c2}")
    plt.tight_layout()
    plt.show()
    pausar()


# ==========================
# MÓDULO 5: GRÁFICOS AUTOMÁTICOS
# ==========================

def menu_graficos_automaticos(df: pd.DataFrame):
    limpiar_pantalla()
    print("=== GRÁFICOS AUTOMÁTICOS ===")
    print("Esto generará algunos gráficos básicos para revisar el dataset.")

    cols_num = df.select_dtypes(include=["number"]).columns.tolist()
    cols_cat = df.select_dtypes(include=["object", "string", "category"]).columns.tolist()

    # Histograma para cada numérica (máx 4)
    mostrar_explicacion("histograma")   # <<--- NUEVO
    for col in cols_num[:4]:
        print(f"\nHistograma para '{col}'")
        plt.figure(figsize=(6, 4))
        sns.histplot(df[col].dropna(), kde=True)
        plt.title(f"Histograma de {col}")
        plt.tight_layout()
        plt.show()

    # Barras para cada categórica (máx 4)
    mostrar_explicacion("frecuencias")   # <<--- NUEVO
    for col in cols_cat[:4]:
        print(f"\nGráfico de barras para '{col}' (top 10 categorías)")
        plt.figure(figsize=(8, 4))
        df[col].value_counts(dropna=False).head(10).plot(kind="bar")
        plt.title(f"Frecuencias de {col}")
        plt.tight_layout()
        plt.show()

    pausar()


# ==========================
# MENÚ PRINCIPAL
# ==========================

def mostrar_menu_principal():
    print("=== MENÚ PRINCIPAL - ANÁLISIS DE DATOS ===")
    print("1) Visión general")
    print("2) Calidad de datos")
    print("3) Distribuciones (univariado)")
    print("4) Relaciones entre variables")
    print("5) Gráficos automáticos")
    print("6) Modo reporte (varios análisis a Excel)")
    print("0) Salir")


def main():
    df = cargar_dataframe()
    if df is None:
        return

    while True:
        limpiar_pantalla()
        mostrar_menu_principal()
        op = input("\nElige una opción: ").strip()
        limpiar_pantalla()

        if op == "1":
            menu_vision_general(df)
        elif op == "2":
            menu_calidad_datos(df)
        elif op == "3":
            menu_distribuciones(df)
        elif op == "4":
            menu_relaciones(df)
        elif op == "5":
            menu_graficos_automaticos(df)
        elif op == "6":
            modo_reporte(df)
        elif op == "0":
            print("Saliendo...")
            break
        else:
            print("Opción inválida.")
            pausar()


if __name__ == "__main__":
    main()