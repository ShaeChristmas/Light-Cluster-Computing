import json
array = ['localhost', '192.0.0.1']

with open('ips.json','w') as f:
    json.dump(array, f)