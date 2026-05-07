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

st.title("Análisis de la industria textil (2018–2024)")

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
    df_textil_long["Año"] <= 2023
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

""")
# =========================================================
# COMERCIO EXTERIOR
# EXPORTACIONES VS IMPORTACIONES
# INDUSTRIA DE PRENDAS EN MÉXICO
# =========================================================

import pandas as pd
import plotly.express as px
import streamlit as st

# =========================================================
# TÍTULO
# =========================================================

st.header("Comercio exterior del sector prendas")

st.write("""
Este análisis compara el comportamiento de las exportaciones
e importaciones de prendas en México entre 2018 y 2023.

El objetivo es identificar posibles cambios en la balanza
comercial y evaluar si el crecimiento de importaciones podría
estar relacionado con la desaceleración de la confección nacional.
""")

# =========================================================
# CARGAR EXPORTACIONES
# =========================================================

df_exp_raw = pd.read_excel(
    "Matriz Volumen Anual Productos.xlsx",
    header=None
)

# usar fila correcta como headers
df_exp_raw.columns = df_exp_raw.iloc[2]

# eliminar filas basura
df_exp = df_exp_raw.iloc[3:].reset_index(drop=True)

# conservar columnas necesarias
df_exp = df_exp.iloc[:, :7]

# renombrar columnas
df_exp.columns = [
    "Categoria",
    "2018",
    "2019",
    "2020",
    "2021",
    "2022",
    "2023"
]

# =========================================================
# FILTRAR PRENDAS
# categorías 61 y 62
# =========================================================

df_exp_filtrado = df_exp[
    df_exp["Categoria"].astype(str).str.startswith(("61", "62"))
].copy()

# =========================================================
# CONVERTIR A NUMÉRICO
# =========================================================

años = ["2018", "2019", "2020", "2021", "2022", "2023"]

for año in años:
    df_exp_filtrado[año] = pd.to_numeric(
        df_exp_filtrado[año],
        errors="coerce"
    )

# =========================================================
# SUMAR EXPORTACIONES
# =========================================================

exportaciones = []

for año in años:
    total = df_exp_filtrado[año].sum()
    exportaciones.append(total)

df_exportaciones = pd.DataFrame({
    "Año": años,
    "Exportaciones": exportaciones
})

# =========================================================
# CARGAR IMPORTACIONES
# =========================================================

df_imp_raw = pd.read_excel(
    "CE Volumen Producto Anual.xlsx",
    header=None
)

# usar fila correcta como headers
df_imp_raw.columns = df_imp_raw.iloc[2]

# eliminar filas basura
df_imp = df_imp_raw.iloc[3:].reset_index(drop=True)

# conservar columnas necesarias
df_imp = df_imp.iloc[:, :7]

# renombrar columnas
df_imp.columns = [
    "Categoria",
    "2018",
    "2019",
    "2020",
    "2021",
    "2022",
    "2023"
]

# =========================================================
# FILTRAR PRENDAS
# =========================================================

df_imp_filtrado = df_imp[
    df_imp["Categoria"].astype(str).str.startswith(("61", "62"))
].copy()

# =========================================================
# CONVERTIR A NUMÉRICO
# =========================================================

for año in años:
    df_imp_filtrado[año] = pd.to_numeric(
        df_imp_filtrado[año],
        errors="coerce"
    )

# =========================================================
# SUMAR IMPORTACIONES
# =========================================================

importaciones = []

for año in años:
    total = df_imp_filtrado[año].sum()
    importaciones.append(total)

df_importaciones = pd.DataFrame({
    "Año": años,
    "Importaciones": importaciones
})

# =========================================================
# UNIR DATAFRAMES
# =========================================================

df_comparativa = pd.merge(
    df_exportaciones,
    df_importaciones,
    on="Año"
)

# =========================================================
# CALCULAR BALANZA
# =========================================================

df_comparativa["Balanza"] = (
    df_comparativa["Exportaciones"]
    - df_comparativa["Importaciones"]
)

# =========================================================
# KPI PRINCIPAL
# =========================================================

balanza_2023 = round(
    df_comparativa.loc[
        df_comparativa["Año"] == "2023",
        "Balanza"
    ].values[0] / 1_000_000,
    1
)

crecimiento_importaciones = round(
    (
        (
            df_comparativa["Importaciones"].iloc[-1]
            /
            df_comparativa["Importaciones"].iloc[0]
        ) - 1
    ) * 100,
    1
)

st.subheader("Insight clave")

st.metric(
    label="Balanza comercial 2023 (millones)",
    value=f"{balanza_2023} M",
)

st.write(f"""
Las importaciones crecieron aproximadamente
**{crecimiento_importaciones}%**
entre 2018 y 2023.

El crecimiento de importaciones fue superior al de exportaciones,
lo que amplió la brecha comercial del sector prendas.
""")

# =========================================================
# GRÁFICA EXPORTACIONES VS IMPORTACIONES
# =========================================================

st.subheader("Exportaciones vs importaciones")

fig = px.line(
    df_comparativa,
    x="Año",
    y=["Exportaciones", "Importaciones"],
    markers=True,
    title="Exportaciones vs Importaciones de prendas en México"
)

fig.update_layout(
    template="plotly_dark",
    xaxis_title="Año",
    yaxis_title="Valor comercial"
)

st.plotly_chart(fig, use_container_width=True)

# =========================================================
# GRÁFICA BALANZA COMERCIAL
# =========================================================

st.subheader("Balanza comercial")

fig2 = px.bar(
    df_comparativa,
    x="Año",
    y="Balanza",
    title="Balanza comercial del sector prendas"
)

fig2.update_layout(
    template="plotly_dark",
    xaxis_title="Año",
    yaxis_title="Balanza"
)

st.plotly_chart(fig2, use_container_width=True)

# =========================================================
# TABLA RESUMIDA
# =========================================================

st.subheader("Datos resumidos")

tabla = df_comparativa.copy()

tabla["Exportaciones"] = (
    tabla["Exportaciones"] / 1_000_000
).round(1)

tabla["Importaciones"] = (
    tabla["Importaciones"] / 1_000_000
).round(1)

tabla["Balanza"] = (
    tabla["Balanza"] / 1_000_000
).round(1)

st.dataframe(
    tabla,
    use_container_width=True
)

# =========================================================
# INTERPRETACIÓN
# =========================================================

st.header("Interpretación")

st.subheader("Hallazgos principales")

st.markdown("""
- Las importaciones crecieron de manera acelerada después de 2020.
- Las exportaciones también aumentaron, pero a menor ritmo.
- La brecha comercial del sector prendas se amplió entre 2021 y 2023.
- La confección nacional permanece por debajo de niveles prepandemia.
""")

st.subheader("Posibles implicaciones")

st.markdown("""
- mayor dependencia de prendas importadas
- presión competitiva internacional
- crecimiento del fast fashion
- posible sustitución de producción nacional
- debilitamiento del sector confección
""")


