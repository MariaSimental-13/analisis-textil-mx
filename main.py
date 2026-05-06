# =========================
# 1. IMPORTS
# =========================
import pandas as pd
import plotly.express as px
import streamlit as st

# =========================
# 2. CONFIG DASHBOARD
# =========================
st.set_page_config(page_title="Análisis Confección México", layout="wide")

# =========================
# 3. TÍTULO + CONTEXTO
# =========================
st.title("Análisis de la industria de confección en México (2018–2023)")

st.markdown("""
### Insight clave

En 2023, la producción de confección sigue aproximadamente **19% por debajo** de los niveles pre-pandemia (2019).

Esto sugiere una recuperación incompleta del sector.
""")

# =========================
# 4. CARGA Y LIMPIEZA DE DATOS
# =========================
df_conf = pd.read_excel("Indicadores20260503191827.xls", header=None, engine="xlrd")

df_conf.columns = df_conf.iloc[5]
df_conf = df_conf[6:].reset_index(drop=True)

df_conf = df_conf[df_conf["Indicador"].str.contains("prendas", na=False)]
df_conf = df_conf.iloc[[0]]

# =========================
# 5. TRANSFORMACIÓN
# =========================
df_conf_long = df_conf.melt(
    id_vars=["Indicador", "Área geográfica"],
    var_name="Fecha",
    value_name="Indice"
)

df_conf_long["Indice"] = pd.to_numeric(df_conf_long["Indice"], errors="coerce")
df_conf_long = df_conf_long.dropna(subset=["Indice"])

df_conf_long["Año"] = df_conf_long["Fecha"].str[:4].astype(int)

# =========================
# 6. AGREGACIÓN
# =========================
df_conf_trend = (
    df_conf_long
    .groupby("Año", as_index=False)["Indice"]
    .mean()
    .sort_values("Año")
)

# =========================
# 7. TABLA FINAL
# =========================
df_tabla = df_conf_trend.copy()
df_tabla["Indice"] = df_tabla["Indice"].round(1)

df_tabla["YoY %"] = df_tabla["Indice"].pct_change() * 100
df_tabla["YoY %"] = df_tabla["YoY %"].round(1)

base_2019 = df_tabla.loc[df_tabla["Año"] == 2019, "Indice"].values[0]
df_tabla["Index 2019=100"] = (df_tabla["Indice"] / base_2019) * 100
df_tabla["Index 2019=100"] = df_tabla["Index 2019=100"].round(1)

# =========================
# 8. KPI
# =========================
st.metric(
    label="Nivel vs 2019",
    value=f"{df_tabla[df_tabla['Año']==2023]['Index 2019=100'].values[0]}",
    delta="-18.7%"
)

# =========================
# 9. GRÁFICA
# =========================
fig = px.line(
    df_conf_trend,
    x="Año",
    y="Indice",
    markers=True,
    title="Evolución del índice de confección"
)

st.plotly_chart(fig, use_container_width=True)

# =========================
# 10. TABLA
# =========================
st.subheader("Datos resumidos")
st.dataframe(df_tabla, use_container_width=True)

# =========================
# 11. INTERPRETACIÓN FINAL
# =========================
st.markdown("""
### Interpretación

Aunque hubo una recuperación en 2021 y 2022, el sector no ha logrado regresar a niveles pre-pandemia.

Esto podría estar relacionado con:

- aumento en importaciones de prendas
- cambios en la cadena global de suministro
- crecimiento del fast fashion

El comportamiento sugiere una posible **debilidad estructural** en la industria de confección en México.
""")

# ==============================
# 1. IMPORTS
# ==============================

import pandas as pd
import plotly.express as px
import streamlit as st

# ==============================
# 2. CONFIG DASHBOARD
# ==============================

st.set_page_config(
    page_title="Industria Textil México",
    layout="wide"
)

# ==============================
# 3. TÍTULO
# ==============================

st.title("Análisis de la industria textil y confección en México (2018–2024)")

st.markdown("""
Este análisis compara el comportamiento de:

- Manufactura textil (SCIAN 313)
- Confección de prendas

El objetivo es identificar si ambos sectores se recuperaron de manera similar después de la pandemia.
""")

# =========================================================
# =========================================================
# 4. DATOS CONFECCIÓN
# =========================================================
# =========================================================

df_conf = pd.read_excel(
    "Indicadores20260503191827.xls",
    header=None
)

# headers
df_conf.columns = df_conf.iloc[5]

# eliminar basura
df_conf = df_conf[6:]
df_conf = df_conf.reset_index(drop=True)

# filtrar confección
df_conf = df_conf[
    df_conf["Indicador"].str.contains("prendas", na=False)
]

# tomar primera fila
df_conf = df_conf.iloc[[0]]

# formato largo
df_conf_long = df_conf.melt(
    id_vars=["Indicador", "Área geográfica"],
    var_name="Fecha",
    value_name="Indice"
)

# limpiar
df_conf_long["Indice"] = pd.to_numeric(
    df_conf_long["Indice"],
    errors="coerce"
)

df_conf_long = df_conf_long.dropna(subset=["Indice"])

# año
df_conf_long["Año"] = (
    df_conf_long["Fecha"]
    .str[:4]
    .astype(int)
)

# agrupar
df_conf_trend = (
    df_conf_long
    .groupby("Año")["Indice"]
    .mean()
    .reset_index()
)

df_conf_trend = df_conf_trend.sort_values("Año")

# YoY
df_conf_trend["YoY %"] = (
    df_conf_trend["Indice"]
    .pct_change() * 100
)

df_conf_trend["YoY %"] = (
    df_conf_trend["YoY %"]
    .round(1)
)

# index 2019 = 100
base_2019 = df_conf_trend.loc[
    df_conf_trend["Año"] == 2019,
    "Indice"
].values[0]

df_conf_trend["Index 2019=100"] = (
    df_conf_trend["Indice"] / base_2019
) * 100

df_conf_trend["Index 2019=100"] = (
    df_conf_trend["Index 2019=100"]
    .round(1)
)

# =========================================================
# =========================================================
# 5. DATOS MANUFACTURA TEXTIL
# =========================================================
# =========================================================

df_textil = pd.read_excel(
    "EMIM_37 - copia.xlsx",
    header=None
)

# headers
header_years = df_textil.iloc[5]
header_months = df_textil.iloc[6]

columns = []

for y, m in zip(header_years, header_months):

    if pd.notna(y) and pd.notna(m):
        columns.append(f"{y}_{m}")
    else:
        columns.append(y)

df_textil.columns = columns

# limpiar
df_textil = df_textil.iloc[7:]
df_textil = df_textil.reset_index(drop=True)

# melt
df_textil_long = df_textil.melt(
    id_vars=[
        "Variable_Variable",
        "Tipo de dato_Tipo de dato",
        "Sector SCIAN_Sector SCIAN"
    ],
    var_name="Fecha",
    value_name="Produccion"
)

# numeric
df_textil_long["Produccion"] = pd.to_numeric(
    df_textil_long["Produccion"],
    errors="coerce"
)

df_textil_long = df_textil_long.dropna(
    subset=["Produccion"]
)

# año
df_textil_long[["Año", "Mes"]] = (
    df_textil_long["Fecha"]
    .str.split("_", expand=True)
)

df_textil_long["Año"] = (
    df_textil_long["Año"]
    .astype(int)
)

# solo hasta 2024
df_textil_clean = df_textil_long[
    df_textil_long["Año"] <= 2024
]

# agrupar
df_textil_trend = (
    df_textil_clean
    .groupby("Año")["Produccion"]
    .sum()
    .reset_index()
)

# normalizar base 2019
base_textil_2019 = df_textil_trend.loc[
    df_textil_trend["Año"] == 2019,
    "Produccion"
].values[0]

df_textil_trend["Index 2019=100"] = (
    df_textil_trend["Produccion"] /
    base_textil_2019
) * 100

df_textil_trend["Index 2019=100"] = (
    df_textil_trend["Index 2019=100"]
    .round(1)
)

# =========================================================
# 6. INSIGHT PRINCIPAL
# =========================================================

st.header("Insight clave")

ultimo_conf = df_conf_trend.iloc[-1]["Index 2019=100"]

st.metric(
    label="Confección vs 2019",
    value=round(ultimo_conf, 1),
    delta=round(ultimo_conf - 100, 1)
)

st.markdown("""
La confección mexicana sigue por debajo de los niveles pre-pandemia.

Esto podría indicar una recuperación incompleta del sector,
a diferencia de otras áreas manufactureras.
""")

# =========================================================
# 7. GRÁFICA CONFECCIÓN
# =========================================================

st.header("Evolución del índice de confección")

fig_conf = px.line(
    df_conf_trend,
    x="Año",
    y="Indice",
    markers=True,
    title="Confección de prendas"
)

st.plotly_chart(
    fig_conf,
    use_container_width=True
)

# =========================================================
# 8. GRÁFICA TEXTIL
# =========================================================

st.header("Evolución manufactura textil")

fig_textil = px.line(
    df_textil_trend,
    x="Año",
    y="Index 2019=100",
    markers=True,
    title="Manufactura textil"
)

st.plotly_chart(
    fig_textil,
    use_container_width=True
)

# =========================================================
# 9. COMPARATIVA
# =========================================================

st.header("Comparativa textil vs confección")

df_compare = pd.DataFrame({
    "Año": df_conf_trend["Año"],
    "Confección": df_conf_trend["Index 2019=100"],
    "Textil": df_textil_trend["Index 2019=100"]
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
    title="Comparativa sectorial"
)

st.plotly_chart(
    fig_compare,
    use_container_width=True
)

# =========================================================
# 10. TABLAS
# =========================================================

st.header("Datos resumidos")

col1, col2 = st.columns(2)

with col1:

    st.subheader("Confección")

    st.dataframe(
        df_conf_trend,
        use_container_width=True
    )

with col2:

    st.subheader("Manufactura textil")

    st.dataframe(
        df_textil_trend,
        use_container_width=True
    )

# =========================================================
# 11. INTERPRETACIÓN
# =========================================================

st.header("Interpretación")

st.markdown("""
## Hallazgos principales

- La manufactura textil muestra una recuperación más estable.
- La confección permanece por debajo de niveles pre-pandemia.
- Existe una posible desconexión entre producción de insumos y producto final.

## Posibles causas

- aumento de importaciones
- crecimiento del fast fashion
- competencia internacional
- cambios en consumo post-pandemia
- pérdida de competitividad industrial

## Próximos pasos

Se incorporarán:

- exportaciones BANXICO
- empleo manufacturero
- comparación con importaciones
- análisis del impacto del fast fashion
""")

