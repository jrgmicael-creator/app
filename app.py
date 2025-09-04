import streamlit as st
import pandas as pd

# =======================
# Simulação da "planilha"
# =======================
if "presentes" not in st.session_state:
    st.session_state.presentes = pd.DataFrame([
        {"Item": "Conjunto de pratos", "Categoria": "Cozinha", "Quantidade": 1, "Status": "Disponível", "Nome da Pessoa": "", "Cor Preferida": "Branco", "Link de Referência": "https://www.lojaexemplo.com/pratos", "Observações": "Porcelana"},
        {"Item": "Jogo de toalhas", "Categoria": "Banho", "Quantidade": 2, "Status": "Disponível", "Nome da Pessoa": "", "Cor Preferida": "Azul", "Link de Referência": "https://www.lojaexemplo.com/toalhas", "Observações": "100% algodão"},
        {"Item": "Liquidificador", "Categoria": "Cozinha", "Quantidade": 1, "Status": "Disponível", "Nome da Pessoa": "", "Cor Preferida": "Vermelho", "Link de Referência": "https://www.lojaexemplo.com/liquidificador", "Observações": "1000W potência"},
        {"Item": "Tapete de sala", "Categoria": "Decoração", "Quantidade": 1, "Status": "Disponível", "Nome da Pessoa": "", "Cor Preferida": "Bege", "Link de Referência": "https://www.lojaexemplo.com/tapete", "Observações": "2x1,5m"}
    ])

df = st.session_state.presentes

# =======================
# Interface
# =======================
st.title("🎁 Lista de Presentes - Chá de Casa Nova")

# Filtro por categoria
categorias = ["Todas"] + sorted(df["Categoria"].unique().tolist())
categoria_sel = st.selectbox("Filtrar por categoria:", categorias)

if categoria_sel != "Todas":
    df_filtrado = df[df["Categoria"] == categoria_sel]
else:
    df_filtrado = df

# Mostrar tabela
st.subheader("Presentes disponíveis")
st.dataframe(df_filtrado, use_container_width=True)

# Escolher item para reservar
st.subheader("Reservar um presente")
opcoes = df[df["Status"] == "Disponível"]["Item"].tolist()
if opcoes:
    item_escolhido = st.selectbox("Selecione o presente:", opcoes)
    nome = st.text_input("Seu nome:")

    if st.button("Reservar"):
        if nome.strip() == "":
            st.warning("Digite seu nome antes de reservar.")
        else:
            idx = df[df["Item"] == item_escolhido].index[0]
            df.at[idx, "Status"] = "Reservado"
            df.at[idx, "Nome da Pessoa"] = nome
            st.success(f"🎉 {item_escolhido} reservado por {nome}!")
else:
    st.info("Todos os presentes já foram reservados.")

# Mostrar tabela atualizada
st.subheader("📋 Situação atualizada da lista")
st.dataframe(df, use_container_width=True)
