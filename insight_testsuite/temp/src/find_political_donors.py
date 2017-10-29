import time
import sys
import pandas as pd
import numpy as np
from numpy import median
'''
Function to extract required feilds CMTE_ID, ZIP_CODE etc. from each line
'''
def extract_values(line):
    line = line.split("|")
    ##3. Considering first 5 characters of zip code
    return line[0],line[10][:5],line[13],line[14],line[15]
'''
Class to store tracsaction amount, median for given zip code.
'''
class ZipObject(object):
    def __init__(self,totalAmount):
        self.medianAmount = list()
        self.medianAmount.append(totalAmount)
        self.zipCount = 1
        self.totalAmount = totalAmount
        
    def setCount(self):
        self.zipCount += 1
        
    def settotalAmount(self,amount):
        self.totalAmount += amount
        self.setCount()
        self.setmedianAmount(amount)
        
    def setmedianAmount(self,amount):
        self.medianAmount.append(amount)
        
    def getCount(self):
        return self.zipCount
    
    def gettotalAmount(self):
        return self.totalAmount
    
    def getmedianAmount(self):
        return int(round(median(self.medianAmount)))
'''
Fucntion to calculate median transaction amount based on zip code.
'''
def taskZipCode(inputFilePath,outputZipPath):
	d = dict()
	file = open(outputZipPath, "w")

	with open(inputFilePath) as f:
	    for line in f:
	        record = extract_values(line)
	        ## 1. Checking if other id is empty and 4.invalid zip code and 5.cmte and transaction amount is empty
	        if((len(record[-1]) == 0) and len(record[1]) > 4  and len(record[0]) != 0 and len(record[3])!=0):
	            if record[1] in d:
	                d[record[1]].settotalAmount(int(record[3]))
	                #print "{}|{}|{}|{}|{}".format(record[0],record[1],d[record[1]].getmedianAmount(),d[record[1]].getCount(),d[record[1]].gettotalAmount())
	                file.write("{}|{}|{}|{}|{} \n".format(record[0],record[1],d[record[1]].getmedianAmount(),d[record[1]].getCount(),d[record[1]].gettotalAmount()))
	                continue
	            else:
	                d[record[1]] = ZipObject(int(record[3]))
	            #print "{}|{}|{}|{}|{} \n".format(record[0],record[1],d[record[1]].getmedianAmount(),d[record[1]].getCount(),d[record[1]].gettotalAmount())
	         	file.write("{}|{}|{}|{}|{} \n".format(record[0],record[1],d[record[1]].getmedianAmount(),d[record[1]].getCount(),d[record[1]].gettotalAmount()))
	file.close() 

'''
Fucntion to calculate median transaction amount based on dates.
'''

def taskDate(inputFilePath,outputDatePath):
	colnames = ['CMTE_ID','ZIP','TRANSACTION_DT','TRANSACTION_AMT','OTHER_ID']
	with open(inputFilePath) as f:
		df = pd.DataFrame([extract_values(line) for line in f],columns=colnames)
	
	df = df.drop(['ZIP'],axis=1)
	## 5.checking if transaction amount is empty
	df = df[df['TRANSACTION_AMT'].str.len() != 0]
	df['TRANSACTION_AMT'] = df['TRANSACTION_AMT'].astype(int)

	## 1. Checking if other id is empty 
	df = df[df['OTHER_ID'].str.len() == 0]

	## 5. checking if cmte is empty
	df = df[df['CMTE_ID'].str.len() != 0 ]
	

	## 2. Checking if date is malformed 
	df = df[df['TRANSACTION_DT'].str.len() == 8]


	df = df.groupby(['CMTE_ID', 'TRANSACTION_DT']).TRANSACTION_AMT.agg([('medianamt','median'),('countamt','count'),('totalamt','sum')]).reset_index()
	df['medianamt'] = df['medianamt'].round().astype(int)

	df = df.sort_values(['CMTE_ID', 'TRANSACTION_DT'], ascending=[True,True])
	df.to_csv(outputDatePath,sep="|",index=False,header=None)

'''
Main function to call methods to calculate medians based on zipcode and date. 
'''		
def main():
	inputFilePath = "input/itcont.txt"
	outputZipPath = "output/medianvals_by_zip.txt"
	outputDatePath = "output/medianvals_by_date.txt"
	start = time.time()
	taskZipCode(inputFilePath,outputZipPath)
	stop = time.time()
	print "The time take to calculate median by Zip Code {} seconds".format(stop-start)

	start = time.time()
	taskDate(inputFilePath,outputDatePath)
	stop = time.time()
	print "The time take to calculate median by Date {} seconds".format(stop-start)

    


if __name__ =='__main__':
	main()
