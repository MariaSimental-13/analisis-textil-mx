# =========================
# 1. IMPORTS
# =========================
import pandas as pd
import matplotlib.pyplot as plt

# =========================
# 2. CARGA DE DATOS
# =========================
df_conf = pd.read_excel("Indicadores20260503191827.xls", header=None)

# =========================
# 3. LIMPIEZA
# =========================
# asignar headers correctos
df_conf.columns = df_conf.iloc[5]

# eliminar filas basura iniciales
df_conf = df_conf[6:].reset_index(drop=True)

# filtrar solo confección (prendas)
df_conf = df_conf[df_conf["Indicador"].str.contains("prendas", na=False)]

# ⚠️ nos quedamos con una sola serie (la buena)
df_conf = df_conf.iloc[[0]]

# =========================
# 4. TRANSFORMACIÓN (LONG)
# =========================
df_conf_long = df_conf.melt(
    id_vars=["Indicador", "Área geográfica"],
    var_name="Fecha",
    value_name="Indice"
)

# limpiar valores
df_conf_long["Indice"] = pd.to_numeric(df_conf_long["Indice"], errors="coerce")
df_conf_long = df_conf_long.dropna(subset=["Indice"])

# extraer año
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
# 6. VISUALIZACIÓN
# =========================
plt.figure()

plt.plot(df_conf_trend["Año"], df_conf_trend["Indice"])

plt.title("Índice confección por año")
plt.xlabel("Año")
plt.ylabel("Índice")

plt.xticks(df_conf_trend["Año"])

plt.show()

# =========================
# 7. TABLA FINAL (PORTAFOLIO)
# =========================
df_tabla = df_conf_trend.copy()

# redondear
df_tabla["Indice"] = df_tabla["Indice"].round(1)

# variación anual
df_tabla["YoY %"] = df_tabla["Indice"].pct_change() * 100
df_tabla["YoY %"] = df_tabla["YoY %"].round(1)

# índice base 2019
base_2019 = df_tabla.loc[df_tabla["Año"] == 2019, "Indice"].values[0]
df_tabla["Index 2019=100"] = (df_tabla["Indice"] / base_2019) * 100
df_tabla["Index 2019=100"] = df_tabla["Index 2019=100"].round(1)

df_tabla
# Esto crea un archivo HTML con tu tabla estilizada
html_tabla = df_tabla.to_html(classes='table table-hover', index=False)

# Guardamos el archivo para descargarlo
with open("mi_analisis.html", "w") as f:
    f.write(f"<html><head><link rel='stylesheet' href='https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css'></head><body><div class='container'><h1>Análisis de Confección</h1>{html_tabla}</div></body></html>")
import plotly.express as px

fig = px.line(df_tabla, x="Año", y="Indice", title="Índice confección por año (Interactivo)", markers=True)
fig.show()

# Y lo mejor: lo puedes guardar como HTML interactivo
fig.write_html("grafica_pro.html")
