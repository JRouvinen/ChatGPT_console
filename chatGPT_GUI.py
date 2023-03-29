import PySimpleGUI as sg

gpt_ver_list = [1,2,3,4]
gpt_mode_list = ['Complete', 'Chat (Beta)', 'Insert (Beta)', 'Edit (Beta)']
pre_defined_list = ['a','b','c','d']

tab1_layout =  [[sg.Frame('Promt', [[sg.Multiline(s=(40,6))]])],
                [sg.Button('Send'),sg.T('Pre defined promts'),sg.Combo(pre_defined_list, default_value=pre_defined_list[0], s=(15, 22), enable_events=True, readonly=True,
                         k='-COMBO-')],
                [sg.Frame('Response', [[sg.Output(s=(40,6))]])],
                [sg.Frame('Info', [[sg.Multiline(s=(40,4))]])]


                ]

tab2_layout = [[sg.T('GPT model')],
               [sg.Combo(gpt_ver_list, default_value=gpt_ver_list[0], s=(15, 22), enable_events=True, readonly=True,
                         k='-COMBO-')],
                [sg.T('Mode')],
               [sg.Combo(gpt_mode_list, default_value=gpt_mode_list[0], s=(15, 22), enable_events=True, readonly=True,
                         k='-COMBO-')],
                [sg.T('Max tokens (1-4000)'),sg.Input(s=15)],
                [sg.T('Temperature (0-1, 0.01)'),sg.Input(s=15)],
                [sg.T('Top p (0-1, 0.01)'),sg.Input(s=15)],
                [sg.T('N'),sg.Input(s=15)],
                [sg.T('Autosave'), sg.Checkbox('Checkbox')],
                [sg.T('Organization'),sg.Input(s=25)],
                [sg.T('API Key'),sg.Input(s=25)],
                [sg.Button('Version')],

               ]

layout = [[sg.TabGroup([[sg.Tab('Main', tab1_layout, tooltip='tip'), sg.Tab('Settings', tab2_layout)]], tooltip='TIP2')],
          [sg.Button('Save')]]

window = sg.Window('ChatGPT GUI', layout, default_element_size=(12,1))

while True:
    event, values = window.read()
    print(event,values)
    if event == sg.WIN_CLOSED:           # always,  always give a way out!
        break
