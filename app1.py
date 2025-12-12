import os
import streamlit as st
import pandas as pd
import plotly.express as px
import datetime
import os
import streamlit as st
import pandas as pd
import plotly.express as pxstreamlit 
import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header

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
        plot_bgcolor='rgba(44, 62, 80, 1)',  # azul fondo
        paper_bgcolor='rgba(44, 62, 80, 1)',
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

custom_css = """
<style>
/* Fondo general app */
[data-testid="stAppViewContainer"], 
[data-testid="stAppViewContainer"] > div {
  background-color: #1e272e !important;  /* gris oscuro azulado */
  color: #e1e1e1 !important; /* texto gris claro */
}

/* Sidebar fondo igual al fondo principal */
section[data-testid="stSidebar"] {
  background-color: #1e272e !important;  /* mismo gris para sidebar */
  color: #e1e1e1 !important;
  border: 5px solid black;
}

/* Texto en sidebar */
section[data-testid="stSidebar"] * {
  color: #e1e1e1 !important;
}

/* Botones */
div.stButton > button {
  background-color: #34495e !important;  /* azul grisáceo oscuro */
  color: #ecf0f1 !important; /* texto blanco humo */
  border-radius: 6px;
  font-weight: 600;
  border: 1px solid #2c3e50;
  padding: 8px 20px;
  transition: background-color 0.3s ease, border-color 0.3s ease;
  box-shadow: 1px 1px 3px rgba(0,0,0,0.3);
  font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;
}

div.stButton > button:hover {
  background-color: #3d566e !important;  /* azul gris claro */
  border-color: #2980b9;
  color: #ffffff !important;
  cursor: pointer;
}

/* Inputs, textareas y selectboxes */
input, textarea, select {
  background-color: #2f3e4e !important;
  color: #f0f0f0 !important;
  border: 1.5px solid #506d84 !important;
  border-radius: 6px !important;
  padding: 6px 10px !important;
  font-size: 15px !important;
  font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;
  transition: border-color 0.3s ease;
}

input::placeholder, textarea::placeholder {
  color: #a0aebf !important;
}

input:focus, textarea:focus, select:focus {
  border-color: #7fb3d5 !important; /* azul claro al enfocar */
  outline: none !important;
  box-shadow: 0 0 8px #7fb3d5aa !important;
}

/* Ajuste para headers y textos que a veces no heredan color */
h1, h2, h3, h4, h5, h6, p, label, span, div {
  color: #e1e1e1 !important;
  font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;
}
</style>
"""



st.markdown(custom_css, unsafe_allow_html=True)


# ======== TÍTULO PRINCIPAL MEJORADO ========
st.markdown('<h1 class="main-title">🗂️ Procesos Clínica Viva 1A</h1>', unsafe_allow_html=True)

def rerun():
    st.session_state["dummy"] = not st.session_state["dummy"]

def logout():
    st.session_state["logged"] = False
    st.session_state["user"] = None
    st.session_state["role"] = None
    rerun()

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

st.set_page_config(page_title="Procesos", layout="wide")

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


st.subheader("Gestión de Procesos")

if st.session_state["role"] == "admin":
    st.button("Agregar / Editar Proceso")
else:
    st.info("Solo lectura — no tienes permisos de edición.")

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

    options = ["Inicio", "Procesos", "Documentos", "Análisis"]
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
            "Análisis": "📊 Análisis de Calidad",
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
    st.markdown("<h1 style='color: white;'>🏠 Inicio</h1>", unsafe_allow_html=True)
    st.write("Bienvenido al sistema de procesos de la Clínica Viva 1A.")
    st.write("Resumen de documentos por tipo:")

    try:
        df = cargar_excel()
    except FileNotFoundError:
        st.error("No se encontró el archivo Bitacora1.xlsx.")
        return

    tipos = [
        "PROCEDIMIENTO", "FORMATO", "MANUAL", "INSTRUCTIVO", "GUIA",
        "CERTIFICADO", "PLAN DE CALIDAD", "PROGRAMA",
        "PROTOCOLO", "REGLAMENTO"
    ]

    df["TIPO DE DOCUMENTO"] = df["TIPO DE DOCUMENTO"].astype(str).str.upper()
    conteo = df["TIPO DE DOCUMENTO"].value_counts().reindex(tipos, fill_value=0)

    df_tabla = pd.DataFrame({
        "Tipo de Documento": list(conteo.index),
        "Cantidad": list(conteo.values)
    })

    total_docs = conteo.values.sum()
    df_tabla = pd.concat([
        df_tabla,
        pd.DataFrame({"Tipo de Documento": ["TOTAL"], "Cantidad": [total_docs]})
    ], ignore_index=True)

    st.write("Cantidad de documentos por tipo (incluye TOTAL):")
    st.table(df_tabla)

    fig = px.bar(
       df_tabla[df_tabla["Tipo de Documento"] != "TOTAL"],
       y="Tipo de Documento",
       x="Cantidad",
       orientation='h',
       color="Tipo de Documento",
       color_discrete_sequence=px.colors.sequential.Teal,
       title="Documentos por Tipo",
       text="Cantidad"   # <-- Aquí agregamos para mostrar etiquetas
)
    fig.update_layout(
       template="plotly_dark",
       showlegend=False,
       plot_bgcolor='rgba(44, 62, 80, 1)',  # azul fondo
       paper_bgcolor='rgba(44, 62, 80, 1)',
       font_color='white',
       xaxis=dict(
         title_text="Cantidad",
         tickfont=dict(size=18)  # tamaño etiquetas eje X
    ),
       yaxis=dict(
         tickfont=dict(size=18)  # tamaño etiquetas eje Y
    ),
       title=dict(font=dict(size=24))  # tamaño título
)

    fig.update_traces(
       textposition="outside",
       cliponaxis=False,
       textfont_size=20  # tamaño etiquetas en barras (números)
)

    st.plotly_chart(fig, use_container_width=True)


    total_docs_real = df_tabla[df_tabla["Tipo de Documento"] != "TOTAL"]["Cantidad"].sum()
    st.markdown(f"**Total de documentos:** {total_docs_real}")

def pagina_procesos():
    st.header("📌 Procesos")

    # Cargar Excel
    df = cargar_excel()
    df_proced = df[df["TIPO DE DOCUMENTO"].str.upper() == "PROCEDIMIENTO"]

    # Crear filtro lateral para ÁREA / PROCESO
    with st.sidebar:
        st.subheader("Filtrar por Área / Proceso")
        areas = df_proced["PROCESO"].dropna().unique().tolist()
        areas.sort()
        areas = ["Todos"] + areas  # Añadimos opción para mostrar todos

        area_seleccionada = st.selectbox("Selecciona área:", areas, index=0, key="filtro_area_proceso")

    # Filtrar df_proced según área seleccionada
    if area_seleccionada != "Todos":
        df_filtrado = df_proced[df_proced["PROCESO"] == area_seleccionada]
    else:
        df_filtrado = df_proced

    # Lista de títulos filtrados
    nombres_procesos = df_filtrado["TITULO DE DOCUMENTO"].astype(str).tolist()

    if not nombres_procesos:
        st.info("No hay procesos disponibles para esta área.")
        return

    st.subheader("📋 Selecciona un proceso")
    seleccionado = st.selectbox("Procesos disponibles:", nombres_procesos, key="selector_procesos")

    st.markdown("---")

    # Fila del proceso escogido
    fila = df_filtrado[df_filtrado["TITULO DE DOCUMENTO"] == seleccionado].iloc[0]

    # ======================
    # MOSTRAR ENLACE
    # ======================
    st.subheader("📎 Archivo del Proceso")

    enlace = fila["ABRIR"]

    if enlace and str(enlace).strip() != "":
        st.markdown(f"🔗 **Abrir archivo:** [Clic aquí]({enlace})", unsafe_allow_html=True)
    else:
        st.info("Este proceso no tiene enlace registrado en el Excel.")

    st.markdown("---")

    # ======================
    # MOSTRAR DIAGRAMA
    # ======================
    st.subheader("📊 Diagrama del Proceso")

    # RUTA BASE DONDE GUARDAS IMÁGENES
    ruta_base = "/Users/jair/Desktop/apps procesos/DIAGRAMA"

    # Listar todos los archivos reales de esa carpeta
    try:
        archivos = os.listdir(ruta_base)
    except FileNotFoundError:
        st.error("❌ La carpeta 'apps procesos/DIAGRAMA' no existe o no es accesible.")
        return

    # NORMALIZAMOS EL TEXTO DEL PROCESO (sin tildes, minúsculas)
    def normalizar(texto):
        return (
            texto.lower()
            .replace("á", "a").replace("é", "e").replace("í", "i")
            .replace("ó", "o").replace("ú", "u")
            .replace("ñ", "n")
            .replace(" ", "")
        )

    nombre_normalizado = normalizar(seleccionado)

    # BUSCAR COINCIDENCIA ENTRE EL PROCESO Y LOS ARCHIVOS REALES
    archivo_encontrado = None
    for archivo in archivos:
        if normalizar(archivo.replace(".png", "")) in nombre_normalizado:
            archivo_encontrado = archivo
            break

    # Si no encontró exacto, intentar por palabra clave
    if not archivo_encontrado:
        if "fallec" in nombre_normalizado:
            archivo_encontrado = "procesodefallecimiento.png"

    # Mostrar imagen si hay
    if archivo_encontrado:
        ruta_final = os.path.join(ruta_base, archivo_encontrado)
        st.image(ruta_final, width=1000)
    else:
        # Si no hay diagrama, no mostrar nada o mostrar un mensaje opcional
        st.info("No hay diagrama disponible para este proceso.")

    # ... (resto de tu código para formulario y comentarios)


    



# Formulario para nuevo comentario + fecha revisión
    with st.form("form_nuevo_comentario"):
     nuevo_coment = st.text_area("Agregar nuevo comentario")
     fecha_revision = st.date_input(
        "Selecciona la fecha para revisar este proceso",
        min_value=datetime.date.today()
    )

     enviar_coment = st.form_submit_button("Enviar comentario")  # Esto debe estar dentro del `with st.form`

     if enviar_coment and nuevo_coment.strip() != "":
        # Aquí tu lógica para guardar el comentario y fecha
        ...

        try:
          df_coment = cargar_comentarios()
          if df_coment is None:
             df_coment = pd.DataFrame(columns=["PROCESO", "COMENTARIO", "USUARIO", "FECHA", "FECHA_REVISION"])
        except Exception as e:
          df_coment = pd.DataFrame(columns=["PROCESO", "COMENTARIO", "USUARIO", "FECHA", "FECHA_REVISION"])
          st.error(f"No se pudieron cargar los comentarios: {e}")

        if enviar_coment and nuevo_coment.strip() != "":
            fechas_ocupadas = df_coment[
                (df_coment["PROCESO"] == seleccionado) &
                (pd.to_datetime(df_coment["FECHA_REVISION"]).dt.date == fecha_revision)
            ]

        if not fechas_ocupadas.empty:
            st.warning("La fecha seleccionada ya está tomada para este proceso. Por favor, elige otra fecha.")
        else:
            nuevo_reg = {
                "PROCESO": seleccionado,
                "COMENTARIO": nuevo_coment.strip(),
                "USUARIO": st.session_state["user"],
                "FECHA": datetime.datetime.now(),
                "FECHA_REVISION": pd.Timestamp(fecha_revision)
            }

            df_coment = pd.concat([df_coment, pd.DataFrame([nuevo_reg])], ignore_index=True)
            guardar_comentarios(df_coment)
            
            correo_receptor = "jairft12@gmail.com"  # Tu correo donde quieres recibir la notificación

            asunto = f"Nuevo comentario en proceso: {seleccionado}"
            cuerpo = f"""
            Usuario: {st.session_state['user']}
            Proceso: {seleccionado}
            Comentario: {nuevo_coment.strip()} 
            Fecha para revisión: {fecha_revision}
            """

            enviado = False
            try:
              enviado = enviar_correo_gmail(correo_receptor, asunto, cuerpo)
              if enviado:
                 st.success("Comentario guardado y correo enviado.")
              else:
                 st.error("Comentario guardado pero fallo el envío del correo.")
            except Exception as e:
                 st.error(f"Comentario guardado pero fallo el envío del correo. Error: {e}")

            st.success("Comentario y fecha de revisión guardados.")
            rerun()


   
  
def pagina_documentos():
    st.title("📄 Documentos")

    try:
        df = cargar_excel()
    except FileNotFoundError:
        st.error("No se encontró el archivo.")
        return

    # Excluir procedimientos
    df = df[df["TIPO DE DOCUMENTO"].str.upper() != "PROCEDIMIENTO"]

    # Lista de procesos/áreas para filtro
    procesos = sorted(df["PROCESO"].dropna().unique())
    opciones_proceso = ["Todos"] + procesos

    # Selector en sidebar
    proceso_seleccionado = st.sidebar.selectbox("Filtrar por proceso / área", opciones_proceso)

    # Filtro por proceso
    if proceso_seleccionado != "Todos":
        df = df[df["PROCESO"] == proceso_seleccionado]

    # Buscador en sidebar también (opcional)
    busqueda = st.sidebar.text_input("🔍 Buscar documento por palabra")

    if busqueda:
        filtro = df.apply(lambda row: row.astype(str).str.contains(busqueda, case=False).any(), axis=1)
        df_filtrado = df[filtro]
    else:
        df_filtrado = df

    # Formatear columna ABRIR con links
    df_filtrado["ABRIR"] = df_filtrado["ABRIR"].apply(
        lambda x: f'<a href="{x}" target="_blank">Abrir</a>' if pd.notna(x) and x != "" else ""
    )

    columnas_mostrar = [
        "CODIGO", "TIPO DE DOCUMENTO", "VERSIÓN", "EMISION", "VIGENCIA",
        "TITULO DE DOCUMENTO", "PROCESO", "SUBPROCESO", "RESPONSABLE",
        "ABRIR"
    ]

    st.write(df_filtrado[columnas_mostrar].to_html(escape=False, index=False), unsafe_allow_html=True)


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
elif pagina_activa == "Análisis":
    pagina_analisis()
