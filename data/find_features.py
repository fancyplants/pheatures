import json

with open('text.json') as f:
    dataset = json.load(f)
plus_syllabic = [phone for phone in dataset if dataset[phone]['CORONAL'] == '+']

print(plus_syllabic)
