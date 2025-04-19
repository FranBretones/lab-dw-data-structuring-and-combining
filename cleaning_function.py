def clean_dataframe(df):
    """
    Limpia el DataFrame con transformaciones estándar y muestra un resumen del proceso.
    
    Operaciones incluidas:
    - Limpieza de nombres de columnas
    - Renombrado de columnas específicas
    - Relleno de nulos (moda para categóricas, media para numéricas)
    - Estandarización de valores categóricos
    - Normalización de 'number_of_open_complaints'
    - Eliminación de duplicados y reseteo de índice
    
    Retorna:
        df_cleaned (pd.DataFrame): DataFrame limpio
    """
    import pandas as pd

    df = df.copy()
    resumen = {}

    # -------- Limpieza de nombres de columnas --------
    df.columns = df.columns.str.replace(' ', '_').str.lower()
    df = df.rename(columns={'st': 'state'})
    resumen['column_cleaning'] = True

    # -------- Nulos antes de limpieza --------
    nulls_before = df.isnull().sum().sum()

    # -------- Relleno de nulos: categóricas --------
    cat_filled = []
    categorical_col = df.select_dtypes(include=[object]).columns
    for col in categorical_col:
        if df[col].isnull().any():
            df[col] = df[col].fillna(df[col].mode()[0])
            cat_filled.append(col)

    # -------- Relleno de nulos: numéricas --------
    num_filled = []
    num_columns = df.select_dtypes(include=['float64']).columns
    for col in num_columns:
        if df[col].isnull().any():
            df[col] = df[col].fillna(df[col].mean())
            num_filled.append(col)

    nulls_after = df.isnull().sum().sum()
    resumen['nulls_filled'] = nulls_before - nulls_after
    resumen['categorical_columns_filled'] = cat_filled
    resumen['numeric_columns_filled'] = num_filled

    # -------- Estandarización de valores --------
    estandarizadas = []

    if 'gender' in df.columns:
        df['gender'] = df['gender'].replace({
            'female': 'F', 'Femal': 'F', 'Female': 'F',
            'male': 'M', 'Male': 'M'
        })
        estandarizadas.append('gender')

    if 'state' in df.columns:
        df['state'] = df['state'].replace({
            'Cali': 'California',
            'WA': 'Washington',
            'AZ': 'Arizona'
        })
        estandarizadas.append('state')

    if 'education' in df.columns:
        df['education'] = df['education'].replace({
            'Bachelors': 'Bachelor'
        })
        estandarizadas.append('education')

    if 'vehicle_class' in df.columns:
        df['vehicle_class'] = df['vehicle_class'].replace({
            'Sports Car': 'Luxury',
            'Luxury SUV': 'Luxury',
            'Luxury Car': 'Luxury'
        })
        estandarizadas.append('vehicle_class')

    resumen['standardized_columns'] = estandarizadas

    # -------- Normalizar number_of_open_complaints --------
    complaints_transformed = False
    if 'number_of_open_complaints' in df.columns:
        df['number_of_open_complaints'] = df['number_of_open_complaints'].apply(
            lambda x: int(x.split('/')[1]) if isinstance(x, str) and '/' in x else x
        )
        complaints_transformed = True

    resumen['number_of_open_complaints_transformed'] = complaints_transformed

    # -------- Eliminar duplicados --------
    rows_before = df.shape[0]
    df = df.drop_duplicates().reset_index(drop=True)
    rows_after = df.shape[0]
    resumen['duplicates_removed'] = rows_before - rows_after

    # -------- Mostrar resumen --------
    print("Limpieza completada:")
    print(f"• Nulos rellenados: {resumen['nulls_filled']}")
    print(f"• Columnas categóricas rellenadas: {resumen['categorical_columns_filled']}")
    print(f"• Columnas numéricas rellenadas: {resumen['numeric_columns_filled']}")
    print(f"• Columnas estandarizadas: {resumen['standardized_columns']}")
    print(f"• Transformación en 'number_of_open_complaints': {resumen['number_of_open_complaints_transformed']}")
    print(f"• Duplicados eliminados: {resumen['duplicates_removed']}")
    
    
    return df.reset_index(drop=True)