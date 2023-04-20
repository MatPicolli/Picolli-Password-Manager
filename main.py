import os
import csv
import PySimpleGUI as sg
import file_handle as fh


lista = []
lista_busca = []
lista_para_mostrar = []
lista_para_buscar = []


def verifica_senha_mestre(senha_escrita):
    if senha_escrita == '1969':
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
        lista_para_buscar.append(lista_busca[linha][0])


def atualiza_lista():
    global lista, lista_para_mostrar
    lista_para_mostrar = []
    # atualiza a lista de senhas
    with open('senhas.csv', 'r') as f:
        lista = list(csv.reader(f))
        for linha in range(len(lista)):
            lista_para_mostrar.append(lista[linha][0])
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
    sg.theme('DarkBrown6')
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


def visualiza_senha_busca(index):
    # tema e fonte
    sg.theme('DarkBrown6')
    sg.set_options(font=('Roboto', 11))

    # layout da janela
    layout = [
        [sg.Text('Index *', size=(8, 1)), sg.InputText(lista_busca[index][0], disabled=True, size=(20, 1), key='-INDEX-')],
        [sg.Text('Usuário', size=(8, 1)), sg.InputText(lista_busca[index][1], disabled=True, size=(20, 1), key='-USER-')],
        [sg.Text('Senha', size=(8, 1)), sg.InputText(lista_busca[index][2], disabled=True, size=(20, 1), key='-PASS-')],
        [sg.Text('E-mail', size=(8, 1)), sg.InputText(lista_busca[index][3], disabled=True, size=(20, 1), key='-EMAIL-')],
        [sg.Text('Adicional 1', size=(8, 1)), sg.InputText(lista_busca[index][4], disabled=True, size=(20, 1), key='-ADD1-')],
        [sg.Text('Adicional 2', size=(8, 1)), sg.InputText(lista_busca[index][5], disabled=True, size=(20, 1), key='-ADD2-')]
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


def visualisa_senha(index):
    # tema e fonte
    sg.theme('DarkBrown6')
    sg.set_options(font=('Roboto', 11))

    # layout da janela
    layout = [
        [sg.Text('Index *', size=(8, 1)), sg.InputText(lista[index][0], disabled=True, size=(20, 1), key='-INDEX-')],
        [sg.Text('Usuário', size=(8, 1)), sg.InputText(lista[index][1], disabled=True, size=(20, 1), key='-USER-')],
        [sg.Text('Senha', size=(8, 1)), sg.InputText(lista[index][2], disabled=True, size=(20, 1), key='-PASS-')],
        [sg.Text('E-mail', size=(8, 1)), sg.InputText(lista[index][3], disabled=True, size=(20, 1), key='-EMAIL-')],
        [sg.Text('Adicional 1', size=(8, 1)), sg.InputText(lista[index][4], disabled=True, size=(20, 1), key='-ADD1-')],
        [sg.Text('Adicional 2', size=(8, 1)), sg.InputText(lista[index][5], disabled=True, size=(20, 1), key='-ADD2-')]
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


def modifica_senha(index):
    # tema e fonte
    sg.theme('DarkBrown6')
    sg.set_options(font=('Roboto', 11))

    # layout da janela
    layout = [
        [sg.Text('Index *', size=(8, 1)), sg.InputText(lista[index][0], disabled=True, size=(20, 1), key='-INDEX-')],
        [sg.Text('Usuário', size=(8, 1)), sg.InputText(lista[index][1], size=(20, 1), key='-USER-')],
        [sg.Text('Senha', size=(8, 1)), sg.InputText(lista[index][2], size=(20, 1), key='-PASS-')],
        [sg.Text('E-mail', size=(8, 1)), sg.InputText(lista[index][3], size=(20, 1), key='-EMAIL-')],
        [sg.Text('Adicional 1', size=(8, 1)), sg.InputText(lista[index][4], size=(20, 1), key='-ADD1-')],
        [sg.Text('Adicional 2', size=(8, 1)), sg.InputText(lista[index][5], size=(20, 1), key='-ADD2-')],
        [sg.Button('Salvar', button_color=('white', 'green'), size=(13, 1), key='-SALVAR-'),
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
                     valores['-EMAIL-'], valores['-ADD1-'], valores['-ADD2-']]
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
    sg.theme('DarkBrown6')
    sg.set_options(font=('Roboto', 11))

    # layout da janela
    layout = [
        [sg.Text('Index *', size=(8, 1)), sg.InputText(size=(20, 1), key='-INDEX-')],
        [sg.Text('Usuário', size=(8, 1)), sg.InputText(size=(20, 1), key='-USER-')],
        [sg.Text('Senha', size=(8, 1)), sg.InputText(size=(20, 1), key='-PASS-')],
        [sg.Text('E-mail', size=(8, 1)), sg.InputText(size=(20, 1), key='-EMAIL-')],
        [sg.Text('Adicional 1', size=(8, 1)), sg.InputText(size=(20, 1), key='-ADD1-')],
        [sg.Text('Adicional 2', size=(8, 1)), sg.InputText(size=(20, 1), key='-ADD2-')],
        [sg.Button('Criar Senha', size=(19, 1)),
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
                         valores['-EMAIL-'], valores['-ADD1-'], valores['-ADD2-']]
                salva_senha(dados)
                break

    # fecha a janela
    janela.close()


def janela_principal():
    
    fh.decrypt_file()

    # chama a variavel global de lista
    global lista, lista_busca, lista_para_mostrar, lista_para_buscar

    # verifica se o arquivo senhas.txt existe
    if not os.path.exists('senhas.csv'):
        # caso não exista cria o arquivo
        with open('senhas.csv', 'w') as f:
            f.close()

    # lista recebe dados de senhas.csv
    atualiza_lista()

    # tema e fonte
    sg.theme('DarkBrown6')
    sg.set_options(font=('Roboto', 11))

    layout = [
        # cria um caixa de texto e um botão de busca
        [sg.Text('Buscar'), sg.InputText(size=(29, 1), key='-BUSCA-'), sg.Button('🔍')],
        [sg.Listbox(lista_para_mostrar, size=(40, 20), key='-LISTBOX-', enable_events=True, select_mode=sg.LISTBOX_SELECT_MODE_SINGLE)],
        [sg.Button('➕', size=(18, 1), key='-ADICIONAR-'), sg.Button('✏️', size=(17, 1), key='-MODIFICAR-')],
        [sg.Text('© 2023 Picoword'), sg.Text('info@picoword.com', size=(24, 1), justification='right')],
    ]

    # cria a janela
    janela = sg.Window('PICOWORD v0.0.1 - Tela Principal', layout, finalize=True)
    janela['-LISTBOX-'].bind('<Double-Button-1>', '-DOUBLE-')
    janela['-BUSCA-'].bind('<Return>', '-ENTER-')

    # enquanto o usuário não fechar a janela
    na_busca = False
    primeiro_update = False
    while True:
        # recebe os valores da tela
        eventos, valores = janela.read()

        if not primeiro_update:
            janela['-LISTBOX-'].update(lista_para_mostrar)
            primeiro_update = True

        # caso o usuario clique em adicionar
        elif eventos == '-ADICIONAR-':
            try:
                # adiciona a senha
                adiciona_senha()
                # atualiza lista
                atualiza_lista()
                # atualiza a Listbox com apenas a primeira coluna da lista
                janela['-LISTBOX-'].update(lista_para_mostrar)
            except ValueError:
                pass

        # se o usuário fechar a janela
        elif eventos == sg.WINDOW_CLOSED:
            break

        elif eventos == '-MODIFICAR-':
            if valores['-LISTBOX-']:
                try:
                    if na_busca:
                        sg.PopupOK('Não é possível modificar uma senha na busca!')
                    else:
                        # pega o index do item selecionado
                        index_selecionado = lista_para_mostrar.index(valores['-LISTBOX-'][0])
                        # modifica senha
                        modifica_senha(index_selecionado)
                        # atualiza lista
                        atualiza_lista()
                        # atualiza a Listbox
                        janela['-LISTBOX-'].update(lista_para_mostrar)
                except ValueError:
                    pass

        # caso o usuário selecione um item da lista e dê clique duplo nele
        elif eventos == '-LISTBOX-' + '-DOUBLE-':
            if valores['-LISTBOX-']:
                try:
                    print('entrou 1')
                    print(na_busca)
                    if na_busca:
                        # pega o index do item selecionado
                        index_selecionado = lista_para_buscar.index(valores['-LISTBOX-'][0])
                        print('entrou 2')
                        visualiza_senha_busca(index_selecionado)
                    else:
                        # pega o index do item selecionado
                        index_selecionado = lista_para_mostrar.index(valores['-LISTBOX-'][0])
                        visualisa_senha(index_selecionado)
                except ValueError:
                    pass

        elif eventos == '🔍' or eventos == '-BUSCA-' + '-ENTER-':
            if valores['-BUSCA-'] == '':
                # atualiza lista
                atualiza_lista()
                # atualiza a Listbox
                janela['-LISTBOX-'].update(lista_para_mostrar)
                na_busca = False
            else:
                busca = valores['-BUSCA-']
                # filtra a lista de senhas com base no texto de busca
                lista_busca = [senha for senha in lista if busca.lower() in senha[0].lower()]
                # atualiza a lista_busca
                atualiza_lista_busca()
                # atualiza a Listbox com a lista filtrada
                janela['-LISTBOX-'].update(lista_para_buscar)
                na_busca = True

    fh.encrypt_file()

    # fecha a janela
    janela.close()


def janela_de_login():
    # Tema e cor de fundo da janela
    sg.theme('DarkBrown6')
    sg.set_options(font=('Roboto', 11))

    # Layout da janela
    layout = [
        # Texto na esquerda e campo de entrada na direita (senha com *) e botão de confirmação
        [sg.Text('SENHA-MESTRE', size=(13, 1)),
         sg.InputText(key='Input1', size=(30, 1), password_char='*'), sg.Button('✔')],
        # Texto com dados da empresa e versão do software
        [sg.Text('')],
        [sg.Text('© 2023 Picoword'), sg.Text('info@picoword.com', size=(31, 1), justification='right')],
    ]

    # cria a janela
    janela = sg.Window('PICOWORD v0.0.1 - Login', layout, finalize=True)
    janela['Input1'].bind('<Return>', '-ENTER-')

    # Loop para manter a janela aberta
    while True:
        eventos, valores = janela.read()

        # caso o usuário clique em fechar a janela
        if eventos == sg.WINDOW_CLOSED or eventos == 'Sair':
            break
        # caso aperte enter na caixa de escrita ou clique no botão ✔
        elif eventos == 'Input1' + '-ENTER-' or eventos == '✔':
            if verifica_senha_mestre(valores['Input1']):
                janela.close()
                janela_principal()

            else:
                sg.popup('Senha incorreta!', title='PICOWORD')
                break

    # Fecha a janela
    janela.close()


janela_de_login()


# Notas do desenvolvedor:
# A função de modificação e salvamento de dados está quebrada, precisa ser concertado ambos.
# A a função de busca ainda não foi implementada
# clique duplo na ListBox não funciona 100%