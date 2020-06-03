#THIS CODE IS MY OWN WORK, IT WAS WRITTEN WITHOUT CONSULTING

#A TUTOR OR CODE WRITTEN BY OTHER STUDENTS - GABRIEL KIM

import sys
import random
import numpy as np

def writeFunction(coefficient, sseVal, inputF, outputFile, k,inputname):
	f = open(outputFile, "w+")
	for l in inputF: 
		f.write(str(l[1])+ "\n")

	f.write(str("SSE Value on data points: ") + str(sseVal[0]) + "\t" + "SSE Value on clusters: "+ str(sseVal[1]) + "\n" +"Silhouette Coefficient: " + str(coefficient))
	f.close()
	print("__________________________")
	print("\n")
	print("Output created")
	
	print("\n")
	print("____Review for the input___")
	print("K Value entered (number of clusters): " + k)
	print("Input file name entered: " + inputname)
	print("\n")
	print("____Review for the data____")
	print("Squared Sum Errorss on Clutsers: " + str(sseVal[1]))
	print("Squared Sum Errors on Datapoints within Clusters: " + str(sseVal[0]))
	print("Silhouette Coefficient: " + str(coefficient))


def euc_distance (a1,a2):  #function for euc_distance calculation
	t =[]
	v = 0.0
	

	len1 = len(a1)
	len2 = len(a2)
	for a in range(len1):
		v = a1[a] - a2[a]
		v = v**2
		t.append(v)
	sumV = sum(t)
	sumV = sumV ** 1/2
	return(sumV)


def kmeans (inputFile, k, outputFile):   #beginning of kmeans 
	temp = []
	initCluster = []
	maxandmin = []
	cluster = []
	attributeLen = 0
	finalCluster = []

	dataset = []
	kval = int(k)
	
	with open(inputFile) as data:   #preprocess the data
		row = data.readlines()
		for each in row: 
			e = each.split('\n')
			temp = []
			elements = e[0].split(",")   #seprate data by indicator
			length = len(elements)

			for x in range(length-1): 
				value = float(elements[x])
				temp22 = [value]
				if len(temp22) == 1:
					temp.append(float(value))
			dataset.append(temp)
		dataset.pop(len(dataset)-1)
		attributeLen = len(dataset[0])

	for each in dataset:   # check if any data points are broken
		p = 0
		p_ = []
		for a in range(attributeLen):
			if each[a] is not None: 
				p_.append(each[a])
			else: 
				p=1 
			if p == 0: 
				temp.append(p_)
	
	for a in range(attributeLen):
		tmp = []
		maxval = 0
		minval = 0
		for each in dataset: 
			if each[a] is not None: 
				tmp.append(each[a])
		
		maxval = max(tmp)
		minval = min(tmp)
		maxandmin.append([maxval, minval])  #calculate the max min for random varialbe 
		# maxandmin.append([std, avg])

	for p in range(kval):
		clusterTemp = []
		for p_ in range(attributeLen):
			
			clusterVal = random.uniform(maxandmin[p_][0], maxandmin[p_][1])
			# clusterVal = random.gauss(maxandmin[p_][1], maxandmin[p_][0]).  # option for gauss random variable 
			clusterTemp.append(clusterVal)

		initCluster.append(clusterTemp)
	
	
	if len(cluster)== 0: 
		cluster1 = []
		for g in initCluster:
			cluster.append(g)
	oldcluster = []

	difference = 1.0
	counter = 0
	iteration = 0

	while cluster != oldcluster:    #iterate untill the cluster doesnot change 
	# while counter != 4 or iteration < 1111:
		list1 = []
		for element in dataset: 
			temp0 =[]
			point = []
			for x in cluster: 
				d = euc_distance(element, x)
				temp0.append(d)
				minvalue = min(temp0)
				if minvalue == d: 
					point = x
			list1.append([element,point])
		oldcluster = cluster 
		cluster = []
		for clu in oldcluster: 
			clutemp = []
			for b in range(attributeLen):
				sumvalue = 0.000000000  #incorporates float 
				length = 0.000000
				for element in list1: 
					if element[1] == clu: 
						sumvalue = sumvalue + element[0][b]
						
						length += 1
				if length == 0: 
					length = 1
				newval = sumvalue / length 
				
				clutemp.append(newval)
			cluster.append(clutemp)
		sumdif = []
		counter = 0
			
		for x in range(kval):

			counter0 = 0
			for y in range(attributeLen):
				p = oldcluster[x][y] - cluster[x][y]  #calculates the difference between old and new cluster
				p = abs((p))
				if p == 0.0001:
					counter0+=1
			if counter0 == 4: 
				counter += 1

		iteration+= 1 
		if iteration == 1000000:  #safe system in case loop gets stuck in infinite loop 

			counter = 4

		difference = sum(sumdif)
		
	sortedList = sorting(cluster,list1,outputFile)
	silouetteCoef = silouette_Calculation(list1,cluster,sortedList)
	resultValue = sseCalculation(sortedList,kval, attributeLen)
	writeFunction(silouetteCoef, resultValue, sortedList,outputFile,k,inputFile)
	
	

	
def sorting(cluster, inputVal,output):   #replaces the complex clusters into easily readable integer cluster label 
	
	result = []
	for each in inputVal:  
		numbering = 0
		for a in cluster: 
			tem = []
			if each[1] == a: 
				tem.append(each[0])
				tem.append(numbering)		
				result.append(tem)
			numbering += 1
	
	return(result)
def silouette_Calculation(inputList, cluster,sortedL):   #silhouette calcuation function 
	
	sil = []
	atLen = len(cluster)

	for each in sortedL: #data points that will compare
		temp3 = []
		eachCluster = []
		length = 0
		sameCluster = []
		differentCluster = []

		for each2 in sortedL:   #loops 
			for a in range(atLen): 
				result = []
				if each[1] == a:
					length = 0
					if each2[1] == each[1] and each != each2: 
						dist = euc_distance(each[0], each2[0])
						sameCluster.append(dist)
					elif each != each2: 
						dist_dif = euc_distance(each[0], each2[0])
						differentCluster.append([dist_dif,each2[1]])

		sumSC = sum(sameCluster)	
		a1 = sumSC/len(sameCluster)				
		diff=[]
		for each_ in range(atLen): # 2 clusters 
			t_0 = []
			temp4 = []
			length = 0.0				
			for x in differentCluster:
				if x[1] == each_: #filters out 
					temp4.append(float(x[0]))    #adds one cluster in an array / adds the distance 
					length += 1									
			sumD = 0.0					
			sumD = sum(temp4)
			# length = len(temp4)
			if length == 0: 
				length = 1
			differentAvg = sumD / length    # avg euc distance 		
			diff.append(differentAvg)				
		b1 = max(diff)
		silouette = 0.0			
		parts = 0.0
		if a1 == b1: 
			silouette = 0.0 			
		elif b1 > a1: 			
			parts = a1/b1
			silouette = abs(1.0-parts)			
		elif a1 > b1: 
			parts = b1/a1 
			silouette = abs(1.0-parts)		
		sil.append(silouette)				
	silSum = sum(sil)
	silLength = len(sil)
	silAvg = silSum/silLength
	
	
	return(silAvg)

def sseCalculation(inputList, k, attribute): #sse calcaution
	result = []
	average = []
	for a in range(k):
		indexStrg = []
		index = 0
		for x in range(attribute):  #divide by attributes 
			strg = []
			for each in inputList:
				if a == each[1] and index == x:
					strg.append(each[0][index])
			
			sumin = sum(strg)
			length = len(strg)
			if length == 0:
				length = 1
			sumAvgi = sumin/length
			indexStrg.append(sumAvgi)
			index += 1
		average.append([indexStrg,a])
	resultVal = 0.0
	count = 0
	for eachavg in average: #[averages],clutsernumber 
		for each in inputList: 
			if eachavg[1] == each[1]:
				for x in range(attribute):
					differ = each[0][x] - eachavg[0][x]
					differ = differ ** 2 
					result.append(differ)
					resultVal = resultVal + differ 
					count += 1
	resulta = sum(result)


	difavg = []

	for each in inputList: 
		difavg.append(each[1])
	dfav = sum(difavg)
	difaa = dfav / len(difavg)
	tm6 = []

	for each in inputList: 
		calc = each[1] - difaa
		calc = calc**2 
		tm6.append(calc)
	resultb = sum(tm6)


	realResult = []
	realResult.append(resulta)
	realResult.append(resultb)
	return(realResult)



if __name__ == "__main__": #main method 
    
    kmeans(sys.argv[1],sys.argv[2],sys.argv[3])



