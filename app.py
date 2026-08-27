import streamlit as st
import pandas as pd
import random
from supabase import create_client, Client

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(page_title="Aliados de la Circularidad", page_icon="🌱", layout="centered")

# --- CSS: ESTILO MODERNO AZUL / NEUTRO ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');

    /* Ocultar menú nativo */
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}

    /* Fuente y fondo general con gradiente sutil */
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    .stApp { background: linear-gradient(180deg, #EEF3FB 0%, #F7F9FC 320px, #F7F9FC 100%); }
    .block-container { padding-top: 1.5rem; max-width: 760px; }

    /* ===== HERO ===== */
    .hero-wrap {
        position: relative; border-radius: 20px; overflow: hidden; margin-bottom: 8px;
        box-shadow: 0 10px 30px -10px rgba(15, 42, 74, 0.25);
    }
    .hero-wrap img { display: block; width: 100%; height: 220px; object-fit: cover; filter: saturate(1.05); }
    .hero-overlay {
        position: absolute; inset: 0; background: linear-gradient(180deg, rgba(10,25,50,0.15) 0%, rgba(8,20,45,0.75) 100%);
        display: flex; flex-direction: column; justify-content: flex-end; padding: 22px 26px;
    }
    .hero-eyebrow {
        display: inline-block; align-self: flex-start; background: rgba(255,255,255,0.16);
        backdrop-filter: blur(6px); color: #EAF1FF; font-size: 0.72rem; font-weight: 700;
        letter-spacing: 0.08em; text-transform: uppercase; padding: 5px 12px; border-radius: 999px;
        margin-bottom: 10px; border: 1px solid rgba(255,255,255,0.25);
    }
    .hero-title { color: #FFFFFF; font-size: 1.7rem; font-weight: 800; letter-spacing: -0.5px; margin: 0; line-height: 1.2; }
    .hero-subtitle { color: #D7E4FA; font-size: 0.95rem; font-weight: 500; margin-top: 4px; }

    /* Divisor sutil en vez de línea dura */
    hr { border: none !important; border-top: 1px solid #E3E9F2 !important; margin: 1.6rem 0 !important; }

    /* Contenedores con borde -> tarjetas flotantes */
    div[data-testid="stVerticalBlockBorderWrapper"] {
        background-color: #FFFFFF; border-radius: 16px !important; border: 1px solid #EBEFF5 !important;
        box-shadow: 0 6px 20px -8px rgba(15, 42, 74, 0.10); padding: 20px; transition: box-shadow 0.2s ease;
    }

    /* Subtítulos dentro de tarjetas, con acento lateral */
    h4 { color: #14304F !important; font-weight: 700 !important; font-size: 1.05rem !important; display: flex; align-items: center; gap: 8px; margin-bottom: 14px !important; }
    h4::before { content: ""; width: 4px; height: 18px; background: linear-gradient(180deg, #2563EB, #60A5FA); border-radius: 3px; display: inline-block; }

    /* Labels de inputs */
    label p { font-weight: 600 !important; color: #3D4C63 !important; font-size: 0.88rem !important; }

    /* Inputs y selects */
    div[data-baseweb="select"] > div, div[data-baseweb="input"] > div, .stNumberInput input, .stTextInput input {
        border-radius: 10px !important; border: 1px solid #DCE4EF !important; background-color: #FBFCFE !important;
    }
    div[data-baseweb="select"] > div:focus-within, .stTextInput input:focus, .stNumberInput input:focus {
        border-color: #2563EB !important; box-shadow: 0 0 0 3px #2563EB1F !important; background-color: #FFFFFF !important;
    }

    /* Botones generales */
    .stButton > button {
        border-radius: 10px; border: 1px solid #DCE4EF; background-color: #FFFFFF; color: #1B3A5C;
        font-weight: 600; transition: all 0.15s ease;
    }
    .stButton > button:hover { border-color: #2563EB; color: #2563EB; background-color: #F0F5FE; transform: translateY(-1px); }

    /* Botón primario (Registrar y Calcular) */
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #2563EB, #1D4ED8); border: none; color: #FFFFFF;
        box-shadow: 0 6px 16px -4px rgba(29, 78, 216, 0.45); font-weight: 700;
    }
    .stButton > button[kind="primary"]:hover { box-shadow: 0 8px 20px -4px rgba(29, 78, 216, 0.55); transform: translateY(-1px); color: #FFFFFF; }

    /* Tabs estilo pill */
    div[role="tablist"] { gap: 4px !important; background-color: #E9EFF8 !important; padding: 5px !important; border-radius: 12px !important; border: 1px solid #E1E8F0 !important; width: fit-content; }
    [role="tab"] { border-radius: 9px !important; padding: 8px 18px !important; color: #5B6B82 !important; font-weight: 600 !important; background-color: transparent !important; border: none !important; box-shadow: none !important; text-decoration: none !important; }
    [role="tab"] p, [role="tab"] div, [role="tab"] span { color: inherit !important; font-weight: 600 !important; text-decoration: none !important; }
    [role="tab"][aria-selected="true"] { color: #1D4ED8 !important; background-color: #FFFFFF !important; box-shadow: 0 2px 8px -2px rgba(15, 42, 74, 0.15) !important; }
    div[role="tablist"]::after, [role="tab"]::after, [role="tab"]::before { background-color: transparent !important; background: none !important; border-color: transparent !important; box-shadow: none !important; height: 0 !important; content: none !important; }
    div[role="tablist"] > div:not([role="tab"]) { display: none !important; }

    /* Dataframe y Métricas nativas */
    div[data-testid="stDataFrame"] { border-radius: 12px; overflow: hidden; border: 1px solid #E1E8F0; }
    div[data-testid="stMetric"] { background-color: #FFFFFF; border: 1px solid #EBEFF5; border-radius: 14px; padding: 14px 10px; box-shadow: 0 4px 12px -4px rgba(15, 42, 74, 0.08); }
    div[data-testid="stMetricLabel"] { color: #5B6B82; }
    div[data-testid="stMetricValue"] { color: #0F2A4A; font-weight: 800; }
    div[data-testid="stAlertContainer"] { background-color: #F0F5FE; border: 1px solid #D3E0F5; border-radius: 12px; }

    /* Tarjeta de Resultado */
    .resultado-card {
        background: linear-gradient(180deg, #FFFFFF 0%, #F8FAFF 100%); border: 1px solid #E1E8F0;
        border-top: 4px solid #2563EB; border-radius: 16px; box-shadow: 0 10px 24px -8px rgba(15, 42, 74, 0.15);
        padding: 28px 25px; text-align: center; margin-top: 15px; margin-bottom: 15px;
    }
    .metric-label { font-size: 0.95rem; color: #5B6B82; font-weight: 500; margin-bottom: 6px; }
    .metric-big { font-size: 2.6rem; font-weight: 800; color: #0F2A4A; margin: 0; line-height: 1.1; letter-spacing: -1px; }
    .metric-blue { color: #1D4ED8; }
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

# --- CATÁLOGO DE LAS BAMBAS ---
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

# --- CARGAR COMUNIDADES DESDE SUPABASE ---
def cargar_comunidades():
    try:
        res = supabase.table("catalogos").select("nombre").eq("tipo", "comunidades_bambas").execute()
        if res.data:
            return sorted([item["nombre"] for item in res.data])
    except Exception:
        pass
    return ["Comunidad Base A", "Comunidad Base B"] # Valores por defecto si la base está vacía

opciones_comunidades = cargar_comunidades()
if "Otra / No especificada" not in opciones_comunidades:
    opciones_comunidades.append("Otra / No especificada")

# --- VARIABLES DE SESIÓN ---
if "lista_prendas" not in st.session_state:
    st.session_state.lista_prendas = []

# --- ENCABEZADO (HERO) ---
st.markdown("""
    <div class="hero-wrap">
        <img src="https://images.unsplash.com/photo-1542601906990-b4d3fb778b09?auto=format&fit=crop&q=80&w=1200&h=440" />
        <div class="hero-overlay">
            <span class="hero-eyebrow">Economía Circular</span>
            <p class="hero-title">Aliados de la Circularidad</p>
            <p class="hero-subtitle">Pequeños Detalles &amp; Mina Las Bambas</p>
        </div>
    </div>
""", unsafe_allow_html=True)

st.write("")

# --- PESTAÑAS (TABS) ---
tab1, tab2 = st.tabs(["Registro Comunitario", "Historial de Aportes"])

with tab1:
    with st.container(border=True):
        st.markdown("<h4>Datos del Participante</h4>", unsafe_allow_html=True)
        nombre = st.text_input("¿Cuál es tu nombre completo?")
        comunidad = st.selectbox("¿A qué comunidad perteneces?", opciones_comunidades)

    st.write("")
    
    with st.container(border=True):
        st.markdown("<h4>¿Qué prendas vamos a reciclar?</h4>", unsafe_allow_html=True)
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
        st.markdown("<h4>Tu Bolsa Actual</h4>", unsafe_allow_html=True)
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
                        <p class="metric-big"><span class="metric-blue">{co2_evitado:.1f} kg</span> de CO2</p>
                        <p style="color: #5B6B82; margin-top: 15px; font-size: 0.95rem;">
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

    # --- PANEL ADMINISTRATIVO OCULTO ---
    st.write("---")
    with st.expander("⚙️ Administrar Comunidades (Solo Coordinadores)"):
        st.markdown("<p style='font-size: 0.85rem; color: #5B6B82;'>Ingresa la contraseña para agregar o eliminar comunidades de la lista.</p>", unsafe_allow_html=True)
        pwd_input = st.text_input("Contraseña:", type="password", key="admin_pwd")
        
        # Contraseña configurada por defecto
        if pwd_input == "Bambas2026":
            st.success("Acceso autorizado")
            
            c_add, c_del = st.columns(2)
            with c_add:
                nueva_comunidad = st.text_input("Nueva comunidad:")
                if st.button("➕ Agregar"):
                    if nueva_comunidad.strip():
                        try:
                            supabase.table("catalogos").insert({"tipo": "comunidades_bambas", "nombre": nueva_comunidad.strip(), "valor_num": 0}).execute()
                            st.toast("✅ Comunidad agregada a la nube")
                            st.rerun()
                        except Exception as e:
                            st.error(f"Error: {e}")
                            
            with c_del:
                comunidades_borrables = [c for c in opciones_comunidades if "Otra" not in c]
                comunidad_borrar = st.selectbox("Comunidad a eliminar:", comunidades_borrables)
                if st.button("🗑️ Eliminar"):
                    if comunidad_borrar:
                        try:
                            supabase.table("catalogos").delete().eq("tipo", "comunidades_bambas").eq("nombre", comunidad_borrar).execute()
                            st.toast("🗑️ Comunidad eliminada")
                            st.rerun()
                        except Exception as e:
                            st.error(f"Error: {e}")
        elif pwd_input != "":
            st.error("❌ Contraseña incorrecta")

with tab2:
    st.markdown("<h4>Registro General</h4>", unsafe_allow_html=True)
    
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
