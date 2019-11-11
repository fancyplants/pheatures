import json
import gzip

with open('../public/text.json') as f:
    data = json.load(f)

with open('../public/text.json', 'w+') as f:
    json.dump(data, f, ensure_ascii=False)
