import streamlit as st

st.set_page_config(page_title="IA Recopilador Académico", page_icon="🎓", layout="centered")

# =========================================================
# ESTILO VISUAL PROFESIONAL
# =========================================================
st.markdown("""
<style>

.stApp{
background-image:url("https://images.unsplash.com/photo-1524995997946-a1c2e315a42f?w=1600");
background-size:cover;
background-position:center;
background-attachment:fixed;
}

.block-container{
background:rgba(255,255,255,0.94);
padding:35px;
border-radius:18px;
box-shadow:0px 8px 30px rgba(0,0,0,0.35);
animation:fadein 0.7s;
}

@keyframes fadein{
from{opacity:0; transform:translateY(10px);}
to{opacity:1; transform:translateY(0);}
}

.block-container p,
.block-container li,
.block-container span,
.block-container label,
.block-container div{
color:#1a1a1a !important;
}

.block-container h1,
.block-container h2,
.block-container h3{
color:#1a1a1a !important;
}

div.stButton > button{
height:52px;
font-size:18px !important;
font-weight:bold;
border-radius:10px;
background:#78681E;
color:white;
box-shadow:0px 4px 12px rgba(0,0,0,0.3);
}

div.stButton > button:hover{
background:#5a4e17;
}

.stProgress > div > div > div{
background-color:#78681E;
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# TITULO
# =========================================================
st.markdown("""
<div style="
background:linear-gradient(90deg,#361201,#6b2d05);
padding:28px;
border-radius:16px;
text-align:center;
box-shadow:0px 6px 20px rgba(0,0,0,0.4);
">
<h1 style="
color:#FFD700;
margin:0;
letter-spacing:1px;
text-shadow:2px 2px 6px black;
">
🎓 IA de Personalización de Búsquedas Académicas
</h1>
</div>
""", unsafe_allow_html=True)

st.markdown("")

# =========================================================
# PREGUNTAS
# =========================================================
preguntas_info = [
{
"pregunta":"¿Cuál es tu materia favorita?",
"explicacion":"Esto nos ayudará a encontrar recursos relacionados con lo que más disfrutas estudiar.",
"clave":"materia",
"placeholder":"Ejemplo: Matemáticas, Historia..."
},
{
"pregunta":"¿Qué tipo de contenido te gusta?",
"explicacion":"Videos, artículos, tutoriales, podcasts o cursos.",
"clave":"tipo_contenido",
"placeholder":"Ejemplo: Videos, tutoriales..."
},
{
"pregunta":"¿Qué tema te gustaría aprender este mes?",
"explicacion":"Algo específico que quieras dominar.",
"clave":"tema_aprender",
"placeholder":"Ejemplo: Python, Energía solar..."
},
{
"pregunta":"¿Cómo prefieres aprender?",
"explicacion":"Visual, práctico, teórico o mixto.",
"clave":"estilo_aprendizaje",
"placeholder":"Ejemplo: Visual"
},
{
"pregunta":"¿Qué carrera te interesa?",
"explicacion":"Esto ayuda a personalizar mejor la búsqueda.",
"clave":"carrera",
"placeholder":"Ejemplo: Ingeniería"
}
]

# =========================================================
# ESTADO
# =========================================================
if "gustos_estudiante" not in st.session_state:
    st.session_state.gustos_estudiante = {}

if "paso" not in st.session_state:
    st.session_state.paso = 0

if "historial_chat" not in st.session_state:
    st.session_state.historial_chat = []

# =========================================================
# FUNCION BUSQUEDA
# =========================================================
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

# =========================================================
# PANTALLA INICIAL
# =========================================================
if st.session_state.paso == 0:

    st.markdown("""
    <div style="
    background:white;
    padding:25px;
    border-radius:12px;
    box-shadow:0px 4px 14px rgba(0,0,0,0.2);
    ">
    <h3>Bienvenido</h3>
    <p>Esta herramienta usa IA básica para conocer tus intereses académicos y crear una búsqueda personalizada en Google.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("")

    if st.button("▶️ Iniciar Recopilación", use_container_width=True):
        st.session_state.paso = 1
        st.session_state.gustos_estudiante = {}
        st.session_state.historial_chat = []
        st.rerun()

# =========================================================
# PREGUNTAS
# =========================================================
elif 1 <= st.session_state.paso <= 5:

    info = preguntas_info[st.session_state.paso - 1]
    total = len(preguntas_info)

    st.progress(st.session_state.paso / total)

    st.markdown(f"### Pregunta {st.session_state.paso} de {total}")

    st.markdown(f"""
    <div style="
    background:rgba(245,245,245,0.98);
    border-radius:12px;
    padding:25px;
    border-left:6px solid #3498db;
    ">
    <h3>{info['pregunta']}</h3>
    <p>{info['explicacion']}</p>
    </div>
    """, unsafe_allow_html=True)

    respuesta = st.text_input("Tu respuesta:", placeholder=info["placeholder"], key=f"resp_{st.session_state.paso}")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Siguiente", use_container_width=True):

            if not respuesta.strip():
                st.warning("Escribe una respuesta antes de continuar.")
            else:
                st.session_state.gustos_estudiante[info["clave"]] = respuesta.strip()

                st.session_state.historial_chat.append({
                    "pregunta": info["pregunta"],
                    "respuesta": respuesta.strip()
                })

                st.session_state.paso += 1
                st.rerun()

    with col2:
        if st.button("Reiniciar", use_container_width=True):
            st.session_state.paso = 0
            st.rerun()

# =========================================================
# RESULTADO
# =========================================================
elif st.session_state.paso == 6:

    st.success("Recopilación completada")

    st.markdown("### Tus respuestas")

    for i,(clave,valor) in enumerate(st.session_state.gustos_estudiante.items(),1):
        nombre = clave.replace("_"," ").title()
        st.write(f"{i}. **{nombre}:** {valor}")

    idea = construir_idea_busqueda()

    st.markdown("### Búsqueda generada")
    st.code(idea)

    url = f"https://www.google.com/search?q={idea.replace(' ','+')}"

    st.markdown(f"""
    <a href="{url}" target="_blank">
    <button style="
    background:#00129A;
    color:white;
    font-size:16px;
    padding:12px 30px;
    border:none;
    border-radius:8px;
    width:100%;
    ">
    Buscar en Google
    </button>
    </a>
    """, unsafe_allow_html=True)

    if st.button("Reiniciar desde el inicio", use_container_width=True):
        st.session_state.paso = 0
        st.rerun()
