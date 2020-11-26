import json
import sys
import os
import getopt

if len(sys.argv) == 1:
    print('use default file names')
    source_config_file = '/home/username/.config/qv2ray/generated/config.gen.json'
    dest_config_file = '/usr/local/etc/v2ray/config.json'
    template_config_file = 'template.json'
else:
    try:
        args, o_args = getopt.getopt(sys.argv[1:], 'i:o:t:')
        for arg in args:
            if arg[0] == '-i':
                source_config_file = arg[1]
            elif arg[0] == '-o':
                dest_config_file = arg[1]
            elif arg[0] == '-t':
                template_config_file = arg[1]
    except:
        print('useage: python3 convert2TransparentConfig.py -i qv2rayfilename -o resultfilename -t templatefilename')
        sys.exit(1)

try:
    with open(source_config_file) as f:
        source_data = json.load(f)
except:
    print(f'open {source_config_file} file error')
    sys.exit(2)
try:
    with open(template_config_file) as f:
        template_data = json.load(f)
except:
    print(f'open {template_config_file} file error')
    sys.exit(2)

source_data['dns'] = template_data['dns']
source_data['inbounds'] = template_data['inbounds']

servers = []    # remote servers
for i, out_protocol in enumerate(source_data['outbounds']):
    if out_protocol['protocol'] == 'vmess':
        for server in out_protocol['settings']['vnext']:
            servers.append(server['address'])
        source_data['dns']['servers'][-1]['domains'].extend(servers)
        # add remote servers to DNS set
        source_data['outbounds'][i]['streamSettings']['sockopt'] = {"mark": 255}
        source_data['outbounds'][i]['mux'] = {"enabled": True}
        source_data['outbounds'][i]['tag'] = 'proxy'
    elif out_protocol['protocol'] == 'freedom':
        for temp_out_protocol in template_data['outbounds']:
            if temp_out_protocol['protocol'] == 'freedom':
                source_data['outbounds'][i] = temp_out_protocol
                break
    elif out_protocol['protocol'] == 'blackhole':
        source_data['outbounds'][i]['tag'] = 'block'
for temp_out_protocol in template_data['outbounds']:
    if temp_out_protocol['protocol'] == 'dns':
        source_data['outbounds'].append(temp_out_protocol)
        break

source_data['routing'] = template_data['routing']

try:
    with open(dest_config_file, 'w', encoding='utf-8') as f:
        json.dump(source_data, f, indent = 4)
except:
    print(f'write to {dest_config_file} file error.')
    sys.exit(2)

print('done.')

