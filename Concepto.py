import streamlit as st
import folium
from folium import plugins
from streamlit_folium import st_folium
import json
import os
import base64

# ─── CONFIG ──────────────────────────────────────────────────────────────────

st.set_page_config(
    layout="wide",
    page_title="UACh Guide",
    page_icon="🗺️",
    initial_sidebar_state="collapsed"
)

# ─── CSS MOBILE-FIRST ─────────────────────────────────────────────────────────

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;700;800&family=DM+Sans:wght@300;400;500&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

#MainMenu, footer, header,
[data-testid="stToolbar"],
[data-testid="stDecoration"],
[data-testid="stStatusWidget"] { display: none !important; }

[data-testid="stAppViewContainer"] {
    background: #0f1117;
    font-family: 'DM Sans', sans-serif;
}

.block-container {
    padding: 0 !important;
    max-width: 100% !important;
}

/* ── Header ── */
.app-header {
    background: linear-gradient(135deg, #0f1117 0%, #1a1f2e 100%);
    padding: 20px 16px 12px;
    border-bottom: 1px solid rgba(255,255,255,0.07);
}

.app-title {
    font-family: 'Syne', sans-serif;
    font-weight: 800;
    font-size: 22px;
    color: #ffffff;
    letter-spacing: -0.5px;
    line-height: 1;
}

.app-subtitle {
    font-family: 'DM Sans', sans-serif;
    font-weight: 300;
    font-size: 12px;
    color: #6b7280;
    margin-top: 4px;
    letter-spacing: 0.5px;
    text-transform: uppercase;
}

.accent-dot {
    display: inline-block;
    width: 8px; height: 8px;
    background: #3b82f6;
    border-radius: 50%;
    margin-right: 8px;
    animation: pulse 2s infinite;
}

@keyframes pulse {
    0%, 100% { opacity: 1; transform: scale(1); }
    50%       { opacity: 0.5; transform: scale(0.8); }
}

/* ── Selectbox ── */
[data-testid="stSelectbox"] > div > div {
    background: #1a1f2e !important;
    border: 1px solid rgba(59,130,246,0.3) !important;
    border-radius: 12px !important;
    color: white !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 15px !important;
    min-height: 52px !important;
}

[data-testid="stSelectbox"] label {
    color: #6b7280 !important;
    font-size: 11px !important;
    font-family: 'DM Sans', sans-serif !important;
    text-transform: uppercase !important;
    letter-spacing: 1px !important;
}

/* ── Mapa ── */
.map-wrapper { padding: 0 16px; }

[data-testid="stIframe"] {
    border-radius: 16px !important;
    overflow: hidden !important;
    border: 1px solid rgba(255,255,255,0.07) !important;
}

/* ── Leyenda scroll ── */
.legend-scroll {
    display: flex;
    gap: 8px;
    padding: 10px 16px;
    overflow-x: auto;
    -webkit-overflow-scrolling: touch;
    scrollbar-width: none;
}
.legend-scroll::-webkit-scrollbar { display: none; }

.legend-chip {
    display: flex;
    align-items: center;
    gap: 6px;
    background: #1a1f2e;
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 20px;
    padding: 6px 12px;
    white-space: nowrap;
    font-size: 11px;
    color: #9ca3af;
    font-family: 'DM Sans', sans-serif;
}

.legend-dot { width: 8px; height: 8px; border-radius: 50%; flex-shrink: 0; }

/* ── Info card ── */
.info-card {
    margin: 0 16px 16px;
    background: #1a1f2e;
    border-radius: 20px;
    border: 1px solid rgba(255,255,255,0.08);
    overflow: hidden;
    animation: slideUp 0.3s ease;
}

@keyframes slideUp {
    from { opacity: 0; transform: translateY(12px); }
    to   { opacity: 1; transform: translateY(0); }
}

.foto-placeholder {
    width: 100%;
    aspect-ratio: 16/9;
    background: linear-gradient(135deg, #1a1f2e, #0f1117);
    display: flex;
    align-items: center;
    justify-content: center;
    flex-direction: column;
    gap: 8px;
    color: #374151;
}

.foto-placeholder-icon  { font-size: 32px; opacity: 0.35; }
.foto-placeholder-text  { font-size: 12px; font-family: 'DM Sans', sans-serif; opacity: 0.35; }

.info-card-header {
    padding: 18px 20px 14px;
    border-bottom: 1px solid rgba(255,255,255,0.06);
}

.info-card-title {
    font-family: 'Syne', sans-serif;
    font-weight: 700;
    font-size: 20px;
    color: #ffffff;
    line-height: 1.2;
}

.info-card-badge {
    display: inline-flex;
    align-items: center;
    gap: 5px;
    background: rgba(59,130,246,0.15);
    border: 1px solid rgba(59,130,246,0.25);
    color: #93c5fd;
    border-radius: 6px;
    padding: 3px 10px;
    font-size: 11px;
    margin-top: 8px;
    font-family: 'DM Sans', sans-serif;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

.info-section {
    padding: 14px 20px;
    border-bottom: 1px solid rgba(255,255,255,0.05);
}
.info-section:last-child { border-bottom: none; }

.info-section-label {
    font-size: 10px;
    font-weight: 500;
    color: #4b5563;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    margin-bottom: 8px;
    font-family: 'DM Sans', sans-serif;
}

.info-section-text {
    font-size: 14px;
    color: #d1d5db;
    line-height: 1.6;
    font-family: 'DM Sans', sans-serif;
    font-weight: 300;
}

.geo-card {
    background: rgba(59,130,246,0.08);
    border: 1px solid rgba(59,130,246,0.15);
    border-radius: 12px;
    padding: 14px;
}

.tip-card {
    background: rgba(251,191,36,0.08);
    border: 1px solid rgba(251,191,36,0.2);
    border-radius: 12px;
    padding: 14px;
}

.empty-state {
    padding: 48px 20px;
    text-align: center;
    color: #374151;
}

.empty-state-icon  { font-size: 48px; margin-bottom: 12px; display: block; opacity: 0.35; }
.empty-state-text  { font-family: 'DM Sans', sans-serif; font-size: 14px; line-height: 1.6; }

/* ── Misiones ── */
.misiones-title {
    font-family: 'Syne', sans-serif;
    font-weight: 700;
    font-size: 16px;
    color: #ffffff;
    padding: 16px 16px 4px;
}

.mision-item {
    display: flex;
    align-items: flex-start;
    gap: 12px;
    padding: 14px 16px;
    background: #1a1f2e;
    border-radius: 12px;
    margin: 0 16px 8px;
    border: 1px solid rgba(255,255,255,0.06);
}

.mision-numero {
    width: 26px; height: 26px;
    border-radius: 50%;
    background: rgba(59,130,246,0.2);
    border: 1px solid rgba(59,130,246,0.3);
    color: #93c5fd;
    font-size: 11px;
    font-weight: 700;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
    font-family: 'Syne', sans-serif;
}

.mision-texto {
    font-size: 13px;
    color: #9ca3af;
    line-height: 1.5;
    font-family: 'DM Sans', sans-serif;
}

.mision-texto strong { color: #e5e7eb; font-weight: 500; }

/* ── Tabs ── */
[data-testid="stTabs"] { padding: 0 16px; }

[data-testid="stTabs"] button {
    font-family: 'DM Sans', sans-serif !important;
    font-size: 13px !important;
    color: #6b7280 !important;
    border-radius: 8px !important;
}

[data-testid="stTabs"] button[aria-selected="true"] {
    color: #3b82f6 !important;
    background: rgba(59,130,246,0.1) !important;
}

.section-divider {
    height: 1px;
    background: rgba(255,255,255,0.05);
    margin: 8px 16px;
}

/* ── Mobile: apilar columnas ── */
@media (max-width: 768px) {
    [data-testid="stHorizontalBlock"] { flex-direction: column !important; }
    [data-testid="column"] { width: 100% !important; flex: none !important; min-width: 100% !important; }
}
</style>
""", unsafe_allow_html=True)


# ─── DATOS ───────────────────────────────────────────────────────────────────

diccionario_campus = {
    "Nahmias": {
        "info": "El clásico de clásicos. Aquí tendrás la mayoría de tus ramos masivos y de plan común. Llega temprano porque los pasillos son un laberinto los primeros días.",
        "dato_geo": "El edificio presenta una alta densidad de flujo peatonal. Su orientación ayuda a mitigar los vientos predominantes del norte durante las tormentas invernales de Valdivia.",
        "tip": "⚠️ El edificio es confuso al principio — busca el número de sala en los paneles de cada piso."
    },
    "Pugin": {
        "info": "El corazón de la Facultad de Ciencias. Albergue de laboratorios de biología, química y física. Hay una cafetería en el primer piso.",
        "dato_geo": "Construido sobre suelos con alta capacidad portante en la terraza fluvial de Isla Teja.",
        "tip": "☕ La cafetería del primer piso a veces está menos llena que la central."
    },
    "GG": {
        "info": "¡Tu casa matriz! El Pabellón de Geología y Geografía. Aquí conocerás a tus profes de carrera y organizarás tus primeras salidas a terreno.",
        "dato_geo": "Punto estratégico. En sus alrededores se realizan las primeras prácticas de levantamiento topográfico y calibración de equipos GNSS.",
        "tip": "🗺️ El mural de la entrada es una buena referencia para orientarte en el campus."
    },
    "Salita SIG": {
        "info": "El búnker de la carrera. El laboratorio donde ocurre toda la magia de la teledetección, la cartografía y el modelamiento espacial. Pasarás muchas horas aquí.",
        "dato_geo": "Centro de procesamiento de alto rendimiento. Aquí transformamos imágenes satelitales crudas en Modelos Digitales de Elevación y análisis de riesgos.",
        "tip": "💾 Siempre guarda tu trabajo en tu pendrive — los computadores se reinician solos."
    },
    "Biblio": {
        "info": "Tu principal refugio para estudiar en silencio, sacar libros físicos o usar las salas de estudio grupal (¡resérvalas con tiempo!).",
        "dato_geo": "Diseño arquitectónico con gran aprovechamiento de la luz natural, minimizando la huella de carbono por iluminación artificial.",
        "tip": "📅 Las salas grupales se agotan rápido en época de pruebas. Resérvalas con días de anticipación."
    },
    "DAE": {
        "info": "Dirección de Asuntos Estudiantiles. Ven aquí para tramitar tu TNE (Pase Escolar), temas de becas, salud y beneficios.",
        "dato_geo": "Nodo administrativo central. Su ubicación minimiza la 'distancia de fricción' promedio desde cualquier punto del campus.",
        "tip": "🪪 Trae tu cédula y certificado de alumno regular para tramitar la TNE."
    },
    "Paradero": {
        "info": "El portal de conexión con el resto de Valdivia. Aquí tomas las micros de vuelta al centro o a tu casa después de clases.",
        "dato_geo": "Punto de máxima convergencia en la red de transporte intraurbano. Nodo crítico en la isócrona de accesibilidad del campus.",
        "tip": "🚌 Después de las 18:00 se llena. La micro 3 y 7 pasan con más frecuencia."
    },
    "Cafeteria Central": {
        "info": "El punto de encuentro principal para almorzar o tomar un café entre ventanas.",
        "dato_geo": "Zona de alta concentración de calor antrópico al mediodía.",
        "tip": "🕐 Entre 12:30 y 13:30 es un caos. Almuerza a las 12:00 o después de las 14:00."
    },
    "Cafeteria Forestal": {
        "info": "Ideal si andas cerca del sector botánico/forestal.",
        "dato_geo": "Rodeada de una alta densidad de biomasa que regula la temperatura local.",
        "tip": "🌿 Más tranquila y con buena vista. Vale el caminado extra."
    },
    "Cafeteria Humanidade": {
        "info": "Un ambiente más bohemio y relajado en el sector de humanidades.",
        "dato_geo": "Ubicada en el sector de menor pendiente del área oeste del campus.",
        "tip": "📚 Buen ambiente para estudiar mientras comes."
    },
    "Cafeteria Vete": {
        "info": "Punto de recarga estratégico cerca de las facultades del fondo.",
        "dato_geo": "Sector con alta permeabilidad de suelos en sus alrededores.",
        "tip": "🐄 Te encontrarás con estudiantes de veterinaria y agronomía. Buena onda generalmente."
    },
    "Arqui": {
        "info": "La cafetería de Arquitectura. Excelente diseño y buenos cafés.",
        "dato_geo": "Estructura que maximiza la eficiencia espacial del entorno construido.",
        "tip": "☕ Uno de los mejores cafés del campus. Vale la pena aunque quede lejos."
    },
    "GYM": {
        "info": "Gimnasio de la UACh. Para tus ramos de deportes o si quieres entrenar en tu tiempo libre.",
        "dato_geo": "Infraestructura de gran volumen que genera una 'isla de calor' microscópica controlada.",
        "tip": "🏋️ Los ramos de deportes son obligatorios los primeros semestres. Inscríbete temprano."
    },
    "Registro Academico": {
        "info": "Donde gestionas tus certificados de alumno regular y concentración de notas.",
        "dato_geo": "Punto de gestión de flujos de información del estudiantado.",
        "tip": "📄 Puedes solicitar certificados online desde el portal — ahorra el viaje."
    },
    "PD": {
        "info": "Pabellón Docente. Aulas clásicas para clases teóricas de diversas facultades.",
        "dato_geo": "Edificación estandarizada para maximizar la capacidad de aforo por metro cuadrado.",
        "tip": "🔑 Algunas salas quedan con llave. Si es el caso, pregunta en secretaría."
    },
    "PC": {
        "info": "Pabellón Federico Saelzer. Usualmente ocupado por ciencias agrarias o forestales.",
        "dato_geo": "Colindante a áreas de experimentación fenológica.",
        "tip": "🌱 Los jardines cercanos son lindos para descansar entre clases."
    },
    "PA": {
        "info": "Pabellón de Producción Animal. Clases específicas de veterinaria y agronomía.",
        "dato_geo": "Conectividad directa con los predios de uso silvoagropecuario del campus.",
        "tip": "🐾 Puede haber animales en los alrededores — es completamente normal."
    },
    "Instapanel": {
        "info": "Laboratorios específicos y talleres técnicos.",
        "dato_geo": "Estructura de material ligero con rápida respuesta térmica ante la radiación solar.",
        "tip": "🛠️ Los laboratorios tienen horarios específicos — revisa tu horario con anticipación."
    },
    "Cidfil": {
        "info": "Pabellón de clases del sector sur del campus. Aquí encontrarás aulas para ramos de distintas facultades. Revisa bien tu horario para no confundirte de edificio.",
        "dato_geo": "Su posición en el campus genera un corredor peatonal que conecta el sector académico sur con los servicios centrales de Isla Teja.",
        "tip": "🧭 Si es tu primera vez yendo, dale 5 minutos extra — queda un poco más alejado del núcleo central."
    },
    "Fame": {
        "info": "Casino Fame, uno de los puntos de alimentación del campus. Buena opción para almorzar si la Cafetería Central está muy llena o queda lejos de tus clases.",
        "dato_geo": "Nodo secundario en la red de servicios de alimentación del campus, alivia la presión sobre el casino central durante las horas punta.",
        "tip": "🍽️ Menos conocido por los mechones, así que suele estar más tranquilo a la hora de almuerzo."
    }
}

colores_uso = {
    "Salas de clases":    "#3b82f6",
    "Biblioteca":         "#8b5cf6",
    "Administrativo":     "#6b7280",
    "Laboratorios":       "#06b6d4",
    "Gimnasio":           "#22c55e",
    "Cafeteria":          "#f97316",
    "Paradero de micros": "#ef4444"
}

iconos_uso = {
    "Salas de clases":    "📚",
    "Biblioteca":         "📖",
    "Administrativo":     "🏢",
    "Laboratorios":       "🔬",
    "Gimnasio":           "🏋️",
    "Cafeteria":          "☕",
    "Paradero de micros": "🚌"
}

misiones_mechon = [
    ("Saca tu TNE",
     "Ve a la <strong>DAE</strong> en las fechas estipuladas que se subirán en IG @daeuach y @cegeouach. Recuerda es una fecha muy concurrida, ve temprano."),
    ("Aprovecha cada actividad",
     "En especial los savalazos o los carretes. Al principio del semestre son muy seguidos; luego, la lluvia y las pruebas los acaban"),
    ("Ubica el Pabellón GG",
     "Pasa por el <strong>GG</strong>, es el edificio más icónico de la carrera y donde tendrás tus primeras clases. Es un buen punto de referencia para orientarte en el campus."),
    ("Recorre la Ciudad",
     "Si eres <strong>nuevo en la ciudad</strong>, tómate un tiempo para conocer los alrededores y los puntos clave de la misma."),
    ("Practica la ruta al paradero",
     "Camina hasta el <strong>Paradero</strong> y chequea qué micros te sirven para tu casa. Puedes usar la App de la Red Regional."),
]


# ─── CARGA DE DATOS ───────────────────────────────────────────────────────────

@st.cache_data
def cargar_datos():
    with open('Edificios.geojson', 'r', encoding='utf-8') as f:
        return json.load(f)

geojson_data = cargar_datos()
import os
if os.path.exists("imagenes"):
    st.write("✅ Carpeta imagenes encontrada:", os.listdir("imagenes"))
elif os.path.exists("fotos"):
    st.write("✅ Carpeta fotos encontrada:", os.listdir("fotos"))
else:
    st.write("❌ No se encuentra ninguna carpeta de fotos")
    st.write("📁 Archivos en raíz:", os.listdir("."))
lista_edificios = sorted([f['properties']['alias'] for f in geojson_data['features']])

CARPETA_FOTOS = "imagenes"

def buscar_foto(alias):
    for ext in ['jpg', 'jpeg', 'png', 'webp', 'JPG', 'JPEG', 'PNG', 'WEBP']:
        path = os.path.join(CARPETA_FOTOS, f"{alias}.{ext}")
        if os.path.exists(path):
            return path
    return None

def foto_a_html(path):
    """Convierte una foto local a un <img> base64 embebido en HTML."""
    ext = path.rsplit('.', 1)[-1].lower()
    mime = 'image/jpeg' if ext in ('jpg', 'jpeg') else f'image/{ext}'
    with open(path, 'rb') as f:
        b64 = base64.b64encode(f.read()).decode()
    return f'<img src="data:{mime};base64,{b64}" style="width:100%;max-height:260px;object-fit:contain;display:block;background:#0f1117;">'


# ─── HEADER ──────────────────────────────────────────────────────────────────

st.markdown("""
<div class="app-header">
    <div class="app-title"><span class="accent-dot"></span>UACh Guide</div>
    <div class="app-subtitle">Mapa de supervivencia · Isla Teja</div>
</div>
""", unsafe_allow_html=True)


# ─── TABS ─────────────────────────────────────────────────────────────────────

tab_mapa, tab_misiones = st.tabs(["🗺️  Mapa", "🎯  Primeras misiones"])


# ══════════════════════════════════════════════════════════════════════════════
# TAB 1: MAPA
# ══════════════════════════════════════════════════════════════════════════════

with tab_mapa:

    edificio_buscado = st.selectbox(
        "BUSCAR LUGAR",
        ["Selecciona un lugar..."] + lista_edificios,
    )

    st.markdown('<div class="map-wrapper">', unsafe_allow_html=True)
    m = folium.Map(
        location=[-39.806, -73.250],
        zoom_start=16,
        tiles="CartoDB dark_matter",
        prefer_canvas=True
    )

    plugins.LocateControl(
        position="topleft", drawCircle=False, flyTo=True,
        strings={"title": "Mi ubicación"}
    ).add_to(m)

    def style_fn(feature):
        uso = feature['properties'].get('tipo_uso', '').strip()
        color = colores_uso.get(uso, '#4b5563')
        if feature['properties']['alias'] == edificio_buscado:
            return {'fillColor': '#f472b6', 'color': '#f472b6', 'weight': 3, 'fillOpacity': 0.85}
        return {'fillColor': color, 'color': color, 'weight': 1.5, 'fillOpacity': 0.55}

    folium.GeoJson(
        geojson_data,
        name="Edificios UACh",
        tooltip=folium.GeoJsonTooltip(
            fields=["alias", "tipo_uso"],
            aliases=["Edificio:", "Uso:"],
            style="background:#1a1f2e;color:white;font-family:sans-serif;font-size:13px;"
                  "border-radius:8px;border:1px solid rgba(255,255,255,0.1);"
        ),
        style_function=style_fn,
        highlight_function=lambda x: {'weight': 3, 'fillOpacity': 0.9}
    ).add_to(m)

    map_data = st_folium(m, height=340, use_container_width=True,
                         returned_objects=["last_active_drawing"])
    st.markdown('</div>', unsafe_allow_html=True)

    # Leyenda scrollable
    leyenda_html = '<div class="legend-scroll">'
    for uso, color in colores_uso.items():
        icono = iconos_uso.get(uso, "📍")
        leyenda_html += f'<div class="legend-chip"><div class="legend-dot" style="background:{color}"></div>{icono} {uso}</div>'
    leyenda_html += '</div>'
    st.markdown(leyenda_html, unsafe_allow_html=True)

    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

    # ── Resolver edificio seleccionado ────────────────────────────────────────
    alias_sel = None
    tipo_uso_sel = ""

    if map_data and map_data.get("last_active_drawing"):
        props = map_data["last_active_drawing"]["properties"]
        alias_sel    = props["alias"]
        tipo_uso_sel = props.get("tipo_uso", "").strip()
    elif edificio_buscado != "Selecciona un lugar...":
        alias_sel = edificio_buscado
        for f in geojson_data['features']:
            if f['properties']['alias'] == edificio_buscado:
                tipo_uso_sel = f['properties']['tipo_uso'].strip()
                break

    # ── Info card ─────────────────────────────────────────────────────────────
    if alias_sel:
        datos  = diccionario_campus.get(alias_sel, {})
        icono  = iconos_uso.get(tipo_uso_sel, "📍")
        info   = datos.get("info",     "Información en construcción.")
        geo    = datos.get("dato_geo", "Dato en levantamiento topográfico.")
        tip    = datos.get("tip",      None)

        foto_path = buscar_foto(alias_sel)

        # ── Apertura de card ──
        st.markdown('<div class="info-card">', unsafe_allow_html=True)

        # ── Foto o placeholder ──
        if foto_path:
            st.markdown(foto_a_html(foto_path), unsafe_allow_html=True)
        else:
            st.markdown('''
            <div class="foto-placeholder">
                <span class="foto-placeholder-icon">📷</span>
                <span class="foto-placeholder-text">Foto próximamente</span>
            </div>''', unsafe_allow_html=True)

        # ── Header ──
        st.markdown(f'''
        <div class="info-card-header">
            <div class="info-card-title">{icono} {alias_sel}</div>
            <div class="info-card-badge">{tipo_uso_sel}</div>
        </div>''', unsafe_allow_html=True)

        # ── Descripción ──
        st.markdown(f'''
        <div class="info-section">
            <div class="info-section-label">Descripción</div>
            <div class="info-section-text">{info}</div>
        </div>''', unsafe_allow_html=True)

        # ── Tip (si existe) ──
        if tip:
            st.markdown(f'''
            <div class="info-section">
                <div class="tip-card">
                    <div class="info-section-label">💡 Tip mechón</div>
                    <div class="info-section-text">{tip}</div>
                </div>
            </div>''', unsafe_allow_html=True)

        # ── Ojo de Geógrafo ──
        st.markdown(f'''
        <div class="info-section">
            <div class="geo-card">
                <span style="font-size:16px;display:block;margin-bottom:4px;">🌍</span>
                <div class="info-section-label">Ojo de Geógrafo</div>
                <div class="info-section-text">{geo}</div>
            </div>
        </div>''', unsafe_allow_html=True)

        # ── Cierre de card ──
        st.markdown('</div>', unsafe_allow_html=True)

    else:
        st.markdown('''
        <div class="info-card">
            <div class="empty-state">
                <span class="empty-state-icon">👆</span>
                <div class="empty-state-text">
                    Busca un lugar arriba o<br>toca un polígono en el mapa
                </div>
            </div>
        </div>
        ''', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# TAB 2: PRIMERAS MISIONES
# ══════════════════════════════════════════════════════════════════════════════

with tab_misiones:
    st.markdown('<div style="height:12px"></div>', unsafe_allow_html=True)
    st.markdown('<div class="misiones-title">🎯 Tus primeras misiones</div>', unsafe_allow_html=True)
    st.markdown('''
    <div style="padding:4px 16px 12px; font-size:13px; color:#6b7280; font-family:'DM Sans',sans-serif; line-height:1.5;">
        Estas son las cosas que <strong style="color:#9ca3af">DEBES</strong> hacer la primera semana/mes para no quedar perdido.
    </div>
    ''', unsafe_allow_html=True)

    for i, (titulo, desc) in enumerate(misiones_mechon, 1):
        st.markdown(f'''
        <div class="mision-item">
            <div class="mision-numero">{i}</div>
            <div class="mision-texto">
                <strong>{titulo}</strong><br>{desc}
            </div>
        </div>
        ''', unsafe_allow_html=True)

    st.markdown('''
    <div style="height:12px"></div>
    <div style="margin:0 16px; background:rgba(34,197,94,0.08); border:1px solid rgba(34,197,94,0.2);
                border-radius:12px; padding:14px 16px;">
        <div style="font-size:10px; color:#4b5563; text-transform:uppercase; letter-spacing:1px;
                    font-family:'DM Sans',sans-serif; margin-bottom:6px;">REGLA DE ORO</div>
        <div style="font-size:13px; color:#86efac; font-family:'DM Sans',sans-serif; line-height:1.6;">
            🌧️ <strong style="color:#bbf7d0">Compra ropa de lluvia.</strong>
            Valdivia es la ciudad más lluviosa de Chile y el campus no tiene techos entre edificios.
            Aprenderás a la mala si no lo haces.
        </div>
    </div>
    <div style="height:24px"></div>
    ''', unsafe_allow_html=True)
    

