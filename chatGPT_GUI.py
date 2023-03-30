import PySimpleGUI as sg
import os
import clipboard

from bin import util_tools
from bin import chatGPT_api

try:
    from configparser import ConfigParser
except ImportError:
    from configparser import ConfigParser  # ver. < 3.0

def load_settings():
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
        #print(def_values[9])
        return gpt_models_list, gpt_mode_list,def_values

    except Exception as e:
        print(e)
        gpt_models_list = ['code-davinci-002', 'text-davinci-002', 'text-davinci-003', 'gpt-3.5-turbo-0301',
                           'gpt-3.5-turbo']
        gpt_mode_list = ['Complete', 'Chat (Beta)', 'Insert (Beta)', 'Edit (Beta)']
        def_values = [gpt_models_list[2], gpt_mode_list[0], 258, 0.7, 0, 0, True,'/log','','']
        return gpt_models_list, gpt_mode_list,def_values

def load_own_commands():

    #load prompts from Prompts folder
    try:
        # get local path
        local_directory = util_tools.get_local_path()
        prompts_path = local_directory+'/Prompts/'
        prompts_path = prompts_path.replace('\\', '/')
        #prompts_dict = {'<name>':'<prompt>'}
        prompts_dict = {}
        prompts_list = []
        # instantiate
        for filename in os.listdir(prompts_path):
            f = os.path.join(prompts_path, filename)
            f.replace('\\','/')
            #print(f)
            #print(os.path.isfile(f))
            #file = open(f, 'r')
            #print(file.read())
            # checking if it is a file
            if os.path.isfile(f):
                file = open(f, 'r')
                name = filename[:-4]
                prompts_dict[name] = file.read()
                prompts_list.append(name)

        return prompts_list, prompts_dict

    except Exception as e:
        print(e)
        return [0],{}

def textsave(text,type):
    local_directory = util_tools.get_local_path()
    if type == 'log':
        if def_values[6] is True:
            date = str(util_tools.get_date())
            time = str(util_tools.get_time())
            directory = local_directory + '/log/'
            directory = directory.replace('\\', '/')
            file_name = directory + date + '.txt'
            f = open(file_name, "a")
            f.write(f'{date} - {time} - {text} \n')
            f.close()
    if type == 'save':
        date = str(util_tools.get_date())
        time = str(util_tools.get_time())
        time = time.replace(':', '_')
        directory = local_directory + '/saves/'
        directory = directory.replace('\\', '/')
        file_name = directory + date + '_' + time + '.txt'
        save_file = open(file_name, "w")
        save_file.write(f'{date} - {time} \n {text} \n')
        save_file.close()

def send_to_chatGPT(text, values):
    # args list: model,prompt,max_tokens,temp,top_p,n,stream,logprobs
    #def_values = [gpt_models_list[gpt_models_def], gpt_mode_list[gpt_mode_def], max_tokens_def, temp_def, top_p_def,
                  #n_def, autosave_def,autosave_loc,org_def,api_key_def]
    model = values[0]
    prompt = text
    max_tokens = values[2]
    temp = values[3]
    top_p = values[4]
    n = values[5]
    stream = None
    logprobs = None
    api_k = values[9]
    response = chatGPT_api.send_prompt(model, prompt, max_tokens, temp, top_p, n, stream, logprobs, api_k)
    response_text = str(response[0])
    response_text = response_text.replace('\n', '')
    token_cons = response[1]
    return response_text, token_cons

def copy_to_clipboard(text):
    text = str(text)
    clipboard.copy(text)  # now the clipboard content will be string "abc"

def save_defaults(values):
    print(values)
    model = str(gpt_models_list.index(values[0]))
    mode = str(gpt_mode_list.index(values[1]))
    tokens = str(int(values[2]))
    temp = str(values[3])
    top_p = str(values[4])
    n = str(values[5])
    autos = str(values[6])
    org = values[7]
    api_k = values[8]
    # instantiate
    config = ConfigParser()
    # parse existing file
    config.read('settings.ini')
    # update existing value
    config.set('GPT_Models', 'default', model)
    config.set('GPT_Modes', 'default', mode)
    config.set('Max_tokens', 'default', tokens)
    config.set('Temperature', 'default', temp)
    config.set('Top-p', 'default', top_p)
    config.set('N', 'default', n)
    config.set('Autosave', 'default', autos)
    config.set('Organization', 'default', org)
    config.set('API_key', 'default', api_k)
    #set_values = [set_gpt_model,set_gpt_mode,set_max_tokens,set_temp,set_top_p,set_n,set_autosave,set_org,set_api_key]

    with open('settings.ini', 'w') as configfile:
        config.write(configfile)

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
    def_values = [gpt_models_list[gpt_models_def], gpt_mode_list[gpt_mode_def], max_tokens_def, temp_def,
                  top_p_def,
                  n_def, autosave_def, autosave_loc, org_def, api_key_def]


    # add a new section and some values
    # config.add_section('section_b')
    # config.set('section_b', 'meal_val', 'spam')
    # config.set('section_b', 'not_found_val', '404')

    # save to a file
    #
    # config.write(configfile)


def collect_set_values():
    set_values = [set_gpt_model, set_gpt_mode, set_max_tokens, set_temp, set_top_p, set_n, set_autosave, set_org,
                  set_api_key]
    return set_values

#gpt_models_list = ['code-davinci-002', 'text-davinci-002', 'text-davinci-003', 'gpt-3.5-turbo-0301',
                           #'gpt-3.5-turbo']
#gpt_mode_list = ['Complete', 'Chat (Beta)', 'Insert (Beta)', 'Edit (Beta)']
#def_values = []
prompts_dict = {}
prompts_list = [0]

#startup functions
settings_values = load_settings()
gpt_models_list = settings_values[0]
gpt_mode_list = settings_values[1]
def_values = settings_values[2]
own_commands = load_own_commands()
prompts_list = own_commands[0]
prompts_dict = own_commands[1]

#Variables
ver = '0.5'
debug = False
prompt = ''
prompts = ''
response = ''
info = ''
in_out = []
gpt_model = gpt_models_list.index(def_values[0])
gpt_mode = gpt_mode_list.index(def_values[1])
set_gpt_model = gpt_models_list[gpt_model]
set_gpt_mode = gpt_mode_list[gpt_mode]
set_max_tokens = def_values[2]
set_temp = def_values[3]
set_top_p = def_values[4]
set_n = def_values[5]
set_autosave = def_values[6]
set_org = def_values[8]
set_api_key = def_values[9]
set_values = [set_gpt_model,set_gpt_mode,set_max_tokens,set_temp,set_top_p,set_n,set_autosave,set_org,set_api_key]
submits = 0
responses = 0

tab1_layout =  [[sg.Frame('Submit', [[sg.Multiline(prompts, s=(50,10),key='prompt',enable_events=True,enter_submits=True)]
                ,[sg.Button('Submit', key='submit'),sg.Button('Set pre defined', key='pre_set')],
                [sg.T('Pre defined commands'),sg.Combo(prompts_list, default_value=prompts_list[0], s=(20, 22),
                                                       enable_events=True, readonly=True, k='pre_prompts')],
                [sg.Button('Reload commands', key='reload_comm')]

                                     ])],
                [sg.Frame('Response', [[sg.Multiline(s=(50,10),key='response',disabled=True)]])],
                [sg.Button('Save', key='save'),sg.Button('Copy', key='copy'), sg.Button('Clear', key='clear')],
                [sg.Frame('Info', [[sg.Multiline(info, s=(50,6),key='info',disabled=True)]])]


                ]

tab2_layout = [[sg.T('GPT model')],
               [sg.Combo(gpt_models_list, default_value=def_values[0], s=(30, 25), enable_events=True, readonly=True,
                         k='gpt_model')],
                [sg.T('Mode')],
               [sg.Combo(gpt_mode_list, default_value=def_values[1], s=(30, 25), enable_events=True, readonly=True,
                         k='gpt_mode')],
                [sg.T('Max tokens', tooltip='Maximum number of tokens to generate')],
                [sg.Slider((1,4000), resolution=1,orientation='h', s=(30,15), default_value=def_values[2],key='max_tokens',enable_events=True)],
                [sg.T('Temperature', tooltip='Controls randomness')],
                [sg.Slider((0.00,2.00), resolution=0.01,orientation='h', s=(20,15), default_value=def_values[3],key='temp',enable_events=True)],
                [sg.T('Top p', tooltip='Controls diversity')],[sg.Slider((0.00,1.00), resolution=0.01,orientation='h', s=(20,15), default_value=def_values[4],key='top_p',enable_events=True)],
                [sg.T('N',tooltip='How many completions to generate for each prompt')],[sg.Slider((1,50), resolution=1,orientation='h', s=(20,15), default_value=def_values[5],key='n',enable_events=True)],
                [sg.T('Autosave')], [sg.Checkbox('Checkbox',default=def_values[6],key='autosave',enable_events=True)],
                #[sg.T('Autosave location')],[sg.Input(s=15,default_text=def_values[7],key='autos_loc')],
                [sg.T('Organization')],[sg.Input(s=40,default_text=def_values[8],key='org',enable_events=True)],
                [sg.T('API Key')],[sg.Multiline(s=(40,3),default_text=def_values[9],key='api_key',enable_events=True)],
                [sg.Button('Restore Default',key='default'),
                 sg.Button('Save default',key='save_default')],

               ]

layout = [[sg.TabGroup([[sg.Tab('Main', tab1_layout), sg.Tab('Settings', tab2_layout)]])],
          [sg.Button('Exit',key='Exit'),sg.Button('Version',key='version'),sg.Button('About',key='about')]]

window = sg.Window('ChatGPT GUI v'+ver, layout, default_element_size=(12,1))



while True:
    event, values = window.read()
    if debug is True:
        print(event,values)
    if event == sg.WIN_CLOSED or event == 'Exit':           # always,  always give a way out!
        window.close()
        break
    if event == 'submit':
        prompt = ''
        prompt = values['prompt']
        submits += 1
        window['response'].print(f'[ChatGPT <- {submits}] - '+prompt)
        window['info'].print('[-] Data send')
        window['prompt'].update('')
        textsave(info,'log')
        response = send_to_chatGPT(prompt,set_values)
        responses += 1
        textsave('[-] Response received:'+str(response[0]),'log')
        window['info'].print('[-] Response received')
        window['response'].print(f'[ChatGPT -> {responses}] - '+response[0])
        window['response'].print('----------------------------------------------------------')
    if event == 'pre_set':
        prompt_name = values['pre_prompts']
        prompt = prompts_dict[prompt_name]
        window['prompt'].update(prompt)
    if event == 'clear':
        window['response'].update('')
    if event == 'copy':
        copy_to_clipboard(response[0])
        window['info'].print('[-] Response copied to clipboard')
    if event == 'gpt_model':
        set_gpt_model = values['gpt_model']
    if event == 'gpt_mode':
        set_gpt_mode = values['gpt_mode']
    if event == 'max_tokens':
        set_max_tokens = values['max_tokens']
        print(set_max_tokens)
    if event == 'temp':
        set_temp = values['temp']
    if event == 'top_p':
        set_top_p = values['top_p']
    if event == 'n':
        set_n = values['n']
    if event == 'autosave':
        set_autosave = not set_autosave
    if event == 'org':
        set_org = values['org']
    if event == 'api_key':
        set_api_key = values['api_key']
    if event == 'reload_comm':
        own_commands = load_own_commands()
        prompts_list = own_commands[0]
        prompts_dict = own_commands[1]
        window['pre_prompts'].update(value=prompts_list[0], values=prompts_list)
        window['info'].print('[-] Reload commands')
    if event == 'save_default':
        values = collect_set_values()
        save_defaults(values)
    if event == 'default':
        window['gpt_model'].update(def_values[0])
        window['gpt_mode'].update(def_values[1])
        window['max_tokens'].update(def_values[2])
        window['temp'].update(def_values[3])
        window['top_p'].update(def_values[4])
        window['n'].update(def_values[5])
        window['autosave'].update(def_values[6])
        window['org'].update(def_values[8])
        window['api_key'].update(def_values[9])
    if event == 'save':
        text_to_wr = 'Prompt: '+str(prompt)+'\n'+'Response: '+str(response[0])+'\n'+'----------------------------------'+'\n'
        textsave(text_to_wr, 'save')
        window['info'].print('[-] Prompt and response saved')
        window['response'].update('')
    elif event == 'version':
        sg.popup_scrolled(sg.get_versions())
#def_values = [gpt_models_list[gpt_models_def], gpt_mode_list[gpt_mode_def], max_tokens_def, temp_def, top_p_def,
                  #n_def, autosave_def,autosave_loc,org_def,api_key_def]