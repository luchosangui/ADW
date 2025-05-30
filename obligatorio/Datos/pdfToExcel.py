import camelot
import pandas as pd

# Archivos y años manuales
pdf_files = [
    ("utiles_cadenas_2021.pdf", "2021"),
    ("utiles_medianos_2022.pdf", "2022"),
    ("utiles_medianos_2023.pdf", "2023"),
    ("utiles_medianos_2024.pdf", "2024"),
]

all_data = []
standard_columns = None  # Para fijar los nombres de columna estándar

for pdf_file, year in pdf_files:
    print(f"Processing {pdf_file} for year {year}...")
    # Extraer tabla con Camelot
    tables_stream = camelot.read_pdf(pdf_file, pages='all', flavor='stream')
    tables_lattice = camelot.read_pdf(pdf_file, pages='all', flavor='lattice')
    tables = tables_stream if tables_stream.n >= tables_lattice.n else tables_lattice
    if tables.n == 0:
        print(f"No tables found in {pdf_file}")
        continue

    df = tables[0].df
    # df = df.dropna(how='all').replace('--', pd.NA)
    df = df.dropna(how='all')

    # Detectar la fila de encabezado real
    header_row = df[df.iloc[:,0].str.contains('Producto', case=False, na=False)].index
    if len(header_row) == 0:
        print(f"WARNING: No header row found in {pdf_file}, using first row as header.")
        df.columns = df.iloc[0]
        df = df[1:]
    else:
        header_idx = header_row[0]
        df.columns = df.iloc[header_idx]
        df = df[header_idx+1:]

    df = df.reset_index(drop=True).dropna(axis=1, how='all')
    df['Año'] = year

    # Guardar el estándar de columnas en la primera vuelta
    if standard_columns is None:
        standard_columns = list(df.columns)
    else:
        # Forzar el mismo orden y nombres de columnas
        missing_cols = [col for col in standard_columns if col not in df.columns]
        for col in missing_cols:
            df[col] = pd.NA  # Agrega columnas faltantes como vacías
        # Eliminar columnas de más
        df = df[standard_columns]

    print(f"Columns for {year}: {list(df.columns)}")
    all_data.append(df)





def unir_descripciones_partidas(df, col_producto='Producto'):
    otras_cols = [c for c in df.columns if c not in [col_producto, 'Año']]
    filas_corregidas = []
    for idx, fila in df.iterrows():
        # Si todas las columnas (menos Producto y Año) son '--'
        solo_guiones = all(str(fila[col]).strip() == '--' for col in otras_cols)
        # Si todas las columnas (menos Producto y Año) son vacías o nulas
        todas_vacias = all((str(fila[col]).strip() == '' or pd.isna(fila[col])) for col in otras_cols)
        # Si la fila es una continuación válida
        if idx > 0 and (solo_guiones or todas_vacias):
            if str(fila[col_producto]).strip() != "":
                filas_corregidas[-1][col_producto] += " " + str(fila[col_producto]).strip()
            continue
        # Si la fila tiene Producto vacío, la salto (no la agrego)
        if str(fila[col_producto]).strip() == "" or pd.isna(fila[col_producto]):
            continue
        # Reemplazo nulos por '--' en columnas de precios
        for col in otras_cols:
            if str(fila[col]).strip() == "" or pd.isna(fila[col]):
                fila[col] = '--'
        filas_corregidas.append(fila.to_dict())
    return pd.DataFrame(filas_corregidas)



final_df = pd.concat(all_data, ignore_index=True)
final_df = unir_descripciones_partidas(final_df)
final_df.to_excel("consolidado_utiles_2021_2024_version3.xlsx", index=False)
print("¡Listo! Consolidado en 'consolidado_utiles_2021_2024_version3.xlsx'")
