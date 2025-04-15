
import streamlit as st
import pandas as pd
from openpyxl import load_workbook

st.set_page_config(page_title="Dieta e Treino", layout="wide")

st.title("📋 Gerenciador de Dieta e Treino")
st.markdown("Este app permite visualizar suas **refeições e treinos** diretamente do Excel.")

# Caminho do arquivo
file_path = "Dieta_e_Treino.xlsx"

# Tenta carregar a planilha
try:
    xls = pd.ExcelFile(file_path)
    abas = xls.sheet_names
    aba_escolhida = st.sidebar.selectbox("Escolha a aba:", abas)

    df = pd.read_excel(xls, sheet_name=aba_escolhida)
    st.subheader(f"Aba: {aba_escolhida}")
    st.dataframe(df)

except FileNotFoundError:
    st.error(f"Arquivo {file_path} não encontrado. Verifique o nome e localização.")
except Exception as e:
    st.error(f"Ocorreu um erro ao carregar a planilha: {e}")
