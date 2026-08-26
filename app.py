import streamlit as st
import pandas as pd
import random

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(page_title="Aliados de la Circularidad", page_icon="🌱", layout="centered")

# --- ESTILOS CSS ---
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    .resultado-card {
        background-color: #ECFDF5;
        border: 2px solid #10B981;
        border-radius: 15px;
        padding: 20px;
        text-align: center;
        margin-top: 20px;
    }
    .metric-big { font-size: 2.5rem; font-weight: 800; color: #047857; margin: 0; }
    .metric-label { font-size: 1.1rem; color: #065F46; font-weight: 600; }
    </style>
""", unsafe_allow_html=True)

# --- CATÁLOGO Y FACTORES DE CO2 (Por kg) ---
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
# Para almacenar la lista de prendas que se van agregando
if "lista_prendas" not in st.session_state:
    st.session_state.lista_prendas = []
# Para el registro de quienes ya participaron
if "registro_historico" not in st.session_state:
    st.session_state.registro_historico = []

# --- ENCABEZADO ---
st.image("https://images.unsplash.com/photo-1542601906990-b4d3fb778b09?auto=format&fit=crop&q=80&w=800&h=300", use_container_width=True)
st.markdown("<h2 style='text-align: center; color: #1E293B;'>Aliados de la Circularidad</h2>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center; color: #64748B;'>Pequeños Detalles & Mina Las Bambas</h4>", unsafe_allow_html=True)

st.write("---")

# --- PESTAÑAS (TABS) ---
tab1, tab2 = st.tabs(["🌱 Registrar Aporte", "📋 Ver Registro Comunitario"])

with tab1:
    st.markdown("### 👤 Datos del Participante")
    nombre = st.text_input("¿Cuál es tu nombre completo?")
    comunidad = st.selectbox("¿A qué comunidad perteneces?", ["Comunidad A", "Comunidad B", "Comunidad C", "Otra"])

    st.write("---")
    st.markdown("### ♻️ ¿Qué vamos a reciclar hoy?")
    
    # Caja para ir agregando prendas
    with st.container(border=True):
        prenda_sel = st.selectbox("Selecciona el tipo de EPP / Uniforme:", list(CATALOGO_MINA.keys()))
        col_u, col_p = st.columns(2)
        unidades = col_u.number_input("Unidades:", min_value=1, value=1, step=1)
        peso_kg = col_p.number_input("Peso Total (kg):", min_value=0.1, value=1.0, step=0.1)
        
        if st.button("➕ Añadir a mi bolsa de reciclaje"):
            st.session_state.lista_prendas.append({
                "Prenda": prenda_sel,
                "Unidades": unidades,
                "Peso (kg)": peso_kg,
                "CO2_Factor": CATALOGO_MINA[prenda_sel]
            })
            st.success(f"Añadido: {unidades}x {prenda_sel} ({peso_kg} kg)")

    # Mostrar lo que se ha agregado hasta el momento
    if st.session_state.lista_prendas:
        st.write("")
        st.markdown("#### 📦 Tu bolsa actual:")
        df_actual = pd.DataFrame(st.session_state.lista_prendas)
        st.dataframe(df_actual[["Prenda", "Unidades", "Peso (kg)"]], use_container_width=True, hide_index=True)
        
        col_calc, col_vaciar = st.columns([3, 1])
        if col_vaciar.button("🗑️ Vaciar"):
            st.session_state.lista_prendas = []
            st.rerun()

        # Botón final de cálculo
        if col_calc.button("🌱 Registrar y Calcular Impacto", type="primary", use_container_width=True):
            if not nombre:
                st.warning("⚠️ Por favor, ingresa tu nombre en la parte superior.")
            else:
                st.balloons()
                
                # Cálculos matemáticos
                peso_total = sum(item["Peso (kg)"] for item in st.session_state.lista_prendas)
                unidades_total = sum(item["Unidades"] for item in st.session_state.lista_prendas)
                co2_total_evitado = sum(item["Peso (kg)"] * item["CO2_Factor"] for item in st.session_state.lista_prendas)
                
                # Aprovechamiento aleatorio entre 85% y 92%
                eficiencia_upcycling = random.uniform(0.85, 0.92)
                material_recuperado = peso_total * eficiencia_upcycling
                
                arboles_salvados = max(1, int(co2_total_evitado / 22))
                agua_ahorrada = int(peso_total * 2500) # Factor de tu código B2B
                
                st.markdown(f"""
                    <div class="resultado-card">
                        <p class="metric-label">¡Felicidades {nombre.split()[0]}! Has evitado la emisión de:</p>
                        <p class="metric-big">{co2_total_evitado:.1f} kg de CO2</p>
                        <p style="color: #34D399; margin-top: 10px;">¡Y logramos recuperar <b>{material_recuperado:.2f} kg</b> de material útil para nuevos productos!</p>
                    </div>
                """, unsafe_allow_html=True)
                
                st.write("")
                col_i1, col_i2 = st.columns(2)
                with col_i1:
                    st.info(f"🌳 **{arboles_salvados} Árboles**\n\nEquivale al CO2 que absorberían estos árboles en un año.")
                with col_i2:
                    st.info(f"💧 **{agua_ahorrada:,} Litros**\n\nDe agua ahorrada al no fabricar textiles desde cero.")
                
                # Guardar transacción en la memoria de la segunda pestaña
                st.session_state.registro_historico.append({
                    "Nombre": nombre,
                    "Comunidad": comunidad,
                    "Prendas (Unid)": unidades_total,
                    "Peso (kg)": round(peso_total, 2),
                    "Material Recuperado (kg)": round(material_recuperado, 2),
                    "CO2 Evitado (kg)": round(co2_total_evitado, 2)
                })
                
                # Vaciar la bolsa para el siguiente usuario
                st.session_state.lista_prendas = []

with tab2:
    st.markdown("### 📋 Registro de Participación")
    st.caption("Historial de aportes de la comunidad realizados en este dispositivo.")
    
    if st.session_state.registro_historico:
        df_hist = pd.DataFrame(st.session_state.registro_historico)
        st.dataframe(df_hist, use_container_width=True, hide_index=True)
        
        c1, c2, c3 = st.columns(3)
        c1.metric("👥 Total Participantes", len(df_hist))
        c2.metric("⚖️ Material Recuperado", f"{df_hist['Material Recuperado (kg)'].sum():.1f} kg")
        c3.metric("🌍 CO2 Evitado", f"{df_hist['CO2 Evitado (kg)'].sum():.1f} kg")
    else:
        st.info("Aún no hay registros. ¡Anímate a ser el primero en participar!")
