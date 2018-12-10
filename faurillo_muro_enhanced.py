import os
from faurillo_muro_simClasses import *
def cashierfree(cashier_objs):
	""" 
		Checks if a cashier is empty and retrieves the key/index
		This is for the cashiers in Basket Lane (can be transferred to main)
	"""
	emptycashier_list = []
	for cashierKey in range(len(cashier_objs)):
		if cashier_objs[cashierKey].isvacant():
			emptycashier_list.append(cashierKey)
	return emptycashier_list

def clear():
	return os.system('cls' if os.name == 'nt' else 'clear')

#open customer file
filename = 'arrivals'
customer_list = []

while not customer_list:
	try:
		if '.txt' not in filename: filename += '.txt'
		with open(filename,'r') as fn:
			customer_list = fn.read().strip().split('\n')
	except FileNotFoundError:
		print('File '+filename+' not found! Try again!')
		filename = input('Enter a file: ')
		if not filename.strip(): os.sys.exit('bye')


#initialization of lists/dictionaries
customer_objs = []
customers_done = []
customers_wait = []
cashier_objs_Basket = []
cashier_objs_Cart = []
cashier_queue = {}

#Magic numbers
noOfCashiers = 2
simulTimeLength = 9**9	#maximum simulation time 
# Simulation Type:      1 - One to Many      2 - One to One     3 - Both (for comparison)
simulType = 0

#Counters
totalTime = 0
noOfCustomers = len(customer_list)

"""Customers"""
for i in customer_list[0]: 
	if not i.isdigit():             div = i 
for i in range(len(customer_list)):
	temp = customer_list[i].split(div)
	if int(temp[1]) < 20: customer_objs.append(Customer(temp[0],temp[1],i))
	elif int(temp[1]) >= 20: customer_objs.append(Customer1to1(temp[0],temp[1],i))

"""Cashiers"""
for i in range(noOfCashiers):
	cashier_objs_Basket.append(Cashier(i))
	cashier_objs_Cart.append(Cashier1to1(i))

""" Simulation Proper"""
input('Enter to start simulation')
clear()
print('Customers:',[customer for customer in customer_objs])
print('\n--------------------------------------------------Simulation Start--------------------------------------------------')
for simulTime in range(simulTimeLength):
	print('                Time:',simulTime)
	print('Events: ')
	for customerKey in range(len(customer_objs)):
		if customerKey in customers_done: continue                                              #added
		currentCustomer = customer_objs[customerKey]
		if not currentCustomer.arrived(simulTime): continue
		if currentCustomer.type == 'basket':
			if currentCustomer.returnstatus() == 0 and currentCustomer not in customers_wait:
				customers_wait.append(currentCustomer)
			if currentCustomer.depart(simulTime) == -1:
				cashier_objs_Basket[currentCustomer.cashieroccupied()].open()                   #open cashier
				customers_done.append(customerKey)
			for cashKey in cashierfree(cashier_objs_Basket):                                           #fill in empty cashier
				if currentCustomer.service(simulTime,cashKey):
					print(currentCustomer,'lining up in Cashier #',cashKey+1)
					customers_wait.remove(currentCustomer)
					totalTime += currentCustomer.waitingtime()
					cashier_objs_Basket[cashKey].close(currentCustomer)                                                     #close cashier
					break                                                                                                   #break loop when cashier is occupied
		if currentCustomer.type == 'cart':
			if currentCustomer.depart(simulTime,'SM') == -1:
				for cashKey in range(len(cashier_objs_Cart)):
					if currentCustomer in cashier_objs_Cart[cashKey].returnqueue():
						cashier_objs_Cart[cashKey].removecust(currentCustomer)
						customers_done.append(customerKey)
				continue
			if not currentCustomer.arrived(simulTime): continue
			for cashKey in range(len(cashier_objs_Cart)):
				cashier_queue[cashKey] = len(cashier_objs_Cart[cashKey])
			shortLanes = [name for name in cashier_queue if cashier_queue[name]==min(cashier_queue.values())]
			for cashKey in shortLanes:
				if not currentCustomer.isqueued():
					cashier_objs_Cart[cashKey].addcust(currentCustomer)
					currentCustomer.lineup(cashier_objs_Cart[cashKey].returnqueue(),cashKey)
				if currentCustomer.returnqueue().index(currentCustomer) == 0:
					if currentCustomer.service(simulTime,cashKey): 
						totalTime += currentCustomer.waitingtime()
						print(currentCustomer,'being serviced by Cashier #',cashKey+3)
				break

	print('------------------------')
	print('Basket Lane')
	for cashierKey in cashier_objs_Basket:
		print('Cashier {} : {}'.format(cashierKey+1,cashierKey.returnqueue()))
	print('Waiting Line: {}'.format(customers_wait))
	print('------------------------')
	print('Big Cart Lanes')
	for cashierKey in cashier_objs_Cart:
		print('Cashier {} : {}'.format(cashierKey+3,cashierKey.returnqueue()))
	print('\n____________________________________________________________________________________________________________________')
	if len(customers_done) == len(customer_list): break
print('\n--------------------------------------------------Simulation End---------------------------------------------------')
print('\nTotal waiting time: {}\nAverage Wait Time: {}'.format(totalTime,totalTime/noOfCustomers))

input()
