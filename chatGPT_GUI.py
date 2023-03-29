import PySimpleGUI as sg

#Variables
ver = '0.1'
gpt_ver_list = ['code-davinci-002','text-davinci-002','text-davinci-003','gpt-3.5-turbo-0301','gpt-3.5-turbo']
gpt_mode_list = ['Complete', 'Chat (Beta)', 'Insert (Beta)', 'Edit (Beta)']
pre_defined_list = ['a','b','c','d']
prompt = ''
response = ''
info = ''
in_out = []
sel_gpt_model = ''
sel_gpt_mode = ''
sel_max_tokens = ''
def_values = [gpt_ver_list[2],gpt_mode_list[0],1001,0.7,0,0,True]

tab1_layout =  [[sg.Frame('Promt', [[sg.Multiline(s=(40,6),key='prompt',enable_events=True)]])],
                [sg.Button('Send'),sg.T('Pre defined prompts'),sg.Combo(pre_defined_list, default_value=pre_defined_list[0], s=(15, 22), enable_events=True, readonly=True,
                         k='-COMBO-')],
                [sg.Frame('Response', [[sg.Multiline(s=(40,6),key='response')]])],
                [sg.Button('Save')],
                [sg.Frame('Info', [[sg.Multiline(s=(40,4),key='info')]])]


                ]

tab2_layout = [[sg.T('GPT model')],
               [sg.Combo(gpt_ver_list, default_value=gpt_ver_list[2], s=(20, 22), enable_events=True, readonly=True,
                         k='gpt_ver')],
                [sg.T('Mode')],
               [sg.Combo(gpt_mode_list, default_value=gpt_mode_list[0], s=(20, 22), enable_events=True, readonly=True,
                         k='gpt_mode')],
                [sg.T('Max tokens (1-4000)')],[sg.Input(s=15,default_text='1001',key='max_tokens')],
                [sg.T('Temperature (0-1, 0.01)')],[sg.Input(s=15,default_text='0.7',key='temp')],
                [sg.T('Top p (0-1, 0.01)')],[sg.Input(s=15,default_text='0',key='top_p')],
                [sg.T('N')],[sg.Input(s=15,default_text='0',key='n')],
                [sg.T('Autosave')], [sg.Checkbox('Checkbox',default=True,key='autosave')],
                [sg.T('Organization')],[sg.Input(s=25,key='org')],
                [sg.T('API Key')],[sg.Input(s=25,key='api_key')],
                [sg.Button('Version',key='version'),sg.Button('Set Default',key='default')],

               ]

layout = [[sg.TabGroup([[sg.Tab('Main', tab1_layout, tooltip='tip'), sg.Tab('Settings', tab2_layout)]], tooltip='TIP2')],
          [sg.Button('Exit',key='Exit')]]

window = sg.Window('ChatGPT GUI v'+ver, layout, default_element_size=(12,1))

while True:
    event, values = window.read()
    print(event,values)
    if event == sg.WIN_CLOSED or event == 'Exit':           # always,  always give a way out!
        window.close()
        break
    if event == 'prompt':
        prompt = values['prompt']
    elif event == 'version':
        sg.popup_scrolled(sg.get_versions())
