# =========================
# 1. IMPORTS
# =========================
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px  # Movido aquí para evitar errores de espacios

# =========================
# 2. CARGA DE DATOS
# =========================
# Asegúrate de que el nombre del archivo coincida exactamente con el de tu GitHub
df_conf = pd.read_excel("Indicadores20260503191827.xls", header=None)

# =========================
# 3. LIMPIEZA
# =========================
df_conf.columns = df_conf.iloc[5]
df_conf = df_conf[6:].reset_index(drop=True)
df_conf = df_conf[df_conf["Indicador"].str.contains("prendas", na=False)]
df_conf = df_conf.iloc[[0]]

# =========================
# 4. TRANSFORMACIÓN (LONG)
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
# 5. AGREGACIÓN (TREND)
# =========================
df_conf_trend = (
    df_conf_long
    .groupby("Año", as_index=False)["Indice"]
    .mean()
    .sort_values("Año")
)

# =========================
# 6. TABLA FINAL (PORTAFOLIO)
# =========================
df_tabla = df_conf_trend.copy()
df_tabla["Indice"] = df_tabla["Indice"].round(1)
df_tabla["YoY %"] = df_tabla["Indice"].pct_change() * 100
df_tabla["YoY %"] = df_tabla["YoY %"].round(1)

base_2019 = df_tabla.loc[df_tabla["Año"] == 2019, "Indice"].values[0]
df_tabla["Index 2019=100"] = (df_tabla["Indice"] / base_2019) * 100
df_tabla["Index 2019=100"] = df_tabla["Index 2019=100"].round(1)

# =========================
# 7. GENERACIÓN DE ARCHIVOS
# =========================
# Crear tabla HTML
html_tabla = df_tabla.to_html(classes='table table-hover', index=False)
with open("mi_analisis.html", "w") as f:
    f.write(f"<html><head><link rel='stylesheet' href='https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css'></head><body><div class='container'><h1>Análisis de Confección</h1>{html_tabla}</div></body></html>")

# Gráfica interactiva con Plotly
fig = px.line(df_tabla, x="Año", y="Indice", title="Índice confección por año (Interactivo)", markers=True)
fig.write_html("grafica_pro.html")

# ESTO ES LO QUE VERÁS EN STREAMLIT
import streamlit as st
st.title("🧶 Análisis de Confección en México")
st.write("Explorando la caída estructural post-pandemia.")
st.plotly_chart(fig)
st.dataframe(df_tabla)
