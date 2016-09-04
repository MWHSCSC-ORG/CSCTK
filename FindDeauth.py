import subprocess, sys, os
# Start to find the BSSID of the network according to it's name
f = open('/usr/share/aaronstoolkit/DEAUTHOutput.txt', 'r+')
lines=f.readlines()
line = lines[2]
array = line.split(",")
deauth = array[5].replace(" ", "")
f.close()
g = open('/usr/share/aaronstoolkit/deauth.txt', 'w')
g.write(deauth)
