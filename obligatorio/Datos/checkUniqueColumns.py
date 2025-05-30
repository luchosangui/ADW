import pandas as pd

# Cargá tu archivo Excel ya normalizado (ajustá el nombre de archivo y hoja si es necesario)
df = pd.read_excel("precios_medios_2020-2024.xlsx")

# Si usaste otro nombre de columnas, ajustá aquí:
columnas = ["Producto", "Marca", "Especificación"]
for col in columnas:
    if col not in df.columns:
        print(f"Columna no encontrada: {col}")
    else:
        print(f"Valores únicos en '{col}':")
        print(df[col].unique())
        print("-" * 40)
