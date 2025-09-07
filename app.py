import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
from io import BytesIO
import qrcode
import pixqrcode  # pip install pixqrcode

# =======================
# Configuração Google Sheets
# =======================
scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]

creds = Credentials.from_service_account_info(
    st.secrets["gcp_service_account"], scopes=scope
)
client = gspread.authorize(creds)

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
# Configuração Pix
# =======================
PIX_CHAVE = "19993733423"  # sua chave Pix (pode ser celular, e-mail, CPF ou aleatória)
PIX_NOME = "Dani & Micael"  # Nome do recebedor
PIX_CIDADE = "VALINHOS"     # Cidade obrigatória no padrão

# Gera payload Pix válido
payload = pixqrcode.Payload(
    pix_key=PIX_CHAVE,
    merchant_name=PIX_NOME,
    merchant_city=PIX_CIDADE,
    amount=0.0,  # valor opcional, 0.0 = aberto para qualquer valor
    description="Chá de Casa Nova"
).to_str()

# Cria QR Code do payload Pix
qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_H,
    box_size=8,
    border=2,
)
qr.add_data(payload)
qr.make(fit=True)

img = qr.make_image(fill_color="black", back_color="white")
buffer = BytesIO()
img.save(buffer, format="PNG")

# =======================
# Interface
# =======================
st.set_page_config(page_title="🎉 Chá de Casa Nova", layout="wide")
st.title("🎉 Chá de Casa Nova 🎉")
st.subheader("Dani & Micael")
st.write("📅 Domingo, 14 de Setembro - 13h")

st.markdown("## 📲 Dados para Pix")
st.write(f"**Chave Pix:** `{PIX_CHAVE}`")
st.image(buffer.getvalue(), caption="Escaneie o QR Code para pagar via Pix", width=220)
