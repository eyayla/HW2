import json

with open("strategyqa_100.json", "r", encoding="utf-8") as f:
    data = json.load(f)

print(len(data))