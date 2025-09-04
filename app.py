import streamlit as st
import pandas as pd
import os
import base64

st.set_page_config(page_title="Chá de Casa Nova 🎁", layout="wide")

ARQUIVO = "presentes.xlsx"

# =======================
# Funções auxiliares
# =======================
def salvar_dados(df):
    df.to_excel(ARQUIVO, index=False)

def carregar_dados():
    if os.path.exists(ARQUIVO):
        return pd.read_excel(ARQUIVO)
    else:
        df = pd.DataFrame([
            {"Item": "Conjunto de pratos", "Categoria": "Cozinha", "Quantidade": 1, "Status": "Disponível", "Nome da Pessoa": "", "Cor Preferida": "Branco", "Link de Referência": "https://www.lojaexemplo.com/pratos", "Observações": "Porcelana"},
            {"Item": "Jogo de toalhas", "Categoria": "Banho", "Quantidade": 2, "Status": "Disponível", "Nome da Pessoa": "", "Cor Preferida": "Azul", "Link de Referência": "https://www.lojaexemplo.com/toalhas", "Observações": "100% algodão"},
            {"Item": "Liquidificador", "Categoria": "Cozinha", "Quantidade": 1, "Status": "Disponível", "Nome da Pessoa": "", "Cor Preferida": "Vermelho", "Link de Referência": "https://www.lojaexemplo.com/liquidificador", "Observações": "1000W potência"},
            {"Item": "Tapete de sala", "Categoria": "Decoração", "Quantidade": 1, "Status": "Disponível", "Nome da Pessoa": "", "Cor Preferida": "Bege", "Link de Referência": "https://www.lojaexemplo.com/tapete", "Observações": "2x1,5m"}
        ])
        salvar_dados(df)
        return df

# =======================
# Função para adicionar imagem lateral como ornamento
# =======================
def add_side_ornament(image_file):
    with open(image_file, "rb") as f:
        encoded = base64.b64encode(f.read()).decode()
    st.markdown(
        f"""
        <style>
        body {{
            background-image: url("data:image/png;base64,{encoded}");
            background-repeat: no-repeat;
            background-position: right top;
            background-size: 500px;
        }}
        .cabecalho {{
            font-family: Arial, sans-serif;
            text-align: center;
            background-color: rgba(255, 255, 255, 0.8);
            border-radius: 15px;
            padding: 20px;
            margin-bottom: 30px;
        }}
        .cabecalho h1 {{
            font-size: 38px;
            color: #2C3E50;
        }}
        .cabecalho h2 {{
            font-size: 26px;
            color: #34495E;
            margin-top: -10px;
        }}
        .cabecalho h3 {{
            font-size: 24px;
            color: #2980B9;
            margin: 15px 0;
        }}
        .pix {{
            font-size: 18px;
            margin-top: 20px;
            color: #2C3E50;
        }}
        .pix strong {{
            color: #C0392B;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# Adiciona ornamento
add_side_ornament("flores.png")

# =======================
# Cabeçalho Único
# =======================
st.markdown(
    """
    <div class="cabecalho">
        <h1>🎉 Chá de Casa Nova 🎉</h1>
        <h2>Dani & Micael</h2>
        <h3>📅 Domingo, 14 de Setembro - 13h</h3>
        <div class="pix">
            <p>💝 Apoie com uma doação via PIX</p>
            <p>Se preferir, você também pode contribuir com um valor em dinheiro.</p>
            <p><strong>Chave PIX:</strong> email@exemplo.com</p>
            <p><em>Mensagem: Com carinho para o Chá de Casa Nova!</em></p>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# =======================
# Conteúdo principal
# =======================
df = carregar_dados()
st.markdown("### 🔎 Escolha uma categoria")
df["Categoria"] = df["Categoria"].fillna("Outros").astype(str)

categorias = ["Todas"] + sorted(df["Categoria"].unique().tolist())
categoria_sel = st.selectbox("", categorias)

if categoria_sel != "Todas":
    df_filtrado = df[df["Categoria"] == categoria_sel]
else:
    df_filtrado = df

st.markdown("### 🎁 Presentes disponíveis")
st.dataframe(df_filtrado, use_container_width=True, height=300)

st.markdown("### ✍️ Reservar um presente")
opcoes = df[df["Status"] == "Disponível"]["Item"].tolist()

if opcoes:
    with st.form("reserva_form"):
        item_escolhido = st.selectbox("Selecione o presente:", opcoes)
        nome = st.text_input("Seu nome:")
        reservar = st.form_submit_button("Reservar")

        if reservar:
            if nome.strip() == "":
                st.warning("Digite seu nome antes de reservar.")
            else:
                idx = df[df["Item"] == item_escolhido].index[0]
                df.at[idx, "Status"] = "Reservado"
                df.at[idx, "Nome da Pessoa"] = nome
                salvar_dados(df)
                st.success(f"🎉 {item_escolhido} reservado por {nome}!")
else:
    st.info("Todos os presentes já foram reservados.")

st.markdown("### 📋 Situação atualizada da lista")
st.dataframe(df, use_container_width=True, height=300)

# Rodapé
st.markdown("---")
st.markdown("📍 **Endereço:** Rua Ângelo Dalanegra, 201 - Jardim São Luiz - Valinhos/SP")  
st.markdown("🔥 **Sugestão:** Kit Churras 🍖")
