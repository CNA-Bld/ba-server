from ba_data import data
from ba_data import col

SCREEN_WIDTH = col

def find_pos(ori_pos):
    x = ori_pos % SCREEN_WIDTH
    y = (ori_pos - x) / SCREEN_WIDTH
    return chr(0x1B)+chr(0x5B)+str(y+1)+';'+str(x+1)+'H'

new_data = []
new_data.append(data[0])

for i in range(1,len(data)):
    original_str = data[i-1]
    target_str = data[i]
    diff_str = ''
    recent_diff = -2
    for j in range(0,len(data[i])):
        try:
            if original_str[j] != target_str[j]:
                if j-recent_diff > 1:
                    diff_str += find_pos(j) + target_str[j]
                else:
                    diff_str += target_str[j]
                recent_diff = j
        except:
            print str(i)+' '+str(j)
            break
    if len(diff_str)<len(target_str)+3:
        new_data.append(diff_str)
    else:
        new_data.append(chr(0x1B)+chr(0x5B)+'H'+target_str)

print 'data='+str(new_data)
