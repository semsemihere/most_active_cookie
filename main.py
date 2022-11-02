# import argparse
import sys

# reads csv file and store in dictionary as {timestamp : cookie}
    # parameter: file name 
    # return: dictionary of data
def readFile(filepath):
    data = {} 
    try: 
        with open(filepath) as file: 
            file.readline() 
            for line in file: 
                item = line.strip().split(",")
                cookie = item[0]
                timestamp = item[1][:10]

                # check if the date is already in the dictionary
                if timestamp in data:
                    data.get(timestamp).append(cookie)
                else:
                    data[timestamp] = [cookie]
            
    except FileNotFoundError: 
        print("{} could not be found".format(filepath))

    return data

# gets most active cookie(s) of the day
    # parameter: cookies used on the day
    # return: list of most active cookies
def mostActive(cookies):
    cookieDict = {}
    mostActive = []

    # get the count 
    for cookie in cookies:
        if cookie in cookieDict:
            cookieDict[cookie] += 1
        else:
            cookieDict[cookie] = 1
        
    # find the most active cookies
    for key, value in cookieDict.items(): 
        if value == max(cookieDict.values()):
            mostActive.append(key)
    
    return mostActive

# check command line inputs & verify
    # return: tuple of file name and timestamp
def checkInput():
    try:
        fileName = sys.argv[1]
        parameter = sys.argv[2]
        timeStamp = sys.argv[3]

    except IndexError:
        exit(1)

    # check if valid file name: ends with ".csv"
    if (len(fileName) <= 4) or (fileName[-4:] != ".csv"):
        print("Please input valid csv file")
        return None, None

    # check if valid parameter: should be -d
    if parameter != "-d":
        print("Please input valid parameter")
        return None, None

    # check if valid time stamp: should be YYYY-MM-DD format
    if len(timeStamp) != 10: 
        print("Please input timestamp in YYYY-MM-DD format")
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
    

def main(): 
    fileName, timeStamp = checkInput()

    # if None for either fileName or timeStamp: invalid input, return 
    if (fileName is None) or (timeStamp is None):
        return 

    cookieData = readFile(fileName)

    if cookieData: 
        if timeStamp in cookieData: 
            mostActiveCookie = mostActive(cookieData[timeStamp])
            for cookie in mostActiveCookie: 
                print(cookie)
        else:
            print("No Cookie Used")
    
if __name__ == '__main__':
	main()
