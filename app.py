import streamlit as st

st.set_page_config(page_title="Impacto Comunitario - Las Bambas", page_icon="🌱", layout="centered")

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

# Catálogo completo actualizado
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

st.image("https://images.unsplash.com/photo-1542601906990-b4d3fb778b09?auto=format&fit=crop&q=80&w=800&h=300", use_container_width=True)
st.markdown("<h2 style='text-align: center; color: #1E293B;'>Calculadora de Impacto 🌍</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #64748B;'>Transformando los uniformes de Las Bambas.</p>", unsafe_allow_html=True)

st.write("---")

st.markdown("### 👤 Datos del Participante")
nombre = st.text_input("¿Cuál es tu nombre completo?")
comunidad = st.selectbox("¿A qué comunidad perteneces?", ["Comunidad A", "Comunidad B", "Comunidad C", "Otra"])

st.write("---")
st.markdown("### ♻️ ¿Qué vamos a reciclar hoy?")
prenda_seleccionada = st.selectbox("Selecciona el tipo de EPP / Uniforme:", list(CATALOGO_MINA.keys()))
cantidad = st.number_input("¿Cuántas unidades entregarás?", min_value=1, value=1, step=1)

if st.button("🌱 Calcular mi Impacto Positivo", type="primary", use_container_width=True):
    if not nombre:
        st.warning("⚠️ Por favor, ingresa tu nombre antes de calcular.")
    else:
        st.balloons()
        factor_co2 = CATALOGO_MINA[prenda_seleccionada]
        co2_total_evitado = factor_co2 * cantidad
        arboles_salvados = max(1, int(co2_total_evitado / 22))
        agua_ahorrada = int(co2_total_evitado * 110)
        
        st.markdown(f"""
            <div class="resultado-card">
                <p class="metric-label">¡Gracias {nombre.split()[0]}! Has evitado la emisión de:</p>
                <p class="metric-big">{co2_total_evitado:.1f} kg de CO2</p>
                <p style="color: #34D399; margin-top: 10px;">Al reciclar {cantidad} unidad(es) de {prenda_seleccionada.split(' ')[1].lower()}.</p>
            </div>
        """, unsafe_allow_html=True)
        
        st.write("")
        col1, col2 = st.columns(2)
        with col1:
            st.info(f"🌳 **{arboles_salvados} Árboles**\n\nEquivale al CO2 que absorberían estos árboles en un año.")
        with col2:
            st.info(f"💧 **{agua_ahorrada:,} Litros**\n\nDe agua ahorrada al no fabricar textiles nuevos.")
