import json

with open('danube.json') as f:
    data = json.load(f)
mapping = {}
for i in data['mandatory']['value']:
    for j in i['value']:
        for k in j['value']:
            mapping[k] = True
for i in data['optional']['value']:
    for j in i['value']:
        for k in j['value']:
            mapping[k] = False

with open('mandatory.json', 'w') as f:
    f.write(json.dumps(mapping))
