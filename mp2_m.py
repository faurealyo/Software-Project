inf = float('inf') #lolwat
import os

class Customer:
    """ 
            Transfer if statements to main function
    """
    cashierSpeed=1
    isQueued = False
    #items serviced per tick
    # 0 - waiting   1 - being served    -1 - departed
    def __init__(self,arrivalTime,stuff,name):
        self.arrivalTime = int(arrivalTime)
        self.serviceTimeLength = int(stuff*self.cashierSpeed)       #service time length is based on number of items and cashierSpeed
        self.name = name
    def __str__(self):
        return str(self.arrivalTime)+','+str(self.serviceTimeLength)
    def linedUp(self,queue):
        self.isQueued = True
        self.queue=queue
        self.status = 0
        return queue.index(self.name)
    def service(self,simulTime,cashierNo):
        if self.status == 0:
            self.serviceTime = int(simulTime)
            print(self.name,'starting at time',self.serviceTime)
            self.status = 1
            self.departureTime =  self.serviceTime + self.serviceTimeLength
            self.cashierOccupied = cashierNo
            return self.status
        return 0
    def depart(self,simulTime):
        if self.status == 1:
            if simulTime == self.serviceTime + self.serviceTimeLength:
                self.status = -1
        return self.status
    def waitingtime(self):
        self.waitingTime = self.serviceTime - self.arrivalTime
        print(self.name,'waited',self.waitingTime,'time units')
        return self.waitingTime
    
class Cashier:
    def __init__(self,name):
        self.queue = []
        self.name = name
        self.cashierSpeed = 1
        self.vacancy = True
    def __len__(self):
        return len(self.queue)
        

def getcust():
    #filename = input('filename here')
    filename = 'customers'
    if '.txt' not in filename: filename += '.txt'
    customer_list = []
    while not customer_list:
        try:
            with open('customers.txt','r') as fn:
                customer_list = fn.read().strip().split()
        except FileNotFoundError:
            print('File ('+filename+') not found! Try again!')
    return customer_list

def clear():
    return os.system('cls' if os.name == 'nt' else 'clear')

#Magic numbers
noOfCashiers = 4
simulTimeLength = 18

customer_objs = {}
customer_done = []
cashier_objs = {}
cashier_queue = {}
customer_list = getcust()

totalTime = 0
noOfCustomers = len(customer_list)

"""Customers"""
for i in range(len(customer_list)):
    name = chr(ord('a')+i) if i < 26 else chr(ord('A')+i)
    temp = customer_list[i].split(',')
    #named customer objects as letters
    customer_objs[name] = (Customer(temp[0],temp[1],name))
"""Cashiers"""
for i in range(noOfCashiers):
    cashier_objs[i] = (Cashier(i))

print(cashier_objs)
print(customer_objs)
print([str(i) for i in customer_objs.keys()],'\nEnter 111 to start simulation',end='    ')
"""
while 1:
    x = input('\nEnter customer name (letter) to view data (arrival time, no. of items) ')
    if x == '111': break
    print(customer_objs[x] if x in customer_objs.keys() else 'No such customer')
view = input('Display simulation? ("y")')
"""
""" 
        Simulation Proper
"""

clear()

for simulTime in range(simulTimeLength):
    print('\n____________________________________________________________________________________________________________________')
    print('                Time:',simulTime)
    
    print('##########')
    for customerKey in customer_objs:
        if customerKey not in customer_done:
            currentCustomer = customer_objs[customerKey]
            if currentCustomer.arrivalTime > simulTime: continue
            for cashKey in cashier_objs:
                cashier_queue[cashKey] = len(cashier_objs[cashKey])
            shortLanes = [name for name in cashier_queue if cashier_queue[name]==min(cashier_queue.values())]
            for cashKey in shortLanes:
                if not currentCustomer.isQueued:
                    cashier_objs[cashKey].queue.append(customerKey)
                    currentCustomer.linedUp(cashier_objs[cashKey].queue)
                    print(customerKey,'lining up in cashier #',cashKey)
                if currentCustomer.queue.index(customerKey) == 0:
                    if currentCustomer.service(simulTime,cashKey): 
                        totalTime += currentCustomer.waitingtime()
                        print(customerKey,'atm serviced by cashier #',cashKey)
                break
            if currentCustomer.depart(simulTime) == -1:
                for cashKey in cashier_objs:
                    if customerKey in cashier_objs[cashKey].queue:
                        print(customerKey,'departed cashier#',cashKey)
                        cashier_objs[cashKey].queue.remove(customerKey)
                        customer_done.append(customerKey)
    print('---------------')
    print(cashier_queue)
    for key in cashier_objs:
        print('Cashier',key,cashier_objs[key].queue)
print('\nTotal waiting time: {}\nAverage Wait Time: {}'.format(totalTime,totalTime/noOfCustomers))
input()
