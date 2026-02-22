import streamlit as st

st.set_page_config(page_title="IA Recopilador Académico", page_icon="🎓", layout="centered")

# ============================================================================
# IMAGEN DE FONDO DESDE INTERNET
# ============================================================================
st.markdown("""
<style>
    .stApp {
        background-image: url("https://images.unsplash.com/photo-1524995997946-a1c2e315a42f?w=1600");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }
    /* Fondo semi-transparente para que el texto sea legible */
    .block-container {
        background-color: rgba(255, 255, 255, 0.88);
        border-radius: 15px;
        padding: 30px !important;
    }
    /* Botones más bonitos */
    div.stButton > button {
        font-size: 16px !important;
        font-weight: bold !important;
        border-radius: 8px !important;
        padding: 10px !important;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# LISTA DE PREGUNTAS (igual que el original)
# ============================================================================
preguntas_info = [
    {
        "pregunta": "¿Cuál es tu materia favorita?",
        "explicacion": "Esto nos ayudará a encontrar recursos relacionados con las materias que más disfrutas estudiar.",
        "clave": "materia",
        "placeholder": "Ejemplo: Matemáticas, Historia, Biología..."
    },
    {
        "pregunta": "¿Qué tipo de contenido te gusta?",
        "explicacion": "Queremos saber si prefieres videos, artículos, tutoriales interactivos, podcasts, etc.",
        "clave": "tipo_contenido",
        "placeholder": "Ejemplo: Videos de YouTube, artículos, tutoriales..."
    },
    {
        "pregunta": "¿Qué tema te gustaría aprender este mes?",
        "explicacion": "Dinos algo específico que quieras dominar o entender mejor en las próximas semanas.",
        "clave": "tema_aprender",
        "placeholder": "Ejemplo: Programación en Python, Ecuaciones diferenciales..."
    },
    {
        "pregunta": "¿Cómo prefieres aprender?",
        "explicacion": "Cada persona aprende diferente. ¿Prefieres ver (visual), hacer (práctico) o leer (teórico)?",
        "clave": "estilo_aprendizaje",
        "placeholder": "Ejemplo: Visual, Práctico, Teórico, Mixto..."
    },
    {
        "pregunta": "¿Qué carrera o campo profesional te interesa?",
        "explicacion": "Esto nos permitirá contextualizar la búsqueda hacia tu futuro profesional.",
        "clave": "carrera",
        "placeholder": "Ejemplo: Ingeniería, Medicina, Diseño Gráfico..."
    }
]

# ============================================================================
# INICIALIZAR ESTADO
# ============================================================================
if "gustos_estudiante" not in st.session_state:
    st.session_state.gustos_estudiante = {}
if "paso" not in st.session_state:
    st.session_state.paso = 0
if "historial_chat" not in st.session_state:
    st.session_state.historial_chat = []

# ============================================================================
# FUNCIÓN: construir búsqueda (igual que el original)
# ============================================================================
def construir_idea_busqueda():
    g = st.session_state.gustos_estudiante
    partes = []
    if g.get("materia"):            partes.append(g["materia"])
    if g.get("tipo_contenido"):     partes.append(g["tipo_contenido"])
    if g.get("tema_aprender"):      partes.append(g["tema_aprender"])
    if g.get("estilo_aprendizaje"): partes.append(g["estilo_aprendizaje"])
    if g.get("carrera"):            partes.append(f"para {g['carrera']}")
    return " ".join(partes)

# ============================================================================
# TÍTULO
# ============================================================================
st.markdown("""
    <div style='background:#361201; padding:18px; border-radius:10px; text-align:center;'>
        <h2 style='color:white; margin:0;'>🎓 IA de Personalización de Búsquedas Académicas</h2>
    </div>
""", unsafe_allow_html=True)
st.markdown("---")

# ============================================================================
# PANTALLA INICIAL
# ============================================================================
if st.session_state.paso == 0:
    st.markdown("""
    ### ¡Bienvenido al Recopilador de Preferencias Académicas con IA!

    **¿Qué hace esta herramienta?**
    1. Te hace **5 preguntas** sobre tus gustos académicos
    2. Guarda tus respuestas en un diccionario
    3. Construye una **búsqueda personalizada** combinando tus respuestas
    4. Abre **Google** con resultados específicos para ti
    """)
    st.info("Presiona el botón para comenzar.")

    if st.button("▶️ Iniciar Recopilación", use_container_width=True):
        st.session_state.paso = 1
        st.session_state.gustos_estudiante = {}
        st.session_state.historial_chat = []
        st.rerun()

# ============================================================================
# PREGUNTAS (pasos 1 al 5)
# ============================================================================
elif 1 <= st.session_state.paso <= 5:
    info = preguntas_info[st.session_state.paso - 1]
    total = len(preguntas_info)

    st.progress(st.session_state.paso / total)
    st.markdown(f"**Pregunta {st.session_state.paso} de {total}**")

    st.markdown(f"""
        <div style='background:rgba(245,245,245,0.95); border-radius:12px; padding:25px;
        border-left: 5px solid #3498db;'>
            <h3 style='color:#2c3e50;'>{info['pregunta']}</h3>
            <p style='color:#34495e;'>{info['explicacion']}</p>
        </div>
    """, unsafe_allow_html=True)
    st.markdown("")

    respuesta = st.text_input("Tu respuesta:", placeholder=info["placeholder"],
                              key=f"resp_{st.session_state.paso}")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Siguiente ➜", key="btn_siguiente", use_container_width=True):
            if not respuesta.strip():
                st.warning("⚠️ Por favor escribe una respuesta antes de continuar.")
            else:
                st.session_state.gustos_estudiante[info["clave"]] = respuesta.strip()
                st.session_state.historial_chat.append({
                    "pregunta": info["pregunta"],
                    "respuesta": respuesta.strip()
                })
                st.session_state.paso += 1
                st.rerun()
    with col2:
        if st.button("Reiniciar 🔄", key="btn_reiniciar", use_container_width=True):
            st.session_state.paso = 0
            st.rerun()

    if st.session_state.historial_chat:
        st.markdown("---")
        st.markdown("**📋 Respuestas anteriores:**")
        for i, item in enumerate(st.session_state.historial_chat, 1):
            st.write(f"**{i}.** {item['pregunta']}  →  _{item['respuesta']}_")

# ============================================================================
# RESULTADO FINAL (paso 6)
# ============================================================================
elif st.session_state.paso == 6:
    st.success("✅ ¡Recopilación completada!")
    st.markdown("### 📋 Resumen de tus gustos:")

    for i, (clave, valor) in enumerate(st.session_state.gustos_estudiante.items(), 1):
        nombre = clave.replace("_", " ").title()
        st.write(f"**{i}. {nombre}:** {valor}")

    idea = construir_idea_busqueda()
    st.markdown("---")
    st.markdown("### 🔍 Búsqueda generada automáticamente:")
    st.code(idea)

    url = f"https://www.google.com/search?q={idea.replace(' ', '+')}"
    st.markdown(f"""
        <a href="{url}" target="_blank">
            <button style='background:#00129A; color:white; font-size:16px;
            padding:12px 30px; border:none; border-radius:8px;
            cursor:pointer; width:100%; margin-top:10px;'>
            🔎 Buscar en Google
            </button>
        </a>
    """, unsafe_allow_html=True)

    st.markdown("")
    if st.button("🔄 Reiniciar desde el inicio", use_container_width=True):
        st.session_state.paso = 0
        st.rerun()
