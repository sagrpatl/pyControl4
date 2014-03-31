'''
Author: sapatel91
Date: March 30, 2014
File: TestSendSOAP.py

Purpose: Send SOAP Commands to C4

Disclaimer: USE AT YOUR RISK, I TAKE NO RESPONSIBILITY
            Most likely there won't be any though
'''

from Modules.PyControl4 import *

# Establish Connection
# NOTE: IP Address will be different for your system
C4SoapConn('192.168.1.10', 5020)

# Pulse Volume Down in Family Room
Message = '<c4soap name="SendToDeviceAsync" async="1" seq="1615"><param name="iddevice" type="number">10</param><param name="data" type="string"><devicecommand><command>PULSE_VOL_DOWN</command><params></params></devicecommand></param></c4soap>'
C4SoapConn.Send(Message)