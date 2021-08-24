from datetime import datetime

inputData = []
inventory = {}
orderList = []
orderIdList = []
orderTimeList = []
orderGroupTimeList = []
orderResultTimeList = []

with open('input.txt') as file:
	for temp in file:
		inputData.append(temp.strip())

## logic: first input, first process
# get first line for restaurant id, capacity for each
inputList = inputData[0].split(',')

# restaurant id
res_id = inputList[0]

# capacity for restaurant
cooking = int(inputList[1][0])
cooking_time = int(inputList[2]) * 60
assembly = int(inputList[3][0])
assembly_time = int(inputList[4]) * 60
package = int(inputList[5][0])
package_time = int(inputList[6]) * 60

# inventory orders for each materials

inventory['C'] = int(inputList[7])
inventory['L'] = int(inputList[8])
inventory['T'] = int(inputList[9])
inventory['V'] = int(inputList[10])
inventory['B'] = int(inputList[11])

# create list for each order with order_id, order_name, time
for i in range(1, len(inputData)):
	temp = inputData[i].split(',')
	orderGroupTimeList.append([temp[2], datetime.strptime(temp[1], "%Y-%m-%d %H:%M:%S").timestamp()])
	orderIdList.append(temp[2])
	for j in range(3, len(temp)):
		seconds = datetime.strptime(temp[1], "%Y-%m-%d %H:%M:%S").timestamp()
		tempList = [temp[2], temp[j], seconds]
		orderList.append(tempList)

# return time for sorting
def sortByTime(element):
	return element[2]

# sort by time
orderList.sort(key=sortByTime)
# print(orderList)
# print(orderGroupTimeList)

## cooking for all orders
# initialize end cooking time for each order
cTime = [0,0,0,0]

# get end cooking time for each order
for i in range(int(len(orderList) / cooking) + 1):
	# initially
	if i == 0:
		# capacity of cooking, cooking time
		for j in range(cooking):
			# get end cooking time
			cTime[j] = orderList[i*cooking+j][2] + cooking_time
			# save end cooking time for each order
			orderList[i*cooking+j][2] += cooking_time
			# reduce inventory
			for k in range(len(orderList[i*cooking+j][1])):
				inventory[orderList[i*cooking+j][1][k]] -= 1
			if 'V' not in orderList[i*cooking+j][1]:
				inventory['C'] -= 1
	# finally
	elif i == int(len(orderList) / cooking):
		# capacity is 4
		for j in range(len(orderList) % cooking):
			if orderList[i*cooking+j][2] > cTime[j]:
				cTime[j] = orderList[i*cooking+j][2] + cooking_time
				orderList[i*cooking+j][2] += cooking_time
				# reduce inventory
				for k in range(len(orderList[i*cooking+j][1])):
					inventory[orderList[i*cooking+j][1][k]] -= 1
				if 'V' not in orderList[i*cooking+j][1]:
					inventory['C'] -= 1
			else:
				# save end cooking time for each order
				orderList[i*cooking+j][2] = cooking_time + cTime[j]
				# get end cooking time
				cTime[j] = cooking_time + cTime[j]
				# reduce inventory
				for k in range(len(orderList[i*cooking+j][1])):
					inventory[orderList[i*cooking+j][1][k]] -= 1
				if 'V' not in orderList[i*cooking+j][1]:
					inventory['C'] -= 1
	else:
		# capacity is 4
		for j in range(cooking):
			if orderList[i*cooking+j][2] > cTime[j]:
				cTime[j] = orderList[i*cooking+j][2] + cooking_time
				orderList[i*cooking+j][2] += cooking_time
				# reduce inventory
				for k in range(len(orderList[i*cooking+j][1])):
					inventory[orderList[i*cooking+j][1][k]] -= 1
				if 'V' not in orderList[i*cooking+j][1]:
					inventory['C'] -= 1					
			else:
				# save end cooking time for each order
				orderList[i*cooking+j][2] = cooking_time + cTime[j]
				# get end cooking time
				cTime[j] = cooking_time + cTime[j]
				# reduce inventory
				for k in range(len(orderList[i*cooking+j][1])):
					inventory[orderList[i*cooking+j][1][k]] -= 1
				if 'V' not in orderList[i*cooking+j][1]:
					inventory['C'] -= 1

aTime = [0,0,0,0]
# get end assembly time for each order
for i in range(int(len(orderList) / assembly) + 1):
	# initially
	if i == 0:
		# capacity of assembly, assembly time
		for j in range(assembly):
			# get end assembly time
			aTime[j] = orderList[i*assembly+j][2] + assembly_time
			# save end assembly time for each order
			orderList[i*assembly+j][2] += assembly_time
	# finally
	elif i == int(len(orderList) / assembly):
		# capacity is 4
		for j in range(len(orderList) % assembly):
			if orderList[i*assembly+j][2] > aTime[j]:
				aTime[j] = orderList[i*assembly+j][2] + assembly_time
				orderList[i*assembly+j][2] += assembly_time
			else:
				# save end assembly time for each order
				orderList[i*assembly+j][2] = assembly_time + aTime[j]
				# get end assembly time
				aTime[j] = assembly_time + aTime[j]
	else:
		# capacity is 4
		for j in range(assembly):
			if orderList[i*assembly+j][2] > aTime[j]:
				aTime[j] = orderList[i*assembly+j][2] + assembly_time
				orderList[i*assembly+j][2] += assembly_time
			else:
				# save end assembly time for each order
				orderList[i*assembly+j][2] = assembly_time + aTime[j]
				# get end assembly time
				aTime[j] = assembly_time + aTime[j]

pTime = [0,0,0,0]
# get end package time for each order
for i in range(int(len(orderList) / package) + 1):
	# initially
	if i == 0:
		# capacity of package, package time
		for j in range(package):
			# get end package time
			pTime[j] = orderList[i*package+j][2] + package_time
			# save end package time for each order
			orderList[i*package+j][2] += package_time
	# finally
	elif i == int(len(orderList) / package):
		# capacity is 4
		for j in range(len(orderList) % package):
			if orderList[i*package+j][2] > pTime[j]:
				pTime[j] = orderList[i*package+j][2] + package_time
				orderList[i*package+j][2] += package_time
			else:
				# save end package time for each order
				orderList[i*package+j][2] = package_time + pTime[j]
				# get end package time
				pTime[j] = package_time + pTime[j]
	else:
		# capacity is 4
		for j in range(package):
			if orderList[i*package+j][2] > pTime[j]:
				pTime[j] = orderList[i*package+j][2] + package_time
				orderList[i*package+j][2] += package_time
			else:
				# save end package time for each order
				orderList[i*package+j][2] = package_time + pTime[j]
				# get end package time
				pTime[j] = package_time + pTime[j]

# print(orderList)
# print(orderIdList)

# get whole processing time for each order
for i in range(len(orderIdList)):
	tempList = []
	for j in range(len(orderList)):
		if orderIdList[i] == orderList[j][0]:
			tempList.append(orderList[j][2])
	if((max(tempList) - orderGroupTimeList[i][1]) % 60 == 0):
		orderTimeList.append(int((max(tempList) - orderGroupTimeList[i][1]) / 60))
	else:	
		orderTimeList.append(int((max(tempList) - orderGroupTimeList[i][1]) / 60) + 1)

# print for each order
for i in range(len(orderTimeList)):
	if orderTimeList[i] < 20:
		print(res_id + ',' + orderGroupTimeList[i][0] + ',ACCEPTED,' + str(orderTimeList[i]))
	else:
		print(res_id + ',' + orderGroupTimeList[i][0] + ',REJECTED,' + str(orderTimeList[i]))

# get max time for whole processing
tempList = []
for i in range(len(orderList)):
	tempList.append(orderList[i][2])
maxTime = max(tempList)
# get processing time for whole processing
proccessingTime = int((maxTime - orderGroupTimeList[0][1]) / 60) + 1

# print whole processing time
print(res_id + ',Total,' + str(proccessingTime))

# print inventory
print(res_id + ',INVENTORY,' + str(inventory['C']) + ',' + str(inventory['L']) + ',' + str(inventory['T']) + ',' + str(inventory['V']) + ',' + str(inventory['B']))