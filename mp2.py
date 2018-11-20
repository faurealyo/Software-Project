inf = float('inf') #lolwat
import os

class Customer:
	''' 
	'''
	cashierSpeed = 1
	#items serviced per tick
	status = 0
	# 0 - waiting 	1 - being served 	-1 - departed
	def __init__(self,arrivalTime,stuff,name):
		print(name,'Arrived')
		self.arrivalTime = int(arrivalTime)
		self.serviceTimeLength = int(stuff*self.cashierSpeed)			#service time length is based on number of items and cashierSpeed
		self.name = name
	def __str__(self):
		return str(self.arrivalTime)+','+str(self.serviceTimeLength)
	def service(self,simulTime,cashierNo):
		if self.status == 0:
			print(self.name,'Started')
			self.serviceTime = int(simulTime)
			self.departureTime =  self.serviceTime + self.serviceTimeLength
			self.status = 1
			self.cashierNo = cashierNo
			return 1
		return 0
	def depart(self,simulTime):
		if self.status == 1:
			if simulTime == self.serviceTime + self.serviceTimeLength:
				self.status = -1
				print(self.name,'left')
				return self.cashierNo
		return 0
	def waitingtime(self):
		waitingTime = self.serviceTime - self.arrivalTime  
		print(self.name,'Waitingtime:',waitingTime)
		return waitingTime
	#Methods for abstraction
	def cashieroccupied(self):
		return self.cashierNo
	def arrived(self,simulTime):
		return True if simulTime >= self.arrivalTime else False
	def returnstatus(self):
		return self.status

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

def createcust(customer_list,customer_objs = {}):
	for i in range(len(customer_list)):
		name = chr(ord('A')+i) if i < 26 else chr(ord('A')+i)+str(i)
		temp = customer_list[i].split(',')
		#named customer objects as letters
		customer_objs[name] = (Customer(temp[0],temp[1],name))
	return customer_objs

def cashiercreate(noOfCashiers):
	'''
	Creates #noOfCashiers cashiers which are open by default

	cashiers_dict format:
		{cashier number(0-noOfCashiers):if cashier is open or not(True or False)}
	'''
	cashiers_dict = {}
	for i in range(1,noOfCashiers+1):
		cashiers_dict[i] = True
	return cashiers_dict

def cashierfree(cashiers_dict):
	''' 
	Checks if a cashier is empty and retrieves the key
	'''
	emptycashiers_list = []
	for key in cashiers_dict:
		if cashiers_dict[key] == True:
			emptycashiers_list.append(key)
	return emptycashiers_list

def cashierstatus(cashiers_dict):
	for cashKey in cashiers_dict:
		print(cashKey,':','Occupied' if cashiers_dict[cashKey] == False else 'Open',end=' | ')
	print()
	return

def clear():
	return os.system('cls' if os.name == 'nt' else 'clear')

#Magic numbers
noOfCashiers = 4
simulTimeLength = 12

customer_list = getcust()
customer_objs = createcust(customer_list)
cashiers_ = cashiercreate(noOfCashiers)

#Counters
customersDone = 0
totalTime = 0
noOfCustomers = len(customer_list)
	
print([str(i) for i in customer_objs.keys()],'\nEnter 111 to start simulation',end='	')
'''
while 1:
	x = input('\nEnter customer name (letter) to view data (arrival time, no. of items) ')
	if x == '111': break
	print(customer_objs[x] if x in customer_objs.keys() else 'No such customer')
'''
view = 'y'#input('Display simulation? ("y")')
'''
Simulation Proper
'''
clear()
print('\n--------------------------------------------------Simulation Start--------------------------------------------------')
for simulTime in range(simulTimeLength):
	print('                Time:',simulTime)
	cashierstatus(cashiers_)
	for customerKey in customer_objs.keys():
		currentCustomer = customer_objs[customerKey]
		if simulTime == 0: break
		if not currentCustomer.arrived(simulTime): continue
		if currentCustomer.depart(simulTime):
			print(customerKey,'Departed cashier#',currentCustomer.cashieroccupied())
			cashiers_[currentCustomer.cashieroccupied()] = True			#open cashier
			customersDone += 1
	cashierstatus(cashiers_)
	print(customerKey,'Waiting' if not currentCustomer.returnstatus() else 'Being Serviced') if currentCustomer.returnstatus() == 1 else ''
	for cashKey in cashierfree(cashiers_):
		for customerKey in customer_objs.keys():						#fill in empty cashiers
			currentCustomer = customer_objs[customerKey]
			if not currentCustomer.arrived(simulTime): continue		
			if currentCustomer.service(simulTime,cashKey):
				totalTime += currentCustomer.waitingtime()
				print(customerKey,'Occupying cashier#',cashKey)
				cashiers_[cashKey] = False								#close cashier
				break													#break loop when cashier is occupied
	cashierstatus(cashiers_)
	print('\n____________________________________________________________________________________________________________________')
	if customersDone == len(customer_list): break
	#if view != ('y' or 'Y'): clear()
print('\n---------------------------------------------------Simulation End---------------------------------------------------')
print('Total customers:',customersDone)
print('Total waiting time: {}\nAverage Wait Time: {}'.format(totalTime,totalTime/noOfCustomers))
input()