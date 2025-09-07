import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials

# =======================
# Configuração Google Sheets
# =======================
scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]

# Cria credenciais a partir do secrets
creds = Credentials.from_service_account_info(
    st.secrets["gcp_service_account"], scopes=scope
)
client = gspread.authorize(creds)

# ID da planilha (fixo conforme solicitado)
SHEET_ID = "1UoP4mQHMpBk6XuyQnP4S062qOoq0YJuwIjxnLF-czdU"
sheet = client.open_by_key(SHEET_ID).sheet1

# =======================
# Funções auxiliares
# =======================
def carregar_dados():
    data = sheet.get_all_records()
    return pd.DataFrame(data)

def salvar_dados(df: pd.DataFrame):
    sheet.clear()
    sheet.update([df.columns.values.tolist()] + df.values.tolist())

# =======================
# Interface do app
# =======================
st.set_page_config(page_title="🎉 Chá de Casa Nova", layout="wide")

st.title("🎉 Chá de Casa Nova 🎉")
st.subheader("Dani & Micael")
st.write("📅 Domingo, 14 de Setembro - 13h")

st.info("💝 Apoie com uma doação via PIX — Chave: **email@exemplo.com**")

# Carrega os dados
df = carregar_dados()

# Lista de colunas que queremos exibir
colunas_exibidas = ["Item", "Categoria", "Quantidade","Status", "Cor Preferida","Observações"]

# Garantir que só usamos colunas existentes no DataFrame
colunas_existentes = [c for c in colunas_exibidas if c in df.columns]

# Filtro por categoria
st.markdown("### 🔎 Escolha uma categoria")
categorias = ["Todas"] + sorted(df["Categoria"].unique().tolist())
categoria_sel = st.selectbox("", categorias)

if categoria_sel != "Todas":
    df_filtrado = df[df["Categoria"] == categoria_sel]
else:
    df_filtrado = df

# Mostra tabela
st.markdown("### 🎁 Presentes disponíveis")
st.dataframe(df_filtrado[colunas_existentes], use_container_width=True, height=300)

# Formulário para reserva
st.markdown("### ✍️ Reservar um presente")
# Agora só exibe itens realmente disponíveis
if "Status" in df.columns:
    opcoes = df[df["Status"] == "Disponível"]["Item"].tolist()
else:
    opcoes = df["Item"].tolist()  # fallback se não existir Status

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
                if "Status" in df.columns:
                    df.at[idx, "Status"] = "Reservado"
                df.at[idx, "Nome da Pessoa"] = nome
                salvar_dados(df)
                st.success(f"🎉 {item_escolhido} reservado por {nome}!")
                st.experimental_rerun()  # força atualização imediata
else:
    st.info("Todos os presentes já foram reservados.")

# # Situação final
# st.markdown("### 📋 Situação atualizada da lista")
# st.dataframe(df[colunas_existentes], use_container_width=True, height=300)

# Rodapé
st.markdown("---")
st.markdown("📍 **Endereço:** Rua Ângelo Dalanegra, 201 - Jardim São Luiz - Valinhos/SP")  
st.markdown("🔥 **Sugestão:** Kit Churras 🍖")
