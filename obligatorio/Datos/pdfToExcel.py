import camelot


def pdf_to_excel(archivo_pdf,archivo_excel):
    tablas = camelot.read_pdf(archivo_pdf, pages="1", flavor="stream")

    import pandas as pd
    df = tablas[0].df
    df.to_excel(archivo_excel, index=False, header=False)

    print(f"¡Listo! Tabla exportada a {archivo_excel}")


pdf_files = ["utiles_cadenas_2021.pdf","utiles_medianos_2022.pdf","utiles_medianos_2023.pdf","utiles_medianos_2024.pdf"]
excel_file_names = ["utiles_cadenas_2021.xlsx","utiles_medianos_2022.xlsx","utiles_medianos_2023.xlsx","utiles_medianos_2024.xlsx"]


for pdf, excel in zip(pdf_files, excel_file_names):
    pdf_to_excel(pdf, excel)
