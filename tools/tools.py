'''
This is a helper tools, for example translate string to hex
'''
import binascii
import json
import codecs

conf_file = '/home/huddy1985/PycharmProjects/seralcon/rpds/conf/config_boot.json'
config_json = {}
# this conf path will modify when project done


def string2hex(string):
    hexdata = binascii.b2a_hex(string)
    return hexdata


# for json op
def initJson():
    global config_json
    if not config_json:
        with open(conf_file, 'r') as f:
            config = f.read()
            config_json = json.loads(config)

    return config_json

def setValue2Json():
    global config_json
    with codecs.open(conf_file, 'w', 'utf-8') as f:
        f.write(json.dumps(config_json, indent=4, ensure_ascii=False))