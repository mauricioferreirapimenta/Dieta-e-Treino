
import pandas as pd
from openpyxl import load_workbook

# Caminhos
input_path = '../data/Dieta_e_Treino.xlsx'
output_path = '../outputs/Dieta_e_Treino_Atualizado.xlsx'

# Carrega a planilha original
book = load_workbook(input_path)

# Exemplo: acessar aba de dieta
if 'Dieta' in book.sheetnames:
    dieta_sheet = book['Dieta']
    print('Aba "Dieta" carregada com sucesso.')
else:
    print('Aba "Dieta" não encontrada. Você pode criá-la.')

# Exemplo: acessar aba de treino
if 'Treino' in book.sheetnames:
    treino_sheet = book['Treino']
    print('Aba "Treino" carregada com sucesso.')
else:
    print('Aba "Treino" não encontrada. Você pode criá-la.')

# TODO:
# - Editar alimentos, adicionar linhas
# - Substituir treinos em datas específicas
# - Gerar versão com atualizações
# - Exportar para PDF futuramente

# Salvar cópia no diretório de saída
book.save(output_path)
print(f'Planilha salva em: {output_path}')
