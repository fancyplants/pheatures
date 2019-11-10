import json
import gzip

with open('text.json') as f:
    data = json.load(f)

with open('smaller.json', 'wb+') as f:
    serialized = json.dumps(data, ensure_ascii=False)
    compressed = gzip.compress(serialized.encode('utf8'))
    f.write(compressed)

with open('evensmaller.json', 'wb+') as f:
    serialized = json.dumps(data, ensure_ascii=False, separators=(',', ':'))

    compressed = gzip.compress(serialized.encode('utf8'))

    f.write(compressed)
