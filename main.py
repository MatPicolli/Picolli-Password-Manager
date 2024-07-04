import os
import csv
import json
import FreeSimpleGUI as sg
from datetime import datetime


lista = []
lista_busca = []
lista_para_mostrar = []
lista_para_buscar = []
tema_geral = 'Reddit'
versao_app = '2.0'
github_user = 'MatPicolli'
temas_disponiveis = ['Black', 'Black2', 'BlueMono', 'BluePurple', 'BrightColors', 'BrownBlue', 'Dark', 
                     'Dark2', 'DarkAmber', 'DarkBlack', 'DarkBlack1', 'DarkBlue', 'DarkBlue1', 'DarkBlue10', 
                     'DarkBlue11', 'DarkBlue12', 'DarkBlue13', 'DarkBlue14', 'DarkBlue15', 'DarkBlue16', 'DarkBlue17', 
                     'DarkBlue18', 'DarkBlue2', 'DarkBlue3', 'DarkBlue4', 'DarkBlue5', 'DarkBlue6', 'DarkBlue7', 'DarkBlue8', 
                     'DarkBlue9', 'DarkBrown', 'DarkBrown1', 'DarkBrown2', 'DarkBrown3', 'DarkBrown4', 'DarkBrown5', 'DarkBrown6', 
                     'DarkBrown7', 'DarkGreen', 'DarkGreen1', 'DarkGreen2', 'DarkGreen3', 'DarkGreen4', 'DarkGreen5', 'DarkGreen6', 
                     'DarkGreen7', 'DarkGrey', 'DarkGrey1', 'DarkGrey10', 'DarkGrey11', 'DarkGrey12', 'DarkGrey13', 'DarkGrey14', 
                     'DarkGrey15', 'DarkGrey16', 'DarkGrey2', 'DarkGrey3', 'DarkGrey4', 'DarkGrey5', 'DarkGrey6', 'DarkGrey7', 
                     'DarkGrey8', 'DarkGrey9', 'DarkPurple', 'DarkPurple1', 'DarkPurple2', 'DarkPurple3', 'DarkPurple4', 'DarkPurple5', 
                     'DarkPurple6', 'DarkPurple7', 'DarkRed', 'DarkRed1', 'DarkRed2', 'DarkTanBlue', 'DarkTeal', 'DarkTeal1', 'DarkTeal10', 
                     'DarkTeal11', 'DarkTeal12', 'DarkTeal2', 'DarkTeal3', 'DarkTeal4', 'DarkTeal5', 'DarkTeal6', 'DarkTeal7', 'DarkTeal8', 
                     'DarkTeal9', 'Default', 'Default1', 'DefaultNoMoreNagging', 'GrayGrayGray', 'Green', 'GreenMono', 'GreenTan', 'HotDogStand', 
                     'Kayak', 'LightBlue', 'LightBlue1', 'LightBlue2', 'LightBlue3', 'LightBlue4', 'LightBlue5', 'LightBlue6', 'LightBlue7', 
                     'LightBrown', 'LightBrown1', 'LightBrown10', 'LightBrown11', 'LightBrown12', 'LightBrown13', 'LightBrown2', 'LightBrown3', 
                    'LightBrown4', 'LightBrown5', 'LightBrown6', 'LightBrown7', 'LightBrown8', 'LightBrown9', 'LightGray1', 'LightGreen', 'LightGreen1', 'LightGreen10', 
                    'LightGreen2', 'LightGreen3', 'LightGreen4', 'LightGreen5', 'LightGreen6', 'LightGreen7', 'LightGreen8', 'LightGreen9', 'LightGrey', 'LightGrey1', 
                    'LightGrey2', 'LightGrey3', 'LightGrey4', 'LightGrey5', 'LightGrey6', 'LightPurple', 'LightTeal', 'LightYellow', 'Material1', 'Material2', 
                    'NeonBlue1', 'NeonGreen1', 'NeonYellow1', 'NeutralBlue', 'Purple', 'Python', 'PythonPlus', 'Reddit', 'Reds', 'SandyBeach', 'SystemDefault', 
                    'SystemDefault1', 'SystemDefaultForReal', 'Tan', 'TanBlue', 'TealMono', 'Topanga']


def carregar_configuracoes():
    if os.path.exists('config.json'):
        with open('config.json', 'r') as f:
            return json.load(f)
    return {"tema": "Reddit"}  # Tema padrão


def salvar_configuracoes(config):
    with open('config.json', 'w') as f:
        json.dump(config, f)


def mudar_tema(novo_tema):
    global tema_geral
    tema_geral = novo_tema
    sg.theme(tema_geral)
    config = carregar_configuracoes()
    config['tema'] = tema_geral
    salvar_configuracoes(config)


def verifica_senha_mestre(senha_escrita):

    with open('senha_mestre.key', 'r', encoding='utf-8') as f:

        aux = f.read()
        
        # transforma cada caracter da senha escrita em um inteiro
        # divide por 3
        # transforma cada inteiro em um caracter

        aux = ''.join([chr(ord(c) // 3) for c in aux])
        
        print(aux)

        f.close()

        if senha_escrita == aux:
            return True
        else:
            return False


def verifica_indice(indice):
    # verifica se o indice (index) existe na primeira coluna de 'senhas.csv'
    with open('senhas.csv', 'r') as f:
        reader = csv.reader(f)
        for linha in reader:
            if indice in linha:
                return True
    return False


def atualiza_lista_busca():
    global lista_busca, lista_para_buscar
    lista_para_buscar = []
    # atualiza a lista de senhas
    for linha in range(len(lista_busca)):
        lista_para_buscar.append(f'{lista_busca[linha][0]}')


def atualiza_lista():
    global lista, lista_para_mostrar
    lista_para_mostrar = []
    # atualiza a lista de senhas
    with open('senhas.csv', 'r') as f:
        lista = list(csv.reader(f))
        for linha in range(len(lista)):
            lista_para_mostrar.append(f'  {lista[linha][0]}')
        f.close()


def deleta_senha(index):
    aux = []
    for i in range(len(lista)):
        if i != index:
            aux.append(lista[i])
    with open('senhas.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(aux)
        f.close()


def salva_senha(dados):
    with open('senhas.csv', 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(dados)
        f.close()


def confirma_acao():
    # tema e fonte
    sg.theme(tema_geral)
    sg.set_options(font=('Roboto', 11))

    # layout da janela
    layout = [
        [sg.Text('Confirmar?')],
        [sg.Button('Sim', button_color=('white', 'green'), key='-SIM-'),
         sg.Button('Não', button_color=('white', 'red'), key='-NAO-')]
    ]

    # cria a janela
    janela = sg.Window('Confirmação', layout, keep_on_top=True)

    # loop da janela
    while True:
        eventos, valores = janela.read()

        # caso o usuarui feche a janela
        if eventos == sg.WINDOW_CLOSED:
            break

        if eventos == '-SIM-':
            janela.close()
            return True

        elif eventos == '-NAO-':
            janela.close()
            return False

    janela.close()


def visualisa_senha(index, buscando=False):
    
    print('visualizando senha...')
    print('indice:', index)
    
    # tema e fonte
    sg.theme(tema_geral)
    sg.set_options(font=('Roboto', 11))

    if buscando:
        for linha in range(0, len(lista)):
            for coluna in range(0, len(lista)):
                if str(index) == lista[linha][0]:
                    index = linha

    print('indice:', index)

    # layout da janela
    layout = [
        [sg.Text('Index *', size=(8, 1)), sg.InputText(lista[index][0], disabled=True, size=(25, 1), key='-INDEX-')],
        [sg.Text('Usuário', size=(8, 1)), sg.InputText(lista[index][1], disabled=True, size=(25, 1), key='-USER-')],
        [sg.Text('Senha', size=(8, 1)), sg.InputText(lista[index][2], disabled=True, size=(25, 1), key='-PASS-')],
        [sg.Text('E-mail', size=(8, 1)), sg.InputText(lista[index][3], disabled=True, size=(25, 1), key='-EMAIL-')],
        [sg.Text('Adicional', size=(8, 1)), sg.Multiline(lista[index][4], disabled=True, size=(25, 8), key='-ADD-')],
    ]

    # cria janela
    janela = sg.Window('Visualização', layout, keep_on_top=True)

    # loop para receber os valores da janela
    while True:
        # caso clique no X na janela
        eventos, valores = janela.read()
        if eventos == sg.WINDOW_CLOSED:
            break

    # fecha a janela
    janela.close()


def modifica_senha(index, buscando=False):
    # tema e fonte
    sg.theme(tema_geral)
    sg.set_options(font=('Roboto', 11))

    if buscando:
        for linha in range(0, len(lista)):
            for coluna in range(0, len(lista)):
                if str(index) == lista[linha][0]:
                    index = linha

    # layout da janela
    layout = [
        [sg.Text('Index *', size=(8, 1)), sg.InputText(lista[index][0], disabled=True, size=(25, 1), key='-INDEX-')],
        [sg.Text('Usuário', size=(8, 1)), sg.InputText(lista[index][1], size=(25, 1), key='-USER-')],
        [sg.Text('Senha', size=(8, 1)), sg.InputText(lista[index][2], size=(25, 1), key='-PASS-')],
        [sg.Text('E-mail', size=(8, 1)), sg.InputText(lista[index][3], size=(25, 1), key='-EMAIL-')],
        [sg.Text('Adicional', size=(8, 1)), sg.Multiline(lista[index][4], size=(25, 8), key='-ADD-')],
        [sg.Button('Salvar', button_color=('white', 'green'), size=(13, 1), key='-SALVAR-'), sg.Push(), 
         sg.Button('Deletar', button_color=('white', 'red'), size=(12, 1), key='-DELETAR-')]
    ]

    # cria janela
    janela = sg.Window('Modificar Senha', layout, keep_on_top=True)

    # loop para receber os valores da janela
    while True:
        # caso clique no X na janela
        eventos, valores = janela.read()
        if eventos == sg.WINDOW_CLOSED:
            break

        # caso clique no botão de salvar
        elif eventos == '-SALVAR-':
            dados = [valores['-INDEX-'], valores['-USER-'], valores['-PASS-'],
                     valores['-EMAIL-'], valores['-ADD-']]
            deleta_senha(index)
            salva_senha(dados)
            break

        # caso clique no botão de deletar
        elif eventos == '-DELETAR-':
            if confirma_acao():
                deleta_senha(index)
                break
            else:
                continue

    # fecha a janela
    janela.close()


def adiciona_senha():
    # tema e fonte
    sg.theme(tema_geral)
    sg.set_options(font=('Roboto', 11))

    # layout da janela
    layout = [
        [sg.Text('Index *', size=(8, 1)), sg.InputText(size=(25, 1), key='-INDEX-')],
        [sg.Text('Usuário', size=(8, 1)), sg.InputText(size=(25, 1), key='-USER-')],
        [sg.Text('Senha', size=(8, 1)), sg.InputText(size=(25, 1), key='-PASS-')],
        [sg.Text('E-mail', size=(8, 1)), sg.InputText(size=(25, 1), key='-EMAIL-')],
        [sg.Text('Adicional', size=(8, 1)), sg.Multiline(size=(25, 8), key='-ADD-')],
        [sg.Button('Criar Senha', size=(19, 1)),
         sg.Push(),
         sg.Button('❌', size=(6, 1), button_color=('red', sg.theme_button_color_background()))]
    ]

    # cria a janela
    janela = sg.Window('Adicionar Senha', layout)

    # loop para o usuário digitar os dados
    while True:
        eventos, valores = janela.read()

        # caso o usuário feche a janela ou pressione o botão X
        if eventos == sg.WINDOW_CLOSED or eventos == '❌':
            break

        if eventos == 'Criar Senha':
            # se indice deixado em branco
            if valores['-INDEX-'] == '':
                sg.Popup('Index deve ser preenchido!')
                continue

            # verifica se o indice já existe
            if verifica_indice(valores['-INDEX-']):
                sg.Popup('Index existente!')
            else:
                dados = [valores['-INDEX-'], valores['-USER-'], valores['-PASS-'],
                         valores['-EMAIL-'], valores['-ADD-']]
                salva_senha(dados)
                break

    # fecha a janela
    janela.close()


def janela_principal():
    try:
        global lista, lista_busca, lista_para_mostrar, lista_para_buscar, tema_geral

        if not os.path.exists('senhas.csv'):
            with open('senhas.csv', 'w') as f:
                f.close()

        atualiza_lista()

        # Carrega as configurações salvas
        config = carregar_configuracoes()
        tema_geral = config['tema']
        sg.theme(tema_geral)
        sg.set_options(font=('Roboto', 11))

        layout = [
            [sg.Text('Buscar'), sg.InputText(size=(29, 1), key='-BUSCA-', enable_events=True)],
            [sg.Listbox(lista_para_mostrar, size=(40, 20), key='-LISTBOX-', enable_events=True, select_mode=sg.LISTBOX_SELECT_MODE_SINGLE)],
            [sg.Button('➕', size=(18, 1), key='-ADICIONAR-'), sg.Button('✏️', size=(17, 1), key='-MODIFICAR-')],
            [sg.Text('Tema:'), sg.Combo(temas_disponiveis, default_value=tema_geral, key='-TEMA-', enable_events=True, size=(15, 1))],
            [sg.Text(f'© {datetime.now().year} Picoword'), sg.Push(), sg.Text(f'↻ {github_user}')],
        ]

        janela = sg.Window(f'PICOWORD v{versao_app} - Tela Principal', layout, finalize=True)
        janela['-LISTBOX-'].bind('<Double-Button-1>', '-DOUBLE-')

        na_busca = False
        primeiro_update = False
        while True:
            eventos, valores = janela.read()

            if not primeiro_update:
                janela['-LISTBOX-'].update(lista_para_mostrar)
                primeiro_update = True

            elif eventos == '-ADICIONAR-':
                try:
                    adiciona_senha()
                    atualiza_lista()
                    janela['-LISTBOX-'].update(lista_para_mostrar)
                except ValueError:
                    pass

            elif eventos == sg.WINDOW_CLOSED:
                break

            elif eventos == '-MODIFICAR-':
                if valores['-LISTBOX-']:
                    try:
                        if na_busca:
                            index_selecionado = valores['-LISTBOX-'][0]
                            modifica_senha(index_selecionado, True)
                        else:
                            index_selecionado = lista_para_mostrar.index(valores['-LISTBOX-'][0])
                            modifica_senha(index_selecionado)
                        atualiza_lista()
                        busca = valores['-BUSCA-']
                        lista_busca = list(filter(lambda cadastro: busca.lower() in cadastro[1].lower(), lista))
                        atualiza_lista_busca()
                        janela['-LISTBOX-'].update(lista_para_buscar if na_busca else lista_para_mostrar)
                    except ValueError:
                        pass

            elif eventos == '-LISTBOX-' + '-DOUBLE-':
                if valores['-LISTBOX-']:
                    try:
                        if na_busca:
                            index_selecionado = valores['-LISTBOX-'][0]
                            visualisa_senha(index_selecionado, True)
                        else:
                            index_selecionado = lista_para_mostrar.index(valores['-LISTBOX-'][0])
                            visualisa_senha(index_selecionado)
                    except ValueError:
                        pass

            elif eventos == '-BUSCA-':
                busca = valores['-BUSCA-']
                if busca == '':
                    atualiza_lista()
                    janela['-LISTBOX-'].update(lista_para_mostrar)
                    na_busca = False
                else:
                    lista_busca = [senha for senha in lista if busca.lower() in senha[0].lower()]
                    atualiza_lista_busca()
                    janela['-LISTBOX-'].update(lista_para_buscar)
                    na_busca = True

            elif eventos == '-TEMA-':
                novo_tema = valores['-TEMA-']
                mudar_tema(novo_tema)
                # Recria a janela com o novo tema
                janela.close()
                return janela_principal()  # Reinicia a janela principal com o novo tema

        janela.close()
    
    except Exception as e:
        print(f"Ocorreu um erro: {e}")


def nova_senha_mestre():
    # verifica se existe o arquivo chamado senha_mestre.key
    if not os.path.exists('senha_mestre.key'):
        with open('senha_mestre.key', 'w', encoding='utf-8') as f:

            sg.theme(tema_geral)
            sg.set_options(font=('Roboto', 11))

            # layot da janela
            layout = [
                [sg.Text('Nova senha', size=(15, 1)),
                 sg.InputText(key='-NEWPASS1-', size=(18, 1))],
                [sg.Text('Confirmar senha', size=(15, 1)),
                 sg.InputText(key='-NEWPASS2-', size=(18, 1))],
                [sg.Button('CONFIRMAR', size=(13, 1), button_color=('green'))]
            ]

            janela = sg.Window(f'Nova Senha_Mestre', layout, finalize=True)

            while True:
                eventos, valores = janela.read()

                if eventos == sg.WINDOW_CLOSED or eventos == 'Sair':
                    break

                if eventos == 'CONFIRMAR':
                    if valores['-NEWPASS1-'] == valores['-NEWPASS2-']:
                        # grava a nova senha mestre
                        aux = valores['-NEWPASS1-']
                        print(aux)

                        # transforma cada caracter na senha em inteiro
                        # multiplica o intero por 3
                        # converte o interiro para caracter novamente
                        aux = ''.join([chr(ord(c) * 3) for c in aux])
                        print(aux)

                        f.write(aux)

                        janela.close()
                        break
                    else:
                        pass
            janela.close()
            f.close()
            return
    else:
        return


def janela_de_login():
    global tema_geral
    nova_senha_mestre()
    
    # Carrega as configurações salvas
    config = carregar_configuracoes()
    tema_geral = config['tema']
    
    sg.theme(tema_geral)
    sg.set_options(font=('Roboto', 11))

    # Layout da janela
    layout = [
        # Texto na esquerda e campo de entrada na direita (senha com *) e botão de confirmação
        [sg.Text('SENHA-MESTRE', size=(13, 1)),
         sg.InputText(key='-INPUT-', size=(18, 1), password_char='*'), sg.Button('✔')],
        # Texto com dados da empresa e versão do software
        [sg.Text('')],
        # Texto com o copyright no ano atual sempre
        [sg.Text(f'© {datetime.now().year} Picoword'), sg.Push(), sg.Text(f'↻ {github_user}')],
    ]

    # cria a janela
    janela = sg.Window(f'PICOWORD v{versao_app} - Login', layout, finalize=True)
    janela['-INPUT-'].bind('<Return>', '-ENTER-')

    # Loop para manter a janela aberta
    while True:
        eventos, valores = janela.read()

        # caso o usuário clique em fechar a janela
        if eventos == sg.WINDOW_CLOSED or eventos == 'Sair':
            break
        # caso aperte enter na caixa de escrita ou clique no botão ✔
        elif eventos == '-INPUT-' + '-ENTER-' or eventos == '✔':
            if verifica_senha_mestre(valores['-INPUT-']):
                janela.close()
                janela_principal()

            else:
                valores['-INPUT-'] = ''
                janela['-INPUT-'].update('')

    # Fecha a janela
    janela.close()


if __name__ == '__main__':
    janela_de_login()


# Notas do desenvolvedor:
# O salvamento de dados quando modifica uma senha não funciona 100% do jeito que eu queria que funcionasse, mas funciona.
# Explicando melhor, ele salva dos dados e colocando-os no final do arquivo, ao invés de substituir a linha antiga.
