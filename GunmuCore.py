def getBinary(text):
    binary_str = ' '.join(format(byte, '08b') for byte in text.encode('utf-8'))
    return(binary_str)

def encode(text,mode):
    if mode=='滚木':
        text1=text
        text1=text1.replace('0','滚')
        text1=text1.replace('1','木')
    elif mode=='otto':
        text1=text
        text1=text1.replace('0','o')
        text1=text1.replace('1','t')
    elif mode=='emoji':
        text1=text
        text1=text1.replace('0','🌲')
        text1=text1.replace('1','🌳')
    return(text1)

def decode(text,mode):
    if mode=='滚木':
        text1=text
        text1=text1.replace('滚','0')
        text1=text1.replace('木','1')
    elif mode=='otto':
        text1=text
        text1=text1.replace('o','0')
        text1=text1.replace('t','1')
    elif mode=='emoji':
        text1=text
        text1=text1.replace('🌲','0')
        text1=text1.replace('🌳','1')
    return(text1)

def notBinary(text):
    binary_str = text.replace(' ', '')
    byte_list = []
    for i in range(0, len(binary_str), 8):
        byte = binary_str[i:i+8]
        if len(byte) == 8:  
            byte_list.append(int(byte, 2))  
    language_str = bytes(byte_list).decode('utf-8')
    return language_str
