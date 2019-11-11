import json
import gzip

with open('../public/text.json') as f:
    data = f.read()
    data = gzip.compress(data.encode('utf8'))

with open('../public/text.json', 'wb+') as f:
    f.write(data)

