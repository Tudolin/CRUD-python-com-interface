import sqlite3
import PySimpleGUI as sg

conn = sqlite3.connect('exemplo.db')

conn.execute('''CREATE TABLE IF NOT EXISTS exemplo (
                    id INTEGER PRIMARY KEY,
                    nome TEXT NOT NULL,
                    idade INTEGER NOT NULL)''')

layout = [
    [sg.Text('Nome:'), sg.InputText(key='nome')],
    [sg.Text('Idade:'), sg.InputText(key='idade')],
    [sg.Button('Criar'), sg.Button('Ler'), sg.Button('Atualizar'), sg.Button('Deletar')],
    [sg.Text('Resultado:'), sg.Text(key='resultado')],
    [sg.Button('Fechar')]
]

janela = sg.Window('CRUD com PySimpleGUI', layout)

while True:
    evento, valores = janela.read()
    
    if evento == sg.WIN_CLOSED or evento == 'Fechar':
        break
    
    if evento == 'Criar':
        # Cria um registro na tabela
        nome = valores['nome']
        idade = valores['idade']
        conn.execute("INSERT INTO exemplo (nome, idade) VALUES (?, ?)", (nome, idade))
        conn.commit()
        janela['resultado'].update(f'Registro criado: {nome}, {idade}')
    
    elif evento == 'Ler':
        # Lê um registro da tabela
        id = sg.popup_get_text('Digite o ID do registro a ser lido:')
        cursor = conn.execute("SELECT id, nome, idade FROM exemplo WHERE id = ?", (id,))
        registro = cursor.fetchone()
        if registro:
            janela['resultado'].update(f'Registro lido: {registro[0]}, {registro[1]}, {registro[2]}')
        else:
            janela['resultado'].update(f'Registro não encontrado para o ID {id}')
    
    elif evento == 'Atualizar':
        # Atualiza um registro na tabela
        id = sg.popup_get_text('Digite o ID do registro a ser atualizado:')
        nome = valores['nome']
        idade = valores['idade']
        conn.execute("UPDATE exemplo SET nome = ?, idade = ? WHERE id = ?", (nome, idade, id))
        conn.commit()
        janela['resultado'].update(f'Registro atualizado: {id}, {nome}, {idade}')
    
    elif evento == 'Deletar':
        # Deleta um registro da tabela
        id = sg.popup_get_text('Digite o ID do registro a ser deletado:')
        conn.execute("DELETE FROM exemplo WHERE id = ?", (id,))
        conn.commit()
        janela['resultado'].update(f'Registro deletado para o ID {id}')
        
janela.close()
conn.close()
