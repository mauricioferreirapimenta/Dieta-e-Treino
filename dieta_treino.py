
import streamlit as st
import pandas as pd
from openpyxl import load_workbook
from datetime import datetime, date

st.set_page_config(page_title="Gerenciador de Dieta e Treino", layout="wide")
st.title("📘 Gerenciador de Projetos: Dieta e Treino")

file_path = "Dieta_Treino.xlsx"

@st.cache_data
def carregar_planilha(caminho):
    xls = pd.ExcelFile(caminho)
    abas = xls.sheet_names
    projetos = sorted(set(a.split("_")[0] for a in abas if "Projeto" in a))
    dados = {aba: pd.read_excel(xls, sheet_name=aba, dtype=str).fillna("") for aba in abas}
    return abas, projetos, dados

if "dados_memoria" not in st.session_state:
    abas, projetos, dados_planilha = carregar_planilha(file_path)
    st.session_state.dados_memoria = dados_planilha
    st.session_state.abas = abas
    st.session_state.projetos = projetos
else:
    dados_planilha = st.session_state.dados_memoria
    abas = st.session_state.abas
    projetos = st.session_state.projetos

st.sidebar.markdown("### Projeto")
projeto = st.sidebar.selectbox("Selecione o Projeto", [""] + projetos)

# Novo Projeto
st.sidebar.markdown("---")
st.sidebar.markdown("### Criar Novo Projeto")
with st.sidebar.form("novo_projeto_form"):
    novo_nome = st.text_input("Nome do novo projeto")
    criar = st.form_submit_button("Criar Projeto")
    if criar and novo_nome:
        for aba_nova in ["Treinos", "Dieta", "Info"]:
            nome_aba = f"{novo_nome}_{aba_nova}"
            dados_planilha[nome_aba] = pd.DataFrame()
            abas.append(nome_aba)
        projetos.append(novo_nome)
        projetos = sorted(list(set(projetos)))
        st.session_state.projetos = projetos
        st.session_state.dados_memoria = dados_planilha
        st.success(f"Projeto '{novo_nome}' criado com sucesso. Selecione na lista.")
        st.rerun()

# Excluir projeto
if projeto:
    if st.sidebar.button("🗑️ Excluir Projeto Selecionado"):
        for tipo in ["Treinos", "Dieta", "Info"]:
            aba_a_remover = f"{projeto}_{tipo}"
            dados_planilha.pop(aba_a_remover, None)
        projetos.remove(projeto)
        st.session_state.projetos = projetos
        st.success(f"Projeto '{projeto}' excluído.")
        st.rerun()

if projeto:
    aba = st.sidebar.radio("Ver:", ["Info", "Treinos", "Dieta"])
    aba_nome = f"{projeto}_{aba}"
    df = dados_planilha.get(aba_nome, pd.DataFrame())

    if "Data" in df.columns:
        df["Data"] = pd.to_datetime(df["Data"], errors='coerce').dt.date
        df["Data_str"] = df["Data"].apply(lambda x: x.strftime("%d/%m/%Y") if not pd.isnull(x) else "")

    if aba == "Treinos" and not df.empty and "Data" in df.columns:
        df["Mês"] = df["Data"].dt.strftime("%B/%Y")
        meses = sorted(df["Mês"].dropna().unique())
        mes_selecionado = st.selectbox("Filtrar por mês", ["Todos"] + list(meses))
        if mes_selecionado != "Todos":
            df = df[df["Mês"] == mes_selecionado]

    if aba == "Dieta" and not df.empty:
        colunas_numericas = ["Quantidade", "Carboidrato (g)", "Proteína (g)", "Gordura (g)", "Kcal"]
        for col in colunas_numericas:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce').round(1)

    st.subheader(f"📄 {aba_nome}")
    st.dataframe(df.drop(columns=['Mês'], errors='ignore'), use_container_width=True)

    # Excluir linha
    if not df.empty:
        st.markdown("### ❌ Excluir entrada")
        idxs = df.index.tolist()
        idx = st.selectbox("Selecione o índice para excluir", idxs)
        if st.button("Excluir linha"):
            df.drop(index=idx, inplace=True)
            dados_planilha[aba_nome] = df
            st.success("Linha excluída com sucesso.")
            st.rerun()

    if aba == "Treinos":
        st.markdown("### ✏️ Editar ou adicionar treino")
        with st.form("form_editar_treino"):
            data_treino = st.date_input("Data", value=None)
            treino_desc = st.text_input("Descrição do treino")
            editar = st.checkbox("Atualizar treino existente se já houver")
            submitted = st.form_submit_button("Salvar treino")

            if submitted and data_treino:
                nova_linha = {
                    "Data": data_treino,
                    "Dia da Semana": data_treino.strftime("%A"),
                    "Treino": treino_desc
                }
                df["Data"] = pd.to_datetime(df["Data"], errors="coerce").dt.date.dt.date
                if editar and data_treino in df["Data"].values:
                    df.loc[df["Data"] == data_treino, "Treino"] = treino_desc
                    st.success("Treino atualizado.")
                else:
                    df = pd.concat([df, pd.DataFrame([nova_linha])], ignore_index=True)
                    st.success("Novo treino adicionado.")
                df.sort_values("Data", inplace=True)
                dados_planilha[aba_nome] = df
                st.rerun()

    if aba == "Dieta":
        st.markdown("### ✏️ Editar ou adicionar alimento")
        refeicoes_padrao = [
            "Pequeno Almoço",
            "Lanche da Manhã",
            "Almoço",
            "Lanche da Tarde",
            "Jantar",
            "Ceia"
        ]
        with st.form("form_editar_dieta"):
            data_refeicao = st.date_input("Data da refeição", value=None)
            refeicao = st.selectbox("Refeição", ["" ] + refeicoes_padrao)
            alimento = st.text_input("Alimento")
            unidade = st.text_input("Unidade", value="g")
            qtd = st.number_input("Quantidade", min_value=0.0)
            carb = st.number_input("Carboidrato (g)", min_value=0.0)
            prot = st.number_input("Proteína (g)", min_value=0.0)
            gord = st.number_input("Gordura (g)", min_value=0.0)
            kcal = st.number_input("Kcal", min_value=0.0)
            salvar_alimento = st.form_submit_button("Salvar alimento")

            if salvar_alimento and data_refeicao and refeicao:
                nova_linha = {
                    "Data": data_refeicao,
                    "Refeição": refeicao,
                    "Alimentos": alimento,
                    "Unidade": unidade,
                    "Quantidade": round(qtd, 1),
                    "Carboidrato (g)": round(carb, 1),
                    "Proteína (g)": round(prot, 1),
                    "Gordura (g)": round(gord, 1),
                    "Kcal": round(kcal, 1)
                }
                df = pd.concat([df, pd.DataFrame([nova_linha])], ignore_index=True)
                df.sort_values("Data", inplace=True)
                dados_planilha[aba_nome] = df
                st.success("Alimento adicionado à dieta.")
                st.rerun()

# ----------- Exportar alterações ----------
if st.sidebar.button("💾 Exportar Planilha Atualizada"):
    with pd.ExcelWriter(file_path, engine="openpyxl", mode="w") as writer:
        for aba_salvar, df_salvar in dados_planilha.items():
            df_salvar.to_excel(writer, sheet_name=aba_salvar, index=False)
    st.success("Planilha salva com sucesso.")
