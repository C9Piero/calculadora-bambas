import streamlit as st
import pandas as pd
import random
from supabase import create_client, Client

# --- CONFIGURACIÓN DE LA PÁGINA (WIDE PARA MODO DASHBOARD) ---
st.set_page_config(page_title="Aliados de la Circularidad", page_icon="🌱", layout="wide")

# --- ESTILOS CSS (DISEÑO TIPO DASHBOARD) ---
st.markdown("""
    <style>
    /* Ocultar elementos nativos de Streamlit */
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Tipografía y fondo general */
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    .stApp { background-color: #F1F5F9; }
    
    /* Panel Oscuro Superior (KPIs Principales) */
    .dark-dashboard {
        background: linear-gradient(135deg, #0F172A 0%, #1E293B 100%);
        padding: 30px;
        border-radius: 16px;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
        margin-bottom: 25px;
        color: white;
        display: flex;
        justify-content: space-between;
        align-items: center;
        flex-wrap: wrap;
    }
    .kpi-box {
        text-align: center;
        flex: 1;
        min-width: 150px;
        margin: 10px;
    }
    .kpi-title {
        font-size: 0.75rem;
        color: #94A3B8;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 5px;
        font-weight: 600;
    }
    .kpi-value {
        font-size: 2.2rem;
        font-weight: 800;
        color: #34D399; /* Verde esmeralda brillante */
        margin: 0;
    }
    .kpi-subtitle {
        font-size: 0.8rem;
        color: #CBD5E1;
        margin-top: 5px;
    }
    
    /* Tarjetas Blancas (Formularios y Detalles) */
    div[data-testid="stVerticalBlockBorderWrapper"] {
        background-color: #FFFFFF;
        border-radius: 16px !important;
        border: 1px solid #E2E8F0 !important;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        padding: 10px;
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

# --- ENCABEZADO ---
st.markdown("<h2 style='color: #0F172A; font-weight: 800;'>Aliados de la Circularidad ♻️</h2>", unsafe_allow_html=True)
st.markdown("<p style='color: #64748B; font-size: 1.1rem;'>Tablero de Impacto Comunitario - Pequeños Detalles & Mina Las Bambas</p>", unsafe_allow_html=True)
st.write("")

# --- PESTAÑAS (TABS) ---
tab1, tab2 = st.tabs(["🌱 Registro de Aportes", "📊 Tablero del Negocio (Historial)"])

with tab1:
    col_izq, col_der = st.columns([1, 1.5])
    
    with col_izq:
        with st.container(border=True):
            st.markdown("#### 👤 Datos del Participante")
            nombre = st.text_input("Nombre completo")
            comunidad = st.selectbox("Comunidad", ["Comunidad A", "Comunidad B", "Comunidad C", "Otra"])
            
        with st.container(border=True):
            st.markdown("#### ♻️ Añadir prendas")
            prenda_sel = st.selectbox("Tipo de Uniforme:", list(CATALOGO_MINA.keys()))
            c_u, c_p = st.columns(2)
            unidades = c_u.number_input("Unidades:", min_value=1, value=1, step=1)
            peso_kg = c_p.number_input("Peso (kg):", min_value=0.1, value=1.0, step=0.1)
            
            if st.button("➕ Añadir al lote", use_container_width=True):
                st.session_state.lista_prendas.append({
                    "Prenda": prenda_sel, "Unidades": unidades, "Peso (kg)": peso_kg, "CO2_Factor": CATALOGO_MINA[prenda_sel]
                })

    with col_der:
        with st.container(border=True):
            st.markdown("#### 📦 Lote Actual a Registrar")
            if st.session_state.lista_prendas:
                df_actual = pd.DataFrame(st.session_state.lista_prendas)
                st.dataframe(df_actual[["Prenda", "Unidades", "Peso (kg)"]], use_container_width=True, hide_index=True)
                
                c_btn1, c_btn2 = st.columns([1, 3])
                if c_btn1.button("🗑️ Vaciar", use_container_width=True):
                    st.session_state.lista_prendas = []
                    st.rerun()

                if c_btn2.button("🚀 Confirmar y Calcular Impacto", type="primary", use_container_width=True):
                    if not nombre:
                        st.error("⚠️ Falta el nombre del participante.")
                    else:
                        with st.spinner("Guardando registro en Supabase..."):
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
                        # DASHBOARD OSCURO DE RESULTADO
                        st.markdown(f"""
                            <div class="dark-dashboard">
                                <div class="kpi-box">
                                    <div class="kpi-title">CO2 EVITADO</div>
                                    <div class="kpi-value">{co2_evitado:.1f} kg</div>
                                    <div class="kpi-subtitle">Impacto Ambiental Neto</div>
                                </div>
                                <div class="kpi-box">
                                    <div class="kpi-title">MATERIAL RECUPERADO</div>
                                    <div class="kpi-value">{mat_recuperado:.2f} kg</div>
                                    <div class="kpi-subtitle">De {peso_total:.1f} kg totales</div>
                                </div>
                                <div class="kpi-box">
                                    <div class="kpi-title">EQUIVALENCIA ÁRBOLES</div>
                                    <div class="kpi-value">🌳 {arboles}</div>
                                    <div class="kpi-subtitle">Absorción anual</div>
                                </div>
                                <div class="kpi-box">
                                    <div class="kpi-title">AHORRO HÍDRICO</div>
                                    <div class="kpi-value">💧 {agua:,} L</div>
                                    <div class="kpi-subtitle">Agua preservada</div>
                                </div>
                            </div>
                        """, unsafe_allow_html=True)
                        st.success(f"¡Excelente {nombre.split()[0]}! Tu aporte ha sido registrado con éxito en la base de datos.")
                        st.session_state.lista_prendas = []
            else:
                st.info("La bolsa de reciclaje está vacía. Añade prendas desde el panel izquierdo.")

with tab2:
    # LEER DE SUPABASE
    try:
        res = supabase.table("registro_comunitario").select("*").order("created_at", desc=True).execute()
        datos_supa = res.data
    except Exception:
        datos_supa = []
        
    if datos_supa:
        df_hist = pd.DataFrame(datos_supa)
        
        # TABLERO OSCURO (Como la imagen)
        st.markdown(f"""
            <div class="dark-dashboard">
                <div class="kpi-box">
                    <div class="kpi-title">TOTAL PARTICIPANTES</div>
                    <div class="kpi-value">👥 {len(df_hist)}</div>
                    <div class="kpi-subtitle">Personas involucradas</div>
                </div>
                <div class="kpi-box">
                    <div class="kpi-title">PRENDAS RECIBIDAS</div>
                    <div class="kpi-value">📦 {df_hist['prendas_unid'].sum()}</div>
                    <div class="kpi-subtitle">Unidades totales</div>
                </div>
                <div class="kpi-box">
                    <div class="kpi-title">MAT. RECUPERADO EST.</div>
                    <div class="kpi-value">♻️ {df_hist['material_recuperado_kg'].sum():.1f} kg</div>
                    <div class="kpi-subtitle">Tasa éxito ~88%</div>
                </div>
                <div class="kpi-box">
                    <div class="kpi-title">CO2 EVITADO TOTAL</div>
                    <div class="kpi-value">🌍 {df_hist['co2_evitado_kg'].sum():.1f} kg</div>
                    <div class="kpi-subtitle">Mitigación global</div>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        col_graf, col_tabla = st.columns([1, 1.5])
        
        with col_graf:
            with st.container(border=True):
                st.markdown("#### 📈 Aportes por Comunidad (kg CO2)")
                # Agrupar datos para el gráfico
                df_grafico = df_hist.groupby("comunidad")["co2_evitado_kg"].sum().reset_index()
                st.bar_chart(df_grafico.set_index("comunidad"), color="#10B981")
                
        with col_tabla:
            with st.container(border=True):
                st.markdown("#### 📋 Detalle de Operaciones")
                df_vista = df_hist[["created_at", "nombre", "comunidad", "prendas_unid", "material_recuperado_kg", "co2_evitado_kg"]].copy()
                df_vista["created_at"] = pd.to_datetime(df_vista["created_at"]).dt.strftime('%d/%m')
                df_vista.columns = ["Fecha", "Nombre", "Comunidad", "Unid.", "Recuperado (kg)", "CO2 (kg)"]
                st.dataframe(df_vista, use_container_width=True, hide_index=True)
                
                csv = df_vista.to_csv(index=False).encode('utf-8')
                st.download_button("📥 Exportar Reporte", data=csv, file_name="reporte_bambas.csv", mime="text/csv")
    else:
        st.info("Aún no hay registros en la base de datos.")
