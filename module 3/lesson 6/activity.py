import random
import time

def getRandomDate(startDate,endDate ):
    print(f"Printing random date between {startDate} and {endDate}: ")
    randomGenerator = random.random()
    dateFormat = '%d/%m/%y'

    startTime = time.mktime(time.strptime(startDate , dateFormat))
    endTime = time.mktime(time.strptime(endDate, dateFormat))

    randomTime = startTime + randomGenerator * (endTime - startTime)
    randonDate = time.strftime(dateFormat, time.localtime(randomTime))
    return randonDate
print ("Random date = ", getRandomDate("1/1/2024", "12/12/2026"))