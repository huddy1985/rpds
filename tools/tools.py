'''
This is a helper tools, for example translate string to hex
'''
import binascii
import json
import codecs

conf_gprs_file = '/home/huddy1985/PycharmProjects/seralcon/rpds/conf/config_gprs.json'
config_gprs_json = {}
# this conf path will modify when project done

conf_analog_file = '/home/huddy1985/PycharmProjects/seralcon/rpds/conf/config_analog.json'
config_analog_json = {}

def string2hex(string):
    hexdata = binascii.b2a_hex(string)
    return hexdata


# for json op
def initJson():
    global config_gprs_json
    if not config_gprs_json:
        with open(conf_gprs_file, 'r') as f:
            config = f.read()
            config_gprs_json = json.loads(config)

    return config_gprs_json

def setValue2Json():
    global config_gprs_json
    with codecs.open(conf_gprs_file, 'w', 'utf-8') as f:
        f.write(json.dumps(config_gprs_json, indent=4, ensure_ascii=False))

# for json op
def initAnalogJson():
    global config_analog_json
    if not config_analog_json:
        with open(conf_analog_file, 'r') as f:
            config = f.read()
            config_analog_json = json.loads(config)

    return config_analog_json

def setAnalogValue2Json():
    global config_analog_json
    with codecs.open(conf_analog_file, 'w', 'utf-8') as f:
        f.write(json.dumps(config_analog_json, indent=4, ensure_ascii=False))