![alt text](https://raw.githubusercontent.com/cncf/artwork/master/projects/etcd/horizontal/color/etcd-horizontal-color.png)



# etcd V3 api tool 
I have created a new etcdtool for etcd V3 API.
Able to import YAML / JSON into your etcd cluster registry V3.

This tool is open source and for everyone to use.
Based on python3


### Running the script
  python3 etcd-import.py -h for help menu.
  
  
optional arguments:
  -h, --help            show this help message and exit
  -u URL, --url URL     Specify endpoint of etcd server
  -p PORT, --port PORT  Specify port of etcd server
  -f FILE_FORMAT, --file_format FILE_FORMAT
                        Specify file format YAML / JSON
  -c COMMAND, --command COMMAND
                        Specifiy which etcd method GET/PUT
  
  you can use it for all etcd-client API requests.
  
