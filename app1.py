import os
import datetime
import smtplib

import streamlit as st
import pandas as pd
import plotly.express as px

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
st.set_page_config(page_title="Procesos", layout="wide")
# --- CONFIGURACIÓN VISUAL VIVA 1A ---
import streamlit as st
import pandas as pd
import plotly.express as px

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


import streamlit as st
import pandas as pd
import os
import datetime

def pagina_procesos():
    st.markdown("<h1 style='color: #002b5c;'>📌 Gestión de Procesos Institucionales</h1>", unsafe_allow_html=True)

    try:
        # 1. CARGA DE DATOS
        df = cargar_excel()
        df_mapa = cargar_mapeo_procesos() 
        df_proced = df[df["TIPO DE DOCUMENTO"].astype(str).str.upper() == "PROCEDIMIENTO"].copy()
    except Exception as e:
        st.error(f"❌ Error al cargar los datos: {e}")
        return

    # --- SIDEBAR: FILTRO POR ÁREA ---
    with st.sidebar:
        st.markdown("### 🏢 Configuración")
        areas = sorted(df_proced["PROCESO"].dropna().unique().tolist())
        area_seleccionada = st.selectbox("Área / Proceso:", ["Todos"] + areas, key="sb_proceso")

    df_filtrado = df_proced if area_seleccionada == "Todos" else df_proced[df_proced["PROCESO"] == area_seleccionada]
    nombres_procesos = df_filtrado["TITULO DE DOCUMENTO"].astype(str).tolist()
    
    if not nombres_procesos:
        st.info("No hay procesos disponibles.")
        return

    # --- SELECTOR DE PROCESO ---
    seleccionado = st.selectbox("Selecciona el proceso:", nombres_procesos, key="sel_doc")
    fila = df_filtrado[df_filtrado["TITULO DE DOCUMENTO"] == seleccionado].iloc[0]

    st.markdown("---")

    # ==========================================
    # SISTEMA DE PESTAÑAS
    # ==========================================
    tab_doc, tab_mapa = st.tabs(["📄 Ficha del Documento", "📍 Ubicación en Mapa Estratégico"])

    with tab_doc:
        # --- 1. FICHA TÉCNICA ---
        c1, c2, c3, c4 = st.columns(4)
        with c1: st.markdown(f'<div class="kpi-card"><h3>Código</h3><p>{fila.get("CODIGO", "N/A")}</p></div>', unsafe_allow_html=True)
        with c2: st.markdown(f'<div class="kpi-card"><h3>Versión</h3><p>{fila.get("VERSIÓN", "1")}</p></div>', unsafe_allow_html=True)
        with c3: st.markdown(f'<div class="kpi-card"><h3>Emisión</h3><p>{fila.get("EMISION", "N/A")}</p></div>', unsafe_allow_html=True)
        with c4: st.markdown(f'<div class="kpi-card"><h3>Vigencia</h3><p>{fila.get("VIGENCIA", "N/A")}</p></div>', unsafe_allow_html=True)

        # Botón PDF
        enlace = fila.get("ABRIR", "")
        if enlace and str(enlace).strip().startswith("http"):
            st.markdown(f'<a href="{enlace}" target="_blank" style="text-decoration:none;"><div style="background-color:#002b5c;color:white;padding:12px;text-align:center;border-radius:8px;font-weight:bold;border-bottom:4px solid #e31e24;margin-top:10px;">📥 ABRIR PDF OFICIAL</div></a><br>', unsafe_allow_html=True)

        # --- 2. DIAGRAMA DE FLUJO ---
        with st.expander("📊 Ver Diagrama de Flujo del Proceso", expanded=True):
            ruta_base = "DIAGRAMA"
            archivo_encontrado = None

            def normalizar(texto):
                return "".join(c for c in texto.lower() if c.isalnum())

            if os.path.exists(ruta_base):
                extensiones_validas = (".png", ".jpg", ".jpeg", ".webp")
                archivos = [f for f in os.listdir(ruta_base) if f.lower().endswith(extensiones_validas)]
                nombre_target = normalizar(seleccionado)
                
                for archivo in archivos:
                    nombre_archivo_sin_ext = archivo.rsplit(".", 1)[0]
                    if normalizar(nombre_archivo_sin_ext) in nombre_target:
                        archivo_encontrado = archivo
                        break
                
                if archivo_encontrado:
                    st.image(os.path.join(ruta_base, archivo_encontrado), width=1200)
                else:
                    st.info("No hay un diagrama visual cargado para este proceso.")
            else:
                st.error("❌ Carpeta de diagramas no encontrada.")

        # --- 3. GESTIÓN DE COMENTARIOS (DENTRO DE ESTA PESTAÑA) ---
        st.markdown("### 💬 Programar Revisión y Comentarios")
        with st.form("form_nuevo_comentario", clear_on_submit=True):
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
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error al guardar: {e}")
                else:
                    st.warning("Escribe un comentario antes de guardar.")

    with tab_mapa:
        # --- 4. MAPA ESTRATÉGICO (SIN GRÁFICAS, SOLO INFORMACIÓN) ---
        if df_mapa is not None:
            # KPIs del Mapa
            ct1, ct2, ct3 = st.columns(3)
            with ct1: st.markdown(f'<div class="kpi-card"><h3>Total Áreas</h3><p>{len(df_mapa)}</p></div>', unsafe_allow_html=True)
            with ct2: 
                est_n = len(df_mapa[df_mapa["TIPO_PROCESO"].str.contains("Estrategico", na=False, case=False)])
                st.markdown(f'<div class="kpi-card"><h3>Estratégicos</h3><p>{est_n}</p></div>', unsafe_allow_html=True)
            with ct3: 
                mis_n = len(df_mapa[df_mapa["TIPO_PROCESO"].str.contains("Misionales", na=False, case=False)])
                st.markdown(f'<div class="kpi-card"><h3>Misionales</h3><p>{mis_n}</p></div>', unsafe_allow_html=True)

            st.markdown("---")

            # Columnas de Responsables (Incluye Áreas y Líderes con nombre completo)
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown("<h3 style='color: #002b5c;'>🚀 Estratégicos</h3>", unsafe_allow_html=True)
                df_est = df_mapa[df_mapa["TIPO_PROCESO"].str.contains("Estrategico", na=False, case=False)]
                for _, r in df_est.iterrows():
                    resaltado = "border: 2px solid #002b5c; box-shadow: 0px 0px 8px rgba(0,43,92,0.2);" if r['AREA'] == fila['PROCESO'] else ""
                    st.markdown(f"""
                        <div style="border-left: 5px solid #002b5c; background: #f8f9fa; padding: 10px; margin-bottom: 5px; border-radius: 5px; {resaltado}">
                            <b>{r['AREA']}</b><br><small>👤 {r['RESPONSABLE']}</small>
                        </div>
                    """, unsafe_allow_html=True)

            with col2:
                st.markdown("<h3 style='color: #e31e24;'>🏥 Misionales</h3>", unsafe_allow_html=True)
                df_mis = df_mapa[df_mapa["TIPO_PROCESO"].str.contains("Misionales", na=False, case=False)]
                for _, r in df_mis.iterrows():
                    resaltado = "border: 2px solid #e31e24; box-shadow: 0px 0px 8px rgba(227,30,36,0.2);" if r['AREA'] == fila['PROCESO'] else ""
                    st.markdown(f"""
                        <div style="border-left: 5px solid #e31e24; background: #fff5f5; padding: 10px; margin-bottom: 5px; border-radius: 5px; {resaltado}">
                            <b>{r['AREA']}</b><br><small>👤 {r['RESPONSABLE']}</small>
                        </div>
                    """, unsafe_allow_html=True)

            with col3:
                st.markdown("<h3 style='color: #7b7b7b;'>⚙️ Apoyo</h3>", unsafe_allow_html=True)
                df_apo = df_mapa[df_mapa["TIPO_PROCESO"].str.contains("Apoyo", na=False, case=False)]
                for _, r in df_apo.iterrows():
                    resaltado = "border: 2px solid #7b7b7b;" if r['AREA'] == fila['PROCESO'] else ""
                    st.markdown(f"""
                        <div style="border-left: 5px solid #7b7b7b; background: #f1f1f1; padding: 10px; margin-bottom: 5px; border-radius: 5px; {resaltado}">
                            <b>{r['AREA']}</b><br><small>👤 {r['RESPONSABLE']}</small>
                        </div>
                    """, unsafe_allow_html=True)
        else:
            st.warning("No se pudo cargar la información del Mapa Estratégico.")
  
def pagina_documentos():
    st.markdown("<h1 style='color: #002b5c;'>📄 Repositorio de Documentos</h1>", unsafe_allow_html=True)
    
    try:
        df = cargar_excel()
    except FileNotFoundError:
        st.error("No se encontró el archivo 'Bitacora.xlsx'.")
        return

    # --- FILTROS ---
    df = df[df["TIPO DE DOCUMENTO"].astype(str).str.upper() != "PROCEDIMIENTO"]
    
    procesos = sorted(df["PROCESO"].dropna().unique())
    col1, col2 = st.columns([1, 2])
    
    with col1:
        proceso_seleccionado = st.selectbox("📍 Filtrar por Proceso", ["Todos"] + procesos)
    with col2:
        busqueda = st.text_input("🔍 Buscar por palabra clave (Título, Código, Responsable...)")

    # Aplicar Filtros
    if proceso_seleccionado != "Todos":
        df = df[df["PROCESO"] == proceso_seleccionado]
    
    if busqueda:
        # Filtrar en todo el dataframe por la palabra clave
        df = df[df.apply(lambda row: row.astype(str).str.contains(busqueda, case=False).any(), axis=1)]

    # --- PREPARACIÓN DE DATOS ---
    df_mostrar = df.copy()
    
    # Limpiamos nombres de columnas para evitar errores de espacios invisibles
    df_mostrar.columns = df_mostrar.columns.str.strip()

    # Convertimos los links en "Botones"
    if "ABRIR" in df_mostrar.columns:
        df_mostrar["ABRIR"] = df_mostrar["ABRIR"].apply(
            lambda x: f'<a href="{x}" target="_blank" class="btn-abrir">Ver Documento</a>' 
            if pd.notna(x) and str(x).startswith("http") 
            else '<span style="color:gray">No disponible</span>'
        )

    # Definimos las columnas que queremos ver (Basado en tu lista confirmada)
    columnas_a_ver = [
        'CODIGO', 'TIPO DE DOCUMENTO', 'VERSIÓN', 'EMISION', 
        'VIGENCIA', 'TITULO DE DOCUMENTO', 'PROCESO', 'ABRIR'
    ]
    
    # Filtro de seguridad: Solo usamos las que existen en este archivo
    columnas_finales = [col for col in columnas_a_ver if col in df_mostrar.columns]

    # --- ESTILO CSS ---
    st.markdown("""
    <style>
        .table-container {
            height: 600px;
            overflow-y: auto;
            border: 1px solid #e0e0e0;
            border-radius: 8px;
        }
        .tabla-viva {
            width: 100%;
            border-collapse: separate;
            border-spacing: 0;
        }
        .tabla-viva thead th {
            position: sticky;
            top: 0;
            z-index: 10;
            background-color: #002b5c !important;
            color: #FFFFFF !important;
            padding: 15px !important;
            border-bottom: 2px solid #001a38;
        }
        .tabla-viva td {
            white-space: normal;
            word-wrap: break-word;
            padding: 10px;
            border-bottom: 1px solid #eee;
            color: #000000 !important; /* Asegura texto negro en la tabla */
        }
        .btn-abrir {
            background-color: #002b5c;
            color: white !important;
            padding: 6px 12px;
            text-decoration: none;
            border-radius: 4px;
            font-weight: bold;
            display: inline-block;
        }
        .btn-abrir:hover { background-color: #e31e24; }
    </style>
    """, unsafe_allow_html=True)

    # --- RENDERIZADO DE TABLA ---
    if len(columnas_finales) > 0:
        html_tabla = df_mostrar[columnas_finales].to_html(escape=False, index=False, classes='tabla-viva')
        st.markdown(f'<div class="table-container">{html_tabla}</div>', unsafe_allow_html=True)
    else:
        st.error("⚠️ No se encontraron las columnas necesarias en el Excel.")
        st.write("Columnas detectadas:", df_mostrar.columns.tolist())

def pagina_admin():
    st.header("📄 Administración")
    st.subheader("➕ Gestión de Registros")

    ruta_excel = "procesos/Bitacora1.xlsx"

    # Cargar Excel
    try:
        df_excel = pd.read_excel(ruta_excel, sheet_name="Bitacora-Archivos")
    except Exception as e:
        st.error(f"No se pudo cargar el archivo Excel: {e}")
        return

    tabs = st.tabs(["Agregar nuevo", "Editar registro", "Eliminar registro", "Comentarios"])

    # Función para simular rerun sin experimental_rerun()
    if "trigger" not in st.session_state:
        st.session_state["trigger"] = False

    def rerun_without_experimental():
        st.session_state["trigger"] = not st.session_state["trigger"]

    # ====== AGREGAR NUEVO ======
    with tabs[0]:
        st.markdown("## ➕ Agregar Nuevo Registro")

        tipos_documento = [
            "POLÍTICA",
            "PROCEDIMIENTO",
            "INSTRUCTIVO",
            "FORMATO",
            "MANUAL",
            "PROTOCOLO",
            "CHECK LIST",
            "DOCUMENTO"
        ]

        if "formulario_activo" not in st.session_state:
            st.session_state["formulario_activo"] = False
        if "tipo_doc" not in st.session_state:
            st.session_state["tipo_doc"] = None

        if not st.session_state["formulario_activo"]:
            st.write("Seleccione el tipo de documento:")
            for tipo in tipos_documento:
                if st.button(tipo):
                    st.session_state["tipo_doc"] = tipo
                    st.session_state["formulario_activo"] = True
                    rerun_without_experimental()

        else:
            tipo = st.session_state["tipo_doc"]
            st.markdown(f"### Nuevo registro para: **{tipo}**")

            # Campos para llenar
            codigo = st.text_input("Código")
            version = st.text_input("Versión")
            emision = st.date_input("Emisión")
            vigencia = st.date_input("Vigencia")
            titulo = st.text_input("Título del documento")
            proceso = st.text_input("Proceso")
            subproceso = st.text_input("Subproceso")
            responsable = st.text_input("Responsable")
            enlace = st.text_input("Enlace (columna ABRIR)")
            archivo = st.file_uploader("Subir archivo", type=["pdf", "xlsx", "xlsm", "docx"])

            col1, col2 = st.columns(2)

            with col1:
                if st.button("💾 Guardar registro"):
                    # Validar que código no esté vacío
                    if codigo.strip() == "":
                        st.warning("El campo Código es obligatorio.")
                    else:
                        nueva_fila = {
                            "CODIGO": codigo,
                            "TIPO DE DOCUMENTO": tipo,
                            "VERSIÓN": version,
                            "EMISION": emision,
                            "VIGENCIA": vigencia,
                            "TITULO DE DOCUMENTO": titulo,
                            "PROCESO": proceso,
                            "SUBPROCESO": subproceso,
                            "RESPONSABLE": responsable,
                            "DOCUMENTACION": "",
                            "ABRIR": enlace
                        }

                        df_excel = pd.concat([df_excel, pd.DataFrame([nueva_fila])], ignore_index=True)
                        df_excel.to_excel(ruta_excel, sheet_name="Bitacora-Archivos", index=False)

                        if archivo:
                            with open(f"procesos/{archivo.name}", "wb") as f:
                                f.write(archivo.getbuffer())

                        st.success("Registro agregado correctamente.")

                        # Volver a selección inicial
                        st.session_state["formulario_activo"] = False
                        st.session_state["tipo_doc"] = None
                        rerun_without_experimental()

            with col2:
                if st.button("Cancelar"):
                    st.session_state["formulario_activo"] = False
                    st.session_state["tipo_doc"] = None
                    rerun_without_experimental()

    # Aquí puedes agregar los otros tabs: editar, eliminar, comentarios
    # ... (tu código actual)



# ====== EDITAR REGISTRO ======
    with tabs[1]:
        st.markdown("### ✏️ Editar Registro")

        if "editar_activo" not in st.session_state:
              st.session_state["editar_activo"] = False
        if "codigo_edit_actual" not in st.session_state:
              st.session_state["codigo_edit_actual"] = None

        codigos = df_excel["CODIGO"].astype(str).tolist()
        if len(codigos) == 0:
             st.info("No hay registros para editar.")
        else:
             seleccionado = st.selectbox("Seleccione código para editar", codigos, key="select_codigo_edit")

        if st.session_state["codigo_edit_actual"] != seleccionado:
             st.session_state["editar_activo"] = False
             st.session_state["codigo_edit_actual"] = seleccionado
             rerun()

        fila_edit = df_excel[df_excel["CODIGO"].astype(str) == seleccionado].iloc[0]

        # Si no está activo modo edición, solo mostrar datos en modo lectura
        if not st.session_state["editar_activo"]:
               st.text_input("Código", value=fila_edit["CODIGO"], disabled=True)
               st.text_input("Tipo de documento", value=fila_edit["TIPO DE DOCUMENTO"], disabled=True)
               st.text_input("Enlace (ABRIR)", value=fila_edit["ABRIR"] if pd.notna(fila_edit["ABRIR"]) else "", disabled=True)

               if st.button("Editar", key="btn_editar"):
                 st.session_state["editar_activo"] = True
                 rerun()
        else:
            # Modo edición activado
            nuevo_codigo = st.text_input("Código", value=fila_edit["CODIGO"], key="editar_codigo")
            nuevo_tipo = st.selectbox(
                "Tipo de documento",
                options=["PROCEDIMIENTO", "DOCUMENTO"],
                index=["PROCEDIMIENTO", "DOCUMENTO"].index(fila_edit["TIPO DE DOCUMENTO"].upper()) if fila_edit["TIPO DE DOCUMENTO"].upper() in ["PROCEDIMIENTO", "DOCUMENTO"] else 0,
                key="editar_tipo"
            )
            nuevo_abrir = st.text_input(
                "Enlace (ABRIR)",
                value=fila_edit["ABRIR"] if pd.notna(fila_edit["ABRIR"]) else "",
                key="editar_abrir"
            )

            col1, col2 = st.columns(2)
            with col1:
                if st.button("Guardar cambios", key="btn_guardar"):
                    idx = df_excel[df_excel["CODIGO"].astype(str) == seleccionado].index[0]

                    df_excel.at[idx, "CODIGO"] = nuevo_codigo
                    df_excel.at[idx, "TIPO DE DOCUMENTO"] = nuevo_tipo
                    df_excel.at[idx, "ABRIR"] = nuevo_abrir

                    df_excel.to_excel(ruta_excel, sheet_name="Bitacora-Archivos", index=False)
                    st.success("Registro actualizado correctamente.")

                    st.session_state["editar_activo"] = False
                    rerun()

            with col2:
                if st.button("Cancelar", key="btn_cancelar"):
                   st.session_state["editar_activo"] = False
                   rerun()

# ====== ELIMINAR REGISTRO ======
        with tabs[2]:
             st.markdown("### 🗑️ Eliminar Registro")

             if "eliminar_activo" not in st.session_state:
              st.session_state["eliminar_activo"] = False

             codigos = df_excel["CODIGO"].astype(str).tolist()
             if len(codigos) == 0:
              st.info("No hay registros para eliminar.")
             else:
              seleccionado = st.selectbox("Seleccione código para eliminar", codigos, key="select_codigo_eliminar")

             if not st.session_state["eliminar_activo"]:
              st.text(f"Código seleccionado: {seleccionado}")
             if st.button("Eliminar registro", key="btn_eliminar"):
                st.session_state["eliminar_activo"] = True
                rerun()
             else:
              confirm = st.checkbox("Confirmar eliminación", key="confirmar_eliminar")
             if st.button("Confirmar eliminación final", key="btn_confirmar_eliminar"):
                if confirm:
                    df_excel = df_excel[df_excel["CODIGO"].astype(str) != seleccionado]
                    df_excel.to_excel(ruta_excel, sheet_name="Bitacora-Archivos", index=False)
                    st.success("Registro eliminado correctamente.")
                    st.session_state["eliminar_activo"] = False
                    rerun()
                else:
                    st.warning("Marca la casilla para confirmar eliminación.")

                tabs = st.tabs(["Agregar nuevo", "Editar registro", "Eliminar registro", "Comentarios"])

# ... código de agregar, editar, eliminar ...

        with tabs[3]:
             st.subheader("📋 Comentarios de Procesos")

             df_coment = cargar_comentarios()

             if "filtrar_comentarios" not in st.session_state:
              st.session_state["filtrar_comentarios"] = False

# Botón para activar filtro
              if st.button("Limpiar vista (mostrar próximas 20 fechas)"):
               st.session_state["filtrar_comentarios"] = True

              if df_coment.empty:
               st.info("No hay comentarios registrados.")
             else:
    # Para trabajar bien con fechas reales (tipo datetime)
               df_coment["FECHA"] = pd.to_datetime(df_coment["FECHA"])
               df_coment["FECHA_REVISION"] = pd.to_datetime(df_coment["FECHA_REVISION"])

    # Aplica filtro solo si está activo
             if st.session_state["filtrar_comentarios"]:
               hoy = pd.Timestamp.now().normalize()
               df_filtrado = df_coment[df_coment["FECHA_REVISION"] >= hoy]
               df_filtrado = df_filtrado.sort_values("FECHA_REVISION").head(20)
             else:
               df_filtrado = df_coment

    # Formatear fechas para mostrar bonito
               df_filtrado_display = df_filtrado.copy()
               df_filtrado_display["FECHA"] = df_filtrado_display["FECHA"].dt.strftime("%Y-%m-%d %H:%M")
               df_filtrado_display["FECHA_REVISION"] = df_filtrado_display["FECHA_REVISION"].dt.strftime("%Y-%m-%d")

               st.dataframe(df_filtrado_display[["PROCESO", "COMENTARIO", "USUARIO", "FECHA", "FECHA_REVISION"]])

def pagina_analisis():
    st.write("# 📊 Análisis de Calidad y Gestión Documental")

    try:
        df = cargar_excel()
        df_coment = cargar_comentarios()
    except FileNotFoundError:
        st.error("No se encontraron los archivos de datos (Bitacora1.xlsx o comentarios.xlsx).")
        return

    # Asegurarse de que las columnas de fecha son datetime para el análisis
    df["VIGENCIA"] = pd.to_datetime(df["VIGENCIA"], errors='coerce')
    df_coment["FECHA_REVISION"] = pd.to_datetime(df_coment["FECHA_REVISION"], errors='coerce')
    
    # -----------------------------------------------
    st.header("1. Estabilidad Documental (Distribución de Versiones)")
    # -----------------------------------------------
    
    # Limpieza básica de versiones (opcional: podrías normalizar más)
    df_versiones = df["VERSIÓN"].astype(str).str.upper().str.strip()
    
    conteo_versiones = df_versiones.value_counts().reset_index()
    conteo_versiones.columns = ['VERSIÓN', 'Cantidad']
    
    fig1 = px.bar(
        conteo_versiones.sort_values(by="Cantidad", ascending=False),
        x='VERSIÓN',
        y='Cantidad',
        title='Documentos por Versión',
        color='VERSIÓN',
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    
    fig1.update_layout(template="plotly_dark", showlegend=False)
    st.plotly_chart(fig1, use_container_width=True)

    st.markdown("---")

    # -----------------------------------------------
    st.header("2. Carga de Trabajo por Responsable")
    # -----------------------------------------------
    
    # Mapa de Calor/Gráfico de Barras Horizontal
    conteo_responsables = df["RESPONSABLE"].astype(str).value_counts().reset_index().head(10) # Top 10
    conteo_responsables.columns = ['Responsable', 'Carga']
    
    fig2 = px.bar(
        conteo_responsables.sort_values(by="Carga", ascending=True),
        y='Responsable',
        x='Carga',
        orientation='h',
        title='Top 10 Responsables con Mayor Carga Documental',
        color='Responsable',
        color_discrete_sequence=px.colors.sequential.Teal
    )
    
    fig2.update_layout(template="plotly_dark", showlegend=False, yaxis={'categoryorder':'total ascending'})
    st.plotly_chart(fig2, use_container_width=True)

    st.markdown("---")

    # -----------------------------------------------
    st.header("3. Planificación de Revisiones (Vigencias)")
    # -----------------------------------------------

    # Filtrar documentos con fecha de vigencia válida y no vencidos
    df_vigentes = df[df["VIGENCIA"].dt.date >= pd.Timestamp.now().normalize().date()].copy()
    df_vigentes["Mes de Vigencia"] = df_vigentes["VIGENCIA"].dt.strftime("%Y-%m")
    
    conteo_vigencia = df_vigentes["Mes de Vigencia"].value_counts().sort_index().reset_index()
    conteo_vigencia.columns = ['Mes de Vigencia', 'Documentos a Vencer']
    
    fig3 = px.line(
        conteo_vigencia,
        x='Mes de Vigencia',
        y='Documentos a Vencer',
        title='Documentos cuya Vigencia Expira por Mes',
        markers=True
    )
    
    fig3.update_layout(
        template="plotly_dark",
        xaxis_title="Mes de Vigencia (Próximos Vencimientos)",
        yaxis_title="Cantidad de Documentos",
        hovermode="x unified"
    )
    st.plotly_chart(fig3, use_container_width=True)

    st.markdown("---")

    # -----------------------------------------------
    st.header("4. Seguimiento de Comentarios y Tareas de Revisión")
    # -----------------------------------------------

    # Crear una columna de "Estado de Tarea"
    # Para simplificar, asumiremos que un comentario es "ABIERTO" si FECHA_REVISION es futuro/hoy.
    # En un sistema real, necesitarías una columna "CERRADO"
    
    df_coment = df_coment.dropna(subset=["FECHA_REVISION"]) # Solo si tienen fecha de agenda
    
    # Calcular el estado (si la fecha de revisión está en el futuro, es una tarea a hacer)
    hoy = pd.Timestamp.now().normalize()
    df_coment['ESTADO'] = df_coment['FECHA_REVISION'].apply(
        lambda x: "PENDIENTE" if x >= hoy else "ATRASADO"
    )
    
    # Mostrar KPI
    abiertos = df_coment[df_coment["ESTADO"].isin(["PENDIENTE", "ATRASADO"])].shape[0]
    st.metric(label="Total de Revisiones Agendadas Pendientes/Atrasadas", value=abiertos)
    
    # Gráfico de barras apiladas por proceso y estado
    conteo_estado = df_coment.groupby(["PROCESO", "ESTADO"]).size().reset_index(name='Cantidad')
    
    fig4 = px.bar(
        conteo_estado,
        y='PROCESO',
        x='Cantidad',
        color='ESTADO',
        orientation='h',
        title='Distribución de Tareas de Revisión por Proceso y Estado',
        color_discrete_map={
            'PENDIENTE': 'yellowgreen', 
            'ATRASADO': 'darkred'
        }
    )
    
    fig4.update_layout(template="plotly_dark", barmode='stack', yaxis={'categoryorder':'total ascending'})
    st.plotly_chart(fig4, use_container_width=True)
   
    # Después de crear fig1
    aplicar_formato_figura(fig1, color_sequence=px.colors.qualitative.Pastel, horizontal=False)
    st.plotly_chart(fig1, use_container_width=True)

# Después de crear fig2
    aplicar_formato_figura(fig2, color_sequence=px.colors.sequential.Teal, horizontal=True)
    st.plotly_chart(fig2, use_container_width=True)

# === CONFIGURACIÓN PROFESIONAL PARA FIG3 (GRÁFICO DE LÍNEAS) ===
    fig3.update_layout(
      template="plotly_dark",
      plot_bgcolor="rgba(44,62,80,1)",
      paper_bgcolor="rgba(44,62,80,1)",
      font_color="white",
      xaxis_title="Mes de Vigencia (Próximos Vencimientos)",
      yaxis_title="Cantidad de Documentos",
      hovermode="x unified",
      title=dict(
        text="Próximos Vencimientos por Mes",
        font=dict(size=22, family="Arial Black")
    ),
      xaxis=dict(
        showgrid=True,
        gridcolor="rgba(255,255,255,0.15)",
        linecolor="rgba(255,255,255,0.3)"
    ),
      yaxis=dict(
        showgrid=True,
        gridcolor="rgba(255,255,255,0.15)",
        linecolor="rgba(255,255,255,0.3)"
    ),
      legend=dict(
        bgcolor="rgba(0,0,0,0)",
        bordercolor="rgba(255,255,255,0.2)"
    )
)

# Mostrar gráfico
    st.plotly_chart(fig3, use_container_width=True)


# Después de crear fig4
    aplicar_formato_figura(fig4, horizontal=True)
    st.plotly_chart(fig4, use_container_width=True)

# ==========================================
# FUNCIÓN PARA CARGAR LA HOJA ESPECÍFICA
# ==========================================
def cargar_mapeo_procesos():
    archivo = "procesos/Tipo de Procesos por Responsable.xlsx"
    try:
        if not os.path.exists(archivo):
            st.error(f"⚠️ No se encuentra el archivo en la ruta: {archivo}")
            return None
        df = pd.read_excel(archivo, sheet_name="TipoProceso", skiprows=5)
         #2. Eliminamos columnas que Excel a veces carga vacías a la izquierda
         #Nos quedamos solo con las columnas que tienen datos
        df = df.dropna(how='all', axis=1)
        
        #Renombramos según el orden de tus datos: AREA, RESPONSABLE, TIPO
        df.columns = ["AREA", "RESPONSABLE", "TIPO_PROCESO"] + list(df.columns[3:])
        
        # Quitamos filas vacías y la fila de TOTAL
        df = df.dropna(subset=["AREA"])
        df = df[df["AREA"].astype(str).str.upper() != "TOTAL"]
        
        return df
    except Exception as e:
        st.error(f"❌ Error al leer la hoja 'TipoProceso': {e}")
        return None
# ==========================================
# VISTA DE LA PÁGINA MAPA ESTRATÉGICO
# ==========================================
#def pagina_mapa_estrategico():
  #  st.markdown("<h1 style='color: #002b5c;'>📍 Mapa Estratégico de Procesos</h1>", unsafe_allow_html=True)
    
    # Aquí es donde llamamos a la función de arriba
   # df_mapa = cargar_mapeo_procesos()
    
    #if df_mapa is not None:
        # --- TARJETAS KPI (Usando tu estilo kpi-card) ---
     #   total_areas = len(df_mapa)
      #  c1, c2, c3 = st.columns(3)
        
       # with c1:
        #    st.markdown(f'<div class="kpi-card"><h3>Total Áreas</h3><p>{total_areas}</p></div>', unsafe_allow_html=True)
        #with c2:
         #   est = len(df_mapa[df_mapa["TIPO_PROCESO"].str.contains("Estrategico", na=False, case=False)])
          #  st.markdown(f'<div class="kpi-card"><h3>Estratégicos</h3><p>{est}</p></div>', unsafe_allow_html=True)
        #with c3:
         #   mis = len(df_mapa[df_mapa["TIPO_PROCESO"].str.contains("Misionales", na=False, case=False)])
          #  st.markdown(f'<div class="kpi-card"><h3>Misionales</h3><p>{mis}</p></div>', unsafe_allow_html=True)

        #st.markdown("---")

        # --- SECCIONES POR TIPO ---
        #col1, col2, col3 = st.columns(3)
        
        #with col1:
         #   st.markdown("<h3 style='color: #002b5c;'>🚀 Estratégicos</h3>", unsafe_allow_html=True)
          #  df_est = df_mapa[df_mapa["TIPO_PROCESO"].str.contains("Estrategico", na=False, case=False)]
           # for _, r in df_est.iterrows():
            #    st.markdown(f"""
             #       <div style="border-left: 5px solid #002b5c; background: #f8f9fa; padding: 10px; margin-bottom: 5px; border-radius: 5px;">
              #          <b>{r['AREA']}</b><br><small>👤 {r['RESPONSABLE']}</small>
               #     </div>
                #""", unsafe_allow_html=True)

        #with col2:
         #   st.markdown("<h3 style='color: #e31e24;'>🏥 Misionales</h3>", unsafe_allow_html=True)
          #  df_mis = df_mapa[df_mapa["TIPO_PROCESO"].str.contains("Misionales", na=False, case=False)]
           # for _, r in df_mis.iterrows():
            #    st.markdown(f"""
             #       <div style="border-left: 5px solid #e31e24; background: #fff5f5; padding: 10px; margin-bottom: 5px; border-radius: 5px;">
              #          <b>{r['AREA']}</b><br><small>👤 {r['RESPONSABLE']}</small>
               #     </div>
                #""", unsafe_allow_html=True)

      #  with col3:
       #     st.markdown("<h3 style='color: #7b7b7b;'>⚙️ Apoyo</h3>", unsafe_allow_html=True)
        #    df_apo = df_mapa[df_mapa["TIPO_PROCESO"].str.contains("Apoyo", na=False, case=False)]
         #   for _, r in df_apo.iterrows():
          #      st.markdown(f"""
           #         <div style="border-left: 5px solid #7b7b7b; background: #f1f1f1; padding: 10px; margin-bottom: 5px; border-radius: 5px;">
            #            <b>{r['AREA']}</b><br><small>👤 {r['RESPONSABLE']}</small>
             #       </div>
              #  """, unsafe_allow_html=True)
# ============================
# MOSTRAR PÁGINA SEGÚN SELECCIÓN
# ============================

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