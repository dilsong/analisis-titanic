import pandas as pd
import numpy as np
from faker import Faker
import random

fake = Faker('es_MX')
random.seed(42)

# Datos base
tiendas = ['T001', 'T002', 'T003', 'T004', 'T005']
categorias = ['Electrónica', 'Ropa', 'Alimentos', 'Hogar', 'Deportes']
vendedores = ['Ana García', 'Luis Pérez', 'María López', 
              'Carlos Ruiz', 'Sofia Torres']
regiones = ['Norte', 'Sur', 'Este', 'Oeste', 'Centro']

registros = []
for i in range(500):
    # Introducimos errores intencionales
    tienda = random.choice(tiendas)
    
    # Error 1: nombres de categoría inconsistentes
    categoria = random.choice([
        'Electrónica', 'electronica', 'ELECTRONICA',
        'Ropa', 'ROPA', 'ropa',
        'Alimentos', 'alimentos', 'ALIMENTOS',
        'Hogar', 'HOGAR', 'hogar',
        'Deportes', 'deportes', 'DEPORTES'
    ])
    
    # Error 2: vendedores con nombres inconsistentes
    vendedor = random.choice([
        'Ana García', 'ANA GARCIA', 'ana garcia',
        'Luis Pérez', 'LUIS PEREZ', 'luis perez',
        'María López', 'MARIA LOPEZ', 'maria lopez',
        'Carlos Ruiz', 'CARLOS RUIZ', 'carlos ruiz',
        'Sofia Torres', 'SOFIA TORRES', 'sofia torres'
    ])
    
    # Error 3: algunos precios con texto
    precio_base = random.uniform(10, 1000)
    if random.random() < 0.05:
        precio = f"${precio_base:.2f}"  # precio con símbolo
    elif random.random() < 0.05:
        precio = f"{precio_base:.2f} USD"  # precio con texto
    else:
        precio = round(precio_base, 2)
    
    # Error 4: cantidades con decimales o negativos
    cantidad = random.randint(1, 20)
    if random.random() < 0.05:
        cantidad = round(random.uniform(1, 20), 2)  # decimal
    elif random.random() < 0.03:
        cantidad = -random.randint(1, 5)  # negativo
    
    # Error 5: fechas inconsistentes
    fecha = fake.date_between(start_date='-2y', end_date='today')
    if random.random() < 0.05:
        fecha = fecha.strftime('%d/%m/%Y')  # formato diferente
    elif random.random() < 0.05:
        fecha = 'N/A'  # fecha inválida
    
    # Error 6: registros duplicados intencionales
    registros.append({
        'ID_Venta': f'V{i+1:04d}',
        'Fecha': fecha,
        'Tienda': tienda,
        'Region': random.choice(regiones),
        'Categoria': categoria,
        'Vendedor': vendedor,
        'Cantidad': cantidad,
        'Precio_Unitario': precio,
        'Cliente_ID': f'C{random.randint(1,100):03d}'
    })
    
    # Duplicar algunos registros
    if random.random() < 0.05:
        registros.append(registros[-1].copy())

df = pd.DataFrame(registros)

# Error 7: algunos campos nulos
df.loc[random.sample(range(len(df)), 20), 'Vendedor'] = np.nan
df.loc[random.sample(range(len(df)), 15), 'Region'] = np.nan
df.loc[random.sample(range(len(df)), 10), 'Cliente_ID'] = np.nan

df.to_csv('ventas_sucias.csv', index=False)
print(f"✅ Dataset generado con {len(df)} registros")
print(f"Columnas: {df.columns.tolist()}")
print(f"\nMuestra de errores introducidos:")
print(df.head(10).to_string())