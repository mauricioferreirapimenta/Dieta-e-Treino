
import streamlit as st
import pandas as pd
from openpyxl import load_workbook

st.set_page_config(page_title="Gerenciador de Dieta e Treino", layout="wide")
st.title("📘 Gerenciador de Projetos: Dieta e Treino")

# Caminho do arquivo
file_path = "Dieta_Treino.xlsx"

@st.cache_data
def carregar_planilha(caminho):
    xls = pd.ExcelFile(caminho)
    abas = xls.sheet_names
    projetos = sorted(set(a.split("_")[0] for a in abas if "Projeto" in a))
    dados = {aba: pd.read_excel(xls, sheet_name=aba) for aba in abas}
    return abas, projetos, dados

abas, projetos, dados_planilha = carregar_planilha(file_path)

projeto = st.sidebar.selectbox("Selecione o Projeto", projetos)
aba = st.sidebar.radio("Ver:", ["Info", "Treinos", "Dieta"])
aba_nome = f"{projeto}_{aba}"

if aba_nome in dados_planilha:
    df = dados_planilha[aba_nome]
    st.subheader(f"📄 {aba_nome}")
    st.dataframe(df, use_container_width=True)
else:
    st.warning(f"Aba '{aba_nome}' não encontrada.")

# Edição de Treino
if aba == "Treinos":
    with st.expander("➕ Adicionar novo treino"):
        nova_data = st.date_input("Data do treino")
        novo_dia = nova_data.strftime("%A")
        novo_treino = st.text_input("Descrição do treino")
        if st.button("Adicionar treino"):
            nova_linha = pd.DataFrame([[nova_data, novo_dia, novo_treino]],
                                      columns=["Data", "Dia da Semana", "Treino"])
            dados_planilha[aba_nome] = pd.concat([df, nova_linha], ignore_index=True)
            dados_planilha[aba_nome].sort_values("Data", inplace=True)
            st.success("Treino adicionado! Salve a planilha manualmente.")

# Edição de Refeição
if aba == "Dieta":
    with st.expander("➕ Adicionar nova refeição"):
        data_refeicao = st.date_input("Data da refeição")
        tipo_refeicao = st.selectbox("Tipo", ["Pequeno Almoço", "Almoço", "Lanche", "Jantar", "Ceia"])
        alimento = st.text_input("Alimento")
        kcal = st.number_input("Kcal", 0)
        prot = st.number_input("Proteína (g)", 0.0)
        carb = st.number_input("Carboidrato (g)", 0.0)
        gord = st.number_input("Gordura (g)", 0.0)
        if st.button("Adicionar alimento"):
            nova_linha = pd.DataFrame([[data_refeicao, tipo_refeicao, alimento, kcal, prot, carb, gord]],
                                      columns=["Data", "Refeição", "Alimentos", "Kcal", "Proteína (g)", "Carboidrato (g)", "Gordura (g)"])
            dados_planilha[aba_nome] = pd.concat([df, nova_linha], ignore_index=True)
            dados_planilha[aba_nome].sort_values("Data", inplace=True)
            st.success("Refeição adicionada! Salve a planilha manualmente.")

# Exportar planilha com dados atualizados
if st.sidebar.button("💾 Exportar Planilha Atualizada"):
    with pd.ExcelWriter(file_path, engine="openpyxl", mode="w") as writer:
        for aba_nome, df in dados_planilha.items():
            df.to_excel(writer, sheet_name=aba_nome, index=False)
    st.success("Planilha salva com sucesso!")
