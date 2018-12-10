import os 
from faurillo_muro_simClasses import *
import PySimpleGUI as sg
"""
	Simple Graphical User Interface
	pip install --upgrade PySimpleGUI
	https://pypi.org/project/PySimpleGUI/
	https://readthedocs.org/projects/pysimplegui/
"""

def cashierfree(cashier_objs):
	""" 
		Checks if a cashier is empty and retrieves the key/index
		Sim 1 only (can be transferred to main)
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
cashier_objs = []
cashier_queue = {}

#Magic numbers
noOfCashiers = 4
simulTimeLength = 9**9		#maximum simulation time 
# Simulation Type:      1 - One to Many      2 - One to One     3 - Both (for comparison)
simulType = 0

#Counters
totalTime = 0
noOfCustomers = len(customer_list)

while simulType not in (1,2,3):
	simulType = input('Enter simulation type:\n1 - One to Many      2 - One to One          3 - Both\n')
	if not simulType.isdigit(): continue
	simulType = int(simulType)

"""Customers"""
for i in customer_list[0]: 									#automatically detects separator (',',' ', etc.)																
	if not i.isdigit(): div = i
for i in range(len(customer_list)):
	temp = customer_list[i].split(div)
	if simulType in (1,3):          customer_objs.append(Customer(temp[0],temp[1],i))
	elif simulType == 2:    customer_objs.append(Customer1to1(temp[0],temp[1],i))

"""Cashiers"""
for i in range(noOfCashiers):
	if simulType in (1,3): cashier_objs.append(Cashier(i))
	elif simulType == 2: cashier_objs.append(Cashier1to1(i))

""" Simulation Proper"""
clear()
print('Customers:',[customer for customer in customer_objs])

if simulType in (1,3):
	print('\n--------------------------------------------------Simulation 1 Start--------------------------------------------------')
	for simulTime in range(simulTimeLength):
		print('\n____________________________________________________________________________________________________________________')
		print('                Time:',simulTime)
		print('Events: ')
		for customerKey in range(len(customer_objs)):
			if customerKey in customers_done: continue                                              					#checking if the customer has already departed
			currentCustomer = customer_objs[customerKey]
			if not currentCustomer.arrived(simulTime): continue
			if not currentCustomer.returnstatus() and currentCustomer not in customers_wait: customers_wait.append(currentCustomer)	#appends each customer to waiting line if it has just arrived
			if currentCustomer.depart(simulTime) == -1:											#updates the cashier and customer objects with the customer's status (departed)
				cashier_objs[currentCustomer.cashieroccupied()].open()                  						#opens cashier
				customers_done.append(customerKey)
		for cashierKey in cashierfree(cashier_objs):
			for customerKey in range(len(customer_objs)):                                          					#fills in empty cashiers with one customer each and closes it
				currentCustomer = customer_objs[customerKey]
				if not currentCustomer.arrived(simulTime): continue             
				if currentCustomer.service(simulTime,cashierKey):
					customers_wait.remove(currentCustomer)
					totalTime += currentCustomer.waitingtime()
					cashier_objs[cashierKey].close(currentCustomer)                                                    		
					break                                                                                                   	#break loop when cashier is occupied
		for customerKey in range(len(customer_objs)):
			currentCustomer = customer_objs[customerKey]
			if currentCustomer in customers_wait and simulTime == currentCustomer.arrival():  						#only print if customer has arrived and is waiting
				print(currentCustomer,'arrived and waiting')
		print('---------------')
		layout = [[sg.Text('Time: {}'.format(simulTime),size= (25,1), font=('Segoe UI',25))]]
		if simulTime == 0: event = 'Next'
		for cashierKey in cashier_objs:	
			temp = []													#for printing what happens in the simulation
			print('Cashier',cashierKey+1,':',cashierKey.returnqueue())
			for i in cashierKey.returnqueue(): temp += str(i)
			layout.append([sg.Text('Cashier {} : {}'.format(str(cashierKey+1),temp))])
		layout.append([sg.Text('Waiting Line: {}'.format(customers_wait))])
		layout.append([sg.RButton('Next'),sg.RButton('Skip'),sg.Exit()])
		window = sg.Window('Simulation 1', auto_size_text= True).Layout(layout)
		if event == 'Next': event,values = window.Read()
		window.Close()
		if event == 'Exit': os.sys.exit()
		print('Waiting Line: {}'.format(customers_wait))
		if len(customers_done) == len(customer_list): break											#if all the customers are done, stop the simulation 1
	print('\n--------------------------------------------------Simulation 1 End---------------------------------------------------')		#for showing the results of the simulation
	sim1TotalTime,sim1AveTime = totalTime,round(totalTime/noOfCustomers,3)
	print('\nTotal waiting time: {}\nAverage Wait Time: {}'.format(totalTime,totalTime/noOfCustomers))
	layout = [[sg.Text('Results: ',size= (25,1), font=('Segoe UI',25))],
		  [sg.Text('Total Waiting Time: {}'.format(sim1TotalTime))],
		  [sg.Text('Average Waiting Time: {}'.format(sim1AveTime))],
		  [sg.Exit() if simulType == 1 else sg.RButton('Next')]]
	window = sg.Window('Simulation 1', auto_size_text= True).Layout(layout)
	event, values = window.Read()
	window.Close()
if simulType == 3:                     														#resets values for simulation 2
	totalTime = 0
	customer_objs = []
	customers_done = []
	customers_wait = []
	cashier_objs = []
	cashier_queue = {}
	for i in customer_list[0]: 
		if not i.isdigit(): div = i 
	for i in range(len(customer_list)):
		temp = customer_list[i].split(div)
		customer_objs.append(Customer1to1(temp[0],temp[1],i))
	for i in range(noOfCashiers):
		cashier_objs.append(Cashier1to1(i))

if simulType in (2,3):
	print('\n--------------------------------------------------Simulation 2 Start--------------------------------------------------')
	for simulTime in range(simulTimeLength):
		print('\n____________________________________________________________________________________________________________________')
		print('                Time:',simulTime)
		print('Events: ')
		for customerKey in range(len(customer_objs)):											
			if customerKey in customers_done: continue											#checks if the customer is already finished and has departed
			currentCustomer = customer_objs[customerKey]
			if not currentCustomer.arrived(simulTime): continue
			if currentCustomer.depart(simulTime) == -1:											#updates the cashier and customer objects with the customer's status (departed)
				for cashierKey in range(len(cashier_objs)):
					if currentCustomer in cashier_objs[cashierKey].returnqueue():
						cashier_objs[cashierKey].removecust(currentCustomer)
						customers_done.append(customerKey)
				continue
			for cashierKey in range(len(cashier_objs)):
				cashier_queue[cashierKey] = len(cashier_objs[cashierKey])
			shortLanes = [name for name in cashier_queue if cashier_queue[name]==min(cashier_queue.values())]				#putting all the shortest lanes in this instant in a list to serve as choices where the customer will line up 
			for cashierKey in shortLanes:
				if not currentCustomer.isqueued():
					cashier_objs[cashierKey].addcust(currentCustomer)
					currentCustomer.lineup(cashier_objs[cashierKey].returnqueue(),cashierKey)
				if currentCustomer.returnqueue().index(currentCustomer) == 0:							#if the customer is already in front of the line
					if currentCustomer.service(simulTime): 								#updates the status of the customer to being served
						totalTime += currentCustomer.waitingtime()								#adds the waiting time of the customer to the total waiting time pool
				break
		print('---------------')
		layout = [[sg.Text('Time: {}'.format(simulTime),size= (25,1), font=('Segoe UI',25))]]
		if simulTime == 0: event = 'Next'
		for cashierKey in cashier_objs:
			temp = []													#for printing what happens in the simulation
			print('Cashier {} {}'.format(cashierKey+1,cashierKey.returnqueue()))
			for i in cashierKey.returnqueue(): temp += str(i)
			layout.append([sg.Text('Cashier {} : {}'.format(str(cashierKey+1),temp))])
		layout.append([sg.RButton('Next'),sg.RButton('Skip'),sg.Exit()])
		window = sg.Window('Simulation 2', auto_size_text= True, default_element_size=(40,1)).Layout(layout)
		if event == 'Next': event,values = window.Read()
		window.Close()
		if event == 'Exit': os.sys.exit()		
		if len(customers_done) == len(customer_list): break											#if all the customers are done, stop the simulation
	print('\n--------------------------------------------------Simulation 2 End---------------------------------------------------')
	sim2TotalTime,sim2AveTime = totalTime,round(totalTime/noOfCustomers,3)
	print('\nTotal waiting time: {}\nAverage Wait Time: {}'.format(totalTime,totalTime/noOfCustomers))
	layout = [[sg.Text('Results: ',size= (25,1), font=('Segoe UI',25))],
		  [sg.Text('Total Waiting Time: {}'.format(sim2TotalTime))],
		  [sg.Text('Average Waiting Time: {}'.format(sim2AveTime))],
		  [sg.Exit() if simulType == 2 else sg.RButton('Next')]]
	window = sg.Window('Simulation 2', auto_size_text= True).Layout(layout)
	event, values = window.Read()
	window.Close()
if simulType == 3:																	#Prints a table to compare Total and Average Waiting time of the two simulations
	print('\n                  Simulation 1    Simulation 2')											#the constants are the number of spaces to be inserted between values
	print('Total Wait Time: ',sim1TotalTime,' '*(13 if sim1TotalTime <10 else 12),sim2TotalTime)
	print('Ave. Wait Time:  ',sim1AveTime,' '*(9 if sim1AveTime <10 else 8),sim2AveTime)
	
input()
