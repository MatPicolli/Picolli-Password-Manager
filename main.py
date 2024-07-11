import os
import csv
import json
import FreeSimpleGUI as sg
from datetime import datetime

# Constants
VERSAO_APP = '2.5'
GITHUB_USER = 'MatPicolli'
FILES_DIR = 'files'
CONFIG_FILE = os.path.join(FILES_DIR, 'config.json')
PASSWORD_FILE = os.path.join(FILES_DIR, 'senhas.csv')
MASTER_PASSWORD_FILE = os.path.join(FILES_DIR, 'senha_mestre.key')

# Global variables
tema_geral = 'Reddit'
lista = []
lista_busca = []
lista_para_mostrar = []
lista_para_buscar = []

def ensure_files_dir_exists():
    if not os.path.exists(FILES_DIR):
        os.makedirs(FILES_DIR)

def load_config():
    ensure_files_dir_exists()
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    return {"tema": "Reddit"}

def update_password_file():
    global lista
    with open(PASSWORD_FILE, 'w', newline='') as f:
        csv.writer(f).writerows(lista)

def save_config(config):
    ensure_files_dir_exists()
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f)

def change_theme(new_theme):
    global tema_geral
    tema_geral = new_theme
    sg.theme(tema_geral)
    config = load_config()
    config['tema'] = tema_geral
    save_config(config)

def verify_master_password(password):
    ensure_files_dir_exists()
    with open(MASTER_PASSWORD_FILE, 'r', encoding='utf-8') as f:
        stored_password = ''.join([chr(ord(c) // 3) for c in f.read()])
        return password == stored_password

def verify_index(index):
    ensure_files_dir_exists()
    with open(PASSWORD_FILE, 'r') as f:
        return any(index in row for row in csv.reader(f))

def update_search_list():
    global lista_busca, lista_para_buscar
    lista_para_buscar = [f"  {item[0]}" for item in lista_busca]

def update_list():
    global lista, lista_para_mostrar
    ensure_files_dir_exists()
    with open(PASSWORD_FILE, 'r') as f:
        lista = list(csv.reader(f))
        lista_para_mostrar = [f"  {item[0]}" for item in lista]

def delete_password(index):
    global lista
    lista = [item for i, item in enumerate(lista) if i != index]
    with open(PASSWORD_FILE, 'w', newline='') as f:
        csv.writer(f).writerows(lista)

def update_password_file():
    global lista
    ensure_files_dir_exists()
    with open(PASSWORD_FILE, 'w', newline='') as f:
        csv.writer(f).writerows(lista)

def save_password(data):
    ensure_files_dir_exists()
    with open(PASSWORD_FILE, 'a', newline='') as f:
        csv.writer(f).writerow(data)

def confirm_action():
    layout = [
        [sg.Text('Confirmar?')],
        [sg.Button('Sim', button_color=('white', 'green'), key='-SIM-'),
         sg.Button('Não', button_color=('white', 'red'), key='-NAO-')]
    ]
    window = sg.Window('Confirmação', layout, keep_on_top=True)
    event, _ = window.read()
    window.close()
    return event == '-SIM-'

def view_password(index, searching=False):
    global lista
    index = next((i for i, item in enumerate(lista) if item[0] == index.strip()), None)
    if index is None:
        sg.popup_error("Senha não encontrada!")
        return

    layout = [
        [sg.Text(f'{field}:', size=(8, 1)), sg.InputText(lista[index][i], disabled=True, size=(25, 1), key=f'-{field.upper()}-')]
        for i, field in enumerate(['Index', 'Usuário', 'Senha', 'E-mail'])
    ] + [
        [sg.Text('Adicional', size=(8, 1)), sg.Multiline(lista[index][4], disabled=True, size=(25, 8), key='-ADD-')],
    ]

    window = sg.Window('Visualização', layout, keep_on_top=True)
    window.read()
    window.close()

def modify_password(index, searching=False):
    global lista
    index = next((i for i, item in enumerate(lista) if item[0] == index.strip()), None)
    if index is None:
        sg.popup_error("Senha não encontrada!")
        return

    layout = [
        [sg.Text(f'{field}:', size=(8, 1)), sg.InputText(lista[index][i], size=(25, 1), key=f'-{field.upper()}-', disabled=(field == 'Index'))]
        for i, field in enumerate(['Index', 'Usuário', 'Senha', 'E-mail'])
    ] + [
        [sg.Text('Adicional', size=(8, 1)), sg.Multiline(lista[index][4], size=(25, 8), key='-ADD-')],
        [sg.Button('Salvar', button_color=('white', 'green'), size=(13, 1), key='-SALVAR-'), 
         sg.Push(), 
         sg.Button('Deletar', button_color=('white', 'red'), size=(12, 1), key='-DELETAR-')]
    ]

    window = sg.Window('Modificar Senha', layout, keep_on_top=True)

    while True:
        event, values = window.read()
        if event in (sg.WINDOW_CLOSED, '-SALVAR-'):
            if event == '-SALVAR-':
                # Update the password in place
                lista[index] = [values['-INDEX-'], values['-USUÁRIO-'], values['-SENHA-'], values['-E-MAIL-'], values['-ADD-']]
                update_password_file()
            break
        elif event == '-DELETAR-':
            if confirm_action():
                del lista[index]
                update_password_file()
                break

    window.close()

def add_password():
    layout = [
        [sg.Text(f'{field} {"*" if field == "Index" else ""}', size=(8, 1)), sg.InputText(size=(25, 1), key=f'-{field.upper()}-')]
        for field in ['Index', 'Usuário', 'Senha', 'E-mail']
    ] + [
        [sg.Text('Adicional', size=(8, 1)), sg.Multiline(size=(25, 8), key='-ADD-')],
        [sg.Button('Criar Senha', size=(19, 1)),
         sg.Push(),
         sg.Button('❌', size=(6, 1), button_color=('red', sg.theme_button_color()[1]))]
    ]

    window = sg.Window('Adicionar Senha', layout)

    while True:
        event, values = window.read()
        if event in (sg.WINDOW_CLOSED, '❌'):
            break
        if event == 'Criar Senha':
            if not values['-INDEX-']:
                sg.Popup('Index deve ser preenchido!')
                continue
            if verify_index(values['-INDEX-']):
                sg.Popup('Index existente!')
            else:
                # Corrected line
                data = [values['-INDEX-'], values['-USUÁRIO-'], values['-SENHA-'], values['-E-MAIL-'], values['-ADD-']]
                save_password(data)
                break

    window.close()

def main_window():
    global lista, lista_busca, lista_para_mostrar, lista_para_buscar, tema_geral

    ensure_files_dir_exists()
    if not os.path.exists(PASSWORD_FILE):
        open(PASSWORD_FILE, 'w').close()

    update_list()

    config = load_config()
    tema_geral = config['tema']
    sg.theme(tema_geral)
    sg.set_options(font=('Roboto', 11))

    layout = [
        [sg.Text('Buscar'), sg.InputText(size=(29, 1), key='-BUSCA-', enable_events=True)],
        [sg.Listbox(lista_para_mostrar, size=(40, 20), key='-LISTBOX-', enable_events=True, select_mode=sg.LISTBOX_SELECT_MODE_SINGLE)],
        [sg.Button('➕', size=(18, 1), key='-ADICIONAR-'), sg.Button('✏️', size=(17, 1), key='-MODIFICAR-')],
        [sg.Text('Tema:'), sg.Combo(sg.theme_list(), default_value=tema_geral, key='-TEMA-', enable_events=True, size=(15, 1))],
        [sg.Text(f'© {datetime.now().year} Picoword'), sg.Push(), sg.Text(f'↻ {GITHUB_USER}')],
    ]

    window = sg.Window(f'PICOWORD v{VERSAO_APP} - Tela Principal', layout, finalize=True)
    window['-LISTBOX-'].bind('<Double-Button-1>', '-DOUBLE-')

    searching = False
    while True:
        event, values = window.read()

        if event == sg.WINDOW_CLOSED:
            break
        elif event == '-ADICIONAR-':
            add_password()
            update_list()
            window['-LISTBOX-'].update(lista_para_mostrar)
        elif event == '-MODIFICAR-':
            if values['-LISTBOX-']:
                try:
                    index_selected = values['-LISTBOX-'][0].strip()
                    modify_password(index_selected, searching)
                    update_list()
                    search = values['-BUSCA-']
                    lista_busca = [item for item in lista if search.lower() in item[1].lower()]
                    update_search_list()
                    window['-LISTBOX-'].update(lista_para_buscar if searching else lista_para_mostrar)
                except Exception as e:
                    sg.popup_error(f"Erro ao modificar senha: {str(e)}")
        elif event == '-LISTBOX--DOUBLE-':
            if values['-LISTBOX-']:
                try:
                    index_selected = values['-LISTBOX-'][0].strip()
                    view_password(index_selected, searching)
                except Exception as e:
                    sg.popup_error(f"Erro ao visualizar senha: {str(e)}")
        elif event == '-BUSCA-':
            search = values['-BUSCA-']
            if search == '':
                update_list()
                window['-LISTBOX-'].update(lista_para_mostrar)
                searching = False
            else:
                lista_busca = [item for item in lista if search.lower() in item[0].lower()]
                update_search_list()
                window['-LISTBOX-'].update(lista_para_buscar)
                searching = True
        elif event == '-TEMA-':
            new_theme = values['-TEMA-']
            change_theme(new_theme)
            window.close()
            return main_window()
        elif event == '-GITHUB_NAME-':
            os.system("start \"\" https://github.com/MatPicolli")

    window.close()

def create_master_password():
    ensure_files_dir_exists()
    if not os.path.exists(MASTER_PASSWORD_FILE):
        layout = [
            [sg.Text('Nova senha', size=(15, 1)),
             sg.InputText(key='-NEWPASS1-', size=(18, 1))],
            [sg.Text('Confirmar senha', size=(15, 1)),
             sg.InputText(key='-NEWPASS2-', size=(18, 1))],
            [sg.Button('CONFIRMAR', size=(13, 1), button_color=('green'))]
        ]

        window = sg.Window('Nova Senha_Mestre', layout, finalize=True)

        while True:
            event, values = window.read()
            if event in (sg.WINDOW_CLOSED, 'Sair'):
                break
            if event == 'CONFIRMAR':
                if values['-NEWPASS1-'] == values['-NEWPASS2-']:
                    encrypted_password = ''.join([chr(ord(c) * 3) for c in values['-NEWPASS1-']])
                    with open(MASTER_PASSWORD_FILE, 'w', encoding='utf-8') as f:
                        f.write(encrypted_password)
                    break

        window.close()

def login_window():
    global tema_geral
    create_master_password()
    
    config = load_config()
    tema_geral = config['tema']
    
    sg.theme(tema_geral)
    sg.set_options(font=('Roboto', 11))

    layout = [
        [sg.Text('SENHA-MESTRE', size=(13, 1)),
         sg.InputText(key='-INPUT-', size=(18, 1), password_char='*'), sg.Button('✔')],
        [sg.Text('')],
        [sg.Text(f'© {datetime.now().year} Picoword'), sg.Push(), sg.Text(f'↻ {GITHUB_USER}')],
    ]

    window = sg.Window(f'PICOWORD v{VERSAO_APP} - Login', layout, finalize=True)
    window['-INPUT-'].bind('<Return>', '-ENTER-')

    while True:
        event, values = window.read()
        if event in (sg.WINDOW_CLOSED, 'Sair'):
            break
        elif event in ('-INPUT--ENTER-', '✔'):
            if verify_master_password(values['-INPUT-']):
                window.close()
                main_window()
            else:
                window['-INPUT-'].update('')

    window.close()

if __name__ == '__main__':
    login_window()
