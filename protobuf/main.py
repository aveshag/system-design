import json

employees = []

employees.append({
    "name": "Avesh",
    "salary": 1000,
    "id": 1001
})

employees.append({
    "name": "Rohit",
    "salary": 1000,
    "id": 1002
})

employees.append({
    "name": "Saurabh",
    "salary": 1000,
    "id": 1003
})

with open("jsondata.json", "w") as f:
    f.write(json.dumps(employees))
