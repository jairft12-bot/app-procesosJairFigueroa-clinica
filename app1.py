import os
import datetime
import smtplib
import unicodedata
import streamlit as st
import pandas as pd
import plotly.express as px
import streamlit.components.v1 as components
import time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
st.set_page_config(page_title="Procesos", layout="wide")
# --- CONFIGURACIÓN VISUAL VIVA 1A ---
import streamlit as st
import pandas as pd
import plotly.express as px
import pandas as pd


# --- CONFIGURACIÓN GLOBAL DE INTERFAZ ---
st.set_page_config(page_title="Gestión Viva 1A", layout="wide")

st.markdown("""
<style>
    /* 1. CONFIGURACIÓN GLOBAL DEL CUERPO (MAIN) */
    .stApp { 
        background-color: #FFFFFF; 
    }

    /* Forzamos negro SOLO en el contenido principal para no afectar al sidebar */
    [data-testid="stMain"] h1, [data-testid="stMain"] h2, [data-testid="stMain"] h3, 
    [data-testid="stMain"] p, [data-testid="stMain"] label, [data-testid="stMain"] .stMarkdown {
        color: #000000 !important;
    }

    /* 2. CONFIGURACIÓN DEL SIDEBAR */
    [data-testid="stSidebar"] { 
        background-color: #000000 !important; /* Fondo Negro (o el azul que prefieras) */
    }

    /* Forzamos BLANCO para todo lo que esté dentro del Sidebar (Labels, Sliders, Textos) */
    [data-testid="stSidebar"] p, 
    [data-testid="stSidebar"] label, 
    [data-testid="stSidebar"] span,
    [data-testid="stSidebar"] .stMarkdown p {
        color: #FFFFFF !important;
    }

    /* 3. EXPANDER (AZUL VIVA 1A) */
    .st-emotion-cache-p5msec p {
        color: #002b5c !important; 
        font-weight: bold !important;
    }

    details[open] summary, details summary:hover {
        background-color: #002b5c !important; 
        color: white !important; 
        border-radius: 5px;
        transition: 0.3s;
    }

    details[open] summary svg, details[open] summary p {
        fill: white !important;
        color: white !important;
    }

    /* 4. SELECTBOX / MULTISELECT */
    div[data-baseweb="select"] > div {
        background-color: #f0f2f6 !important;
        color: #000000 !important;
    }
    
    /* 5. TABLAS PROFESIONALES */
    .stTable {
        border: 1px solid #e0e0e0;
        border-radius: 8px;
        overflow: hidden;
        background-color: white;
    }

    .stTable thead tr th, 
    .stTable thead tr th *, 
    .stTable tbody tr th, 
    .stTable tbody tr th * {
        background-color: #002b5c !important; 
        color: #FFFFFF !important; 
        font-weight: bold !important;
        text-align: center !important;
    }

    .stTable tbody tr td, 
    .stTable tbody tr td * {
        color: #000000 !important;
        border-bottom: 1px solid #eeeeee !important;
        background-color: white !important;
    }

    .stTable tbody tr:nth-child(even) td {
        background-color: #f9f9f9 !important;
    }

    /* 6. ICONOS DE SISTEMA Y HEADER */
    .stActionButton, [data-testid="stHeader"] {
        background-color: rgba(255, 255, 255, 0.5);
        color: #000000 !important;
    }

    /* 7. TARJETAS KPI */
    .kpi-card {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #e0e0e0;
        border-left: 6px solid #0056b3;
        text-align: center;
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)
def enviar_correo_gmail(destinatario, asunto, cuerpo):
    remitente = "tucorreo@gmail.com"  # Cambia por tu correo
    contraseña = "tu_contraseña_de_aplicacion"  # Cambia por tu contraseña de app

    mensaje = MIMEMultipart()
    mensaje["From"] = remitente
    mensaje["To"] = destinatario
    mensaje["Subject"] = Header(asunto, "utf-8")

    try:
        mensaje.attach(MIMEText(cuerpo, "plain", "utf-8"))
        servidor = smtplib.SMTP("smtp.gmail.com", 587)
        servidor.starttls()
        servidor.login(remitente, contraseña)
        servidor.sendmail(remitente, destinatario, mensaje.as_string())
        servidor.quit()
        print("Correo enviado correctamente")
        return True
    except Exception as e:
      st.error(f"Error al enviar correo: {e}")
      print(f"Error al enviar correo: {e}")
      return False

def aplicar_formato_figura(fig, color_sequence=None, horizontal=False):
    fig.update_layout(
        template="plotly_dark",
        showlegend=False,
        plot_bgcolor='rgba(60, 80, 110, 1)',  # azul fondo
        paper_bgcolor='rgba(60, 80, 110, 1)',
        font_color='white',
        xaxis=dict(
            title_font=dict(size=18),
            tickfont=dict(size=14)
        ),
        yaxis=dict(
            title_font=dict(size=18),
            tickfont=dict(size=14)
        ),
        title=dict(font=dict(size=24))
    )
    if horizontal:
        fig.update_traces(
            textposition="outside",
            cliponaxis=False,
            texttemplate='%{x}',
            textfont_size=16
        )
    else:
        fig.update_traces(
            textposition="outside",
            cliponaxis=False,
            texttemplate='%{y}',
            textfont_size=16
        )
    if color_sequence:
        fig.update_traces(marker_color=color_sequence)






# ======== TÍTULO PRINCIPAL MEJORADO ========
st.markdown('<h1 class="main-title">🗂️ Procesos Clínica Viva 1A</h1>', unsafe_allow_html=True)
COMENTARIOS_PATH = "procesos/comentarios.xlsx"

@st.cache_data
def cargar_comentarios():
    if not os.path.exists(COMENTARIOS_PATH):
        return pd.DataFrame(columns=["PROCESO", "COMENTARIO", "USUARIO", "FECHA", "FECHA_REVISION"])
    else:
        df = pd.read_excel(COMENTARIOS_PATH)
        if "FECHA_REVISION" not in df.columns:
            df["FECHA_REVISION"] = pd.NaT
        return df

def guardar_comentarios(df):
    df.to_excel(COMENTARIOS_PATH, index=False)



# Variable dummy para forzar rerun sin experimental_rerun
if "dummy" not in st.session_state:
    st.session_state["dummy"] = False

def rerun():
    st.session_state["dummy"] = not st.session_state["dummy"]


# --- Usuarios permitidos ---
USERS = {
    "jair": {"password": "Emerita220220", "role": "admin"},
    "jair2": {"password": "1111", "role": "viewer"},
    "jair3": {"password": "2222", "role": "viewer"},
}

# --- Sistema de Login ---
def login():
    st.subheader("Inicio de Sesión")

    with st.form("form_login"):
        username = st.text_input("Usuario", key="login_usuario")
        password = st.text_input("Contraseña", type="password", key="login_password")
        enviar = st.form_submit_button("Ingresar")

        if enviar:
            if username in USERS and USERS[username]["password"] == password:
                st.session_state["logged"] = True
                st.session_state["user"] = username
                st.session_state["role"] = USERS[username]["role"]
                rerun()  # <-- aquí forzamos refresco inmediato para evitar doble clic
            else:
                st.error("Usuario o contraseña incorrectos")
if "logged" not in st.session_state:
    st.session_state.logged = False

def detector_inactividad(minutos=15):
    milisegundos = minutos * 60 * 1000
    # Este script detecta clics, movimiento de mouse y teclas
    # Si pasa el tiempo, busca el botón de "Cerrar sesión" y le hace clic automáticamente
    # O simplemente recarga la página para limpiar el session_state
    
    components.html(f"""
        <script>
        const timeout = {milisegundos};
        let idleTimer = null;

        function logout() {{
            window.parent.location.reload(); 
        }}

        function resetTimer() {{
            if (idleTimer) clearTimeout(idleTimer);
            idleTimer = setTimeout(logout, timeout);
        }}

        // Eventos que resetean el cronómetro
        window.parent.document.onmousemove = resetTimer;
        window.parent.document.onkeypress = resetTimer;
        window.parent.document.onclick = resetTimer;
        window.parent.document.onscroll = resetTimer;

        resetTimer();
        </script>
    """, height=0)

# USO DENTRO DE TU APP:
if st.session_state["logged"]:
    detector_inactividad(15) # Configura aquí los minutos

def logout():
    st.session_state["logged"] = False
    st.session_state["user"] = None
    st.session_state["role"] = None
    rerun()
   

if "logged" not in st.session_state:
    st.session_state["logged"] = False

if not st.session_state["logged"]:
    login()
    st.stop()

# ============================
# FUNCIÓN ÓPTIMA PARA CARGAR EXCEL USANDO TIMESTAMP
# ============================
@st.cache_data
def cargar_excel():
    ruta = "procesos/Bitacora1.xlsx"
    return pd.read_excel(ruta, sheet_name="Bitacora-Archivos")

# Botón para recargar datos
# Botón para recargar datos solo para admin
if st.session_state.get("role") == "admin":
    if st.sidebar.button("🔄 Recargar datos"):
        st.cache_data.clear()
        rerun()


# ====== CONTENIDO DE LA APP (solo si está logueado) ======

st.write(f"Bienvenido **{st.session_state['user']}** (rol: {st.session_state['role']})")


# ============================
# SIDEBAR
# ============================
def render_sidebar():
    st.sidebar.title("HÆLIA")
    st.sidebar.markdown("---")
    st.sidebar.write(f"Usuario: **{st.session_state['user']}**")
    st.sidebar.write(f"Rol: **{st.session_state['role']}**")
    st.sidebar.markdown("---")
    st.write("\n" * 30)  # Ajusta el número para mover más arriba o abajo

    st.image("logo/logo2.jpeg", width=150)

    options = ["Inicio", "Procesos", "Documentos", "Análisis de Calidad"]
    if st.session_state.get("role") == "admin":
        options.append("Administración")

    # Usamos key para que el valor quede guardado en sesión
    if "pagina_activa" not in st.session_state:
        st.session_state["pagina_activa"] = "Inicio"  # valor inicial

    pagina_seleccionada = st.sidebar.radio(
        "Navegación",
        options=options,
        format_func=lambda x: {
            "Inicio": "🏠 Inicio",
            "Procesos": "📌 Procesos",
            "Documentos": "📄 Documentos",
            "Administración": "⚙️ Administración",
            "Análisis de Calidad":"📊 Análisis de Calidad",
            "Mapa Estratégico": "Mapa Estratégico",
        }[x],
        key="pagina_activa"  # Aquí la clave de sesión
    )

    if st.sidebar.button("🚪 Cerrar sesión", key="logout_sidebar"):
        logout()

    return st.session_state["pagina_activa"]


# ============================
# PÁGINAS
# ============================


def pagina_inicio():
    # Título alineado a la izquierda (por defecto)
    st.markdown("<h1 style='color: #002b5c;'>🏥 Panel de Control Viva 1A</h1>", unsafe_allow_html=True)
    st.write("Bienvenido al sistema de procesos de la Clínica Viva 1A.")

    try:
        df = cargar_excel()
        
        # --- FILA DE KPIs (TARJETAS ORIGINALES) ---
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f'<div class="kpi-card"><h3>Total Documentos</h3><h2>{len(df)}</h2></div>', unsafe_allow_html=True)
        with col2:
            proc_count = len(df[df["TIPO DE DOCUMENTO"].astype(str).str.upper() == "PROCEDIMIENTO"])
            st.markdown(f'<div class="kpi-card"><h3>Procedimientos</h3><h2>{proc_count}</h2></div>', unsafe_allow_html=True)
        with col3:
            st.markdown(f'<div class="kpi-card"><h3>Vigencia Actual</h3><h2>2025</h2></div>', unsafe_allow_html=True)
        
        # =========================================================
        # NUEVA SECCIÓN: RESUMEN ESTRATÉGICO (LO NUEVO AQUÍ)
        # =========================================================
        df_mapa = cargar_mapeo_procesos() # Llamamos a la función que lee la hoja 'TipoProceso'
        
        if df_mapa is not None:
            st.markdown("### 🗺️ Clasificación de Áreas por Proceso")
            col_m1, col_m2, col_m3 = st.columns(3)
            
            # Conteo de tipos de procesos usando la columna TIPO_PROCESO que definimos
            est = len(df_mapa[df_mapa["TIPO_PROCESO"].str.contains("Estrategico", na=False, case=False)])
            mis = len(df_mapa[df_mapa["TIPO_PROCESO"].str.contains("Misionales", na=False, case=False)])
            apo = len(df_mapa[df_mapa["TIPO_PROCESO"].str.contains("Apoyo", na=False, case=False)])

            with col_m1:
                st.markdown(f"""
                    <div style="background-color: #002b5c; color: white; padding: 15px; border-radius: 10px; text-align: center; border-bottom: 5px solid #001a38;">
                        <span style="font-size: 20px;">🚀 Estratégicos</span><br>
                        <b style="font-size: 28px;">{est}</b>
                    </div>
                """, unsafe_allow_html=True)
            with col_m2:
                st.markdown(f"""
                    <div style="background-color: #e31e24; color: white; padding: 15px; border-radius: 10px; text-align: center; border-bottom: 5px solid #a81216;">
                        <span style="font-size: 20px;">🏥 Misionales</span><br>
                        <b style="font-size: 28px;">{mis}</b>
                    </div>
                """, unsafe_allow_html=True)
            with col_m3:
                st.markdown(f"""
                    <div style="background-color: #7b7b7b; color: white; padding: 15px; border-radius: 10px; text-align: center; border-bottom: 5px solid #4d4d4d;">
                        <span style="font-size: 20px;">⚙️ Apoyo</span><br>
                        <b style="font-size: 28px;">{apo}</b>
                    </div>
                """, unsafe_allow_html=True)
        # =========================================================

        st.markdown("---")
        
        # --- PREPARACIÓN DE DATOS PARA TABLA Y GRÁFICO (TU CÓDIGO SIGUE IGUAL) ---
        tipos_validos = [
            "PROCEDIMIENTO", "FORMATO", "MANUAL", "INSTRUCTIVO", "GUIA",
            "CERTIFICADO", "PLAN DE CALIDAD", "PROGRAMA",
            "PROTOCOLO", "REGLAMENTO"
        ]

        df["TIPO DE DOCUMENTO"] = df["TIPO DE DOCUMENTO"].astype(str).str.upper().str.strip()
        conteo = df["TIPO DE DOCUMENTO"].value_counts().reindex(tipos_validos, fill_value=0)

        df_tabla = pd.DataFrame({
            "Tipo de Documento": list(conteo.index),
            "Cantidad": list(conteo.values)
        })

        # --- TABLA CON TOTAL ---
        total_docs_real = int(conteo.sum())
        fila_total = pd.DataFrame({"Tipo de Documento": ["TOTAL"], "Cantidad": [total_docs_real]})
        df_tabla_con_total = pd.concat([df_tabla, fila_total], ignore_index=True)
        df_tabla_con_total.index = df_tabla_con_total.index + 1
        st.markdown("### 📋 Resumen por Tipo de Documento")
        st.table(df_tabla_con_total)

        # --- GRÁFICO DE BARRAS ---
        fig = px.bar(
            df_tabla, 
            y="Tipo de Documento",
            x="Cantidad",
            orientation='h',
            color="Tipo de Documento",
            color_discrete_sequence=px.colors.qualitative.Safe, 
            title="Distribución de Documentos",
            text="Cantidad"
        )

        fig.update_layout(
            template="plotly_white",
            showlegend=False,
            plot_bgcolor='rgba(0,0,0,0)', 
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color="black", size=14),
            xaxis=dict(title_text=None, tickfont=dict(color="black"), gridcolor="#eeeeee"),
            yaxis=dict(title_text=None, tickfont=dict(color="black"), categoryorder='total ascending'),
            title=dict(font=dict(size=22, color="black"))
        )

        fig.update_traces(textposition="outside", textfont=dict(color="black", size=14), cliponaxis=False)

        st.plotly_chart(fig, use_container_width=True)

    except Exception as e:
        st.error(f"Error al procesar los datos: {e}")


def normalizar(texto):
    """Limpia el texto: minúsculas, quita tildes, espacios y símbolos."""
    if not texto: 
        return ""
    texto = texto.lower()
    texto = ''.join(
        c for c in unicodedata.normalize('NFD', texto)
        if unicodedata.category(c) != 'Mn'
    )
    return "".join(c for c in texto if c.isalnum())

def pagina_procesos():
    # --- ESTILOS CSS REFORZADOS (Buscador blanco, texto negro) ---
    st.markdown("""
        <style>
        input[type="text"], .stTextInput div div input {
            background-color: white !important;
            color: black !important;
            -webkit-text-fill-color: black !important;
            border: 1px solid #d3d3d3 !important;
        }
        div[data-baseweb="select"] > div {
            background-color: white !important;
            color: black !important;
        }
        div[data-testid="stSelectbox"] p, div[data-testid="stSelectbox"] span {
            color: black !important;
        }
        .kpi-card {
            background-color: #f8f9fa;
            padding: 15px;
            border-radius: 10px;
            text-align: center;
            border-top: 4px solid #002b5c;
            box-shadow: 0px 2px 4px rgba(0,0,0,0.05);
            margin-bottom: 10px;
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("<h1 style='color: #002b5c;'>📌 Gestión de Procesos Institucionales</h1>", unsafe_allow_html=True)

    try:
        df = cargar_excel()
        df_mapa = cargar_mapeo_procesos() 
        df_proced = df[df["TIPO DE DOCUMENTO"].astype(str).str.upper() == "PROCEDIMIENTO"].copy()
    except Exception as e:
        st.error(f"❌ Error al cargar los datos: {e}")
        return

    # --- SIDEBAR ---
    with st.sidebar:
        st.markdown("### 🏢 Configuración")
        areas = sorted(df_proced["PROCESO"].dropna().unique().tolist())
        area_seleccionada = st.selectbox("Área / Proceso:", ["Todos"] + areas, key="sb_proceso")

    df_filtrado = df_proced if area_seleccionada == "Todos" else df_proced[df_proced["PROCESO"] == area_seleccionada]
    nombres_procesos = df_filtrado["TITULO DE DOCUMENTO"].astype(str).tolist()
    
    if not nombres_procesos:
        st.info("No hay procesos disponibles.")
        return

    # ==========================================
    # SISTEMA DE PESTAÑAS
    # ==========================================
    tab_doc, tab_mapa = st.tabs(["📄 Ficha del Documento", "📍 Ubicación en Mapa Estratégico"])

    with tab_doc:
        # --- BUSCADOR Y SELECTOR (DENTRO DE LA FICHA) ---
        st.markdown("### 🔍 Selección de Proceso")
        col_sel, col_busq = st.columns([1, 1])

        with col_busq:
            texto_filtro = st.text_input("Escribe para buscar:", placeholder="Ej: fallecimiento", key="txt_busq_ficha_final")

        palabras = texto_filtro.lower().split()
        opciones_filtradas = [n for n in nombres_procesos if all(p in n.lower() for p in palabras)]

        with col_sel:
            if opciones_filtradas:
                seleccionado = st.selectbox("Selecciona de la lista:", opciones_filtradas, key="sel_doc_ficha_final")
            else:
                st.warning("No hay coincidencias."); st.stop()

        fila = df_filtrado[df_filtrado["TITULO DE DOCUMENTO"] == seleccionado].iloc[0]
        st.markdown("---")

        # --- 1. FICHA TÉCNICA (KPIs) ---
        c1, c2, c3, c4 = st.columns(4)
        with c1: st.markdown(f'<div class="kpi-card"><h3>Código</h3><p>{fila.get("CODIGO", "N/A")}</p></div>', unsafe_allow_html=True)
        with c2: st.markdown(f'<div class="kpi-card"><h3>Versión</h3><p>{fila.get("VERSIÓN", "1")}</p></div>', unsafe_allow_html=True)
        with c3: st.markdown(f'<div class="kpi-card"><h3>Emisión</h3><p>{fila.get("EMISION", "N/A")}</p></div>', unsafe_allow_html=True)
        with c4: st.markdown(f'<div class="kpi-card"><h3>Vigencia</h3><p>{fila.get("VIGENCIA", "N/A")}</p></div>', unsafe_allow_html=True)

        enlace = fila.get("ABRIR", "")
        if enlace and str(enlace).strip().startswith("http"):
            st.markdown(f'<a href="{enlace}" target="_blank" style="text-decoration:none;"><div style="background-color:#002b5c;color:white;padding:12px;text-align:center;border-radius:8px;font-weight:bold;border-bottom:4px solid #e31e24;margin-top:10px;">📥 ABRIR PDF OFICIAL</div></a><br>', unsafe_allow_html=True)

        # --- 2. DIAGRAMA DE FLUJO ---
        with st.expander("📊 Ver Diagrama de Flujo del Proceso", expanded=True):
            ruta_base = "DIAGRAMA"
            archivo_encontrado = None
            if os.path.exists(ruta_base):
                archivos = [f for f in os.listdir(ruta_base) if f.lower().endswith((".png", ".jpg", ".jpeg", ".webp"))]
                nombre_target = normalizar(seleccionado)
                for archivo in archivos:
                    if normalizar(archivo.rsplit(".", 1)[0]) in nombre_target:
                        archivo_encontrado = archivo
                        break
                if archivo_encontrado:
                    if archivo_encontrado:
    # Cambia el 500 por el número de píxeles que desees (ej: 400, 700, 900)
                     st.image(os.path.join(ruta_base, archivo_encontrado), width=1300)

        # --- 3. GESTIÓN DE COMENTARIOS (RESTAURADO) ---
        st.markdown("### 💬 Programar Revisión y Comentarios")
        with st.form("form_comentarios_final", clear_on_submit=True):
            col_f1, col_f2 = st.columns([2, 1])
            with col_f1:
                nuevo_coment = st.text_area("Observaciones o notas de la revisión:")
            with col_f2:
                fecha_revision = st.date_input("Fecha de próxima revisión:", min_value=datetime.date.today())
            
            if st.form_submit_button("🚀 Guardar y Notificar"):
                if nuevo_coment.strip():
                    try:
                        df_coment = cargar_comentarios()
                        nuevo_reg = {
                            "PROCESO": seleccionado,
                            "COMENTARIO": nuevo_coment.strip(),
                            "USUARIO": st.session_state.get("user", "Admin"),
                            "FECHA": datetime.datetime.now(),
                            "FECHA_REVISION": pd.Timestamp(fecha_revision)
                        }
                        df_coment = pd.concat([df_coment, pd.DataFrame([nuevo_reg])], ignore_index=True)
                        guardar_comentarios(df_coment)
                        
                        asunto = f"🚨 REVISIÓN: {seleccionado}"
                        cuerpo = f"Proceso: {seleccionado}\nComentario: {nuevo_coment}\nFecha: {fecha_revision}"
                        enviar_correo_gmail("jairft12@gmail.com", asunto, cuerpo)
                        
                        st.success("✅ Comentario guardado y correo enviado.")
                    except Exception as e:
                        st.error(f"Error al guardar: {e}")
                else:
                    st.warning("Escribe un comentario antes de guardar.")

    with tab_mapa:
        # Pestaña limpia: Solo mapa
        if df_mapa is not None:
            st.markdown(f"### 📍 Ubicación en Mapa: {seleccionado}")
            ct1, ct2, ct3 = st.columns(3)
            with ct1: st.markdown(f'<div class="kpi-card"><h3>Total Áreas</h3><p>{len(df_mapa)}</p></div>', unsafe_allow_html=True)
            with ct2: 
                est_n = len(df_mapa[df_mapa["TIPO_PROCESO"].str.contains("Estrategico", na=False, case=False)])
                st.markdown(f'<div class="kpi-card"><h3>Estratégicos</h3><p>{est_n}</p></div>', unsafe_allow_html=True)
            with ct3: 
                mis_n = len(df_mapa[df_mapa["TIPO_PROCESO"].str.contains("Misionales", na=False, case=False)])
                st.markdown(f'<div class="kpi-card"><h3>Misionales</h3><p>{mis_n}</p></div>', unsafe_allow_html=True)

            st.markdown("---")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown("<h3 style='color: #002b5c;'>🚀 Estratégicos</h3>", unsafe_allow_html=True)
                df_est = df_mapa[df_mapa["TIPO_PROCESO"].str.contains("Estrategico", na=False, case=False)]
                for _, r in df_est.iterrows():
                    res = "border: 2px solid #002b5c; box-shadow: 0px 0px 8px rgba(0,43,92,0.2);" if r['AREA'] == fila['PROCESO'] else ""
                    st.markdown(f'<div style="border-left: 5px solid #002b5c; background: #f8f9fa; padding: 10px; margin-bottom: 5px; border-radius: 5px; {res}"><b>{r["AREA"]}</b><br><small>👤 {r["RESPONSABLE"]}</small></div>', unsafe_allow_html=True)

            with col2:
                st.markdown("<h3 style='color: #e31e24;'>🏥 Misionales</h3>", unsafe_allow_html=True)
                df_mis = df_mapa[df_mapa["TIPO_PROCESO"].str.contains("Misionales", na=False, case=False)]
                for _, r in df_mis.iterrows():
                    res = "border: 2px solid #e31e24; box-shadow: 0px 0px 8px rgba(227,30,36,0.2);" if r['AREA'] == fila['PROCESO'] else ""
                    st.markdown(f'<div style="border-left: 5px solid #e31e24; background: #fff5f5; padding: 10px; margin-bottom: 5px; border-radius: 5px; {res}"><b>{r["AREA"]}</b><br><small>👤 {r["RESPONSABLE"]}</small></div>', unsafe_allow_html=True)

            with col3:
                st.markdown("<h3 style='color: #7b7b7b;'>⚙️ Apoyo</h3>", unsafe_allow_html=True)
                df_apo = df_mapa[df_mapa["TIPO_PROCESO"].str.contains("Apoyo", na=False, case=False)]
                for _, r in df_apo.iterrows():
                    res = "border: 2px solid #7b7b7b;" if r['AREA'] == fila['PROCESO'] else ""
                    st.markdown(f'<div style="border-left: 5px solid #7b7b7b; background: #f1f1f1; padding: 10px; margin-bottom: 5px; border-radius: 5px; {res}"><b>{r["AREA"]}</b><br><small>👤 {r["RESPONSABLE"]}</small></div>', unsafe_allow_html=True)
        else:
            st.warning("No se pudo cargar la información del Mapa Estratégico.")

def pagina_documentos():
    st.markdown("## 📁 Repositorio de Documentos")

    # ===============================
    # CARGA DE DATA
    # ===============================
    @st.cache_data
    def cargar_documentos():
        ruta = "procesos/Bitacora1.xlsx"
        df = pd.read_excel(ruta, sheet_name="Bitacora-Archivos")

        # NORMALIZAR COLUMNAS
        df.columns = (
            df.columns
            .str.strip()
            .str.upper()
            .str.replace("Á", "A")
            .str.replace("É", "E")
            .str.replace("Í", "I")
            .str.replace("Ó", "O")
            .str.replace("Ú", "U")
        )

        return df

    df = cargar_documentos()

    # ===============================
    # COLUMNAS A MOSTRAR
    # ===============================
    columnas = [
        "CODIGO",
        "TIPO DE DOCUMENTO",
        "VERSION",
        "EMISION",
        "VIGENCIA",
        "TITULO DE DOCUMENTO",
        "PROCESO",
        "SUBPROCESO",
        "RESPONSABLE",
        "ABRIR"
    ]

    faltantes = [c for c in columnas if c not in df.columns]
    if faltantes:
        st.error(f"Faltan columnas en el Excel: {', '.join(faltantes)}")
        st.stop()

    # ===============================
    # FILTROS
    # ===============================
    col1, col2 = st.columns([2, 4])

    with col1:
        procesos = ["Todos"] + sorted(df["PROCESO"].dropna().unique().tolist())
        proceso_sel = st.selectbox("📍 Filtrar por Proceso", procesos)

    with col2:
        texto_busqueda = st.text_input("🔍 Buscar documento")

    df_f = df.copy()

    if proceso_sel != "Todos":
        df_f = df_f[df_f["PROCESO"] == proceso_sel]

    if texto_busqueda:
        df_f = df_f[
            df_f.astype(str)
            .apply(lambda x: x.str.contains(texto_busqueda, case=False, na=False))
            .any(axis=1)
        ]

    # ===============================
    # ESTILOS (UNA SOLA VEZ)
    # ===============================
       # ===============================
    # TABLA HTML (CSS DENTRO DEL HTML)
    # ===============================
    tabla = """
    <style>
    .tabla-container {
        max-height: 850px;
        overflow: auto;
        border: 1px solid black;
    }

    table {
        width: 100%;
        border-collapse: collapse;
        font-size: 13px;
    }

    th, td {
        border: 1px solid black !important;
        padding: 6px;
        text-align: center;
        background-color: white;
        color: black;
    }

    th {
        background-color: #0b2c55;
        color: white;
        font-weight: bold;
        position: sticky;
        top: 0;
        z-index: 2;
    }

    td.titulo {
        text-align: left;
        white-space: normal;
    }

    a {
        background-color: #1f77b4;
        color: white !important;
        padding: 3px 8px;
        text-decoration: none;
        border-radius: 4px;
        font-size: 12px;
    }
    </style>

    <div class="tabla-container">
    <table>
        <tr>
    """

    for col in columnas:
        tabla += f"<th>{col}</th>"

    tabla += "</tr>"

    for _, row in df_f.iterrows():
        tabla += "<tr>"
        tabla += f"<td>{row['CODIGO']}</td>"
        tabla += f"<td>{row['TIPO DE DOCUMENTO']}</td>"
        tabla += f"<td>{row['VERSION']}</td>"
        tabla += f"<td>{row['EMISION']}</td>"
        tabla += f"<td>{row['VIGENCIA']}</td>"
        tabla += f"<td class='titulo'>{row['TITULO DE DOCUMENTO']}</td>"
        tabla += f"<td>{row['PROCESO']}</td>"
        tabla += f"<td>{row['SUBPROCESO']}</td>"
        tabla += f"<td>{row['RESPONSABLE']}</td>"

        enlace = row["ABRIR"]
        if isinstance(enlace, str) and enlace.strip():
            boton = f"<a href='{enlace}' target='_blank'>Abrir</a>"
        else:
            boton = "—"

        tabla += f"<td>{boton}</td>"
        tabla += "</tr>"

    tabla += "</table></div>"

    # ===============================
    # MOSTRAR (SIN ERROR removeChild)
    # ===============================
    components.html(
        tabla,
        height=700,
        scrolling=True
    )






# Ejecutar la página
# pagina_documentos()
def pagina_admin():
    st.header("📄 Administración")
    st.subheader("➕ Gestión de Registros")

    ruta_excel = "procesos/Bitacora1.xlsx"

    # 1. CARGA DE EXCEL CON LIMPIEZA
    try:
        df_excel = pd.read_excel(ruta_excel, sheet_name="Bitacora-Archivos")
        df_excel.columns = df_excel.columns.str.strip() # Elimina espacios en blanco en nombres de columnas
    except Exception as e:
        st.error(f"No se pudo cargar el archivo Excel: {e}")
        return

    tabs = st.tabs(["Agregar nuevo", "Editar registro", "Eliminar registro", "Comentarios"])

    # Función de refresco interno
    if "trigger" not in st.session_state:
        st.session_state["trigger"] = False

    def rerun_without_experimental():
        st.session_state["trigger"] = not st.session_state["trigger"]

    # ====== TAB 0: AGREGAR NUEVO ======
    with tabs[0]:
        st.markdown("## ➕ Agregar Nuevo Registro")
        tipos_documento = ["POLÍTICA", "PROCEDIMIENTO", "INSTRUCTIVO", "FORMATO", "MANUAL", "PROTOCOLO", "CHECK LIST", "DOCUMENTO"]

        if "formulario_activo" not in st.session_state:
            st.session_state["formulario_activo"] = False
        if "tipo_doc" not in st.session_state:
            st.session_state["tipo_doc"] = None

        if not st.session_state["formulario_activo"]:
            st.write("Seleccione el tipo de documento para comenzar:")
            cols_tipos = st.columns(4)
            for i, tipo in enumerate(tipos_documento):
                if cols_tipos[i % 4].button(tipo, use_container_width=True):
                    st.session_state["tipo_doc"] = tipo
                    st.session_state["formulario_activo"] = True
                    rerun_without_experimental()
        else:
            tipo_sel = st.session_state["tipo_doc"]
            st.info(f"Registrando nuevo: **{tipo_sel}**")

            # Formulario de entrada
            codigo = st.text_input("Código (ID Único)")
            titulo = st.text_input("Título del documento")
            
            c1, c2 = st.columns(2)
            with c1:
                version = st.text_input("Versión", value="01")
                emision = st.date_input("Fecha de Emisión")
                proceso_peru = st.text_input("Proceso (Sede Local)")
                macroproceso = st.selectbox("Macroproceso", ["ESTRATÉGICO", "MISIONAL", "APOYO"])
            with c2:
                vigencia = st.date_input("Fecha de Vigencia")
                responsable = st.text_input("Responsable del Proceso")
                subproceso = st.text_input("Subproceso")
                viva_col = st.text_input("Equivalencia VIVA 1A (COL)")

            enlace = st.text_input("Enlace Directo (URL)")
            archivo = st.file_uploader("Opcional: Subir archivo físico", type=["pdf", "xlsx", "xlsm", "docx"])

            btn_col1, btn_col2 = st.columns(2)
            with btn_col1:
                if st.button("💾 Guardar en Bitácora"):
                    # --- VALIDACIONES ---
                    if codigo.strip() == "":
                        st.warning("El campo Código es obligatorio.")
                    elif codigo.strip() in df_excel["CODIGO"].astype(str).values:
                        st.error(f"❌ El código **{codigo}** ya existe. No se permiten duplicados.")
                    else:
                        # Crear registro
                        nueva_fila = {
                            "CODIGO": codigo.strip(),
                            "TIPO DE DOCUMENTO": tipo_sel,
                            "VERSIÓN": version,
                            "EMISION": emision,
                            "VIGENCIA": vigencia,
                            "TITULO DE DOCUMENTO": titulo,
                            "PROCESO": proceso_peru,
                            "SUBPROCESO": subproceso,
                            "RESPONSABLE": responsable,
                            "MACROPROCESO": macroproceso,
                            "PROCESO VIVA 1A (COL)": viva_col,
                            "DOCUMENTACION": "",
                            "ABRIR": enlace
                        }

                        df_excel = pd.concat([df_excel, pd.DataFrame([nueva_fila])], ignore_index=True)
                        df_excel.to_excel(ruta_excel, sheet_name="Bitacora-Archivos", index=False)

                        if archivo:
                            with open(f"procesos/{archivo.name}", "wb") as f:
                                f.write(archivo.getbuffer())

                        st.success("✅ Registro guardado exitosamente.")
                        st.session_state["formulario_activo"] = False
                        rerun_without_experimental()

            with btn_col2:
                if st.button("Cancelar"):
                    st.session_state["formulario_activo"] = False
                    rerun_without_experimental()
# ====== TAB 1: EDITAR REGISTRO ======
    with tabs[1]:
        st.markdown("### ✏️ Editar Registro Existente")
        lista_codigos = df_excel["CODIGO"].astype(str).tolist()
        
        if not lista_codigos:
            st.info("No hay datos disponibles.")
        else:
            cod_a_editar = st.selectbox("Busque el código a modificar", lista_codigos, key="edit_search")
            
            if "edit_mode" not in st.session_state: 
                st.session_state["edit_mode"] = False

            fila_data = df_excel[df_excel["CODIGO"].astype(str) == cod_a_editar].iloc[0]

            if not st.session_state["edit_mode"]:
                st.write(f"**Documento:** {fila_data['TITULO DE DOCUMENTO']}")
                st.write(f"**Código Actual:** {fila_data['CODIGO']}")
                if st.button("Habilitar Edición"):
                    st.session_state["edit_mode"] = True
                    st.rerun()
            else:
                # --- CAMPOS DE EDICIÓN AMPLIADOS ---
                st.warning(f"Editando el registro: {cod_a_editar}")
                
                col_ed1, col_ed2 = st.columns(2)
                
                with col_ed1:
                    new_codigo = st.text_input("Código (ID Único)", value=str(fila_data["CODIGO"]))
                    new_titulo = st.text_input("Título", value=fila_data["TITULO DE DOCUMENTO"])
                    new_proceso = st.text_input("Proceso", value=fila_data["PROCESO"] if pd.notna(fila_data["PROCESO"]) else "")
                    new_macro = st.selectbox("Macroproceso", 
                                           ["ESTRATÉGICO", "MISIONAL", "APOYO"], 
                                           index=["ESTRATÉGICO", "MISIONAL", "APOYO"].index(fila_data["MACROPROCESO"]) if pd.notna(fila_data["MACROPROCESO"]) else 0)

                with col_ed2:
                    new_subproceso = st.text_input("Subproceso", value=fila_data["SUBPROCESO"] if pd.notna(fila_data["SUBPROCESO"]) else "")
                    new_viva_col = st.text_input("Proceso VIVA 1A (COL)", value=fila_data["PROCESO VIVA 1A (COL)"] if pd.notna(fila_data["PROCESO VIVA 1A (COL)"]) else "")
                    new_resp = st.text_input("Responsable", value=fila_data["RESPONSABLE"] if pd.notna(fila_data["RESPONSABLE"]) else "")
                    new_link = st.text_input("Enlace ABRIR", value=fila_data["ABRIR"] if pd.notna(fila_data["ABRIR"]) else "")

                # --- BOTONES DE ACCIÓN ---
                ec1, ec2 = st.columns(2)
                with ec1:
                    if st.button("Confirmar Cambios"):
                        # Obtener el índice real en el DataFrame
                        idx = df_excel[df_excel["CODIGO"].astype(str) == cod_a_editar].index[0]
                        
                        # Actualizar todos los campos
                        df_excel.at[idx, "CODIGO"] = new_codigo
                        df_excel.at[idx, "TITULO DE DOCUMENTO"] = new_titulo
                        df_excel.at[idx, "RESPONSABLE"] = new_resp
                        df_excel.at[idx, "ABRIR"] = new_link
                        df_excel.at[idx, "PROCESO"] = new_proceso
                        df_excel.at[idx, "SUBPROCESO"] = new_subproceso
                        df_excel.at[idx, "PROCESO VIVA 1A (COL)"] = new_viva_col
                        df_excel.at[idx, "MACROPROCESO"] = new_macro

                        # Guardar en el archivo físico
                        df_excel.to_excel(ruta_excel, sheet_name="Bitacora-Archivos", index=False)
                        
                        st.success("✅ Registro actualizado correctamente.")
                        st.session_state["edit_mode"] = False
                        st.rerun()
                        
                with ec2:
                    if st.button("Descartar"):
                        st.session_state["edit_mode"] = False
                        st.rerun()

    # ====== TAB 2: ELIMINAR REGISTRO ======
    with tabs[2]:
        st.markdown("### 🗑️ Zona de Eliminación")
        cod_eliminar = st.selectbox("Seleccione código para borrar", df_excel["CODIGO"].astype(str).tolist(), key="del_search")
        
        confirmar = st.checkbox(f"Confirmo que deseo borrar permanentemente el registro {cod_eliminar}")
        if st.button("❌ Eliminar Definitivamente"):
            if confirmar:
                df_excel = df_excel[df_excel["CODIGO"].astype(str) != cod_eliminar]
                df_excel.to_excel(ruta_excel, sheet_name="Bitacora-Archivos", index=False)
                st.success("Registro eliminado.")
                rerun_without_experimental()
            else:
                st.warning("Debe marcar la casilla de confirmación.")

    # ====== TAB 3: COMENTARIOS ======
    with tabs[3]:
        st.subheader("📋 Historial de Revisiones")
        df_coment = cargar_comentarios()
        if not df_coment.empty:
            df_coment["FECHA_REVISION"] = pd.to_datetime(df_coment["FECHA_REVISION"])
            st.dataframe(df_coment.sort_values("FECHA_REVISION", ascending=False), use_container_width=True)
        else:
            st.info("Sin comentarios registrados.")
            # RESTAURAR ESTA FUNCIÓN PARA QUITAR EL ERROR
def cargar_mapeo_procesos():
    archivo = "procesos/Tipo de Procesos por Responsable.xlsx"
    if not os.path.exists(archivo):
        return None
    try:
        df = pd.read_excel(archivo, sheet_name="TipoProceso", skiprows=5)
        df = df.dropna(how='all', axis=1)
        # Ajustamos columnas básicas
        df.columns = ["AREA", "RESPONSABLE", "TIPO_PROCESO"] + list(df.columns[3:])
        df = df.dropna(subset=["AREA"])
        df = df[df["AREA"].astype(str).str.upper() != "TOTAL"]
        return df
    except:
        return None
def pagina_analisis():

    # Título principal (Mantenemos tu estructura)
    st.markdown("<h1 style='text-align: left; color: #002b5c;'>📊 Análisis de Gestión Documental</h1>", unsafe_allow_html=True)
    
    # 1. Cargar y preparar datos
    df = cargar_excel()
    df.columns = df.columns.str.strip()
    df["VIGENCIA"] = pd.to_datetime(df["VIGENCIA"], errors='coerce')
    hoy = pd.Timestamp.now().normalize()
    proximo_vencer = hoy + pd.Timedelta(days=30)

    # --- BLOQUE DE INDICADORES (ESTILO INICIO) ---
    total_docs = len(df)
    vencidos = len(df[df["VIGENCIA"] < hoy])
    por_vencer = len(df[(df["VIGENCIA"] >= hoy) & (df["VIGENCIA"] <= proximo_vencer)])

    c1, c2, c3 = st.columns(3)
    estilo_tarjeta = """
        <div style="border-left: 5px solid #002b5c; background: #f8f9fa; padding: 10px; margin-bottom: 5px; border-radius: 5px; box-shadow: 1px 1px 3px rgba(0,0,0,0.05);">
            <span style="color: #002b5c; font-size: 14px; font-weight: bold;">{titulo}</span><br>
            <b style="color: #1f1f1f; font-size: 24px;">{valor}</b>
        </div>
    """
    with c1: st.markdown(estilo_tarjeta.format(titulo="📄 TOTAL DOCUMENTOS", valor=total_docs), unsafe_allow_html=True)
    with c2: st.markdown(estilo_tarjeta.format(titulo="🚨 DOCUMENTOS VENCIDOS", valor=vencidos), unsafe_allow_html=True)
    with c3: st.markdown(estilo_tarjeta.format(titulo="⚠️ PRÓXIMOS A VENCER", valor=por_vencer), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # --- SUB-PESTAÑAS ---
    sub_tab1, sub_tab2, sub_tab3 = st.tabs(["🚀 Gestión de Vigencias", "🏗️ Estructura Estratégica", "🌍 Homologación Colombia"])
    st.markdown("<style>.card-grafica {background: white; padding: 20px; border-radius: 15px; box-shadow: 0px 10px 20px rgba(0,0,0,0.1); border: 1px solid #f0f2f6;}</style>", unsafe_allow_html=True)
    # ====== PESTAÑA 1: GESTIÓN DE VIGENCIAS (CONTENEDOR BLANCO TIPO CARD) ======
    with sub_tab1:
        # Abrimos el contenedor blanco (el "cuadrado" de la imagen)
        st.markdown("""
            <div style="background-color: white; padding: 25px; border-radius: 15px; border: 1px solid #f0f0f0; box-shadow: 0px 4px 12px rgba(0,0,0,0.05);">
                <h3 style="color: #002b5c; margin-top: 0;">Semáforo de Cumplimiento por Responsable</h3>
        """, unsafe_allow_html=True)
        
        # Filtros dentro del cuadro
        opciones_macro = ["TODOS LOS MACROPROCESOS"] + list(df["MACROPROCESO"].dropna().unique())
        filtro = st.selectbox("Filtrar por Nivel:", opciones_macro, key="filtro_vigencia")
        
        df_f = df if filtro == "TODOS LOS MACROPROCESOS" else df[df["MACROPROCESO"] == filtro]

        def calcular_estado(fecha):
            if pd.isna(fecha): return "Sin Fecha"
            if fecha < hoy: return "Vencido"
            if fecha <= proximo_vencer: return "Próximo (30d)"
            return "Al día"

        df_f["ESTADO"] = df_f["VIGENCIA"].apply(calcular_estado)
        df_plot = df_f.groupby(["RESPONSABLE", "ESTADO"]).size().reset_index(name='Cantidad')

        # Gráfica Horizontal
        fig = px.bar(
            df_plot, 
            y="RESPONSABLE", 
            x="Cantidad", 
            color="ESTADO",
            orientation='h',
            color_discrete_map={
                "Vencido": "#E31E24", 
                "Próximo (30d)": "#FFC107", 
                "Al día": "#28A745", 
                "Sin Fecha": "#7B7B7B"
            },
            barmode="stack", 
            template="plotly_white",
            height=400
        )
        fig.update_layout(
            template="simple_white",
            paper_bgcolor='rgba(0,0,0,0)', 
            plot_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=10, r=10, t=50, b=10),
            
            # Color de todo el texto (Leyenda y nombres)
            font=dict(color="black"), 
            
            # Configuración del Eje Y (Nombres de responsables)
            yaxis=dict(
                showgrid=False, 
                title_text="", 
                tickfont=dict(
                    color="black", 
                    size=12, 
                    weight="bold" # <--- ESTO ES LO CORRECTO (weight en lugar de bold)
                ), 
                ticksuffix="  "
            ),
            
            # Configuración del Eje X (Oculto)
            xaxis=dict(
                showgrid=False, 
                visible=False
            ),
            
            # Leyenda moderna arriba
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="center",
                x=0.5,
                title_text="",
                font=dict(color="black")
            )
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Cerramos el div del contenedor blanco
        st.markdown("</div>", unsafe_allow_html=True)

    # ====== PESTAÑA 2: ESTRUCTURA ESTRATÉGICA ======
    with sub_tab2:
        st.subheader("Balance del Sistema por Macroproceso")
        conteo_macro = df["MACROPROCESO"].value_counts().reset_index()
        fig_pie = px.pie(
            conteo_macro, values='count', names='MACROPROCESO', hole=0.4,
            color_discrete_map={"ESTRATÉGICO": "#002b5c", "MISIONAL": "#E31E24", "APOYO": "#7B7B7B"}
        )
        st.plotly_chart(fig_pie, use_container_width=True)

    with sub_tab3:
        # 1. EL TRUCO DEFINITIVO: Inyectamos el estilo al contenedor de la pestaña 
        # Esto aplica la sombra a TODO lo que esté dentro de un 'st.container' con borde
        st.markdown("""
            <style>
            /* Buscamos el contenedor de la gráfica y le aplicamos el estilo a la fuerza */
            [data-testid="stMetricDelta"] + div, 
            div[data-testid="stVerticalBlockBorderWrapper"] {
                background-color: white !important;
                border: 1px solid #ddd !important;
                border-radius: 20px !important;
                box-shadow: 0px 12px 30px rgba(0,0,0,0.2) !important;
                padding: 15px !important;
                display: block !important;
            }
            </style>
        """, unsafe_allow_html=True)

        st.subheader("Sincronización con VIVA 1A (COL)")

        # 2. Tu lógica de datos (sin cambios)
        df_col = df.copy()
        df_col['VINCULADO'] = df_col['PROCESO VIVA 1A (COL)'].apply(
            lambda x: "✅ Vinculado" if pd.notna(x) and str(x).strip() != "" else "❌ Pendiente"
        )
        df_resumen = df_col.groupby(['PROCESO', 'VINCULADO']).size().reset_index(name='Cant')

        # 3. Tu gráfica
        fig_col = px.bar(
            df_resumen,
            x='PROCESO', y='Cant', color='VINCULADO',
            color_discrete_map={"✅ Vinculado": "#002b5c", "❌ Pendiente": "#D3D3D3"},
            template="simple_white"
        )
        
        # 4. EL CONTENEDOR (Esto es lo que recibirá la sombra del CSS de arriba)
        with st.container(border=True):
            st.plotly_chart(fig_col, use_container_width=True, key="grafica_viva_definitiva")

pagina_activa = render_sidebar()

if pagina_activa == "Inicio":
    pagina_inicio()
elif pagina_activa == "Procesos":
    pagina_procesos()   
     
elif pagina_activa == "Documentos":
    pagina_documentos()

elif pagina_activa == "Administración":
    if st.session_state.get("role") == "admin":
        pagina_admin()
    else:
        st.error("No tienes permisos para acceder a esta sección.")
elif pagina_activa == "Análisis de Calidad":
    pagina_analisis()
# Cambio para actualizar