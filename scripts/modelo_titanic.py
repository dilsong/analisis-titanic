import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
import os

def cargar_datos():
    train = pd.read_excel('Entrada/train_ok.xlsx')
    test = pd.read_csv('Entrada/test.csv')
    return train, test

def preparar_datos(df):
    # Convertir Sex a numérico
    df['Sex'] = df['Sex'].map({'male': 0, 'female': 1})
    
    # Convertir Age a numérico
    df['Age'] = pd.to_numeric(df['Age'], errors='coerce')
    df['Age'] = df['Age'].fillna(df['Age'].median())
    
    # Convertir Survived a numérico si existe
    if 'Survived' in df.columns:
        df['Survived'] = pd.to_numeric(df['Survived'], errors='coerce')
    
    return df

def main():
    print("=== MODELO PREDICTIVO TITANIC ===")
    
    # Cargar datos
    train, test = cargar_datos()
    print(f"Train: {train.shape} | Test: {test.shape}")
    
    # Preparar datos
    def preparar_datos(df):
    # Convertir Sex a numérico
        df['Sex'] = df['Sex'].map({'male': 0, 'female': 1})
        
        # Convertir Age a numérico
        df['Age'] = pd.to_numeric(df['Age'], errors='coerce')
        df['Age'] = df['Age'].fillna(df['Age'].median())
    
        # Crear CategoriaEdad
        def categorize_age(age):
            if age < 18:   return 0  # Menor
            elif age <= 29: return 1  # 18-29
            elif age <= 44: return 2  # 30-44
            elif age <= 59: return 3  # 45-59
            else:           return 4  # 60+
        df['CategoriaEdad'] = df['Age'].apply(categorize_age)
                    
                    # Crear tamaño de grupo familiar
        df['TamanoFamilia'] = df['SibSp'] + df['Parch'] + 1
                    
                    # Clasificar si viajaba solo o acompañado
        df['ViajaSolo'] = (df['TamanoFamilia'] == 1).astype(int)
                    
                    # Convertir Embarked a numérico
        df['Embarked'] = df['Embarked'].map({'S': 0, 'C': 1, 'Q': 2})
        df['Embarked'] = df['Embarked'].fillna(0)
    
        # Convertir Survived a numérico si existe
        if 'Survived' in df.columns:
            df['Survived'] = pd.to_numeric(df['Survived'], errors='coerce')
        
        return df
    train = preparar_datos(train)
    test = preparar_datos(test)
    # Verificar columnas creadas
    print(f"Columnas train: {train.columns.tolist()}")
    # Seleccionar características
    features = ['Pclass', 'Sex', 'Age', 'Fare', 
            'SibSp', 'Parch', 'CategoriaEdad', 
            'TamanoFamilia', 'ViajaSolo', 'Embarked']
    
    X_train = train[features]
    y_train = train['Survived']
    X_test = test[features]
    
    # Llenar nulos en test
    X_test = X_test.fillna(X_test.median())
    
    # Entrenar modelo
    print("\nEntrenando modelo...")
    modelo = LogisticRegression(max_iter=1000)
    modelo.fit(X_train, y_train)
    
    # Precisión en train
    precision = accuracy_score(y_train, modelo.predict(X_train))
    print(f"Precisión del modelo: {precision*100:.1f}%")
    
    # Predecir test
    predicciones = modelo.predict(X_test)
    
    # Crear submission
    submission = pd.DataFrame({
        'PassengerId': test['PassengerId'],
        'Survived': predicciones
    })
    
    if not os.path.exists('Salida'):
        os.makedirs('Salida')
    
    submission.to_csv('Salida/submission.csv', index=False)
    print(f"\n✅ submission.csv generado con {len(submission)} predicciones")
    print(submission.head(10))

if __name__ == "__main__":
    main()