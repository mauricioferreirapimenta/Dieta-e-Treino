
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
    dados = {aba: pd.read_excel(xls, sheet_name=aba, dtype=str).fillna("") for aba in abas}
    return abas, projetos, dados

# Sessão local (para atualizar sem recarregar cache)
if "dados_memoria" not in st.session_state:
    abas, projetos, dados_planilha = carregar_planilha(file_path)
    st.session_state.dados_memoria = dados_planilha
    st.session_state.abas = abas
    st.session_state.projetos = projetos

dados_planilha = st.session_state.dados_memoria
abas = st.session_state.abas
projetos = st.session_state.projetos

projeto = st.sidebar.selectbox("Selecione o Projeto", projetos)
aba = st.sidebar.radio("Ver:", ["Info", "Treinos", "Dieta"])
aba_nome = f"{projeto}_{aba}"

df = dados_planilha.get(aba_nome, pd.DataFrame())

# Limpar hora das datas
if "Data" in df.columns:
    try:
        df["Data"] = pd.to_datetime(df["Data"], errors='coerce').dt.date
    except Exception:
        pass

st.subheader(f"📄 {aba_nome}")
st.dataframe(df, use_container_width=True)

# ----------- Edição direta ------------

if aba == "Treinos":
    st.markdown("### ✏️ Editar ou adicionar treino")
    with st.form("form_editar_treino"):
        data_treino = st.date_input("Data")
        treino_desc = st.text_input("Descrição do treino")
        editar = st.checkbox("Atualizar treino existente se já houver")
        submitted = st.form_submit_button("Salvar treino")

        if submitted:
            nova_linha = {
                "Data": data_treino,
                "Dia da Semana": data_treino.strftime("%A"),
                "Treino": treino_desc
            }

            df["Data"] = pd.to_datetime(df["Data"], errors="coerce").dt.date
            if editar and data_treino in df["Data"].values:
                df.loc[df["Data"] == data_treino, "Treino"] = treino_desc
                st.success("Treino atualizado.")
            else:
                df = pd.concat([df, pd.DataFrame([nova_linha])], ignore_index=True)
                st.success("Novo treino adicionado.")
            df.sort_values("Data", inplace=True)
            dados_planilha[aba_nome] = df
            st.experimental_rerun()

if aba == "Dieta":
    st.markdown("### ✏️ Editar ou adicionar alimento")
    with st.form("form_editar_dieta"):
        data_refeicao = st.date_input("Data da refeição")
        refeicao = st.text_input("Refeição", value="Refeição 1 - Pequeno Almoço")
        alimento = st.text_input("Alimento")
        unidade = st.text_input("Unidade", value="g")
        qtd = st.number_input("Quantidade", min_value=0.0)
        carb = st.number_input("Carboidrato (g)", min_value=0.0)
        prot = st.number_input("Proteína (g)", min_value=0.0)
        gord = st.number_input("Gordura (g)", min_value=0.0)
        kcal = st.number_input("Kcal", min_value=0.0)
        salvar_alimento = st.form_submit_button("Salvar alimento")

        if salvar_alimento:
            nova_linha = {
                "Data": data_refeicao,
                "Refeição": refeicao,
                "Alimentos": alimento,
                "Unidade": unidade,
                "Quantidade": qtd,
                "Carboidrato (g)": carb,
                "Proteína (g)": prot,
                "Gordura (g)": gord,
                "Kcal": kcal
            }
            df = pd.concat([df, pd.DataFrame([nova_linha])], ignore_index=True)
            df.sort_values("Data", inplace=True)
            dados_planilha[aba_nome] = df
            st.success("Alimento adicionado à dieta.")
            st.experimental_rerun()

# ----------- Exportar alterações ----------
if st.sidebar.button("💾 Exportar Planilha Atualizada"):
    with pd.ExcelWriter(file_path, engine="openpyxl", mode="w") as writer:
        for aba_salvar, df_salvar in dados_planilha.items():
            df_salvar.to_excel(writer, sheet_name=aba_salvar, index=False)
    st.success("Planilha salva com sucesso.")
