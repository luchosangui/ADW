import pandas as pd

# Cargá los datos existentes 2021-2024
df_21_24 = pd.read_excel("consolidado_utiles_2021_2024.xlsx")

# Cargá el 2025, asegurate de usar header=1 si corresponde (ajustalo si ves que cambia el lugar del header)
df_2025 = pd.read_excel("cuadro_comparativo_cadenas_utiles_2025.xlsx", header=1)

# Renombrar columnas de 2025 para que coincidan con las del consolidado
rename_map = {
    "ÚTIL ESCOLAR": "Producto",
    "Micro-Macro": "Micro Macro",
    "Red Expres": None,  # No existe en 2021-2024, la vamos a ignorar
    "Geant": None,       # No existe en 2021-2024, la vamos a ignorar
    "Office2000": None,  # No existe en 2021-2024, la vamos a ignorar
    "Escool.uy": None,   # No existe en 2021-2024, la vamos a ignorar
}

df_2025 = df_2025.rename(columns={k: v for k, v in rename_map.items() if v})

# Limpiar columnas extra (sólo quedarnos con las del consolidado)
standard_columns = list(df_21_24.columns)
for col in standard_columns:
    if col not in df_2025.columns:
        df_2025[col] = pd.NA

# Solo dejá las columnas en el orden correcto
df_2025 = df_2025[standard_columns]

# Agregá el año
df_2025["Año"] = 2025

# Juntá los dos dataframes
final_df = pd.concat([df_21_24, df_2025], ignore_index=True)

# Opcional: eliminá filas totalmente vacías
final_df = final_df.dropna(subset=["Producto"], how="all")

# Guardá el resultado
final_df.to_excel("utiles_2021_2025_total.xlsx", index=False)
print("¡Listo! Archivo unificado: 'utiles_2021_2025_total.xlsx'")
