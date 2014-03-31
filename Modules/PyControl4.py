'''
Author: sapatel91
Date: March 29, 2014
File: Control4Lights.py

Purpose: Encapsulate Control4 Devices

Disclaimer: USE AT YOUR RISK, I TAKE NO RESPONSIBILITY
            Most likely there won't be any though
'''

import socket
from bs4 import BeautifulSoup

#Global variable used to share socket connection between classes
socketConn = 0
BUFFER_SIZE = 8192

class C4SoapConn:
    '''
    Establish connection to Control4 system
    Parameters: 
        TCP_IP - IP Address of system
        TCP_PORT - should be 5020
    '''
    def __init__(self, TCP_IP, TCP_PORT):
        global socketConn
        socketConn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socketConn.connect((TCP_IP, TCP_PORT))
    
    @staticmethod
    def Send(MESSAGE):
         socketConn.sendall(MESSAGE + "\0")

class C4Light:
    '''
    Instantiate light object with id
    Parameters: 
        id - device id
    '''
    def __init__(self, id):
        self.id = id
    
    '''
    Sets intensity of dimmer switch
    Parameters: 
        value - 0 to 100
    '''
    def setLevel(self,value):
        MESSAGE = '<c4soap name="SendToDeviceAsync" async="1"><param name="data" type="STRING"><devicecommand><command>SET_LEVEL</command><params><param><name>LEVEL</name><value type="INT"><static>%d</static></value></param></params></devicecommand></param><param name="idDevice" type="INT">%d</param></c4soap>' % (value, self.id)
        socketConn.sendall(MESSAGE + "\0")
    
    '''
    Ramps to a specified level in milliseconds
    Parameters:
        percent - Intensity
        time - Duration in milliseconds
    '''
    def rampToLevel(self,percent, time):
        MESSAGE = '<c4soap name="SendToDeviceAsync" async="1"><param name="data" type="STRING"><devicecommand><command>RAMP_TO_LEVEL</command><params><param><name>TIME</name><value type="INTEGER"><static>%d</static></value></param><param><name>LEVEL</name><value type="PERCENT"><static>%d</static></value></param></params></devicecommand></param><param name="idDevice" type="INT">%d</param></c4soap>' % (time, percent, self.id)
        socketConn.sendall(MESSAGE + "\0")
    
    '''
    Returns the light level for a dimmer. Value between 0 and 100.
    NOTE: will return an error if used on light switches use getLightState instead
    '''
    def getLevel(self):
        MESSAGE = '<c4soap name="GetVariable" async="False"><param name = "iddevice" type = "INT">%d</param><param name = "idvariable" type = "INT">1001</param></c4soap>' % (self.id)
        socketConn.sendall(MESSAGE + "\0")
        data = socketConn.recv(BUFFER_SIZE)
        data = BeautifulSoup(data)
        value = data.find("variable")
        value = value.findAll(text=True)
        value = ''.join(value)
        return value
    
    '''
    Returns the light state. Output is 0 or 1.
    '''
    def getLightState(self):
        MESSAGE = '<c4soap name="GetVariable" async="False"><param name = "iddevice" type = "INT">%d</param><param name = "idvariable" type = "INT">1000</param></c4soap>' % (self.id)
        socketConn.sendall(MESSAGE + "\0")
        data = socketConn.recv(BUFFER_SIZE)
        data = BeautifulSoup(data)
        value = data.find("variable")
        value = value.findAll(text=True)
        value = ''.join(value)
        return value
    
class C4Remote:
    def VolDown(self):
        MESSAGE = '<c4soap name="SendToDeviceAsync" async="1"><param name="iddevice" type="number">10</param><param name="data" type="string"><devicecommand><command>PULSE_VOL_DOWN</command><params></params></devicecommand></param></c4soap>'
        socketConn.sendall(MESSAGE + "\0")
        
    def VolUp(self):
        MESSAGE = '<c4soap name="SendToDeviceAsync" async="1"><param name="iddevice" type="number">10</param><param name="data" type="string"><devicecommand><command>PULSE_VOL_UP</command><params></params></devicecommand></param></c4soap>'
        socketConn.sendall(MESSAGE + "\0")
        
    def Info(self):
        MESSAGE = '<c4soap name="SendToDeviceAsync" async="1"><param name="iddevice" type="number">10</param><param name="data" type="string"><devicecommand><command>INFO</command><params></params></devicecommand></param></c4soap>'
        socketConn.sendall(MESSAGE + "\0")
        
    def Cancel(self):
        MESSAGE = '<c4soap name="SendToDeviceAsync" async="1"><param name="iddevice" type="number">10</param><param name="data" type="string"><devicecommand><command>CANCEL</command><params></params></devicecommand></param></c4soap>'
        socketConn.sendall(MESSAGE + "\0")
        