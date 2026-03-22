import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os
import plotly.express as px


load_dotenv()

# Conexión
host=os.getenv('DB_HOST')
user=os.getenv('DB_USER')
password=os.getenv('DB_PASSWORD')
database=os.getenv('DB_NAME')
engine = create_engine(f"mysql+pymysql://{user}:{password}@{host}/{database}")
#)
def mostrar_grafica(fig, titulo):
    print(f"\n📊 {titulo}")
    opcion = input("¿Deseas ver la gráfica? (1=Sí / Enter=Omitir): ").strip()
    if opcion == '1':
        fig.show()

# Consulta SQL
# Empleados por departamento
query = """SELECT d.nombre AS departamento, COUNT(e.id_empleado) AS cantidad_empleados
FROM empleados e
JOIN departamentos d ON e.id_departamento = d.id_departamento
GROUP BY d.nombre"""
df_departamentos = pd.read_sql(query, engine)
print("Cantidad de empleados por departamento:")
# Calcular totales
total_empleados = df_departamentos['cantidad_empleados'].sum()
# Crear fila total
fila_total = pd.DataFrame({
    'departamento': ['TOTAL'],
    'cantidad_empleados': [total_empleados]    
})
# Agregar al DataFrame original
df_departamentos = pd.concat([df_departamentos, fila_total], ignore_index=True)
print(df_departamentos)
print("\n")
# Salarios promedio por departamento
query = """SELECT d.nombre AS departamento, AVG(e.salario_mensual) AS salario_promedio 
FROM empleados e
JOIN departamentos d ON e.id_departamento = d.id_departamento
GROUP BY d.nombre"""
df_salarios = pd.read_sql(query, engine)
print("Salarios promedio por departamento:")
print(df_salarios)
print("\n")
# Cuantos empleados renunciaron por departamento
query = """SELECT d.nombre AS departamento, COUNT(e.id_empleado) AS cantidad_renuncias
FROM empleados e
JOIN departamentos d ON e.id_departamento = d.id_departamento
WHERE e.rotacion = 'Yes'
GROUP BY d.nombre"""
df_renuncias = pd.read_sql(query, engine)
print("Cantidad de renuncias por departamento:")
# Calcular totales
total_renuncias = df_renuncias['cantidad_renuncias'].sum()
# Crear fila total
fila_total = pd.DataFrame({
    'departamento': ['TOTAL'],
    'cantidad_renuncias': [total_renuncias]    
})
# Agregar al DataFrame original
df_renuncias = pd.concat([df_renuncias, fila_total], ignore_index=True)
print(df_renuncias)
print("\n")

# Porcentaje de rotacion por departamento
query = """SELECT d.nombre AS departamento, SUM(CASE WHEN e.rotacion = 'Yes' THEN 1 ELSE 0 END) AS cantidad_renuncias,
    COUNT(e.id_empleado) AS total_empleados,
    (SUM(CASE WHEN e.rotacion = 'Yes' THEN 1 ELSE 0 END) / COUNT(e.id_empleado)) * 100 AS rotacion_porcentaje
FROM empleados e
JOIN departamentos d ON e.id_departamento = d.id_departamento
GROUP BY d.nombre;
"""
df_rotacion = pd.read_sql(query, engine)
print("Porcentaje de rotación por departamento:")
# Calcular totales
total_renuncias = df_rotacion['cantidad_renuncias'].sum()
total_empleados = df_rotacion['total_empleados'].sum()
total_porcentaje = (total_renuncias / total_empleados) * 100

# Crear fila total
fila_total = pd.DataFrame({
    'departamento': ['TOTAL'],
    'cantidad_renuncias': [total_renuncias],
    'total_empleados': [total_empleados],
    'rotacion_porcentaje': [total_porcentaje]
})
# Agregar al DataFrame original
df_rotacion = pd.concat([df_rotacion, fila_total], ignore_index=True)
print(df_rotacion)
print("\n")
    # visualizacion del porcentaje de rotacion por departamento
df_rotacion = df_rotacion.sort_values(by="rotacion_porcentaje", ascending=False)
fig0 = px.bar(df_rotacion,
    x="rotacion_porcentaje",
    y="departamento",
    orientation="h",
    color="rotacion_porcentaje",
    color_continuous_scale="Reds",
    labels={"rotacion_porcentaje": "Porcentaje de Rotación (%)",
        "departamento": "Departamento"
    },
    title="Porcentaje de Rotación por Departamento")
# Etiquetas al final de cada barra
fig0.update_traces(
    text=df_rotacion["rotacion_porcentaje"].round(2).astype(str) + "%",
    textposition="outside")
# Ajustes visuales
fig0.update_layout(
    xaxis_title="Porcentaje de Rotación (%)",
    yaxis_title="Departamento",
    coloraxis_colorbar_title="Rotación (%)",
    margin=dict(l=80, r=40, t=60, b=40))
mostrar_grafica(fig0, "Porcentaje de Rotación por Departamento")
    # fin visualizacion del porcentaje de rotacion por departamento

# Rotacion por genero
query = """SELECT d.nombre AS departamento, e.genero, SUM(CASE WHEN e.rotacion = 'Yes' THEN 1 ELSE 0 END) AS cantidad_renuncias,
    COUNT(e.id_empleado) AS total_empleados,
    (SUM(CASE WHEN e.rotacion = 'Yes' THEN 1 ELSE 0 END) / COUNT(e.id_empleado)) * 100 AS rotacion_porcentaje
FROM empleados e
JOIN departamentos d ON e.id_departamento = d.id_departamento
GROUP BY d.nombre, e.genero;
"""
df_rotacion_genero = pd.read_sql(query, engine)
print("Porcentaje de rotación por departamento y género:")
print(df_rotacion_genero)
print("\n")

# Rotacion solo por genero
query = """SELECT e.genero, SUM(CASE WHEN e.rotacion = 'Yes' THEN 1 ELSE 0 END) AS cantidad_renuncias,
    COUNT(e.id_empleado) AS total_empleados,
    (SUM(CASE WHEN e.rotacion = 'Yes' THEN 1 ELSE 0 END) / COUNT(e.id_empleado)) * 100 AS rotacion_porcentaje
FROM empleados e
GROUP BY e.genero;
"""
df_rotacion_genero = pd.read_sql(query, engine)
print("Porcentaje de rotación solo por género:")
print(df_rotacion_genero)
print("\n")

# Salario promedio por rotacion los empleados que renunciaron vs los que no renunciaron
query = """SELECT e.rotacion as rotacion, AVG(e.salario_mensual) AS salario_promedio
FROM empleados e
GROUP BY e.rotacion;
"""
df_salario_rotacion = pd.read_sql(query, engine)
print("Salario promedio por rotación:")
print(df_salario_rotacion)
print("\n")
# Salario promedio por rotacion los empleados que renunciaron vs los que no renunciaron
query = """
SELECT 
    e.rotacion AS rotacion, 
    AVG(e.salario_mensual) AS salario_promedio
FROM empleados e
GROUP BY e.rotacion;
"""
df_salario_rotacion = pd.read_sql(query, engine)
print("Salario promedio por rotación:")
print(df_salario_rotacion)
print("\n")

# Ordenar (opcional)
df_salario_rotacion = df_salario_rotacion.sort_values(by="rotacion")

# Visualización
fig1 = px.bar(
    df_salario_rotacion,
    x="rotacion",
    y="salario_promedio",
    #orientation="v",
    color="rotacion",
    color_discrete_sequence=["#d62728", "#1f77b4"],  # rojo y azul
    labels={
        "rotacion": "Rotación (Yes/No)",
        "salario_promedio": "Salario Promedio"
    },
    title="Salario Promedio por Rotación",
    text="salario_promedio"
)

# Etiquetas encima de cada barra
fig1.update_traces(
    texttemplate='$%{text:,.0f}',
    textposition="outside"
)

# Ajustes visuales
fig1.update_layout(
    xaxis_title="Rotación (Yes/No)",
    yaxis_title="Salario Promedio",
    margin=dict(l=80, r=40, t=60, b=40)
)
mostrar_grafica(fig1, "Salario Promedio por Rotación")
    # fin visualizacion de salario promedio por rotacion los empleados que renunciaron vs los que no renunciaron

# Rotacion por horas extras
query = """SELECT e.horas_extra, SUM(CASE WHEN e.rotacion = 'Yes' THEN 1 ELSE 0 END) AS cantidad_renuncias,
    COUNT(e.id_empleado) AS total_empleados,
    ROUND(100.0 * SUM(CASE WHEN e.rotacion = 'Yes' THEN 1 ELSE 0 END) / COUNT(e.id_empleado), 2) AS porcentaje_rotacion
FROM empleados e
GROUP BY e.horas_extra
ORDER BY e.horas_extra;
"""
df_rotacion_horas = pd.read_sql(query, engine)
print("Rotación por horas extras:")
print(df_rotacion_horas)
print("\n")
    # visualización de rotación por horas extras
fig2 = px.bar(
    df_rotacion_horas,
    x="horas_extra",
    y="porcentaje_rotacion",
    color="horas_extra",
    color_discrete_sequence=["#ff7f0e"],  # naranja
    labels={
        "horas_extra": "Horas Extra",
        "porcentaje_rotacion": "Porcentaje de Rotación"
    },
    title="Rotación por Horas Extras",
    text="porcentaje_rotacion"
)
# Etiquetas encima de cada barra
fig2.update_traces(
    texttemplate='%{text:.2f}%',
    textposition="outside"
)
# Ajustes visuales
fig2.update_layout(
    xaxis_title="Horas Extra",
    yaxis_title="Porcentaje de Rotación",
    margin=dict(l=80, r=40, t=60, b=40)
)
mostrar_grafica(fig2, "Rotación por Horas Extras")
# fin visualización de rotación por horas extras
# fin de rotacion por horas extras


# Rotacion por años en la empresa 
# ----- leido directamente del csv para hacer el corte por años, 
# ya que no se tiene esa columna en la base de datos
df_rotacion_anos = pd.read_csv('entrada/rrhh_s.csv')
df_rotacion_anos['RangoAños'] = pd.cut(df_rotacion_anos['YearsAtCompany'], 
                          bins=[0, 2, 5, 10, 40],
                          labels=['0-2 años', '3-5 años', '6-10 años', '10+ años'])

rotacion_años = df_rotacion_anos.groupby('RangoAños', observed=True).agg(
    total=('Attrition', 'count'),
    renuncias=('Attrition', lambda x: (x=='Yes').sum()),
    salario_promedio=('MonthlyIncome', 'mean')
).reset_index()
rotacion_años['porcentaje'] = (rotacion_años['renuncias'] / rotacion_años['total'] * 100).round(2)
rotacion_años['salario_promedio'] = rotacion_años['salario_promedio'].round(2)
print(rotacion_años)
    # visualización de rotación por años en la empresa
    # grafico de barras eje x = RangoAños, eje y = porcentaje, color = porcentaje (escala de colores) 
    # y agregar linea con salario_promedio en eje secondario
fig3 = px.bar(rotacion_años, x='RangoAños', y='porcentaje', color='porcentaje',
             color_continuous_scale='Blues', labels={'porcentaje': 'Porcentaje de Rotación', 'RangoAños': 'Años en la Empresa'},
             title='Rotación por Años en la Empresa')
fig3.update_traces(texttemplate='%{y:.2f}%', textposition='outside')
fig3.update_layout(yaxis_title='Porcentaje de Rotación', xaxis_title='Años en la Empresa', margin=dict(l=80, r=40, t=60, b=40))
fig3.add_scatter(x=rotacion_años['RangoAños'], y=rotacion_años['salario_promedio'], mode='lines+markers', name='Salario Promedio', yaxis='y2')
fig3.update_layout(yaxis2=dict(title='Salario Promedio', overlaying='y', side='right'))
mostrar_grafica(fig3, "Rotación por Años en la Empresa")
    # fin de visualización de rotación por años en la empresa

# fin de rotacion por años en la empresa

# Rotacion por nivel de cargo
query_nivel = """
    SELECT c.nivel,
           COUNT(*) as total_empleados,
           SUM(CASE WHEN e.rotacion = 'Yes' THEN 1 ELSE 0 END) as renuncias,
           ROUND(AVG(e.salario_mensual), 2) as salario_promedio,
           ROUND(SUM(CASE WHEN e.rotacion = 'Yes' THEN 1 ELSE 0 END) / COUNT(*) * 100, 2) as porcentaje_rotacion
    FROM empleados e
    JOIN cargos c ON e.id_cargo = c.id_cargo
    GROUP BY c.nivel
    ORDER BY c.nivel
"""
df_nivel = pd.read_sql(query_nivel, engine)
print("\nRotación por nivel de cargo:")
print(df_nivel)
print("\n")
    # visualización de rotación por nivel de cargo
    # Barras horizontales, Eje X → porcentaje_rotacion, Eje Y → nivel (1, 2, 3, 4), Color → porcentaje_rotacion (escala de rojo)
    # Agregar texto con salario_promedio en cada barra
fig4 = px.bar(df_nivel, x='porcentaje_rotacion', y='nivel', color='porcentaje_rotacion', orientation='h',
             color_continuous_scale='Reds', labels={'porcentaje_rotacion': 'Porcentaje de Rotación', 'nivel': 'Nivel de Cargo'},
             title='Rotación por Nivel de Cargo')
fig4.update_traces(texttemplate='%{x:.2f}%', textposition='outside')
fig4.update_layout(xaxis_title='Porcentaje de Rotación', yaxis_title='Nivel de Cargo', margin=dict(l=80, r=40, t=60, b=40))
mostrar_grafica(fig4, "Rotación por Nivel de Cargo")
print("VER GRAFICO---->")
print("\n")
    # fin visualización de rotación por nivel de cargo
# fin de rotacion por nivel de cargo

# analisis de satisfaccion laboral - 6 campos acumulados por valor (1-4) y clasificado por rotación
query_satisfaccion = """SELECT 
    e.rotacion,
    'satisfaccion_trabajo' AS item,
    s.satisfaccion_trabajo AS valor
FROM empleados e
JOIN satisfaccion s ON e.id_empleado = s.id_empleado

UNION ALL

SELECT 
    e.rotacion,
    'satisfaccion_ambiente' AS item,
    s.satisfaccion_ambiente AS valor
FROM empleados e
JOIN satisfaccion s ON e.id_empleado = s.id_empleado

UNION ALL

SELECT 
    e.rotacion,
    'satisfaccion_relacion' AS item,
    s.satisfaccion_relacion AS valor
FROM empleados e
JOIN satisfaccion s ON e.id_empleado = s.id_empleado

UNION ALL

SELECT 
    e.rotacion,
    'balance_vida' AS item,
    s.balance_vida AS valor
FROM empleados e
JOIN satisfaccion s ON e.id_empleado = s.id_empleado

UNION ALL

SELECT 
    e.rotacion,
    'involucramiento' AS item,
    s.involucramiento AS valor
FROM empleados e
JOIN satisfaccion s ON e.id_empleado = s.id_empleado;
"""
df = pd.read_sql(query_satisfaccion, engine)

tabla = df.pivot_table(
    index=['item', 'rotacion'],   # filas = item + rotación
    columns='valor',              # columnas = valores 1–5
    aggfunc='size',
    fill_value=0
)
print("Tabla de satisfacción laboral:")
print(tabla)
print("\n")

