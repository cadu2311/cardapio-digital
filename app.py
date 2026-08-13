import streamlit as st

st.set_page_config(page_title="Aviso", page_icon="⚠️")

st.error("⚠️ Sistema Temporariamente Indisponível")
st.write(
    "Este cardápio encontra-se suspenso. Entre em contato com o administrador para regularizar o acesso."
)
import urllib.parse
import streamlit as st

st.set_page_config(page_title="Cardápio Digital", page_icon="🍔", layout="centered")

NOME_RESTAURANTE = "Burger & Cia"
TELEFONE_WHATSAPP = "5544999999999"

MENU = [
    {"id": 1, "nome": "X-Burger", "desc": "Pao e hamburguer 180g", "preco": 25.0},
    {"id": 2, "nome": "X-Salada", "desc": "Pao, burguer e salada", "preco": 22.0},
    {"id": 3, "nome": "Batata Frita", "desc": "Porcao de 200g", "preco": 12.0},
    {"id": 4, "nome": "Refrigerante", "desc": "350ml gelado", "preco": 3.0}
]

if 'carrinho' not in st.session_state:
    st.session_state.carrinho = []

st.title(f"🍔 {NOME_RESTAURANTE}")
st.subheader("Faça seu pedido pelo WhatsApp")
st.divider()

st.header("Cardápio")

for item in MENU:
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown(f"**{item['nome']}** — R$ {item['preco']:.2f}")
        st.caption(item['desc'])
    with col2:
        if st.button("➕ Add", key=f"btn_{item['id']}"):
            st.session_state.carrinho.append(item)
            st.toast(f"{item['nome']} adicionado!")

st.divider()
st.header("🛒 Seu Pedido")

if not st.session_state.carrinho:
    st.info("Seu carrinho está vazio.")
else:
    total = 0
    for idx, item in enumerate(st.session_state.carrinho):
        col_item, col_del = st.columns([4, 1])
        col_item.write(f"• **{item['nome']}** - R$ {item['preco']:.2f}")
        total += item['preco']
        if col_del.button("❌", key=f"del_{idx}"):
            st.session_state.carrinho.pop(idx)
            st.rerun()
            
    st.subheader(f"Total: R$ {total:.2f}")
    st.write("---")
    
    nome = st.text_input("Seu Nome:")
    endereco = st.text_input("Endereço Completo:")
    pagamento = st.selectbox("Forma de Pagamento:", ["PIX", "Cartão", "Dinheiro"])
    
    if st.button("🚀 Enviar Pedido no WhatsApp", type="primary"):
        if not nome or not endereco:
            st.error("Preencha nome e endereço!")
        else:
            itens_texto = "\n".join([f"- {i['nome']} (R$ {i['preco']:.2f})" for i in st.session_state.carrinho])
            msg = f"*NOVO PEDIDO*\n\n*Cliente:* {nome}\n*Endereço:* {endereco}\n*Pagamento:* {pagamento}\n\n*Itens:*\n{itens_texto}\n\n*Total:* R$ {total:.2f}"
            
            encoded = urllib.parse.quote(msg)
            url = f"https://wa.me/{TELEFONE_WHATSAPP}?text={encoded}"
            st.markdown(f"[👉 **Clique para Enviar**]({url})")
