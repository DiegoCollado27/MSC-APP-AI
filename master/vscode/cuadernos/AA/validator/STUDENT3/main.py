
    
    
    
import argparse
import numpy as np
import pandas as pd
import sys
import pickle
import warnings
warnings.filterwarnings('ignore')

def llenar_plan(row):
    if pd.isna(row['Plan']):
        if row['FechaConstruccion'] < 1946:
            return 'Nuevo'
        else:
            return 'Antiguo'
    else:
        return row['Plan']
def predict (input, modelo_cargado, modelodata_cargado, df_encoded):
    """
    Generates the prediction.
    In this case, it generates a random price.

    @param input: the input dataframe.
    @return a dataframe with two columns: ID and price.
    """
 
        
    datos = input
    # imputacion de datos
    
    datos['Plan'] = datos.apply(llenar_plan, axis=1) 
    datos['multiplo_medio'] = datos['Superficie'] / datos['PerimParcela']
    multiplo_medio = datos['multiplo_medio'].mean()
    valores_faltantes = datos['PerimParcela'].isna()
    datos.loc[valores_faltantes, 'PerimParcela'] = datos.loc[valores_faltantes, 'Superficie'] / multiplo_medio
    datos.drop(['multiplo_medio'], axis=1, inplace= True)
    
    # Hacer dummies
    
    columnas_no_numericas = datos.select_dtypes(exclude=[int, float]).columns
    df = pd.get_dummies(datos, columns=columnas_no_numericas)
    df_encoded = df_encoded.drop('Precio', axis=1)
    for col in df_encoded.columns:
        if col not in df.columns:
            df[col] = 0  
    columnas_orden_df1 = df_encoded.columns
    # Reorganizar las columnas de df2 para que coincidan con el orden de df1
    df = df[columnas_orden_df1]  
    
    # Hacer el transform

    datos = modelodata_cargado.transform(df)
    # Ahora puedes usar el modelo cargado para hacer predicciones
    y_pred = modelo_cargado.predict(datos) 
    
    output = pd.DataFrame()
    output['Id'] = input['Id']
    output['Precio'] = y_pred
    return output



if __name__ == '__main__':

    # Creates a parser to receive the input argument.
    parser = argparse.ArgumentParser()
    parser.add_argument('file', help='Path to the data file.')
    args = parser.parse_args()

    # Read the argument and load the data.
    try:
        data = pd.read_csv(args.file)
        
    except:
        print("Error: the input file does not have a valid format.", file=sys.stderr)
        exit(1)

    # Computes the predictions.
    # NOTE: this stage is simulated.

    with open('STUDENT3\modelogbr3.pkl', 'rb') as archivo:
        modelo_cargado = pickle.load(archivo)
    with open('STUDENT3\modelodata.pkl', 'rb') as archivo:
        modelodata_cargado = pickle.load(archivo) 
    with open('STUDENT3\dummy_encoding.pkl', 'rb') as file:
        df_encoded = pickle.load(file) 
    output = predict(data, modelo_cargado, modelodata_cargado, df_encoded)  
    # Writes the output.
    print('Id,Precio')
    for r in output.itertuples():
        print(f'{r.Id},{r.Precio}')
