inf = float('inf') #lolwat
import os

class Customer:
	''' 
	...Transfer if statements to main function
	'''
	cashierSpeed = 1
	#items serviced per tick
	status = 0
	# 0 - waiting 	1 - being served 	-1 - departed
	def __init__(self,arrivalTime,stuff,name):
		self.arrivalTime = int(arrivalTime)
		self.serviceTimeLength = int(stuff*self.cashierSpeed)									#service time length is based on number of items and cashierSpeed
		self.name = name
	def __str__(self):
		return str(self.arrivalTime)+','+str(self.serviceTimeLength)
	def service(self,simulTime,cashierNo):
		if self.status == 0:
			print(self.name,'started')
			self.serviceTime = int(simulTime)
			self.departureTime =  self.serviceTime + self.serviceTimeLength
			self.status = 1
			self.cashierOccupied = cashierNo
			return 1
		else: return 0
	def depart(self,simulTime):
		if self.status == 1:
			if simulTime == self.serviceTime + self.serviceTimeLength:
				self.status = -1
				print(self.name,'left')
				return self.cashierOccupied
			else: return -1
		else: return -1
	def waitingtime(self):
		waitingTime = self.serviceTime - self.arrivalTime  
		print(self.name,'waitingtime',waitingTime)
		return waitingTime

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
	return customer_list#sorted(customer_list)

def cashiercreate(noOfCashiers):
	'''
	Creates #noOfCashiers cashiers which are open by default

	cashiers_dict format:
		{cashier number(0-noOfCashiers):if cashier is open or not(True or False)}
	'''
	cashiers_dict = {}
	for i in range(noOfCashiers):
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

def clear():
	return os.system('cls' if os.name == 'nt' else 'clear')

#Magic numbers
noOfCashiers = 4
simulTimeLength = 12

customer_objs = {}
customer_list = getcust()
cashiers_ = cashiercreate(noOfCashiers)

totalTime = 0
noOfCustomers = len(customer_list)


for i in range(len(customer_list)):
	name = chr(ord('a')+i) if i < 26 else chr(ord('A')+i)
	temp = customer_list[i].split(',')
	#named customer objects as letters
	customer_objs[name] = (Customer(temp[0],temp[1],name))				
print([str(i) for i in customer_objs.keys()],'\nEnter 111 to start simulation',end='	')

while 1:
	x = input('\nEnter customer name (letter) to view data (arrival time, no. of items) ')
	if x == '111': break
	print(customer_objs[x] if x in customer_objs.keys() else 'No such customer')
view = input('Display simulation? ("y")')
'''
Simulation Proper
'''
clear()
for simulTime in range(simulTimeLength):
	print('\n____________________________________________________________________________________________________________________')
	print('                Time:',simulTime)
	print('##timestart##')
	
	print(cashiers_)
	#loops below are swappable
	for customerKey in customer_objs.keys():
		currentCustomer = customer_objs[customerKey]
		if currentCustomer.arrivalTime > simulTime: continue
		if currentCustomer.depart(simulTime) != -1:
			print(customerKey,'departed cashier#',cashKey)
			cashiers_[currentCustomer.cashierOccupied] = True			#open cashier
	
	print('##departed##')
	print(cashiers_)
	for customerKey in customer_objs.keys():
		currentCustomer = customer_objs[customerKey]
		if currentCustomer.arrivalTime > simulTime: continue
		print(customerKey,'status',currentCustomer.status,end=' | ' if customer_objs[customerKey].status else '\n') if currentCustomer.status != -1 else ''
		for cashKey in cashierfree(cashiers_):		#fill in empty cashiers
			if currentCustomer.service(simulTime,cashKey):
				totalTime += currentCustomer.waitingtime()
				print(customerKey,'occupying cashier#',cashKey)
				cashiers_[cashKey] = False								#close cashier
				break													#break loop when cashier is occupied
	print()
	print('##started##')
	print(cashiers_)
	if view != ('y' or 'Y'): clear()

print('\nTotal waiting time: {}\nAverage Wait Time: {}'.format(totalTime,totalTime/noOfCustomers))

input()