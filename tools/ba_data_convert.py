SCREEN_HEIGHT = 24

while True:
    tempstr = ''
    for i in range(0, SCREEN_HEIGHT):
        tempstr += raw_input()[5:] + '\\r\\n'
    raw_input()
    raw_input()
    print("'"+tempstr[:-4]+"', ")