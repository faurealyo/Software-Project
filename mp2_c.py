import os

class Customer:
    """ 
            Transfer if statements to main function
    """
    cashierSpeed=1
    #items serviced per tick
    # 0 - waiting   1 - being served    -1 - departed
    def __init__(self,arrivalTime,stuff,index):
        self.arrivalTime = int(arrivalTime)
        self.serviceTimeLength = int(stuff*self.cashierSpeed)
        self.index = index
        self.name = chr(ord('A')+index)
        self.status = 0
    def __str__(self):
        return self.name
    def service(self,simulTime,cashierNo):
        if self.status == 0:
            self.serviceTime = int(simulTime)
            print(self.name,'starting at time',self.serviceTime)
            self.status = 1
            self.departureTime =  self.serviceTime + self.serviceTimeLength
            self.cashierNo = cashierNo
            return 1
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
    def arrived(self,simulTime):
        return False if simulTime < self.arrivalTime else True
    def returnStatus(self):
        return self.status

class Customer1to1(Customer):
    queued = False
    def linedUp(self,queue):
        self.queued = True
        self.queue=queue
        return queue.index(self.index)
    def returnQueue(self):
        return self.queue
    def isQueued(self):
        return True if self.queued else False

class Cashier:
    def __init__(self,name):
        self.queue = []
        self.name = name
        self.cashierSpeed = 1
    def __len__(self):
        return len(self.queue)
    def isVacant(self):
        return True if len(self.queue) == 0 else False
    def removeCust(self,customer):
        self.queue.remove(customer)
    def addCust(self,customer):
        self.queue.append(customer)
    def returnQueue(self):
        return self.queue
    def returnQueueNamed(self):
        return [chr(ord('A')+i) for i in cashier_objs[key].returnQueue()]
        

def getcust():
    ###filename = input('filename here')
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
simulTimeLength = 15
# Simulation Type:      1 - One to Many      2 - One to One
simulType = 2

customer_objs = []
customer_done = []
cashier_objs = {}
cashier_queue = {}
customer_list = getcust()

#Counters
customerDone = 0
totalTime = 0
noOfCustomers = len(customer_list)

"""Customers"""
for i in range(len(customer_list)):
    ###name = chr(ord('A')+i)
    temp = customer_list[i].split(',')
    #named customer objects as letters
    if simulType == 1: customer_objs.append(Customer(temp[0],temp[1],i))
    elif simulType == 2: customer_objs.append(Customer1to1(temp[0],temp[1],i))
"""Cashiers"""
for i in range(1,noOfCashiers+1):
    cashier_objs[i]=(Cashier(i))

#print([i for i in customer_objs],'\nEnter 111 to start simulation',end='    ')
"""
while 1:
    x = input('\nEnter customer name (letter) to view data (arrival time, no. of items) ')
    if x == '111': break
    print(customer_objs[x] if x in customer_objs else 'No such customer')
view = input('Display simulation? ("y")')
"""
""" 
        Simulation Proper
"""
clear()
print([customer.name for customer in customer_objs])

for simulTime in range(simulTimeLength):
    print('\n____________________________________________________________________________________________________________________')
    print('                Time:',simulTime)
    print('##########')
    if simulType == 1:
        for customerKey in range(len(customer_objs)):
            currentCustomer = customer_objs[customerKey]
            if not currentCustomer.arrived(simulTime): continue
            if currentCustomer.depart(simulTime):
                print(currentCustomer,'departed cashier#',currentCustomer.cashieroccupied())
                cashiers_[currentCustomer.cashieroccupied()] = True

    if simulType == 2:
        for customerKey in range(len(customer_objs)):
            if customerKey not in customer_done:
                currentCustomer = customer_objs[customerKey]
                if currentCustomer.depart(simulTime) == -1:
                    for cashKey in cashier_objs:
                        if customerKey in cashier_objs[cashKey].returnQueue():  
                            print(currentCustomer,'departed cashier#',cashKey)
                            cashier_objs[cashKey].removeCust(customerKey)
                            customer_done.append(customerKey)
                            customerDone += 1
                    continue
                if not currentCustomer.arrived(simulTime): continue
                for cashKey in cashier_objs:
                    cashier_queue[cashKey] = len(cashier_objs[cashKey])
                shortLanes = [name for name in cashier_queue if cashier_queue[name]==min(cashier_queue.values())]
                for cashKey in shortLanes:
                    if not currentCustomer.isQueued():
                        cashier_objs[cashKey].addCust(customerKey)
                        currentCustomer.linedUp(cashier_objs[cashKey].returnQueue())
                        print(currentCustomer,'lining up in cashier #',cashKey)
                    if currentCustomer.returnQueue().index(customerKey) == 0:
                        if currentCustomer.service(simulTime,cashKey): 
                            totalTime += currentCustomer.waitingtime()
                            print(currentCustomer,'atm serviced by cashier #',cashKey)
                    break
    
        print('---------------')
        print(cashier_queue) if cashier_queue else ''
        for key in cashier_objs:
            ###print('Cashier',key,cashier_objs[key].returnqueue())
            print('Cashier {} {}'.format(key,cashier_objs[key].returnQueueNamed()))
        if customerDone == len(customer_list): break
print('\nTotal waiting time: {}\nAverage Wait Time: {}'.format(totalTime,totalTime/noOfCustomers))

input()
