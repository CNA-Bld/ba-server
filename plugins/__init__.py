import bad_apple, bad_apple_hd

plugin_list = ['Bad Apple', 'Bad Apple HD']
plugin_code = [bad_apple, bad_apple_hd]

def formatted_plugin_list():
    formatted_str = ''
    for i in range(0,len(plugin_list)):
        formatted_str += '%d: %s\r\n' % (i, plugin_list[i])
    return formatted_str

def plugin_id_list():
    return [str(i) for i in range(0,len(plugin_list))]

def get_plugin_code(id):
    return plugin_code[int(id)]
