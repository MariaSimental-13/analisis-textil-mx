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

En 2023, la industria de confección en México permanece aproximadamente **19% por debajo** de los niveles observados antes de la pandemia (2019).

Aunque el sector mostró una recuperación parcial después de 2020, el comportamiento reciente sugiere una desaceleración estructural y una recuperación menos sólida frente a otras actividades manufactureras.
""")

# =========================
# 4. CARGA Y LIMPIEZA DE DATOS
# =========================
df_conf = pd.read_excel(
    "Indicadores20260503191827.xls",
    header=None,
    engine="xlrd"
)

df_conf.columns = df_conf.iloc[5]
df_conf = df_conf[6:].reset_index(drop=True)

df_conf = df_conf[
    df_conf["Indicador"].str.contains("prendas", na=False)
]

df_conf = df_conf.iloc[[0]]

# =========================
# 5. TRANSFORMACIÓN
# =========================
df_conf_long = df_conf.melt(
    id_vars=["Indicador", "Área geográfica"],
    var_name="Fecha",
    value_name="Indice"
)

df_conf_long["Indice"] = pd.to_numeric(
    df_conf_long["Indice"],
    errors="coerce"
)

df_conf_long = df_conf_long.dropna(subset=["Indice"])

df_conf_long["Año"] = (
    df_conf_long["Fecha"]
    .str[:4]
    .astype(int)
)

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

df_tabla["Indice"] = (
    df_tabla["Indice"]
    .round(1)
)

df_tabla["YoY %"] = (
    df_tabla["Indice"]
    .pct_change() * 100
)

df_tabla["YoY %"] = (
    df_tabla["YoY %"]
    .round(1)
)

base_2019 = df_tabla.loc[
    df_tabla["Año"] == 2019,
    "Indice"
].values[0]

df_tabla["Index 2019=100"] = (
    df_tabla["Indice"] / base_2019
) * 100

df_tabla["Index 2019=100"] = (
    df_tabla["Index 2019=100"]
    .round(1)
)

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

st.dataframe(
    df_tabla,
    use_container_width=True
)

# =========================
# 11. INTERPRETACIÓN FINAL
# =========================
st.markdown("""
### Interpretación

Después de la caída observada en 2020, la confección mexicana registró una recuperación parcial durante 2021 y 2022. Sin embargo, en 2023 el sector continúa por debajo de los niveles previos a la pandemia.

El comportamiento podría estar asociado con factores como:

- incremento de importaciones de prendas
- cambios en las cadenas globales de suministro
- expansión del fast fashion
- presión competitiva internacional

En conjunto, los datos sugieren una posible pérdida de competitividad en la industria nacional de confección.
""")

# =========================================================
# =========================================================
# ANÁLISIS TEXTIL VS CONFECCIÓN
# =========================================================
# =========================================================

st.title("Análisis de la industria textil (2018–2023)")

st.markdown("""
Este análisis compara la evolución de dos segmentos clave de la industria textil mexicana:

- Manufactura textil (SCIAN 313)
- Confección de prendas

El objetivo es evaluar si ambos sectores mostraron patrones de recuperación similares después de la pandemia y detectar posibles diferencias estructurales dentro de la cadena productiva.
""")

# =========================================================
# DATOS CONFECCIÓN
# =========================================================

df_conf = pd.read_excel(
    "Indicadores20260503191827.xls",
    header=None
)

df_conf.columns = df_conf.iloc[5]

df_conf = df_conf[6:]
df_conf = df_conf.reset_index(drop=True)

df_conf = df_conf[
    df_conf["Indicador"].str.contains("prendas", na=False)
]

df_conf = df_conf.iloc[[0]]

df_conf_long = df_conf.melt(
    id_vars=["Indicador", "Área geográfica"],
    var_name="Fecha",
    value_name="Indice"
)

df_conf_long["Indice"] = pd.to_numeric(
    df_conf_long["Indice"],
    errors="coerce"
)

df_conf_long = df_conf_long.dropna(subset=["Indice"])

df_conf_long["Año"] = (
    df_conf_long["Fecha"]
    .str[:4]
    .astype(int)
)

df_conf_trend = (
    df_conf_long
    .groupby("Año")["Indice"]
    .mean()
    .reset_index()
)

df_conf_trend = df_conf_trend.sort_values("Año")

df_conf_trend["YoY %"] = (
    df_conf_trend["Indice"]
    .pct_change() * 100
)

df_conf_trend["YoY %"] = (
    df_conf_trend["YoY %"]
    .round(1)
)

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
# DATOS MANUFACTURA TEXTIL
# =========================================================

df_textil = pd.read_excel(
    "EMIM_37 - copia.xlsx",
    header=None
)

header_years = df_textil.iloc[5]
header_months = df_textil.iloc[6]

columns = []

for y, m in zip(header_years, header_months):

    if pd.notna(y) and pd.notna(m):
        columns.append(f"{y}_{m}")
    else:
        columns.append(y)

df_textil.columns = columns

df_textil = df_textil.iloc[7:]
df_textil = df_textil.reset_index(drop=True)

df_textil_long = df_textil.melt(
    id_vars=[
        "Variable_Variable",
        "Tipo de dato_Tipo de dato",
        "Sector SCIAN_Sector SCIAN"
    ],
    var_name="Fecha",
    value_name="Produccion"
)

df_textil_long["Produccion"] = pd.to_numeric(
    df_textil_long["Produccion"],
    errors="coerce"
)

df_textil_long = df_textil_long.dropna(
    subset=["Produccion"]
)

df_textil_long[["Año", "Mes"]] = (
    df_textil_long["Fecha"]
    .str.split("_", expand=True)
)

df_textil_long["Año"] = (
    df_textil_long["Año"]
    .astype(int)
)

df_textil_clean = df_textil_long[
    df_textil_long["Año"] <= 2023
]

df_textil_trend = (
    df_textil_clean
    .groupby("Año")["Produccion"]
    .sum()
    .reset_index()
)

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
# INSIGHT PRINCIPAL
# =========================================================

st.header("Insight clave")

ultimo_conf = df_conf_trend.iloc[-1]["Index 2019=100"]

st.metric(
    label="Confección vs 2019",
    value=round(ultimo_conf, 1),
    delta=round(ultimo_conf - 100, 1)
)

st.markdown("""
La confección mexicana continúa por debajo de los niveles observados antes de la pandemia.

A diferencia de la manufactura textil, la recuperación del sector confección ha sido más lenta e inestable, lo que podría reflejar una pérdida de dinamismo en el producto final dentro de la cadena textil nacional.
""")

# =========================================================
# GRÁFICA CONFECCIÓN
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
# GRÁFICA TEXTIL
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
# COMPARATIVA
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
# TABLAS
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
# INTERPRETACIÓN
# =========================================================

st.header("Interpretación")

st.markdown("""
## Hallazgos principales

- La manufactura textil mostró una recuperación más sólida después de 2020.
- La confección de prendas continúa rezagada frente a niveles pre-pandemia.
- Existe una posible desconexión entre la producción de insumos textiles y el desempeño del producto final.

## Posibles factores explicativos

- crecimiento acelerado de importaciones de prendas
- expansión del modelo fast fashion
- presión competitiva internacional
- cambios en los patrones de consumo post-pandemia
- pérdida de competitividad en confección nacional

## Implicaciones potenciales

La diferencia entre ambos sectores podría indicar que parte de la recuperación manufacturera no se está traduciendo en mayor producción nacional de prendas terminadas.

Esto podría aumentar la dependencia de productos importados y debilitar la participación de la confección mexicana dentro del mercado interno.
""")

# =========================================================
# COMERCIO EXTERIOR
# EXPORTACIONES VS IMPORTACIONES
# =========================================================

st.header("Comercio exterior del sector prendas")

st.write("""
Este análisis evalúa la evolución de las exportaciones e importaciones de prendas en México entre 2018 y 2023.

El objetivo es identificar cambios en la balanza comercial del sector y analizar si el crecimiento acelerado de las importaciones podría estar relacionado con el debilitamiento relativo de la confección nacional.
""")

# =========================================================
# EXPORTACIONES
# =========================================================

df_exp_raw = pd.read_excel(
    "Matriz Volumen Anual Productos.xlsx",
    header=None
)

df_exp_raw.columns = df_exp_raw.iloc[2]

df_exp = df_exp_raw.iloc[3:].reset_index(drop=True)

df_exp = df_exp.iloc[:, :7]

df_exp.columns = [
    "Categoria",
    "2018",
    "2019",
    "2020",
    "2021",
    "2022",
    "2023"
]

df_exp_filtrado = df_exp[
    df_exp["Categoria"].astype(str).str.startswith(("61", "62"))
].copy()

años = ["2018", "2019", "2020", "2021", "2022", "2023"]

for año in años:

    df_exp_filtrado[año] = pd.to_numeric(
        df_exp_filtrado[año],
        errors="coerce"
    )

exportaciones = []

for año in años:

    total = df_exp_filtrado[año].sum()
    exportaciones.append(total)

df_exportaciones = pd.DataFrame({
    "Año": años,
    "Exportaciones": exportaciones
})

# =========================================================
# IMPORTACIONES
# =========================================================

df_imp_raw = pd.read_excel(
    "CE Volumen Producto Anual.xlsx",
    header=None
)

df_imp_raw.columns = df_imp_raw.iloc[2]

df_imp = df_imp_raw.iloc[3:].reset_index(drop=True)

df_imp = df_imp.iloc[:, :7]

df_imp.columns = [
    "Categoria",
    "2018",
    "2019",
    "2020",
    "2021",
    "2022",
    "2023"
]

df_imp_filtrado = df_imp[
    df_imp["Categoria"].astype(str).str.startswith(("61", "62"))
].copy()

for año in años:

    df_imp_filtrado[año] = pd.to_numeric(
        df_imp_filtrado[año],
        errors="coerce"
    )

importaciones = []

for año in años:

    total = df_imp_filtrado[año].sum()
    importaciones.append(total)

df_importaciones = pd.DataFrame({
    "Año": años,
    "Importaciones": importaciones
})

# =========================================================
# COMPARATIVA
# =========================================================

df_comparativa = pd.merge(
    df_exportaciones,
    df_importaciones,
    on="Año"
)

df_comparativa["Balanza"] = (
    df_comparativa["Exportaciones"]
    - df_comparativa["Importaciones"]
)

# =========================================================
# KPI
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
Entre 2018 y 2023, las importaciones de prendas crecieron aproximadamente **{crecimiento_importaciones}%**.

Aunque las exportaciones también aumentaron durante el periodo, el crecimiento de las importaciones fue considerablemente mayor, ampliando el déficit comercial del sector prendas.

La aceleración observada después de 2021 podría estar relacionada con una mayor dependencia de productos importados dentro del mercado nacional.
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
# BALANZA
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
# TABLA
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
# INTERPRETACIÓN FINAL
# =========================================================

st.header("Interpretación")

st.subheader("Hallazgos principales")

st.markdown("""
- Las importaciones mostraron una aceleración significativa después de 2020.
- Las exportaciones crecieron durante el mismo periodo, aunque a menor ritmo.
- El déficit comercial del sector prendas se amplió de forma importante entre 2021 y 2023.
- La confección nacional continúa por debajo de niveles pre-pandemia.
- El comportamiento comercial coincide con el rezago observado en la producción nacional de prendas.
""")

st.subheader("Posibles implicaciones")

st.markdown("""
- mayor dependencia del mercado nacional respecto a prendas importadas
- incremento de la presión competitiva internacional
- expansión del modelo fast fashion
- posible sustitución de producción nacional por importaciones
- pérdida de competitividad en la confección mexicana
""")
