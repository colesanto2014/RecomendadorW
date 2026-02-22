import streamlit as st

st.set_page_config(page_title="IA Recopilador Académico", page_icon="🎓", layout="centered")

# ============================================================================
# FONDO + TEXTO OSCURO LEGIBLE
# ============================================================================
st.markdown("""
<style>
    .stApp {
        background-image: url("https://images.unsplash.com/photo-1524995997946-a1c2e315a42f?w=1600");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }

    .block-container {
        background-color: rgba(255, 255, 255, 0.93);
        border-radius: 15px;
        padding: 30px !important;
    }

    /* TEXTO GENERAL */
    .block-container p,
    .block-container li,
    .block-container span,
    .block-container label,
    .block-container div {
        color: #1a1a1a !important;
    }

    /* SOLO LOS TITULOS DEL CONTENIDO */
    .block-container h1,
    .block-container h2,
    .block-container h3,
    .block-container h4 {
        color: #1a1a1a !important;
    }

    /* BOTONES */
    div.stButton > button {
        font-size: 16px !important;
        font-weight: bold !important;
        border-radius: 8px !important;
        background-color: #78681E !important;
        color: white !important;
    }

    div.stButton > button:hover {
        background-color: #5a4e17 !important;
    }

    /* INPUT */
    input {
        color: #1a1a1a !important;
        background-color: white !important;
    }

    /* INFO BOX */
    .stAlert {
        color: #1a1a1a !important;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# LISTA DE PREGUNTAS
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
# ESTADO
# ============================================================================
if "gustos_estudiante" not in st.session_state:
    st.session_state.gustos_estudiante = {}

if "paso" not in st.session_state:
    st.session_state.paso = 0

if "historial_chat" not in st.session_state:
    st.session_state.historial_chat = []

def construir_idea_busqueda():
    g = st.session_state.gustos_estudiante
    partes = []

    if g.get("materia"):
        partes.append(g["materia"])

    if g.get("tipo_contenido"):
        partes.append(g["tipo_contenido"])

    if g.get("tema_aprender"):
        partes.append(g["tema_aprender"])

    if g.get("estilo_aprendizaje"):
        partes.append(g["estilo_aprendizaje"])

    if g.get("carrera"):
        partes.append(f"para {g['carrera']}")

    return " ".join(partes)

# ============================================================================
# TITULO SUPERIOR
# ============================================================================
st.markdown("""
<div style='background:#361201; padding:18px; border-radius:10px; text-align:center;'>
<h2 style='color:#FFD700; margin:0; text-shadow:2px 2px 4px black;'>
🎓 IA de Personalización de Búsquedas Académicas
</h2>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# ============================================================================
# PANTALLA INICIAL
# ============================================================================
if st.session_state.paso == 0:

    st.markdown("<h3>¡Bienvenido al Recopilador de Preferencias Académicas con IA!</h3>", unsafe_allow_html=True)

    st.markdown("<b>¿Qué hace esta herramienta?</b>", unsafe_allow_html=True)

    st.markdown("""
    <ol>
        <li>Te hace <b>5 preguntas</b> sobre tus gustos académicos</li>
        <li>Guarda tus respuestas en un diccionario</li>
        <li>Construye una <b>búsqueda personalizada</b> combinando tus respuestas</li>
        <li>Abre <b>Google</b> con resultados específicos para ti</li>
    </ol>
    """, unsafe_allow_html=True)

    if st.button("▶️ Iniciar Recopilación", use_container_width=True):
        st.session_state.paso = 1
        st.session_state.gustos_estudiante = {}
        st.session_state.historial_chat = []
        st.rerun()

# ============================================================================
# PREGUNTAS
# ============================================================================
elif 1 <= st.session_state.paso <= 5:

    info = preguntas_info[st.session_state.paso - 1]
    total = len(preguntas_info)

    st.progress(st.session_state.paso / total)

    st.markdown(f"<b>Pregunta {st.session_state.paso} de {total}</b>", unsafe_allow_html=True)

    st.markdown(f"""
    <div style='background:rgba(245,245,245,0.98);
    border-radius:12px;
    padding:25px;
    border-left: 5px solid #3498db;'>

    <h3>{info['pregunta']}</h3>
    <p>{info['explicacion']}</p>

    </div>
    """, unsafe_allow_html=True)

    respuesta = st.text_input(
        "Tu respuesta:",
        placeholder=info["placeholder"],
        key=f"resp_{st.session_state.paso}"
    )

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Siguiente ➜", use_container_width=True):

            if not respuesta.strip():
                st.warning("⚠️ Escribe una respuesta antes de continuar.")
            else:
                st.session_state.gustos_estudiante[info["clave"]] = respuesta.strip()

                st.session_state.historial_chat.append({
                    "pregunta": info["pregunta"],
                    "respuesta": respuesta.strip()
                })

                st.session_state.paso += 1
                st.rerun()

    with col2:
        if st.button("Reiniciar 🔄", use_container_width=True):
            st.session_state.paso = 0
            st.rerun()

    if st.session_state.historial_chat:

        st.markdown("---")
        st.markdown("📋 **Respuestas anteriores:**")

        for i, item in enumerate(st.session_state.historial_chat, 1):
            st.write(f"{i}. {item['pregunta']} → {item['respuesta']}")

# ============================================================================
# RESULTADO FINAL
# ============================================================================
elif st.session_state.paso == 6:

    st.success("✅ ¡Recopilación completada!")

    st.markdown("### 📋 Resumen de tus gustos")

    for i, (clave, valor) in enumerate(st.session_state.gustos_estudiante.items(), 1):
        nombre = clave.replace("_", " ").title()
        st.write(f"{i}. **{nombre}:** {valor}")

    idea = construir_idea_busqueda()

    st.markdown("---")
    st.markdown("### 🔍 Búsqueda generada")

    st.code(idea)

    url = f"https://www.google.com/search?q={idea.replace(' ', '+')}"

    st.markdown(f"""
    <a href="{url}" target="_blank">
        <button style='background:#00129A;
        color:white;
        font-size:16px;
        padding:12px 30px;
        border:none;
        border-radius:8px;
        cursor:pointer;
        width:100%;
        margin-top:10px;'>

        🔎 Buscar en Google

        </button>
    </a>
    """, unsafe_allow_html=True)

    if st.button("🔄 Reiniciar desde el inicio", use_container_width=True):
        st.session_state.paso = 0
        st.rerun()
