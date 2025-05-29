import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

#Quise hacer está práctica con colores que me gustan y que son muy lindos para darle variación a las regiones y hacerlo atractivo, por lo que elegí estos colores
pastel_bg = "#ffeef7"
pink_accent = "#ffa4bc"
mint_pastel = "#b4f8c8"
lilac_pastel = "#caa8f5"
sky_pastel = "#b2e0f7"
grey_text = "#495057"

#personalizar textos (tuve que investigar esto)
st.markdown(f"""
    <style>
        .stApp {{
            background-color: {pastel_bg};
        }}
        .block-container {{
            background-color: {pastel_bg} !important;
        }}
        h1, h2, h3, .stMarkdown > p, .stTable th, .stSelectbox label {{
            color: {pink_accent} !important;
        }}
        .stDataFrame thead tr th {{
            background-color: {pink_accent} !important;
            color: #fff !important;
        }}
        .stButton>button, .stSelectbox>div>div>div>div {{
            background-color: {lilac_pastel} !important;
            color: {grey_text} !important;
            border-radius: 10px !important;
        }}
        .vendedor-section .stMarkdown > p {{
            color: #111 !important;
            font-weight: bold;
        }}
    </style>
""", unsafe_allow_html=True)

#Primero cargamos lo que es la base de datos proporcionada por el profesor
@st.cache_data
def load_data():
    df = pd.read_excel("sellers.xlsx")
    return df

df = load_data()

st.title("Testing Streamlit Homework  (˶ᵔ ᵕ ᵔ˶)") #Título

# Aquí filtramos las regiones.
st.header("1. Filtrar tabla por región")
regions = ["Todos"] + sorted(df["REGION"].unique().tolist())
selected_region = st.selectbox("Selecciona una región", regions, key="region_filter")

if selected_region != "Todos":
    filtered_df = df[df["REGION"] == selected_region].copy()
else:
    filtered_df = df.copy()

st.dataframe(filtered_df, use_container_width=True)

# Datos por Vendedor pero filtrado por nombre y apellido
st.header("2. Ver datos de un vendedor específico")
# Crear columna de nombre completo (en ambos df)
df["NOMBRE_COMPLETO"] = df["NOMBRE"].astype(str) + " " + df["APELLIDO"].astype(str)
filtered_df["NOMBRE_COMPLETO"] = filtered_df["NOMBRE"].astype(str) + " " + filtered_df["APELLIDO"].astype(str)

nombres_vendedores = ["Todos"] + sorted(filtered_df["NOMBRE_COMPLETO"].unique())
selected_nombre = st.selectbox("Selecciona el nombre del vendedor", nombres_vendedores, key="vendedor_nombre")

if selected_nombre != "Todos":
    vendedor_data = filtered_df[filtered_df["NOMBRE_COMPLETO"] == selected_nombre]
else:
    vendedor_data = filtered_df

with st.container():
    st.markdown('<div class="vendedor-section">**Datos del vendedor:**</div>', unsafe_allow_html=True)
    if not vendedor_data.empty:
        st.dataframe(
            vendedor_data[["NOMBRE", "APELLIDO", "REGION", "SALARIO", "UNIDADES VENDIDAS", "VENTAS TOTALES", "PORCENTAJE DE VENTAS"]],
            use_container_width=True
        )

# Filtro para gráficas (por región y vendedor)
st.header("3. Gráficas de ventas filtradas")
st.markdown("Puedes filtrar por región y/o por vendedor para ver los resultados en las gráficas:")

# Filtros para las gráficas (pueden ser iguales a los anteriores pero independientes si quieres)
region_graficas = st.selectbox("Selecciona una región para las gráficas", regions, key="region_graficas")
if region_graficas != "Todos":
    df_graf = df[df["REGION"] == region_graficas].copy()
else:
    df_graf = df.copy()

nombres_graficas = ["Todos"] + sorted(df_graf["NOMBRE_COMPLETO"].unique())
nombre_grafica = st.selectbox("Selecciona el vendedor para las gráficas", nombres_graficas, key="nombre_grafica")

if nombre_grafica != "Todos":
    df_graf = df_graf[df_graf["NOMBRE_COMPLETO"] == nombre_grafica]

# Si hay datos, mostramos las gráficas, si no, mostramos un mensajito cute
if not df_graf.empty:
    # Unidades Vendidas por Región (o por vendedor)
    summary = df_graf.groupby("REGION").agg(
        UNIDADES_VENDIDAS=("UNIDADES VENDIDAS", "sum"),
        VENTAS_TOTALES=("VENTAS TOTALES", "sum"),
        PROMEDIO_VENTAS=("VENTAS TOTALES", "mean")
    ).reset_index()

    with st.container():
        st.subheader("Unidades vendidas por región")
        fig, ax = plt.subplots()
        bars = ax.bar(summary["REGION"], summary["UNIDADES_VENDIDAS"],
                      color=[pink_accent, lilac_pastel, sky_pastel, mint_pastel][:len(summary)], edgecolor="#fff")
        ax.set_ylabel("Unidades vendidas", color=pink_accent)
        ax.set_xlabel("Región", color=pink_accent)
        ax.set_title("Unidades vendidas por región", color=pink_accent)
        ax.set_facecolor(pastel_bg)
        fig.patch.set_facecolor(pastel_bg)
        ax.tick_params(colors=pink_accent)
        st.pyplot(fig)

    with st.container():
        st.subheader("Ventas totales por región")
        fig, ax = plt.subplots()
        bars = ax.bar(summary["REGION"], summary["VENTAS_TOTALES"],
                      color=[lilac_pastel, pink_accent, mint_pastel, sky_pastel][:len(summary)], edgecolor="#fff")
        ax.set_ylabel("Ventas totales", color=pink_accent)
        ax.set_xlabel("Región", color=pink_accent)
        ax.set_title("Ventas totales por región", color=pink_accent)
        ax.set_facecolor(pastel_bg)
        fig.patch.set_facecolor(pastel_bg)
        ax.tick_params(colors=pink_accent)
        st.pyplot(fig)

    with st.container():
        st.subheader("Promedio de ventas por región")
        fig, ax = plt.subplots()
        bars = ax.bar(summary["REGION"], summary["PROMEDIO_VENTAS"],
                      color=[mint_pastel, sky_pastel, pink_accent, lilac_pastel][:len(summary)], edgecolor="#fff")
        ax.set_ylabel("Promedio de ventas", color=pink_accent)
        ax.set_xlabel("Región", color=pink_accent)
        ax.set_title("Promedio de ventas por región", color=pink_accent)
        ax.set_facecolor(pastel_bg)
        fig.patch.set_facecolor(pastel_bg)
        ax.tick_params(colors=pink_accent)
        st.pyplot(fig)
else:
    st.markdown('<div style="color:#bf4270;font-size:20px;font-weight:bold;">No hay datos para el filtro seleccionado (╥﹏╥)</div>', unsafe_allow_html=True)

st.markdown(f"<br><hr><center style='color:{pink_accent};'>Andrea Alvarado A00836907, Testing Streamlit (๑˃ᴗ˂)ﻭ</center>", unsafe_allow_html=True)
