
import pandas as pd
from openpyxl import load_workbook

# Caminhos atualizados
input_path = './data/Dieta_e_Treino.xlsx'
output_path = './outputs/Dieta_e_Treino.xlsx'  # Mantendo o mesmo nome

# Carrega a planilha original
book = load_workbook(input_path)

# Acessa ou cria aba de dieta
if 'Dieta' in book.sheetnames:
    dieta_sheet = book['Dieta']
    print('Aba "Dieta" carregada com sucesso.')
else:
    dieta_sheet = book.create_sheet('Dieta')
    print('Aba "Dieta" criada.')

# Acessa ou cria aba de treino
if 'Treino' in book.sheetnames:
    treino_sheet = book['Treino']
    print('Aba "Treino" carregada com sucesso.')
else:
    treino_sheet = book.create_sheet('Treino')
    print('Aba "Treino" criada.')

# Exemplo de função para adicionar alimento a uma refeição
def adicionar_alimento(sheet, linha, dados):
    for i, valor in enumerate(dados):
        sheet.cell(row=linha, column=i+1, value=valor)
    print(f"Alimento adicionado na linha {linha}.")

# Exemplo de função para alterar um treino por data
def alterar_treino(sheet, data, novo_treino):
    for row in sheet.iter_rows(min_row=2):  # Ignorar cabeçalho
        if row[0].value == data:
            row[2].value = novo_treino
            print(f"Treino atualizado para {data}: {novo_treino}")
            break

# Salvar cópia atualizada com o mesmo nome
book.save(output_path)
print(f'Planilha salva como: {output_path}')
