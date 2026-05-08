import pandas as pd
import plotly.express as px
import streamlit as st

# =========================================================
# CONFIG
# =========================================================

st.set_page_config(
    page_title="Análisis Textil México",
    layout="wide"
)

# =========================================================
# CARGAR CONFECCIÓN
# =========================================================

@st.cache_data
def cargar_confeccion():

    df = pd.read_excel("Indicadores confeccion.xls")
   

    # convertir índice a numérico
    df["Confeccion_Indice"] = pd.to_numeric(
        df["Confeccion_Indice"],
        errors="coerce"
    )

    # obtener año desde columna Año
    df["Año_temp"] = (
        df["Año"]
        .astype(str)
        .str[:4]
    )

    df["Año_temp"] = pd.to_numeric(
        df["Año_temp"],
        errors="coerce"
    )

    # eliminar NaN
    df = df.dropna(subset=["Año_temp"])

    # convertir a int
    df["Año_temp"] = df["Año_temp"].astype(int)

    # promedio anual
    df_final = (
        df.groupby("Año_temp", as_index=False)
        ["Confeccion_Indice"]
        .mean()
    )

    # renombrar columna
    df_final = df_final.rename(
        columns={"Año_temp": "Año"}
    )

    # índice base 2018
    base_2018 = df_final.loc[
        df_final["Año"] == 2018,
        "Confeccion_Indice"
    ].values[0]

    df_final["Index 2018=100"] = (
        df_final["Confeccion_Indice"]
        /
        base_2018
    ) * 100

    # variación anual
    df_final["YoY %"] = (
        df_final["Confeccion_Indice"]
        .pct_change() * 100
    )

    return df_final.round(1)

# =========================================================
# CARGAR TEXTILES
# =========================================================

@st.cache_data
def cargar_textil():

    df = pd.read_excel("Indicadores textiles.xls")

    # convertir índice a numérico
    df["Indice_Textiles"] = pd.to_numeric(
        df["Indice_Textiles"],
        errors="coerce"
    )

    # obtener año
    df["Año_temp"] = (
        df["Año"]
        .astype(str)
        .str[:4]
    )

    df["Año_temp"] = pd.to_numeric(
        df["Año_temp"],
        errors="coerce"
    )

    # eliminar NaN
    df = df.dropna(subset=["Año_temp"])

    # convertir a int
    df["Año_temp"] = df["Año_temp"].astype(int)

    # promedio anual
    df_final = (
        df.groupby("Año_temp", as_index=False)
        ["Indice_Textiles"]
        .mean()
    )

    # renombrar columna
    df_final = df_final.rename(
        columns={"Año_temp": "Año"}
    )

    # índice base 2018
    base_2018 = df_final.loc[
        df_final["Año"] == 2018,
        "Indice_Textiles"
    ].values[0]

    df_final["Index 2018=100"] = (
        df_final["Indice_Textiles"]
        /
        base_2018
    ) * 100

    # variación anual
    df_final["YoY %"] = (
        df_final["Indice_Textiles"]
        .pct_change() * 100
    )

    return df_final.round(1)

# =========================================================
# CARGAR DATOS
# =========================================================

conf = cargar_confeccion()
textil = cargar_textil()

# =========================================================
# TÍTULO
# =========================================================

st.title("Análisis de la industria textil en México (2018-2025)")

st.markdown("""
Este análisis evalúa la evolución de la industria de confección y manufactura textil en México entre 2018 y 2025.

El objetivo es identificar diferencias en la recuperación sectorial y analizar posibles señales de debilitamiento estructural dentro de la cadena manufacturera nacional.
""")

# =========================================================
# KPI
# =========================================================

ultimo_conf = conf.iloc[-1]["Index 2018=100"]

st.metric(
    label="Confección vs 2018",
    value=round(ultimo_conf, 1),
    delta=round(ultimo_conf - 100, 1)
)

# =========================================================
# GRÁFICA CONFECCIÓN
# =========================================================

st.subheader("Industria de confección")

fig_conf = px.line(
    conf,
    x="Año",
    y="Index 2018=100",
    markers=True,
    title="Industria de confección en México"
)

st.plotly_chart(
    fig_conf,
    use_container_width=True
)

# =========================================================
# GRÁFICA TEXTILES
# =========================================================

st.subheader("Industria textil")

fig_textil = px.line(
    textil,
    x="Año",
    y="Index 2018=100",
    markers=True,
    title="Industria textil en México"
)

st.plotly_chart(
    fig_textil,
    use_container_width=True
)

# =========================================================
# COMPARATIVA
# =========================================================

st.subheader("Comparativa sectorial")

df_compare = pd.DataFrame({
    "Año": conf["Año"],
    "Confección": conf["Index 2018=100"],
    "Textiles": textil["Index 2018=100"]
})

df_compare_long = df_compare.melt(
    id_vars="Año",
    var_name="Sector",
    value_name="Indice"
)

fig_compare = px.line(
    df_compare_long,
    x="Año",
    y="Indice",
    color="Sector",
    markers=True,
    title="Confección vs textiles"
)

st.plotly_chart(
    fig_compare,
    use_container_width=True
)

# =========================================================
# TABLAS
# =========================================================

st.subheader("Datos resumidos")

col1, col2 = st.columns(2)

with col1:

    st.write("Confección")

    st.dataframe(
        conf,
        use_container_width=True
    )

with col2:

    st.write("Textiles")

    st.dataframe(
        textil,
        use_container_width=True
    )

# =========================================================
# INTERPRETACIÓN
# =========================================================

st.header("Hallazgos principales")

st.markdown("""
- La confección mexicana continúa por debajo de niveles pre-pandemia.
- La manufactura textil mostró una recuperación más sólida después de 2020.
- A partir de 2023 ambos sectores presentan una desaceleración.
- La caída en confección es más pronunciada hacia 2025.
- Los datos podrían sugerir una pérdida relativa de dinamismo dentro del sector confección en México.
""")

@st.cache_data
def cargar_exportaciones():

    df = pd.read_excel("Exportaciones.xlsx")

    # limpiar nombres columnas
    df.columns = df.columns.str.strip()

    # filtrar capítulos 61 y 62
    df = df[
        df["Sector"]
        .astype(str)
        .str.startswith(("61", "62"))
    ]

    años = [
        "2018",
        "2019",
        "2020",
        "2021",
        "2022",
        "2023",
        "2024",
        "2025"
    ]

    # convertir a numérico
    for año in años:

        df[año] = pd.to_numeric(
            df[año],
            errors="coerce"
        )

    exportaciones = []

    for año in años:

        total = df[año].sum()

        exportaciones.append(total)

    df_final = pd.DataFrame({
        "Año": [int(a) for a in años],
        "Exportaciones": exportaciones
    })

    return df_final
@st.cache_data
def cargar_importaciones():

    df = pd.read_excel("Importaciones.xlsx")

    # limpiar columnas
    df.columns = df.columns.str.strip()

    # filtrar capítulos 61 y 62
    df = df[
        df["Sector"]
        .astype(str)
        .str.startswith(("61", "62"))
    ]

    años = [
        "2018",
        "2019",
        "2020",
        "2021",
        "2022",
        "2023",
        "2024",
        "2025"
    ]

    # convertir numérico
    for año in años:

        df[año] = pd.to_numeric(
            df[año],
            errors="coerce"
        )

    importaciones = []

    for año in años:

        total = df[año].sum()

        importaciones.append(total)

    df_final = pd.DataFrame({
        "Año": [int(a) for a in años],
        "Importaciones": importaciones
    })

    return df_final
exp = cargar_exportaciones()
imp = cargar_importaciones()

trade = pd.merge(
    exp,
    imp,
    on="Año"
)

trade["Balanza"] = (
    trade["Exportaciones"]
    -
    trade["Importaciones"]
)

# =========================================================
# EXPORTACIONES
# =========================================================

@st.cache_data
def cargar_exportaciones():

    df = pd.read_excel(
        "Exportaciones.xlsx"
    )

    # limpiar columnas
    df.columns = df.columns.str.strip()

    # filtrar capítulos prendas
    df = df[
        df["Sector"]
        .astype(str)
        .str.startswith(("61", "62"))
    ]

    años = [
        "2018",
        "2019",
        "2020",
        "2021",
        "2022",
        "2023",
        "2024",
        "2025"
    ]

    # convertir numérico
    for año in años:

        df[año] = pd.to_numeric(
            df[año],
            errors="coerce"
        )

    exportaciones = []

    for año in años:

        total = df[año].sum()

        exportaciones.append(total)

    df_final = pd.DataFrame({
        "Año": [int(a) for a in años],
        "Exportaciones": exportaciones
    })

    return df_final.round(0)

# =========================================================
# IMPORTACIONES
# =========================================================

@st.cache_data
def cargar_importaciones():

    df = pd.read_excel(
        "Importaciones.xlsx"
    )

    # limpiar columnas
    df.columns = df.columns.str.strip()

    # filtrar capítulos prendas
    df = df[
        df["Sector"]
        .astype(str)
        .str.startswith(("61", "62"))
    ]

    años = [
        "2018",
        "2019",
        "2020",
        "2021",
        "2022",
        "2023",
        "2024",
        "2025"
    ]

    # convertir numérico
    for año in años:

        df[año] = pd.to_numeric(
            df[año],
            errors="coerce"
        )

    importaciones = []

    for año in años:

        total = df[año].sum()

        importaciones.append(total)

    df_final = pd.DataFrame({
        "Año": [int(a) for a in años],
        "Importaciones": importaciones
    })

    return df_final.round(0)

# =========================================================
# CARGAR DATOS
# =========================================================

exp = cargar_exportaciones()

imp = cargar_importaciones()

# =========================================================
# SECCIÓN COMERCIO EXTERIOR
# =========================================================

st.header("Comercio exterior del sector prendas")

st.markdown("""
Esta sección analiza el comportamiento de las exportaciones e importaciones relacionadas con prendas de vestir en México entre 2018 y 2025.

El objetivo es identificar posibles cambios estructurales dentro del sector y evaluar la presión competitiva internacional sobre la manufactura nacional.
""")

# =========================================================
# EXPORTACIONES
# =========================================================

st.subheader("Exportaciones")

st.markdown("""
Las exportaciones del sector muestran una recuperación importante después de 2020, alcanzando máximos entre 2023 y 2024.
""")

fig_exp = px.line(
    exp,
    x="Año",
    y="Exportaciones",
    markers=True,
    title="Exportaciones del sector prendas en México"
)

st.plotly_chart(
    fig_exp,
    use_container_width=True
)

st.dataframe(
    exp,
    use_container_width=True
)

# =========================================================
# IMPORTACIONES
# =========================================================

st.subheader("Importaciones")

st.markdown("""
Las importaciones crecieron de forma acelerada después de 2021, superando consistentemente el nivel de exportaciones.
""")

fig_imp = px.line(
    imp,
    x="Año",
    y="Importaciones",
    markers=True,
    title="Importaciones del sector prendas en México"
)

st.plotly_chart(
    fig_imp,
    use_container_width=True
)

st.dataframe(
    imp,
    use_container_width=True
)

# =========================================================
# COMPARATIVA
# =========================================================

st.subheader("Comparativa comercial")

trade = pd.merge(
    exp,
    imp,
    on="Año"
)

trade_long = trade.melt(
    id_vars="Año",
    var_name="Tipo",
    value_name="Valor"
)

fig_trade = px.line(
    trade_long,
    x="Año",
    y="Valor",
    color="Tipo",
    markers=True,
    title="Exportaciones vs importaciones"
)

st.plotly_chart(
    fig_trade,
    use_container_width=True
)

# =========================================================
# TABLA COMPARATIVA
# =========================================================

trade["Balanza_Comercial"] = (
    trade["Exportaciones"]
    -
    trade["Importaciones"]
)

st.dataframe(
    trade,
    use_container_width=True
)
st.header("Hallazgos principales")

st.markdown("""
- La industria de confección en México mostró una caída importante entre 2018 y 2025, manteniéndose por debajo de niveles pre-pandemia.

- El sector textil presentó una recuperación más sólida después de 2020 y conservó un mayor dinamismo relativo frente a confección.

- Las exportaciones del sector prendas crecieron de forma importante entre 2021 y 2024.

- Las importaciones aumentaron más rápidamente que las exportaciones después de 2021.

- A partir de 2022 la balanza comercial del sector se volvió negativa, mostrando un incremento en la dependencia de productos importados.
""")
st.header("Implicaciones del análisis")

st.markdown("""
Los resultados sugieren posibles cambios estructurales dentro de la industria textil y de confección en México.

Aunque el país mantiene una actividad exportadora relevante, el crecimiento acelerado de las importaciones y el menor dinamismo de la confección podrían indicar una presión competitiva creciente dentro del mercado nacional, particularmente en segmentos relacionados con prendas de consumo masivo y fast fashion.

Al mismo tiempo, la mayor resiliencia del sector textil podría estar relacionada con una especialización progresiva hacia segmentos de mayor valor agregado, incluyendo aplicaciones industriales, técnicas y médicas.

La desaceleración observada en 2025 podría estar influenciada por factores externos como tensiones comerciales, cambios arancelarios, incertidumbre económica y disrupciones logísticas internacionales.
""")
st.header("Pregunta abierta")

st.markdown("""
¿Está experimentando México una transformación estructural dentro de su industria textil y de confección?

Los datos podrían sugerir una transición gradual desde la confección tradicional hacia segmentos textiles más especializados y de mayor valor agregado. Sin embargo, también abren preguntas sobre el impacto de la competencia internacional, el crecimiento de las importaciones y el futuro de la manufactura nacional orientada al consumo cotidiano.
""")
