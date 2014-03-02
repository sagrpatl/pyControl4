'''
Author: sapatel91
Date: March 2, 2014
File: getControl4Items.py

Purpose: Prints ID and Name of various items from a Control4 system
'''

from bs4 import BeautifulSoup
import socket

# Insert the IP of your Control4 system here. Can be obtained from Composer.
TCP_IP = '192.168.1.10' # Will need to change for your system's IP
TCP_PORT = 5020
BUFFER_SIZE = 8192

# Function used to extract text between tags
# For example "<value> 43 </value>" returns 43
def getText(soupData,tag):
    tag = soupData.find(tag)
    try:
        text_parts = tag.findAll(text=True)
        text = ''.join(text_parts)
        return text.strip()
    except:
        return "Value not found!"

# Connect to Director and issue soap command to get all items on system.
directorConn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
directorConn.connect((TCP_IP,TCP_PORT))
MESSAGE = '<c4soap name="GetItems" async="False"><param name="filter" type="number">0</param></c4soap>'
directorConn.sendall(MESSAGE + "\0") # The null terminating character is VERY important to include
data = ""
out_string = ""
while not '</c4soap>' in data:
    data = directorConn.recv(BUFFER_SIZE)
    out_string += data
    if '</c4soap>' in data:
        break
soapData = BeautifulSoup(out_string.decode('ascii', 'ignore'))
directorConn.close()

# Parse SOAP data
items = soapData.findAll('item')
for item in items:
    '''
        Change the type value for the following:
            2 - Site
            3 - Building
            4 - Floor
            6 - Device Type
            7 - Device
            8 - Room
    '''
    if getText(item,"type") == "7":
            print "%s, %s" % (getText(item, "id"), getText(item, "name"))