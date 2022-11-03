# Author: Semi Hong
# Quantcast coding assessment: most active coookie

import sys

# check command line inputs & verify
def checkInput():
    try:
        fileName = sys.argv[1]
        parameter = sys.argv[2]
        timeStamp = sys.argv[3]
    except IndexError:
        return

    # check if valid file name: ends with ".csv"
    if fileName[-4:] != ".csv":
        print("please input valid csv file")
        return None, None

    # check if valid parameter: should be -d
    if parameter != "-d":
        print("Please input valid parameter")
        return None, None

    # check if valid time stamp: should be YYYY-MM-DD format
    if len(timeStamp) != 10: 
        print("Please input valid timestamp in YYYY-MM-DD format")
        return None, None

    # check if valid time stamp: year, month, date should be in number
    if (not timeStamp[:4].isnumeric()) or (not timeStamp[5:7].isnumeric()) or (not timeStamp[8:].isnumeric()):
        print("Please input the numbers for year, month, and day")
        return None, None
    
    # check if valid time stamp: year, month, date should be divided by -
    if (timeStamp[4] != "-") or (timeStamp[7] != "-"):
        print("Please divide year, month, and day with -")
        
        return None, None
    
    return fileName, timeStamp

# reads csv file and organize cookie into cookies list and date into dates list
    # parameter: file name 
    # return: list of cookies and list of dates
def readFile(filepath):
    cookies = []
    dates = []

    try: 
        with open(filepath) as file: 
            file.readline() # header
            for line in file: 
                item = line.strip().split(",")

                cookie = item[0]
                timeStamp = item[1][:10]

                cookies.append(cookie)
                dates.append(timeStamp)
    except FileNotFoundError: 
        print("{} could not be found".format(filepath))
        exit(1) 

    return cookies, dates


# remove - from the date
    # parameter: date in format YYYY-MM-DD
    # return: date in format YYYYMMDD
def cleanDate(date):
    date = date[:4] + date[5:7] + date[8:]
    return date

# find the target date from the dates list   
# Parameters
    # dates: list of dates to check
    # targetDate: target date to look for
    # leftBias: boolean that tells whether to search left-most or right-most index of the target date position
        # if True, search left-most; else, search right-most
# Return
    # current index of target date 
    # returns -1 if not found
def binarySearch(dates, targetDate, leftBias):
    # indices
    left, right  = 0, len(dates) - 1
    curr = -1

    targetDate = cleanDate(targetDate) 

    while left <= right: 
        mid  = (left + right) // 2
        currDate = cleanDate(dates[mid])

        if targetDate > currDate:
            right = mid - 1
        elif targetDate < currDate:
            left = mid + 1
        else: 
            curr = mid

            if leftBias:
                right = mid - 1
            else: 
                left = mid + 1  
    return curr
        
# get the entire range of the date
    # parameter: list of dates to check, target date to find
    # return the tuple of indices: start and end of the range
def getRange(dates, targetDate):
    # start index of range
    left = binarySearch(dates, targetDate, True)

    # end index of range
    right = binarySearch(dates, targetDate, False)

    return left, right

# check the cookies list and find the most active cookie(s)

def mostActive(cookies, start, end):
    # dictionary to count the frequency
    cookieDict = {}
    # list to store most active cookie(s)
    mostActive = []
    # frequency of most active cookie
    maximum = 1
    for i in range(start, end+1):
        cookie = cookies[i]
        if cookie in cookieDict:
            cookieDict[cookie] += 1
        else:
            cookieDict[cookie] = 1

        # check if most active
        if cookieDict[cookie] > maximum: 
            maximum = cookieDict[cookie]
            mostActive = cookie
        elif cookieDict[cookie] == maximum:
            mostActive.append(cookie)

    print(mostActive)
    return mostActive
    
def main(): 
    fileName, timeStamp = checkInput()

    # if None for either fileName or timeStamp: invalid input, return 
    if (fileName is None) or (timeStamp is None):
        return 

    # read file to get the lists of cookies and dates
    cookies, dates = readFile(fileName) 

    # using dates, get the range of the indices of the target dates
    start, end = getRange(dates, timeStamp)

    if (start == -1) or (end == -1):
        print("No Cookie Used") 
        return
    
    mostActiveCookie = mostActive(cookies, start, end)
    if mostActiveCookie:
        for cookie in mostActiveCookie: 
            print(cookie)
    else: 
        print("No Cookie Used")

if __name__ == '__main__':
	main()
