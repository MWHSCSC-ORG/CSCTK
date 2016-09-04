# CSCTK (Computer Science Club Toolkit)
A Kali-Linux Toolkit made by the Millard West Computer Science Club that includes the following projects:

1. [Metasploit](#metasploit)
2. [DNS Spoofing](#dns-spoofing) (Functional but in beta)
3. [Slowloris](#slowloris)
4. [Cracking WiFi networks](#rracking-wifi)
5. [Social Engineering Toolkit](#social-engineering-toolkit) (Formerly known "DATA")
6. [CSCipher](#cscipher) (In-Development)

This framework should run under most verions of Linux but is optimized for working on Kali.
The setup is very straight-forward just copy and paste the following code into a terminal:
```{r, engine='bash', count_lines}
wget https://raw.githubusercontent.com/MWHSCSC-ORG/CSCTK/master/setup&&sudo chmod +x setup&&sudo ./setup 
```
The setup file checks/installs the following dependencies:

1. Metasplot Framework
2. aircrack-ng
3. Python 2.7
4. More stuff I have yet to do

For a detailed description on how each module works check the secions below.

## General Layout:
Each individual menu contains multiple sub menus or options for customizibility on each individual module. The structure of this toolkit looks like this:
```
CSCTK
│   README.MD
│   LISENSE  
│
└───Metasploit
│   │   Create an APK
│   │   Use Existing APK
|   |   Exploit APK
│   └───
│   
└───DNS Spoofing
│   │   Use HTTP
│   │   Use HTTPS
│   └───
|
└───Wireless Attack
│   │   Use rockyou.txt
│   │   Use dnsmap.txt
|   |   Use custom wordlist
│   └───
│   
└───Slowloris
│   │   Use HTTP
│   │   Use HTTPS
│   └───
|
└───Social Engineering
│   │   Verbose Mode
│   │   Add Images To HTML Output
|   |   Check Against Every TLD
│   │   Open Links
│   │   Search Multiple Usernames
|   |   Search Douglas County Assessor
│   └───
│   
└───CSCipher
│   │   Enter ciphertext
│   │   Pull from text file
│   └───
└───

```

##Metasploit
text

##DNS Spoofing
text

##Slowloris
text

##Cracking Wifi
text

##Social Engineering-Toolkit
text

##CSCipher
text
