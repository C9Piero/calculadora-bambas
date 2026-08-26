import streamlit as st
import pandas as pd
import random
from supabase import create_client, Client

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(page_title="Aliados de la Circularidad", page_icon="🌱", layout="wide")

# --- SÚPER CSS (DISEÑO PREMIUM TIPO APP WEB) ---
st.markdown("""
    <style>
    /* Ocultar elementos nativos de Streamlit para un look limpio */
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Fondo general */
    .stApp { background-color: #F8FAFC; font-family: 'Inter', sans-serif; }
    
    /* Contenedores blancos tipo tarjeta con sombra suave */
    div[data-testid="stVerticalBlockBorderWrapper"] {
        background-color: #FFFFFF;
        border-radius: 20px !important;
        border: 1px solid #E2E8F0 !important;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.05), 0 8px 10px -6px rgba(0, 0, 0, 0.01);
        padding: 15px;
        transition: transform 0.2s ease-in-out;
    }
    
    /* Banner Superior Oscuro (El Dashboard Híbrido) */
    .dark-dashboard {
        background: linear-gradient(135deg, #0B132B 0%, #1C2541 100%);
        padding: 35px 20px;
        border-radius: 20px;
        box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.2);
        margin-bottom: 30px;
        color: white;
        display: flex;
        justify-content: space-around;
        align-items: center;
        flex-wrap: wrap;
        border-bottom: 4px solid #10B981;
    }
    .kpi-box {
        text-align: center;
        flex: 1;
        min-width: 180px;
        padding: 10px;
        border-right: 1px solid rgba(255,255,255,0.1);
    }
    .kpi-box:last-child { border-right: none; }
    
    .kpi-title {
        font-size: 0.85rem;
        color: #94A3B8;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        margin-bottom: 8px;
        font-weight: 700;
    }
    .kpi-value {
        font-size: 2.8rem;
        font-weight: 900;
        color: #10B981; /* Verde Esmeralda Vibrante */
        margin: 0;
        text-shadow: 0px 0px 15px rgba(16, 185, 129, 0.4);
    }
    .kpi-subtitle {
        font-size: 0.85rem;
        color: #E2E8F0;
        margin-top: 5px;
    }

    /* Estilo de los botones Primarios (Degradado Verde) */
    button[kind="primary"] {
        background: linear-gradient(90deg, #10B981 0%, #059669 100%) !important;
        color: white !important;
        border-radius: 12px !important;
        border: none !important;
        font-weight: 700 !important;
        font-size: 1.1rem !important;
        padding: 10px 0px !important;
        box-shadow: 0 4px 14px rgba(16, 185, 129, 0.4) !important;
        transition: all 0.3s ease !important;
    }
    button[kind="primary"]:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(16, 185, 129, 0.6) !important;
    }
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
    st.error(f"⚠️ No se pudo conectar con Supabase: {e}")
    st.stop()

# --- CATÁLOGO DE LAS BAMBAS ---
CATALOGO_MINA = {
    "👕 Camisa o Blusa de Trabajo (UV)": 5.0,
    "🦺 Chaleco de Seguridad (Alta Visibilidad)": 4.5,
    "👖 Pantalón Jean (Denim)": 5.9,
    "🧥 Casaca / Pantalón Térmico o Impermeable": 6.8,
    "🥼 Overol / Mameluco de Trabajo": 8.5,
    "🔥 Ropa Ignífuga (Anti Arco Eléctrico)": 7.5,
    "🧤 Ropa y Guantes de Cuero (Mandil, Casaca)": 9.5,
    "🧢 Accesorios Textiles (Cortavientos, Fundas)": 1.5,
    "🧗 Correas y Cintas de Poliéster (Arneses)": 2.0,
    "🖐️ Guantes de Algodón": 0.5
}

# --- VARIABLES DE SESIÓN ---
if "lista_prendas" not in st.session_state:
    st.session_state.lista_prendas = []

# --- ENCABEZADO CON IMAGEN RESTAURADA ---
st.image("https://images.unsplash.com/photo-1542601906990-b4d3fb778b09?auto=format&fit=crop&q=80&w=1200&h=350", use_container_width=True)

st.markdown("<h1 style='text-align: center; color: #0F172A; font-weight: 900; margin-top: 10px;'>Aliados de la Circularidad ♻️</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #64748B; font-size: 1.2rem; font-weight: 500;'>Plataforma de Impacto Comunitario — Pequeños Detalles & Mina Las Bambas</p>", unsafe_allow_html=True)
st.write("---")

# --- PESTAÑAS (TABS) MODERNAS ---
tab1, tab2 = st.tabs(["🌱 NUEVO APORTE COMUNITARIO", "📊 TABLERO DEL NEGOCIO (DASHBOARD)"])

with tab1:
    col_izq, spacer, col_der = st.columns([1.2, 0.1, 1])
    
    with col_izq:
        with st.container(border=True):
            st.markdown("<h4 style='color: #1E293B;'>👤 Datos del Participante</h4>", unsafe_allow_html=True)
            st.caption("Ingresa los datos para registrar el impacto a nombre de la comunidad.")
            nombre = st.text_input("Nombre completo")
            comunidad = st.selectbox("Selecciona tu comunidad", ["Comunidad A", "Comunidad B", "Comunidad C", "Otra"])
            
        with st.container(border=True):
            st.markdown("<h4 style='color: #1E293B;'>♻️ Añadir Prendas al Lote</h4>", unsafe_allow_html=True)
            prenda_sel = st.selectbox("Tipo de Uniforme / EPP:", list(CATALOGO_MINA.keys()))
            c_u, c_p = st.columns(2)
            unidades = c_u.number_input("Unidades a reciclar:", min_value=1, value=1, step=1)
            peso_kg = c_p.number_input("Peso Total (kg):", min_value=0.1, value=1.0, step=0.1)
            
            st.write("")
            if st.button("➕ Añadir prenda a la bolsa", use_container_width=True):
                st.session_state.lista_prendas.append({
                    "Prenda": prenda_sel, "Unidades": unidades, "Peso (kg)": peso_kg, "CO2_Factor": CATALOGO_MINA[prenda_sel]
                })

    with col_der:
        with st.container(border=True):
            st.markdown("<h4 style='color: #1E293B;'>📦 Resumen de tu Bolsa Actual</h4>", unsafe_allow_html=True)
            if st.session_state.lista_prendas:
                df_actual = pd.DataFrame(st.session_state.lista_prendas)
                st.dataframe(df_actual[["Prenda", "Unidades", "Peso (kg)"]], use_container_width=True, hide_index=True)
                
                c_btn1, c_btn2 = st.columns([1, 2.5])
                if c_btn1.button("🗑️ Vaciar", use_container_width=True):
                    st.session_state.lista_prendas = []
                    st.rerun()

                if c_btn2.button("🚀 CONFIRMAR Y CALCULAR", type="primary", use_container_width=True):
                    if not nombre:
                        st.error("⚠️ Por favor, ingresa el nombre del participante a la izquierda.")
                    else:
                        with st.spinner("Guardando registro en la base de datos..."):
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
                        
                        st.balloons()
                        
                        # --- PANEL OSCURO DE FELICITACIÓN ---
                        st.markdown(f"""
                            <div class="dark-dashboard" style="margin-top: 20px;">
                                <div style="width: 100%; text-align: center; margin-bottom: 20px;">
                                    <h3 style="color: white; margin: 0;">¡Registro Exitoso, {nombre.split()[0]}! 🎉</h3>
                                </div>
                                <div class="kpi-box">
                                    <div class="kpi-title">CO2 EVITADO</div>
                                    <div class="kpi-value">{co2_evitado:.1f} kg</div>
                                    <div class="kpi-subtitle">Impacto Ambiental</div>
                                </div>
                                <div class="kpi-box">
                                    <div class="kpi-title">MATERIAL RECUPERADO</div>
                                    <div class="kpi-value">{mat_recuperado:.2f} kg</div>
                                    <div class="kpi-subtitle">De {peso_total:.1f} kg procesados</div>
                                </div>
                                <div class="kpi-box">
                                    <div class="kpi-title">EQUIVALENCIA</div>
                                    <div class="kpi-value">🌳 {arboles}</div>
                                    <div class="kpi-subtitle">Árboles salvados</div>
                                </div>
                            </div>
                        """, unsafe_allow_html=True)
                        
                        st.session_state.lista_prendas = []
            else:
                st.info("🛒 Tu bolsa está vacía. Añade uniformes desde el panel izquierdo para calcular el impacto.")

with tab2:
    # LEER DE SUPABASE
    try:
        res = supabase.table("registro_comunitario").select("*").order("created_at", desc=True).execute()
        datos_supa = res.data
    except Exception:
        datos_supa = []
        
    if datos_supa:
        df_hist = pd.DataFrame(datos_supa)
        
        # --- TABLERO OSCURO PRINCIPAL (COMO TU IMAGEN) ---
        st.markdown(f"""
            <div class="dark-dashboard">
                <div class="kpi-box">
                    <div class="kpi-title">TOTAL PARTICIPANTES</div>
                    <div class="kpi-value">{len(df_hist)} 👤</div>
                    <div class="kpi-subtitle">Líderes comunitarios</div>
                </div>
                <div class="kpi-box">
                    <div class="kpi-title">UNIFORMES RECIBIDOS</div>
                    <div class="kpi-value">{df_hist['prendas_unid'].sum()} 📦</div>
                    <div class="kpi-subtitle">Prendas en total</div>
                </div>
                <div class="kpi-box">
                    <div class="kpi-title">MATERIAL RECUPERADO</div>
                    <div class="kpi-value">{df_hist['material_recuperado_kg'].sum():.1f} kg</div>
                    <div class="kpi-subtitle">Listo para Upcycling</div>
                </div>
                <div class="kpi-box">
                    <div class="kpi-title">CO2 EVITADO NETO</div>
                    <div class="kpi-value">{df_hist['co2_evitado_kg'].sum():.1f} kg</div>
                    <div class="kpi-subtitle">Impacto ambiental global</div>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        col_graf, col_tabla = st.columns([1, 1.8])
        
        with col_graf:
            with st.container(border=True):
                st.markdown("<h5 style='color: #0F172A;'>📈 Impacto por Comunidad (kg CO2)</h5>", unsafe_allow_html=True)
                df_grafico = df_hist.groupby("comunidad")["co2_evitado_kg"].sum().reset_index()
                st.bar_chart(df_grafico.set_index("comunidad"), color="#10B981")
                
        with col_tabla:
            with st.container(border=True):
                st.markdown("<h5 style='color: #0F172A;'>📋 Desglose de Operaciones</h5>", unsafe_allow_html=True)
                df_vista = df_hist[["created_at", "nombre", "comunidad", "prendas_unid", "material_recuperado_kg", "co2_evitado_kg"]].copy()
                df_vista["created_at"] = pd.to_datetime(df_vista["created_at"]).dt.strftime('%d/%m/%Y')
                df_vista.columns = ["Fecha", "Nombre", "Comunidad", "Unid.", "Recuperado (kg)", "CO2 (kg)"]
                
                # Tabla elegante
                st.dataframe(df_vista, use_container_width=True, hide_index=True, height=250)
                
                csv = df_vista.to_csv(index=False).encode('utf-8')
                st.download_button("📥 Exportar Reporte a Excel (CSV)", data=csv, file_name="reporte_las_bambas.csv", mime="text/csv")
    else:
        st.info("Aún no hay registros en la base de datos. ¡Sé el primero en registrar un aporte!")
