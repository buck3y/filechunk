'''
WK-4 SCRIPT
April 15, 2026
Version 1.3
'''
'''
Processes a large file in chunks while using a regular expression to find
URL patterns. After the script processes the large file, it outputs the results 
into a pretty table, with the option of saving the output to an .html file.'''

''' IMPORT STANDARD LIBRARIES '''
import sys       # Python system library
import os        # Python os library
import re        # Python regular expression Library
import time      # Python time library

''' IMPORT 3RD PARTY LIBRARIES '''
from prettytable import PrettyTable
from pathlib import Path

''' DEFINE PSEUDO CONSTANTS '''
CHUNKSIZE = 65535
tbl = PrettyTable(["Occurrences", "URLS"])
tbl.title = "Sorted URL Results"
urlDict = {}

''' LOCAL FUNCTIONS '''
def ChunkFile(largeFile):
    ''' Seperates large file into chunks of 65535 bytes'''
    try:     
        with open(largeFile, 'rb') as targetFile:
            print("Processing file...\n")
            while True:
                fileChunk = targetFile.read(CHUNKSIZE)
                if fileChunk:  # if we still have data
                    urlRegex(fileChunk)
                else:
                    PrettyTable(tbl)
                    break
    except Exception as err:
        sys.exit("\nException: " + str(err) + " Script Aborted")

def urlRegex(chunk):
    '''Searches file chunks for URL patterns using a Regular Expression (Regex)'''
    urlRegex = re.compile(b'\w+:\/\/[\w@][\w.:@]+\/?[\w\.?=%&=\-@/$,]*')
    urlMatches = urlRegex.findall(chunk)
    for eachURL in urlMatches:
        try:
            # obtain the value if key exists and increment
            urlDict[eachURL] = urlDict.get(eachURL, 0) + 1
        except Exception:
            urlDict[eachURL] = 1     

def PrettyTable(table):
    '''Formats regular expression 
       results into a pretty table,
       with option of saing output
       to an .html file'''
    print("Generating Sorted Result Table")
    # For loop for formatting
    for url, urlCnt in urlDict.items():
        url = url.decode("utf-8")
        tbl.add_row([urlCnt, url])
    # Format output into pretty table
    tbl.align = 'l'
    print(tbl.get_string(sortby="Occurrences", reversesort=True))
    # HTML output function
    while True:
        saveFile = input("Would you like to save this output as an html file? \n (y)es or (n)o >>> ")
        if saveFile == 'y':       
            now = time.time()
            timeString = time.strftime("%Y-%m-%d-%H-%M-%S", time.gmtime(now))
            htmlFileName = "WK-4-" + timeString + ".html"
            print("\nSaving results as an html file...") 
            outputPath = os.path.dirname(os.path.abspath(sys.argv[0]))            
            # Use the table passed as an argument
            htmlToSave = table.get_html_string(sortby="Occurrences", reversesort=True)  
            with Path(htmlFileName).open(mode="w", encoding="utf-8") as fp:
                fp.write(htmlToSave)
                print(f"\nSaving html file to {outputPath} as {htmlFileName}")                
            break
        elif saveFile == 'n':
            break
        else:
            print("Invalid Reponse. Type 'y' for yes or 'n' for no")
            continue
def Main():
    '''Main function, calls all necessary functions.'''
    while True:
        largeFile = input("Enter the name of a large File i.e d:/WK4/mem.raw >>> ")
        print("")
        if os.path.isfile(largeFile):
            ChunkFile(largeFile)
            break
        else:
            print("Invalid file specified.")
            continue
    
    input("\nFile Processed ... Press any key to exit the scipt >>> ")    
''' MAIN ENTRY POINT '''
if __name__ == '__main__':
    Main()
