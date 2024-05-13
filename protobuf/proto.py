import employees_pb2 as emp

avesh = emp.Employee()
avesh.id = 1001
avesh.name = "Avesh"
avesh.salary = 1000

rohit = emp.Employee()
rohit.id = 1002
rohit.name = "Rohit"
rohit.salary = 1000

saurabh = emp.Employee()
saurabh.id = 1003
saurabh.name = "Saurabh"
saurabh.salary = 1000

employees_obj = emp.Employees()
employees_obj.employees.extend([avesh, rohit, saurabh])

with open('data.bin', 'wb') as f:
    f.write(employees_obj.SerializeToString())

with open('data.bin', 'rb') as f:
    employees_obj2 = emp.Employees()
    employees_obj2.ParseFromString(f.read())

print(employees_obj2.employees)
