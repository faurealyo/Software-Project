
class Customer:
	""" 
		This is the default class for customers. 
		This is used when the simulation type desired is the single line queue or the One Line to All Cashiers Type of Simulation.
	"""
	cashierSpeed = 1									#items serviced per tick
	def __init__(self,arrivalTime,stuff,index):
		self.arrivalTime = int(arrivalTime)
		self.serviceTimeLength = int(stuff*self.cashierSpeed)
		self.index = index
		self.name = chr(ord('A')+index)
		self.type = 'basket' if int(stuff) < 20 else 'cart'
		self.status = 0								# 0 - waiting   1 - being served    -1 - departed
	def __str__(self):
		return self.name
	def __repr__(self):
		return self.name
	def service(self,simulTime,cashierNo='passed'):						#if the customer is already on the top of the line and is ready for service
		if self.status == 0:
			self.serviceTime = int(simulTime)
			print(self.name,'starting at time',self.serviceTime)
			self.status = 1							#the customer is now being served
			self.departureTime =  self.serviceTime + self.serviceTimeLength
			self.cashierNo = cashierNo if not cashierNo == 'passed' else self.cashierNo
			return 1
		return 0
	def depart(self,simulTime,simType='non-SM'):
		if self.status == 1:
			if simulTime == self.serviceTime + self.serviceTimeLength:		#checks if the customer is done
				self.status = -1						#the customer has now departed
				print(self.name,'departed Cashier #',self.cashierNo+1 if simType =='non-SM' or self.type == 'basket' else self.cashierNo+2)
		return self.status
	def waitingtime(self):								#computes how many time units the customer waited before being served
		self.waitingTime = self.serviceTime - self.arrivalTime
		print(self.name,'waited',self.waitingTime,'time units')
		return self.waitingTime
	def cashieroccupied(self):								#for retrieving what cashier does the customer occupies
		return self.cashierNo
	def arrived(self,simulTime):							#for checking if the customer has arrived
		return False if simulTime < self.arrivalTime else True
	def arrival(self):									#for retrieving when the customer arrived
		return self.arrivalTime
	def returnstatus(self):								#for retrieving if the customer is waiting, being served, or departed
		return self.status

class Customer1to1(Customer):
	"""
		This class is inherited from the default Customer class and is used for additional details.
		This is used when the simulation type desired is the four line queue or the One Line to One Cashier Type of Simulation.
	"""
	queued = False
	def lineup(self,queue,cashKey):							#for lining up the customer in the specified Cashier Number
		self.queued = True
		self.queue=queue
		self.cashierNo = cashKey
		print(self.name,'lining up in Cashier #',self.cashierNo+1)
	def returnqueue(self):								#for retrieving the whole queue where the customer is lined up
		return self.queue
	def isqueued(self):									#for checking if the customer is already lined up/queued
		return True if self.queued else False

class Cashier:
	"""
		This class is the default Cashier class
		This is used when the simulation type desired is the single line queue or the One Line to All Cashiers Type of Simulation.
	"""
	def __init__(self,name):								
		self.queue = []                         
		self.name = name
		self.cashierSpeed = 1
	#def __str__(self):
	#	return self.name
	def __len__(self):									#checking how many are queued in the the cashiers
		return len(self.queue)  
	def __add__(self,other):
		return self.name+other
	def close(self,customerKey):							#specific for the One to All simulation type where the cashier only takes one customer in its queue at a time
		self.queue.append(customerKey)						#closes when the cashier already has a customer lined up.
	def open(self):									#also specific for the One to All simulation type
		self.queue = []								#resets the queue, making the cashier open for another customer
	def isvacant(self):									#for checking if the cashier has no customer in hand
		return True if not self.queue else False
	def returnqueue(self):								#for retrieving the cashier's queue 
		return self.queue

class Cashier1to1(Cashier):
	"""
		This class is inherited from the default Cashier class and is used for additional details.
		This is used when the simulation type desired is the four line queue or the One Line to One Cashier Type of Simulation.\
		Since this Cashier type can hold many customers in one queue, remove and add cust is purely for updating the queues.
	"""
	def removecust(self,customer):							
		self.queue.remove(customer)
	def addcust(self,customer):
		self.queue.append(customer)
