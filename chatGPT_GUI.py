import PySimpleGUI as sg

import chatGPT_api as api


try:
    from configparser import ConfigParser
except ImportError:
    from configparser import ConfigParser  # ver. < 3.0

#Load settings from settings.ini
try:
    # instantiate
    config = ConfigParser()
    # parse existing file
    config.read('settings.ini')
    # read values from a section
    gpt_models_list = config.get('GPT_Models', 'Models')
    gpt_models_list = gpt_models_list.rsplit(',')
    gpt_models_def = config.getint('GPT_Models', 'Default')
    gpt_mode_list = config.get('GPT_Modes', 'Modes')
    gpt_mode_list = gpt_mode_list.rsplit(',')
    gpt_mode_def = config.getint('GPT_Modes', 'Default')
    max_tokens_def = config.getint('Max_tokens', 'Default')
    temp_def = config.getfloat('Temperature', 'Default')
    top_p_def = config.getfloat('Top-p', 'Default')
    n_def = config.getfloat('N', 'Default')
    autosave_def = config.getboolean('Autosave', 'Default')
    autosave_loc = config.get('Autosave', 'Location')
    org_def = config.get('Organization', 'Default')
    api_key_def = config.get('API_key', 'Default')
    def_values = [gpt_models_list[gpt_models_def], gpt_mode_list[gpt_mode_def], max_tokens_def, temp_def, top_p_def,
                  n_def, autosave_def,autosave_loc,org_def,api_key_def]
    #print(def_values)

except Exception as e:
    print(e)
    gpt_models_list = ['code-davinci-002', 'text-davinci-002', 'text-davinci-003', 'gpt-3.5-turbo-0301',
                       'gpt-3.5-turbo']
    gpt_mode_list = ['Complete', 'Chat (Beta)', 'Insert (Beta)', 'Edit (Beta)']
    def_values = [gpt_models_list[2], gpt_mode_list[0], 1001, 0.7, 0, 0, True,'/log','','']

#load prompts from Prompts folder
try:
    prompt_list = []
    # instantiate

except Exception as e:
    print(e)
    prompt_list = []


# update existing value
#config.set('section_a', 'string_val', 'world')

# add a new section and some values
#config.add_section('section_b')
#config.set('section_b', 'meal_val', 'spam')
#config.set('section_b', 'not_found_val', '404')

# save to a file
#with open('test_update.ini', 'w') as configfile:
    #config.write(configfile)


#Variables
ver = '0.1'
prompt = ''
response = ''
info = ''
in_out = []
sel_gpt_model = ''
sel_gpt_mode = ''
sel_max_tokens = ''


tab1_layout =  [[sg.Frame('Prompt', [[sg.Multiline(s=(40,6),key='prompt',enable_events=True)]])],
                [sg.Button('Send', key='send'),sg.T('Pre defined prompts'),sg.Combo(prompt_list, default_value='', s=(15, 22), enable_events=True, readonly=True,
                         k='pre_prompts')],
                [sg.Frame('Response', [[sg.Multiline(s=(40,6),key='response')]])],
                [sg.Button('Save', key='save')],
                [sg.Frame('Info', [[sg.Multiline(s=(40,4),key='info')]])]


                ]

tab2_layout = [[sg.T('GPT model')],
               [sg.Combo(gpt_models_list, default_value=def_values[0], s=(20, 22), enable_events=True, readonly=True,
                         k='gpt_ver')],
                [sg.T('Mode')],
               [sg.Combo(gpt_mode_list, default_value=def_values[1], s=(20, 22), enable_events=True, readonly=True,
                         k='gpt_mode')],
                [sg.T('Max tokens (1-4000)')],[sg.Input(s=15,default_text=def_values[2],key='max_tokens')],
                [sg.T('Temperature (0-1, 0.01)')],[sg.Input(s=15,default_text=def_values[3],key='temp')],
                [sg.T('Top p (0-1, 0.01)')],[sg.Input(s=15,default_text=def_values[4],key='top_p')],
                [sg.T('N')],[sg.Input(s=15,default_text=def_values[5],key='n')],
                [sg.T('Autosave')], [sg.Checkbox('Checkbox',default=def_values[6],key='autosave')],
                [sg.T('Autosave location')],[sg.Input(s=15,default_text=def_values[7],key='autos_loc')],
                [sg.T('Organization')],[sg.Input(s=25,key=def_values[8])],
                [sg.T('API Key')],[sg.Input(s=25,key=def_values[9])],
                [sg.Button('Version',key='version'),sg.Button('Restore Default',key='default'),
                 sg.Button('Save default',key='save_default')],

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
