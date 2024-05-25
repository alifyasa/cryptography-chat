from utils.constant import BLOCK_SIZE

def string_to_byte_string(string):
    ret = ""
    for ch in string:
        formatted_ch = format(ord(ch), '08b')
        while len(formatted_ch) % 8 != 0:
            formatted_ch = "0" + formatted_ch
        ret += formatted_ch
    
    return ret

def block_string_to_byte_string(string):
    byte_string = format(int(string, 2), '08b')
    while len(byte_string) % 8 != 0:
        byte_string = "0" + byte_string
    return byte_string
