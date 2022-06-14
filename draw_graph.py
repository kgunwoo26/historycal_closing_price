import csv

from matplotlib import pyplot as plt

title_list= list()
i =j =1

for i in range(12):
    for j in range(12):
        title_list.append(f"{i},{j}")
print(title_list)

value_list = list()
with open('test2.csv', 'r') as f:
    reader = csv.reader(f)
    for i in reader:
        value_list = i
print(value_list)



plt.bar(title_list,value_list, label = 'Dual momentum')
# plt.plot(date_list,money_list, label = 'Relative momentum')
plt.xlabel("date")
plt.ylabel("money")
plt.show()
