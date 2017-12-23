'''
This is a helper tools, for example translate string to hex
'''
import binascii

def string2hex(string):
    hexdata = binascii.b2a_hex(string)
    return hexdata
