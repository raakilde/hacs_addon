import csv
import datetime
import re

class EwiiDataParser():
    def __init__(self, csvFile=None):
        self.__dateIndex=0
        self.__valueIndex=1
        self.__csvDelimitter=";"
        self.dataUnit="MWh"
        self.dateHeader='Dato'
        self.valueHeader='Værdi'
        self.csvFile=csvFile

    @staticmethod
    def __index_containing_substring(the_list, substring):
        for i, s in enumerate(the_list):
            if substring in s:
                return i
        return -1

    @property
    def csvFile(self):
        return self._csvFile

    @csvFile.setter
    def csvFile(self, value):
        self._csvFile = value
        file = open(self.csvFile)
        csvreader = csv.reader(file)      
        self.__csvDelimitter = next(csvreader)[0][-1] #The csv delimitter is expected to be at the first entry of the file
        csvreader = csv.reader(file, delimiter = self.__csvDelimitter)
        dataHeaders = next(csvreader) #The data headers are expected to be at the second entry of the file
        self.__dateIndex=self.__index_containing_substring(dataHeaders, self.dateHeader)
        self.__valueIndex=self.__index_containing_substring(list(dataHeaders), str(self.valueHeader))
        self.dataUnit=dataHeaders[self.__valueIndex][dataHeaders[self.__valueIndex].find('(')+1:dataHeaders[self.__valueIndex].find(')')]
        
        file.close()

    def getDataFromDate(self, requestedDate=""):
        data=[]
        requestedDate=datetime.datetime.strptime(requestedDate, '%Y-%m-%d').date()
        file = open(self.csvFile)
        csvreader = csv.reader(file, delimiter = self.__csvDelimitter)
        for row in reversed(list(csvreader)):
            # searching string
            match_str = re.search(r'\d{4}-\d{2}-\d{2}', row[self.__dateIndex])
            res = datetime.datetime.strptime(match_str.group(), '%Y-%m-%d').date()
            if(res==requestedDate):
                data.append({"date":row[self.__dateIndex], "value":row[self.__valueIndex], "unit":self.dataUnit})
            elif(res<requestedDate):
                break
        file.close()   
        return data

    def getDataFromToday(self):
        data=[]
        today = str(datetime.date.today())
        data=self.getDataFromDate(today)
        return data

    def getDataFromYesterday(self):
        data=[]
        today = datetime.date.today()
        yesterday = str(today - datetime.timedelta(days=1))
        data=self.getDataFromDate(yesterday) 
        return data

if __name__ == "__main__":
    parser = EwiiDataParser('66157990.csv')

    dataToday = parser.getDataFromToday()
    dataYesterday = parser.getDataFromYesterday()
    dataAtSomeData = parser.getDataFromDate("2022-02-23")

    print(dataToday)
    print(dataYesterday)