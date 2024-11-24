#%%writefile erp_streamlit.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
from fpdf import FPDF

logo_path = "data:image/png;base64,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"
# Configuración inicial
st.set_page_config(page_title="Módulos del ERP", layout="wide",page_icon=logo_path)
# Ruta del archivo de imagen (logo)

# Mostrar el logo en la parte superior de la aplicación
st.image(logo_path, width=200)  # Puedes ajustar el tamaño cambiando el valor de 'width'

# Agregar un título o contenido a la aplicación
st.title("Sistema ERP")
st.write("Bienvenido al sistema ERP para la gestión de clientes, inventarios, facturación, reportes y análisis de ventas.")

st.sidebar.title("ERP_ITM")

# Variables de autenticación
USER = "Carlos090"
PASSWORD = "Correa098*"

# Inicialización de variables globales
if "auth" not in st.session_state:
    st.session_state["auth"] = False

if "modulo_seleccionado" not in st.session_state:
    st.session_state["modulo_seleccionado"] = None

# Parámetros de ID
if "id_cliente" not in st.session_state:
    st.session_state["id_cliente"] = 1  # El primer ID de cliente

if "id_producto" not in st.session_state:
    st.session_state["id_producto"] = 1  # El primer ID de producto

if "id_factura" not in st.session_state:
    st.session_state["id_factura"] = 1  # El primer ID de factura

# Inicialización de DataFrames
if "clientes" not in st.session_state:
    st.session_state["clientes"] = pd.DataFrame(columns=["ID", "Nombre", "Correo", "Teléfono"])

if "productos" not in st.session_state:
    st.session_state["productos"] = pd.DataFrame(columns=["ID", "Producto", "Cantidad", "Precio Unitario"])

if "facturas" not in st.session_state:
    st.session_state["facturas"] = pd.DataFrame(columns=["Factura ID", "Cliente ID", "Cliente Nombre", "Productos", "Total", "IVA", "Fecha"])
    
# Función de autenticación
with st.sidebar:
    st.title("Módulos ERP")
if not st.session_state["auth"]:
    st.sidebar.subheader("Iniciar Sesión")
    usuario = st.sidebar.text_input("Usuario")
    contraseña = st.sidebar.text_input("Contraseña", type="password")
    if st.sidebar.button("Ingresar"):
        if usuario == USER and contraseña == PASSWORD:
            st.session_state["auth"] = True
            st.sidebar.success("Inicio de sesión exitoso.")
        else:
            st.sidebar.error("Usuario o contraseña incorrectos.")
else:
    st.sidebar.subheader(f"Bienvenido, {USER}")
    st.session_state["modulo_seleccionado"] = st.sidebar.radio(
        "Selecciona un módulo:",
        ["Gestión de Clientes", "Gestión de Inventario", "Generar Factura", "Generar Reportes", "Análisis de Ventas"],
    )
    if st.sidebar.button("Cerrar Sesión"):
        st.session_state["auth"] = False
        st.session_state["modulo_seleccionado"] = None
        st.sidebar.success("Sesión cerrada correctamente.")


# Funciones auxiliares
def exportar_csv(df, nombre_archivo):
    """Permite exportar un DataFrame como archivo CSV."""
    st.download_button(
        label="Exportar Datos",
        data=df.to_csv(index=False).encode("utf-8"),
        file_name=nombre_archivo,
        mime="text/csv",
    )

# Funciones de los módulos
def gestion_clientes():
    st.header("Gestión de Clientes")
    
    # Registro de nuevo cliente
    with st.form("Registro de Cliente"):
        nombre = st.text_input("Nombre")
        correo = st.text_input("Correo Electrónico")
        telefono = st.text_input("Teléfono")
        submitted = st.form_submit_button("Registrar Cliente")
        
        if submitted:
            # Generación de ID para el nuevo cliente
            cliente_id = st.session_state["id_cliente"]
            nuevo_cliente = pd.DataFrame([{
                "ID": cliente_id, "Nombre": nombre, "Correo": correo, "Teléfono": telefono
            }])
            st.session_state["clientes"] = pd.concat([st.session_state["clientes"], nuevo_cliente], ignore_index=True)
            st.session_state["id_cliente"] += 1  # Incrementar el ID para el siguiente cliente
            st.success(f"Cliente {nombre} registrado correctamente con ID: {cliente_id}.")
    
    # Búsqueda de clientes
    st.subheader("Buscar Cliente")
    search_term = st.text_input("Buscar por nombre o ID")
    if search_term:
        clientes_filtrados = st.session_state["clientes"][st.session_state["clientes"]["Nombre"].str.contains(search_term, case=False)]
        st.dataframe(clientes_filtrados)
    else:
        st.dataframe(st.session_state["clientes"])

    # Edición de cliente
    cliente_a_editar = st.selectbox("Seleccionar cliente para editar", st.session_state["clientes"]["ID"])
    cliente_data = st.session_state["clientes"][st.session_state["clientes"]["ID"] == cliente_a_editar]
    if cliente_data.empty:
        st.warning("Cliente no encontrado.")
    else:
        with st.form("Editar Cliente"):
            nombre_edit = st.text_input("Nuevo Nombre", cliente_data["Nombre"].values[0])
            correo_edit = st.text_input("Nuevo Correo", cliente_data["Correo"].values[0])
            telefono_edit = st.text_input("Nuevo Teléfono", cliente_data["Teléfono"].values[0])
            submitted_edit = st.form_submit_button("Actualizar Cliente")
            
            if submitted_edit:
                st.session_state["clientes"].loc[st.session_state["clientes"]["ID"] == cliente_a_editar, "Nombre"] = nombre_edit
                st.session_state["clientes"].loc[st.session_state["clientes"]["ID"] == cliente_a_editar, "Correo"] = correo_edit
                st.session_state["clientes"].loc[st.session_state["clientes"]["ID"] == cliente_a_editar, "Teléfono"] = telefono_edit
                st.success(f"Cliente con ID {cliente_a_editar} actualizado.")

    # Eliminación de cliente
    cliente_a_eliminar = st.selectbox("Seleccionar cliente para eliminar", st.session_state["clientes"]["ID"])
    if st.button("Eliminar Cliente"):
        st.session_state["clientes"] = st.session_state["clientes"][st.session_state["clientes"]["ID"] != cliente_a_eliminar]
        st.success("Cliente eliminado correctamente.")

def gestion_inventario():

    st.header("Gestión de Inventario")
    
    # Registro de producto
    with st.form("Registro de Producto"):
        producto = st.text_input("Producto")
        cantidad = st.number_input("Cantidad", min_value=1, step=1)
        precio_unitario = st.number_input("Precio Unitario", min_value=0.0, step=0.1)
        submitted = st.form_submit_button("Registrar Producto")
        
        if submitted:
            # Generación de ID para el nuevo producto
            producto_id = st.session_state["id_producto"]
            nuevo_producto = pd.DataFrame([{
                "ID": producto_id, "Producto": producto, "Cantidad": cantidad, "Precio Unitario": precio_unitario
            }])
            st.session_state["productos"] = pd.concat([st.session_state["productos"], nuevo_producto], ignore_index=True)
            st.session_state["id_producto"] += 1  # Incrementar el ID para el siguiente producto
            st.success(f"Producto {producto} registrado correctamente con ID: {producto_id}.")
    
    # Búsqueda de productos
    st.subheader("Buscar Producto")
    search_term = st.text_input("Buscar producto por nombre")
    if search_term:
        inventario_filtrado = st.session_state["productos"][st.session_state["productos"]["Producto"].str.contains(search_term, case=False)]
        st.dataframe(inventario_filtrado)
    else:
        st.dataframe(st.session_state["productos"])

    # Eliminación de producto
    producto_a_eliminar = st.selectbox("Seleccionar producto para eliminar", st.session_state["productos"]["Producto"])
    if st.button("Eliminar Producto"):
        st.session_state["productos"] = st.session_state["productos"][st.session_state["productos"]["Producto"] != producto_a_eliminar]
        st.success("Producto eliminado correctamente.")

def gestion_facturas():
    st.header("Generar Factura")
    st.write("Selecciona un cliente y productos para crear una factura.")
    
    if st.session_state["clientes"].empty:
        st.warning("No hay clientes registrados. Por favor, registra clientes antes de crear una factura.")
        return
    
    if st.session_state["productos"].empty:
        st.warning("No hay productos en el inventario. Por favor, registra productos antes de crear una factura.")
        return
    
    cliente_id = st.selectbox("Seleccionar Cliente", st.session_state["clientes"]["ID"])
    cliente_nombre = st.session_state["clientes"].loc[
        st.session_state["clientes"]["ID"] == cliente_id, "Nombre"
    ].values[0]
    
    # Selección de productos
    productos_seleccionados = st.multiselect(
        "Selecciona productos", 
        st.session_state["productos"]["Producto"].values
    )
    
    if not productos_seleccionados:
        st.info("Selecciona al menos un producto para generar una factura.")
        return
    
    productos_detalle = []
    total = 0
    
    for producto in productos_seleccionados:
        producto_info = st.session_state["productos"].loc[
            st.session_state["productos"]["Producto"] == producto
        ]
        precio_unitario = producto_info["Precio Unitario"].values[0]
        stock_disponible = producto_info["Cantidad"].values[0]
        
        # Selección de cantidad
        cantidad = st.number_input(
            f"Cantidad de {producto} (Disponible: {stock_disponible})", 
            min_value=1, 
            max_value=stock_disponible, 
            step=1
        )
        
        subtotal = precio_unitario * cantidad
        total += subtotal
        productos_detalle.append({
            "Producto": producto,
            "Cantidad": cantidad,
            "Precio Unitario": precio_unitario,
            "Subtotal": subtotal
        })
    
    # Calcular IVA y total final
    iva = total * 0.16
    total_con_iva = total + iva
    
    # Mostrar resumen
    st.subheader("Resumen de Factura")
    st.table(pd.DataFrame(productos_detalle))
    st.write(f"Subtotal: ${total:,.2f}")
    st.write(f"IVA (16%): ${iva:,.2f}")
    st.write(f"Total: ${total_con_iva:,.2f}")
    
    # Confirmación y registro de factura
    if st.button("Confirmar y Generar Factura"):
        factura_id = st.session_state["id_factura"]
        fecha = pd.to_datetime("today").strftime("%Y-%m-%d")
        
        # Registrar factura
        factura = pd.DataFrame([{
            "Factura ID": factura_id, 
            "Cliente ID": cliente_id, 
            "Cliente Nombre": cliente_nombre,
            "Productos": productos_detalle, 
            "Total": total, 
            "IVA": iva, 
            "Fecha": fecha
        }])
        st.session_state["facturas"] = pd.concat([st.session_state["facturas"], factura], ignore_index=True)
        st.session_state["id_factura"] += 1  # Incrementar el ID para la siguiente factura
        
        # Reducir inventario
        for detalle in productos_detalle:
            producto = detalle["Producto"]
            cantidad = detalle["Cantidad"]
            st.session_state["productos"].loc[
                st.session_state["productos"]["Producto"] == producto, "Cantidad"
            ] -= cantidad
        
        st.success(f"Factura {factura_id} generada correctamente.")
        st.write(f"Total con IVA: ${total_con_iva:,.2f}")
        
        # Exportar factura
        exportar_csv(st.session_state["facturas"], f"factura_{factura_id}.csv")

def gestion_reportes():
 

    st.header("Generar Reportes")

    # Generación de reportes contables
    st.write("Aquí pueden ir los reportes contables.")
    st.write("Funciones específicas para reportes como ingresos, gastos y balances se agregarán aquí.")
    
    # Simulando el reporte básico
    st.text_area("Resumen", "Reporte generado: ingresos, gastos, balance general, etc.")
    
    # Exportar el reporte a CSV
    exportar_csv(st.session_state["facturas"], "reportes_contables.csv")

import plotly.express as px

def analisis_ventas():
    st.header("Análisis de Ventas")
    
    # Verificar si hay datos en las facturas
    if st.session_state["facturas"].empty:
        st.warning("No hay datos de facturas para analizar.")
        return

    # Crear una lista para desglosar productos en facturas
    productos_desglosados = []
    for _, fila in st.session_state["facturas"].iterrows():
        for producto in fila["Productos"]:
            productos_desglosados.append({
                "Producto": producto["Producto"],
                "Cantidad": producto["Cantidad"],
                "Subtotal": producto["Subtotal"],
                "Fecha": fila["Fecha"]
            })

    # Crear un DataFrame con los datos desglosados
    df_productos = pd.DataFrame(productos_desglosados)

    # Verificar si hay datos en el DataFrame desglosado
    if df_productos.empty:
        st.warning("No hay datos suficientes para generar análisis.")
        return

    # Análisis de ventas por producto
    st.subheader("Ventas por Producto")
    ventas_por_producto = df_productos.groupby("Producto").sum().reset_index()
    fig1 = px.bar(
        ventas_por_producto, 
        x="Producto", 
        y="Subtotal", 
        title="Ingresos por Producto", 
        labels={"Subtotal": "Ingresos ($)"},
        text="Subtotal"
    )
    st.plotly_chart(fig1, use_container_width=True)

    # Análisis de cantidades vendidas por producto
    st.subheader("Cantidad Vendida por Producto")
    fig2 = px.pie(
        ventas_por_producto, 
        names="Producto", 
        values="Cantidad", 
        title="Distribución de Cantidades Vendidas"
    )
    st.plotly_chart(fig2, use_container_width=True)

    # Análisis temporal de ventas
    st.subheader("Ingresos Totales por Fecha")
    df_productos["Fecha"] = pd.to_datetime(df_productos["Fecha"])
    ingresos_por_fecha = df_productos.groupby("Fecha").sum().reset_index()
    fig3 = px.line(
        ingresos_por_fecha, 
        x="Fecha", 
        y="Subtotal", 
        title="Evolución de Ingresos en el Tiempo",
        labels={"Subtotal": "Ingresos ($)", "Fecha": "Fecha"}
    )
    st.plotly_chart(fig3, use_container_width=True)

    st.success("Gráficos interactivos generados correctamente.")

# Navegación entre módulos
if st.session_state["auth"]:
    if st.session_state["modulo_seleccionado"] == "Gestión de Clientes":
        gestion_clientes()
    elif st.session_state["modulo_seleccionado"] == "Gestión de Inventario":
        gestion_inventario()
    elif st.session_state["modulo_seleccionado"] == "Generar Factura":
        gestion_facturas()
    elif st.session_state["modulo_seleccionado"] == "Generar Reportes":
        gestion_reportes()
    elif st.session_state["modulo_seleccionado"] == "Análisis de Ventas":
        analisis_ventas()
else:
    st.warning("Por favor, inicia sesión para continuar.")
