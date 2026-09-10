import streamlit as st
import urllib.parse

# Configuración de la página
st.set_page_config(
    page_title="Pizzería Don Pepe",
    page_icon="🍕",
    layout="wide"
)

# Estilos visuales
st.markdown("""
    <style>
    div.stButton > button:first-child {
        background-color: #25D366 !important;
        color: white !important;
        font-weight: bold !important;
        border-radius: 8px !important;
        border: none !important;
        padding: 0.8rem 1.5rem !important;
        font-size: 18px !important;
        width: 100%;
    }
    div.stButton > button:first-child:hover {
        background-color: #128C7E !important;
    }
    h1, h2, h3 {
        color: #D32F2F;
    }
    </style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# DATOS DEL RESTAURANTE
# ---------------------------------------------------------
NOMBRE_LOCAL = "Pizzería Don Pepe"
TELEFONO_WHATSAPP = "595975410239"

# Menú por categorías
MENU = {
    "🍕 Pizzas": [
        {
            "nombre": "Pizza Muzzarella",
            "precio": 35000,
            "desc": "Salsa de tomate casera, abundante muzzarella y orégano",
            "img": "https://images.unsplash.com/photo-1513104890138-7c749659a591?w=400"
        },
        {
            "nombre": "Pizza Pepperoni",
            "precio": 45000,
            "desc": "Queso muzzarella y rodajas crocantes de pepperoni",
            "img": "https://images.unsplash.com/photo-1628840042765-356cda07504e?w=400"
        }
    ],
    "🍔 Hamburguesas": [
        {
            "nombre": "Hamburguesa Clásica",
            "precio": 25000,
            "desc": "Carne 150g, queso cheddar, lechuga y tomate",
            "img": "https://images.unsplash.com/photo-1568901346375-23c9450c58cd?w=400"
        }
    ],
    "🍟 Acompañamientos": [
        {
            "nombre": "Papas Tradicionales",
            "precio": 15000,
            "desc": "Porción de papas fritas bastón crocantes",
            "img": "https://images.unsplash.com/photo-1573080496219-bb080dd4f877?w=400"
        }
    ],
    "🥤 Bebidas": [
        {
            "nombre": "Gaseosa 500ml",
            "precio": 8000,
            "desc": "Coca-Cola / Fanta / Sprite",
            "img": "https://images.unsplash.com/photo-1622483767028-3f66f32aef97?w=400"
        }
    ]
}

# ---------------------------------------------------------
# INTERFAZ PRINCIPAL
# ---------------------------------------------------------
st.title(f"🍕 {NOMBRE_LOCAL}")
st.write("Haz tu pedido seleccionando tus productos preferidos:")

pedido = {}

# Recorrer categorías
for categoria, productos in MENU.items():
    st.header(categoria)
    cols = st.columns(len(productos))
    
    for idx, prod in enumerate(productos):
        with cols[idx]:
            st.image(prod["img"], use_container_width=True)
            st.subheader(prod["nombre"])
            st.caption(prod["desc"])
            st.write(f"**Precio:** Gs. {prod['precio']:,}")
            
            cantidad = st.number_input(
                "Cantidad",
                min_value=0,
                max_value=10,
                value=0,
                key=f"{categoria}_{idx}"
            )
            
            if cantidad > 0:
                pedido[prod["nombre"]] = {
                    "cantidad": cantidad,
                    "precio": prod["precio"],
                    "subtotal": cantidad * prod["precio"]
                }
    st.markdown("---")

# ---------------------------------------------------------
# DATOS DE ENTREGA Y RESUMEN
# ---------------------------------------------------------
if pedido:
    st.header("📋 Datos de Entrega")
    
    col_envio, col_notas = st.columns(2)
    with col_envio:
        tipo_entrega = st.radio("Modalidad de entrega:", ["Delivery 🛵", "Retiro del Local 🏃‍♂️", "Mesa 🍽️"])
        direccion = st.text_input("Dirección de envío / N° de Mesa:", value="")
    
    with col_notas:
        notas = st.text_input("Aclaraciones (Ej: Sin cebolla, Salsa aparte):", value="")

    st.markdown("---")
    st.header("🛒 Resumen del Pedido")
    
    total = 0
    mensaje = f"🍕 *NUEVO PEDIDO - {NOMBRE_LOCAL}*\n\n"
    mensaje += f"*Modalidad:* {tipo_entrega}\n"
    if direccion:
        mensaje += f"*Ubicación/Mesa:* {direccion}\n"
    if notas:
        mensaje += f"*Notas:* {notas}\n"
    
    mensaje += "\n*Detalle del pedido:*\n"
    
    for item, datos in pedido.items():
        st.write(f"• **{item}** x{datos['cantidad']} = Gs. {datos['subtotal']:,}")
        mensaje += f"• {datos['cantidad']}x {item} = Gs. {datos['subtotal']:,}\n"
        total += datos["subtotal"]
        
    st.markdown(f"### **Total a Pagar:** Gs. {total:,}")
    mensaje += f"\n*TOTAL:* Gs. {total:,}\n\n¡Quedo a la espera de la confirmación!"

    # Botón directo a WhatsApp
    mensaje_encoded = urllib.parse.quote(mensaje)
    link_wa = f"https://wa.me/{TELEFONO_WHATSAPP}?text={mensaje_encoded}"
    
    st.markdown(f'<a href="{link_wa}" target="_blank"><button>📲 Enviar Pedido por WhatsApp</button></a>', unsafe_allow_html=True)
else:
    st.info("Selecciona al menos 1 producto del menú para armar tu pedido.")
