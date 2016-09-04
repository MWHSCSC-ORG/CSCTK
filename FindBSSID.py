import subprocess, sys, os
# Get the name you entered in the bash script 
with open('/usr/share/csctk/name.txt', 'r') as myfile:
    name=myfile.read().replace('\n', '')
myfile.close()
# Start to find the BSSID of the network according to it's name
f = open('/usr/share/csctk/BSSIDOutput.txt', 'r+')
lines=f.readlines()
line = filter(lambda x: name in x, lines)
string = ' '.join(line)
array = string.split(",") 
bssid = array[0].replace(" ", "")
channel = array[3].replace(" ", "")
f.close()
g = open('/usr/share/csctk/bssid.txt', 'w')
g.write(bssid)
g.close()
h = open('/usr/share/csctk/channel.txt', 'w')
h.write(channel)
h.close()
