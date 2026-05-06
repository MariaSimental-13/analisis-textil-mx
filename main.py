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

