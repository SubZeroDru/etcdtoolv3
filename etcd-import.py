import yaml
import json
import re
import etcd3
import argparse

from pandas.io.json import json_normalize


def argparser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--url', action='store', dest='url', required=True, help="Specify endpoint of etcd server")
    parser.add_argument('-p', '--port', action='store', dest='port', required=True, help="Specify port of etcd server")
    parser.add_argument('-f', '--file_format', action='store', dest='file_format', required=True, help="Specify file format YAML / JSON")
    parser.add_argument('-c', '--command', action='store', dest='command', required=True, help="Specifiy which etcd method GET/PUT")
    args = parser.parse_args()
    return args


# Convert json to one line string.
def flatten_json(y):
    out = {}

    def flatten(x, name=''):
        if type(x) is dict:
            for a in x:
                flatten(x[a], name + a + '_')
        elif type(x) is list:
            out[name[:-1]] = json.dumps(x)
        else:
            out[name[:-1]] = x

    flatten(y)
    return out
def convert_json_key_value(obj):
    res = {}
    for key, value in obj.items():
        converted_key = key.replace("_", "/")
        res[converted_key] = value
    return res
def api_put_request(obj):
    for key, value in obj.items():
        if (value[0] == '@'):
            contents = open(value[1:]).read()
            etcd.put('/' + key, contents)
        else:
            etcd.put('/' + key, value)
def api_get_request(json_obj, sort_order=None, sort_target='key'):
    for key, value in json_obj.items():
        getattr(etcd, args.command)(key)
    for value, metadata in etcd.get_all():
        getattr(etcd, args.command)(key)
        print("Key: " + metadata.key.decode('utf-8'))
        print("Value: " + value.decode('utf-8'))



# Open the yaml file and load it into data as json
args = argparser()
with open(args.file_format) as f:
    data = yaml.load(f, Loader=yaml.FullLoader)

etcd = etcd3.client(host=args.url, port=args.port)

flat_json_data = flatten_json(data)
converted_data = convert_json_key_value(flat_json_data)
if args.command == "get":
    api_get_request(converted_data)
else:
    api_put_request(converted_data)
