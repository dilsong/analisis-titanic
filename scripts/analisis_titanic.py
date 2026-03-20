import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from datetime import datetime

def load_data(file_path):

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"El archivo {file_path} no existe.")
    
    try:
        data = pd.read_excel(file_path)
        return data
    except Exception as e:
        print(f"Error al cargar el archivo: {e}")
        return None

# Crear columna CategoriaEdad      → Menor, 18-29, 30-44, 45-59, 60+
def categorize_age(age):
    try:
        age = float(age)
    except:
        return 'DESCONOCIDO'
    
    if age < 18:
        return 'Menor'
    elif 18 <= age <= 29:
        return '18-29'
    elif 30 <= age <= 44:
        return '30-44'
    elif 45 <= age <= 59:
        return '45-59'
    else:
        return '60+'

# Paso 3 - Grupos familiares por ticket
# Agrupar por Ticket y calcular: 
# ItemsVivos   = suma de Survived por ticket
# ItemsMuertos = total por ticket - ItemsVivos
# ItemsTotales = total de personas por ticket
def graficar_dashboard(df, grupos):
    
    # Gráfica 1 - Survived por Pclass
    df['Survived'] = pd.to_numeric(df['Survived'], errors='coerce')
    g1 = df.groupby('Pclass')['Survived'].sum().reset_index()
    fig1 = px.bar(g1, x='Pclass', y='Survived',
                 title='Sobrevivientes por Clase',
                 color='Pclass', text='Survived')
    fig1.show()

    # Gráfica 2 - Survived por Sex
    g2 = df.groupby('Sex')['Survived'].sum().reset_index()
    fig2 = px.bar(g2, x='Sex', y='Survived',
                 title='Sobrevivientes por Sexo',
                 color='Sex', text='Survived')
    fig2.show()

    # Gráfica 3 - Survived por CategoriaEdad y Sex
    g3 = df.groupby(['CategoriaEdad', 'Sex'])['Survived'].sum().reset_index()
    orden = ['Menor', '18-29', '30-44', '45-59', '60+']
    fig3 = px.bar(g3, x='CategoriaEdad', y='Survived',
                 color='Sex', barmode='group',
                 title='Sobrevivientes por Edad y Sexo',
                 category_orders={'CategoriaEdad': orden},
                 text='Survived')
    fig3.show()

    # Gráfica 4 - EstadoTicket torta
    g4 = grupos['EstadoTicket'].value_counts().reset_index()
    g4.columns = ['EstadoTicket', 'Cantidad']
    fig4 = px.pie(g4, values='Cantidad', names='EstadoTicket',
                 title='Estado por Grupo Familiar',
                 color_discrete_map={'Vivos':'blue','Muertos':'darkblue','Parcial':'orange'})
    fig4.show()

    # Gráfica 5 - ItemsVivos vs ItemsMuertos por ItemsTotales
    grupos_reset = grupos.reset_index()
    g5 = grupos_reset.groupby('ItemsTotales')[['ItemsVivos','ItemsMuertos']].sum().reset_index()
    fig5 = px.bar(g5, x='ItemsTotales', y=['ItemsVivos','ItemsMuertos'],
                 title='Vivos vs Muertos por Tamaño de Grupo Familiar',
                 barmode='group',
                 labels={'value':'Personas', 'ItemsTotales':'Personas por Ticket'})
    fig5.show()
def main():
    file_path = 'entrada/train_ok.xlsx'
    titanic_data = load_data(file_path)
    if titanic_data is not None:
        print("Datos cargados exitosamente.")
        # Crear columna CategoriaEdad
        titanic_data['CategoriaEdad'] = titanic_data['Age'].apply(categorize_age)
        print(titanic_data['CategoriaEdad'].value_counts())
    
        # Grupos familiares por ticket
        # Convertir Survived a numérico (1 para vivos, 0 para muertos)
        titanic_data['Survived'] = pd.to_numeric(titanic_data['Survived'], errors='coerce').fillna(0).astype(int)
        
        # Agrupar por Ticket y calcular métricas
        grouped = titanic_data.groupby('Ticket').agg(
            ItemsVivos=('Survived', 'sum'),
            ItemsTotales=('Survived', 'count')
        )
        grouped['ItemsMuertos'] = grouped['ItemsTotales'] - grouped['ItemsVivos']
        def estado_ticket(row):
                if row['ItemsVivos'] == 0:
                    return 'Muertos'
                elif row['ItemsMuertos'] == 0:
                    return 'Vivos'
                else:
                    return 'Parcial'

        grouped['EstadoTicket'] = grouped.apply(estado_ticket, axis=1)
        print(grouped['EstadoTicket'].value_counts())
        print("Grupos familiares por ticket:")
        print(grouped)
    graficar_dashboard(titanic_data, grouped)
if __name__ == "__main__":
    main()