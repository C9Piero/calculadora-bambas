import streamlit as st
import pandas as pd
import random
from supabase import create_client, Client

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(page_title="Aliados de la Circularidad", page_icon="🌱", layout="centered")

# --- CSS: ESTILO MODERNO Y LIMPIO ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    
    /* Ocultar menú nativo */
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Fuente y fondo general */
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    .stApp { background-color: #F8FAFC; }
    
    /* Contenedores con borde */
    div[data-testid="stVerticalBlockBorderWrapper"] {
        background-color: #FFFFFF;
        border-radius: 12px !important;
        border: 1px solid #E2E8F0 !important;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        padding: 15px;
    }

    /* Tarjeta de Resultado */
    .resultado-card {
        background-color: #FFFFFF;
        border-left: 6px solid #10B981;
        border-radius: 8px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        padding: 25px;
        text-align: center;
        margin-top: 15px;
        margin-bottom: 15px;
    }
    .metric-label { font-size: 1rem; color: #64748B; font-weight: 500; margin-bottom: 5px; }
    .metric-big { font-size: 2.4rem; font-weight: 800; color: #0F172A; margin: 0; line-height: 1.1; }
    .metric-green { color: #10B981; }
    </style>
""", unsafe_allow_html=True)

# --- CONEXIÓN A SUPABASE ---
@st.cache_resource
def init_supabase() -> Client:
    url = st.secrets["supabase"]["SUPABASE_URL"]
    key = st.secrets["supabase"]["SUPABASE_KEY"]
    return create_client(url, key)

try:
    supabase = init_supabase()
except Exception as e:
    st.error(f"Error de conexión con Supabase: {e}")
    st.stop()

# --- CATÁLOGO DE LAS BAMBAS (SIN EMOJIS) ---
CATALOGO_MINA = {
    "Camisa o Blusa de Trabajo (UV)": 5.0,
    "Chaleco de Seguridad (Alta Visibilidad)": 4.5,
    "Pantalón Jean (Denim)": 5.9,
    "Casaca / Pantalón Térmico o Impermeable": 6.8,
    "Overol / Mameluco de Trabajo": 8.5,
    "Ropa Ignífuga (Anti Arco Eléctrico)": 7.5,
    "Ropa y Guantes de Cuero (Mandil, Casaca)": 9.5,
    "Accesorios Textiles (Cortavientos, Fundas)": 1.5,
    "Correas y Cintas de Poliéster (Arneses)": 2.0,
    "Guantes de Algodón": 0.5
}

# --- VARIABLES DE SESIÓN ---
if "lista_prendas" not in st.session_state:
    st.session_state.lista_prendas = []

# --- ENCABEZADO ---
st.image("https://images.unsplash.com/photo-1542601906990-b4d3fb778b09?auto=format&fit=crop&q=80&w=1200&h=350", use_container_width=True)

st.markdown("<h2 style='text-align: center; color: #0F172A; font-weight: 800;'>Aliados de la Circularidad</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #64748B; font-size: 1.1rem;'><b>Pequeños Detalles & Mina Las Bambas</b></p>", unsafe_allow_html=True)
st.write("---")

# --- PESTAÑAS (TABS) ---
tab1, tab2 = st.tabs(["Registro Comunitario", "Historial de Aportes"])

with tab1:
    with st.container(border=True):
        st.markdown("<h4 style='color: #1E293B;'>Datos del Participante</h4>", unsafe_allow_html=True)
        nombre = st.text_input("¿Cuál es tu nombre completo?")
        comunidad = st.selectbox("¿A qué comunidad perteneces?", ["Comunidad A", "Comunidad B", "Comunidad C", "Otra"])

    st.write("")
    
    with st.container(border=True):
        st.markdown("<h4 style='color: #1E293B;'>¿Qué prendas vamos a reciclar?</h4>", unsafe_allow_html=True)
        prenda_sel = st.selectbox("Selecciona el tipo de Uniforme / EPP:", list(CATALOGO_MINA.keys()))
        col_u, col_p = st.columns(2)
        unidades = col_u.number_input("Unidades:", min_value=1, value=1, step=1)
        peso_kg = col_p.number_input("Peso Total (kg):", min_value=0.1, value=1.0, step=0.1)
        
        st.write("")
        if st.button("Añadir a mi bolsa", use_container_width=True):
            st.session_state.lista_prendas.append({
                "Prenda": prenda_sel, "Unidades": unidades, "Peso (kg)": peso_kg, "CO2_Factor": CATALOGO_MINA[prenda_sel]
            })

    # Mostrar la bolsa
    if st.session_state.lista_prendas:
        st.write("")
        st.markdown("<h4 style='color: #1E293B;'>Tu Bolsa Actual</h4>", unsafe_allow_html=True)
        df_actual = pd.DataFrame(st.session_state.lista_prendas)
        st.dataframe(df_actual[["Prenda", "Unidades", "Peso (kg)"]], use_container_width=True, hide_index=True)
        
        col_vaciar, col_calc = st.columns([1, 2.5])
        if col_vaciar.button("Vaciar bolsa"):
            st.session_state.lista_prendas = []
            st.rerun()

        if col_calc.button("Registrar y Calcular Impacto", type="primary", use_container_width=True):
            if not nombre:
                st.error("Por favor, ingresa tu nombre en la parte superior.")
            else:
                with st.spinner("Guardando registro de forma segura..."):
                    peso_total = sum(item["Peso (kg)"] for item in st.session_state.lista_prendas)
                    unid_total = sum(item["Unidades"] for item in st.session_state.lista_prendas)
                    co2_evitado = sum(item["Peso (kg)"] * item["CO2_Factor"] for item in st.session_state.lista_prendas)
                    
                    mat_recuperado = peso_total * random.uniform(0.85, 0.92)
                    arboles = max(1, int(co2_evitado / 22))
                    agua = int(peso_total * 2500)

                    # GUARDAR EN SUPABASE
                    try:
                        supabase.table("registro_comunitario").insert({
                            "nombre": nombre, "comunidad": comunidad, "prendas_unid": int(unid_total),
                            "peso_kg": round(float(peso_total), 2), "material_recuperado_kg": round(float(mat_recuperado), 2),
                            "co2_evitado_kg": round(float(co2_evitado), 2)
                        }).execute()
                    except Exception as e:
                        st.error(f"Error de conexión: {e}")
                
                # TARJETA DE RESULTADO LIMPIA Y ELEGANTE
                st.markdown(f"""
                    <div class="resultado-card">
                        <p class="metric-label">¡Gracias {nombre.split()[0]}! Has evitado la emisión de:</p>
                        <p class="metric-big"><span class="metric-green">{co2_evitado:.1f} kg</span> de CO2</p>
                        <p style="color: #64748B; margin-top: 15px; font-size: 0.95rem;">
                            Logramos recuperar <b>{mat_recuperado:.2f} kg</b> de material útil para nuevos productos.
                        </p>
                    </div>
                """, unsafe_allow_html=True)
                
                st.write("")
                col_i1, col_i2 = st.columns(2)
                with col_i1:
                    st.info(f"**{arboles} Árboles**\n\nEquivale al CO2 que absorberían en un año entero.")
                with col_i2:
                    st.info(f"**{agua:,} Litros**\n\nDe agua ahorrada al no fabricar textiles nuevos.")
                
                st.session_state.lista_prendas = []

with tab2:
    st.markdown("<h4 style='color: #1E293B;'>Registro General</h4>", unsafe_allow_html=True)
    
    # LEER DE SUPABASE
    try:
        res = supabase.table("registro_comunitario").select("*").order("created_at", desc=True).execute()
        datos_supa = res.data
    except Exception:
        datos_supa = []
        
    if datos_supa:
        df_hist = pd.DataFrame(datos_supa)
        
        # MÉTRICAS ESTILO NATIVO DE STREAMLIT
        c1, c2, c3 = st.columns(3)
        c1.metric("Participantes", f"{len(df_hist)}")
        c2.metric("Prendas", f"{df_hist['prendas_unid'].sum()}")
        c3.metric("CO2 Evitado", f"{df_hist['co2_evitado_kg'].sum():.1f} kg")
        
        st.write("---")
        df_vista = df_hist[["created_at", "nombre", "comunidad", "prendas_unid", "material_recuperado_kg", "co2_evitado_kg"]].copy()
        df_vista["created_at"] = pd.to_datetime(df_vista["created_at"]).dt.strftime('%d/%m/%y')
        df_vista.columns = ["Fecha", "Nombre", "Comunidad", "Unid.", "Recuperado (kg)", "CO2 (kg)"]
        
        st.dataframe(df_vista, use_container_width=True, hide_index=True)
        
        csv = df_vista.to_csv(index=False).encode('utf-8')
        st.download_button("Descargar Reporte (Excel)", data=csv, file_name="reporte_las_bambas.csv", mime="text/csv")
    else:
        st.info("Aún no hay registros en la base de datos.")
