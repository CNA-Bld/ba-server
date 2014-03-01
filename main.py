import socket, threading, time

import plugins

HOST = ''
PORT = 23
ISOTIMEFORMAT='%Y-%m-%d %X'
VERSION = 'V2.1011 Alpha B17'
BANNER = 'Copyright 2009-2013 SoftStar Hangzhou [http://www.sshz.org]\r\nServer Version: '+VERSION+'\r\n\r\n'
DEBUG = True
SHOW_INPUT = True
LOG_ENABLED = True
LOG_TO_FILE = False

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(4)

def write_log(info):
    if LOG_ENABLED:
        info = '['+time.strftime(ISOTIMEFORMAT, time.localtime()) + '] ' + info
        print info
        if LOG_TO_FILE:
            output = open('ba.log', 'a')
            output.write(info+'\n')
            output.close()

class bad_apple_server(threading.Thread):
    def __init__(self, (socket,address)):
        threading.Thread.__init__(self)
        self.socket = socket
        self.address = address

    def get_user_input(self, info, allowed_chars=[str(i) for i in range(0,10)]):
        try:
            input_str = ''
            self.socket.send('\r\n'+info)
            while True:
                temp_str = self.socket.recv(1024)
                if SHOW_INPUT:
                    print '['+time.strftime(ISOTIMEFORMAT, time.localtime()) + '] Char=' + temp_str[0]
                if temp_str[0] in allowed_chars:
                    input_str += temp_str
                    if SHOW_INPUT:
                        print '['+time.strftime(ISOTIMEFORMAT, time.localtime()) + '] String=' + input_str
                elif temp_str[0] in ['\r', '\n', '\r\n']:
                    break
                else:
                    self.socket.send('\r\nDisallowed Character.\r\n')
                    return self.get_user_input(info, allowed_chars)

            for i in range(-1,-len(input_str),-1):
                if input_str[i] in allowed_chars:
                    break
            input_str = input_str[:i]

            if SHOW_INPUT:
                print '['+time.strftime(ISOTIMEFORMAT, time.localtime()) + '] String=' + input_str
            return input_str
        except:
            return

    def force_disconnect(self, info):
        try:
            self.socket.send(info)
        finally:
            self.socket.close()
            write_log('%s:%s force disconnected. Info: %s' % (self.address + (info,)))

    def run(self):
        try:
            write_log('%s:%s connected.' % self.address)
            self.socket.send(BANNER)

            self.socket.send('Plugin List:\r\n')
            self.socket.send(plugins.formatted_plugin_list())
            plugin_id = self.get_user_input('Please choose plugin. Input ID before its name:')
            if plugin_id not in plugins.plugin_id_list():
                self.force_disconnect('Plugin ID not recognized.')
                return
            chosen_plugin = plugins.get_plugin_code(plugin_id)

            self.socket.send('\r\n\r\nChosen Plugin: %s\r\nRequired Resolution: %d*%d\r\nAuthor: %s\r\n\r\n' % (plugins.plugin_list[int(plugin_id)], chosen_plugin.col, chosen_plugin.line, chosen_plugin.author))

            delay_str = self.get_user_input('Please input delay in second [Input - for recommended value (%f)]: \r\n' % (1.0/chosen_plugin.frame), [str(i) for i in range(0,10)]+['.','-'])
            if '-' in delay_str:
                delay = 1.0/chosen_plugin.frame
                self.socket.send('Delay set to default value(%f).' % delay)
            else:
                try:
                    delay = float(delay_str)
                    self.socket.send('Delay set to %f.' % delay)
                except:
                    self.force_disconnect('Delay time not recognized.')
                    return

            self.get_user_input('Press Enter to Begin.', [])

            state = 0
            self.socket.send(chr(0x1B)+chr(0x5B)+'H')
            self.socket.send(chr(0x1B)+chr(0x5B)+'J')
            if DEBUG:
                time.sleep(0.1)

            start_time = time.time()

            while True:
                try:
                    if state<len(chosen_plugin.data):
                        time_delta = start_time + delay*state - time.time()
                        if DEBUG:
                            print 'time_delta %f; time_shift %f' % (time_delta, time_delta-delay)
                        if time_delta > 0:
                            time.sleep(time_delta)
                        self.socket.send(chosen_plugin.data[state])
                        state += 1
                    else:
                        state = 0
                        start_time = time.time()
                        self.socket.send(chr(0x1B)+chr(0x5B)+'H')
                except:
                    break

            self.socket.close()
            write_log('%s:%s disconnected.' % self.address)

        except:
            self.socket.close()
            write_log('%s:%s force disconnected for uncaught exception.' % self.address)

write_log('Initialization Finished.')
if DEBUG:
    print 'Debug Mode ON'
while True:
    bad_apple_server(s.accept()).start()
