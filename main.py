@st.cache_data
def cargar_confeccion():

    df = pd.read_excel("Indicadores confeccion.xlsx")

    df["Confeccion_Indice"] = pd.to_numeric(
        df["Confeccion_Indice"],
        errors="coerce"
    )

    df["Año"] = (
        df["Fecha"]
        .astype(str)
        .str[:4]
    )

    df["Año"] = pd.to_numeric(
        df["Año"],
        errors="coerce"
    )

    df = df.dropna(subset=["Año"])

    df["Año"] = df["Año"].astype(int)

    df_final = (
        df.groupby("Año", as_index=False)
        ["Confeccion_Indice"]
        .mean()
    )

    base_2018 = df_final.loc[
        df_final["Año"] == 2018,
        "Confeccion_Indice"
    ].values[0]

    df_final["Index 2018=100"] = (
        df_final["Confeccion_Indice"]
        /
        base_2018
    ) * 100

    df_final["YoY %"] = (
        df_final["Confeccion_Indice"]
        .pct_change() * 100
    )

    return df_final.round(1)
@st.cache_data
def cargar_textil():

    df = pd.read_excel("Indicadores textiles.xlsx")

    df["Indice_Textiles"] = pd.to_numeric(
        df["Indice_Textiles"],
        errors="coerce"
    )

    df["Año"] = (
        df["Fecha"]
        .astype(str)
        .str[:4]
    )

    df["Año"] = pd.to_numeric(
        df["Año"],
        errors="coerce"
    )

    df = df.dropna(subset=["Año"])

    df["Año"] = df["Año"].astype(int)

    df_final = (
        df.groupby("Año", as_index=False)
        ["Indice_Textiles"]
        .mean()
    )

    base_2018 = df_final.loc[
        df_final["Año"] == 2018,
        "Indice_Textiles"
    ].values[0]

    df_final["Index 2018=100"] = (
        df_final["Indice_Textiles"]
        /
        base_2018
    ) * 100

    df_final["YoY %"] = (
        df_final["Indice_Textiles"]
        .pct_change() * 100
    )

    return df_final.round(1)
