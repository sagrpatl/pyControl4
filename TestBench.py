from Modules.PyControl4 import *
import socket
import time

C4SoapConn('192.168.1.10', 5020)

livingRoom = C4Light(264)

livingRoom.setLevel(30)
time.sleep(2)
livingRoom.setLevel(0)

print "hello"
