import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

load_dotenv()

# Conexión
user = os.getenv('DB_USER')
password = os.getenv('DB_PASSWORD')
host = os.getenv('DB_HOST')
engine = create_engine(f'mysql+pymysql://{user}:{password}@{host}/rrhh_analytics')

# Cargar dataset
df = pd.read_csv('entrada/rrhh_s.csv')
print(f"Dataset cargado: {df.shape}")

# Tabla 1 - Departamentos
departamentos = df[['Department']].drop_duplicates().reset_index(drop=True)
departamentos.index += 1
departamentos.columns = ['nombre']
departamentos.index.name = 'id_departamento'
departamentos.to_sql('departamentos', engine, if_exists='append', index=True)
print(f"✅ Departamentos cargados: {len(departamentos)}")

# Tabla 2 - Cargos
cargos = df[['JobRole', 'JobLevel']].drop_duplicates().reset_index(drop=True)
cargos.index += 1
cargos.columns = ['nombre', 'nivel']
cargos.index.name = 'id_cargo'
cargos.to_sql('cargos', engine, if_exists='append', index=True)
print(f"✅ Cargos cargados: {len(cargos)}")

# Mapeos
dep_map = {v: k for k, v in departamentos['nombre'].items()}
cargo_map = {v: k for k, v in cargos['nombre'].items()}

# Tabla 3 - Empleados
empleados = pd.DataFrame({
    'id_empleado':      df['EmployeeNumber'],
    'edad':             df['Age'],
    'genero':           df['Gender'],
    'estado_civil':     df['MaritalStatus'],
    'educacion':        df['Education'],
    'campo_educacion':  df['EducationField'],
    'id_departamento':  df['Department'].map(dep_map),
    'id_cargo':         df['JobRole'].map(cargo_map),
    'salario_mensual':  df['MonthlyIncome'],
    'horas_extra':      df['OverTime'],
    'viaje_negocios':   df['BusinessTravel'],
    'rotacion':         df['Attrition']
})
empleados.to_sql('empleados', engine, if_exists='append', index=False)
print(f"✅ Empleados cargados: {len(empleados)}")

# Tabla 4 - Satisfaccion
satisfaccion = pd.DataFrame({
    'id_empleado':          df['EmployeeNumber'],
    'satisfaccion_trabajo': df['JobSatisfaction'],
    'satisfaccion_ambiente':df['EnvironmentSatisfaction'],
    'satisfaccion_relacion':df['RelationshipSatisfaction'],
    'balance_vida':         df['WorkLifeBalance'],
    'involucramiento':      df['JobInvolvement'],
    'calificacion_desempeño':df['PerformanceRating']
})
satisfaccion.to_sql('satisfaccion', engine, if_exists='append', index=False)
print(f"✅ Satisfacción cargada: {len(satisfaccion)}")

print("\n🎉 Base de datos rrhh_analytics cargada exitosamente!")