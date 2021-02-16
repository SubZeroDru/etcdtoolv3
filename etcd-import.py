import yaml
import json
import re
import etcd3
import argparse

from pandas.io.json import json_normalize


def argparser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--url', action='store', dest='url', required=True,
                        help="Specify endpoint of etcd server")
    parser.add_argument('-p', '--port', action='store', dest='port', help="Specify port of etcd server")
    parser.add_argument('-f', '--file_name', action='store', dest='file_name', help="Specify file name")
    parser.add_argument('-c', '--command', action='store', dest='command', required=True,
                        help="Specifiy which etcd method GET/PUT/Del")
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
        stringvalue = str(value)
        if stringvalue[0] == '@':
            contents = open(stringvalue[1:]).read()
            etcd.put('/' + key, contents)
        else:
            etcd.put('/' + key, stringvalue)


def print_etcd_data():
    list_keys=[]
    for value, metadata in etcd.get_all():
        key = metadata.key.decode('utf-8')
        getattr(etcd, args.command)(key)
        print("Key: " + key)
        list_keys.append(key)
        print("Value: " + value.decode('utf-8'))
    return list_keys


def deletekeys():
    list_keys=[]
    etcd = etcd3.client(host=args.url, port=args.port)
    list_keys=print_etcd_data()
    for key in list_keys:
        etcd.delete(key)


args = argparser()
etcd = etcd3.client(host=args.url, port=args.port)

if args.command == "get":
    print_etcd_data()
elif args.command == "delete":
      deletekeys()
else:
    # Open the yaml file and load it into data as json
    with open(args.file_name) as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
    flat_json_data = flatten_json(data)
    converted_data = convert_json_key_value(flat_json_data)
    api_put_request(converted_data)
