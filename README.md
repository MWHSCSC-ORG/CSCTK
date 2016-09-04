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
This modle uses the Metasploit framework built into Kali-Linux to create and Android APK that will allow a back door into the users phone. The script creates the malicious APK file and embeds it into a normal, unsuspisious APK that whe opened, will automatically trigger a perl script to create a persistant backdoor into the users phone. This can be done in two ways, over your local area network (LAN), or you can open a port for the data to be sent to and listen on the local binding for the data coming in. These options can be specified during the process of the script creating the APK. Here's a list of sample command you could use once you connect to the victims phone:
1. blah
2. blah
3. blah
4. blah
5. blah

##DNS Spoofing
This was intended with the idea in mind to make it as simple as possible to spoof a url quickly and easily. Give it a domain to change to your local IP Adress and it will edit the needed files in your system and fire upa cloned verion of the page on your network that connects back to you. It's as easy as that!

##Slowloris
This toolkit integrates the Slowloris program created by [Robert Hansen](ha.ckers.org/slowloris/) and is a low bandwith DoS attack that eats networks for breakfeast. You simply specify to go through HTTPS or HTTPS, feed the module an IP and a number of threads and it will get to work.

##Cracking Wifi
A tool created by [Aaron Vigal](https://www.github.com/AaronVigal) to brute force the password for any Wifi Network. This tool works by finding the MAC Address of the networks router and sending it deauthentication packets, and sniffing the network for the devices to reconnect. Once the program has intercepted the hand shake then it will start hashing passwords from a chosen wordlist and comparing it to the handshakes hash. This uses a combonation of tools from the [aircrack-ng](https://www.aircrack-ng.org/) suite and would not be possible without it.

##Social Engineering Toolkit
This module was created by [Thomas Gerot](https://www.github.com/tjgerot) with the intention to scrape common social media outlets and gather information about a given user.

##CSCipher
This tool was designed to help crack encryped CTF passwords to obtain a flag. You give the module an encryped string of text via a .txt file or straight through the interface and it will run a variety of analysises and test to determine what kind of cipher it was encryped with, and return the decoded message.

___

Millard West, its Affiliates and all of this projects Contributers in no way promote or encourage un-lawful hacking and this toolkit should be rightfully used for it's purpost for penetration testing on your own network or any etwork that you have explicit concent from the Administrator. Millard West or any Contributers can and will not be held for any damage or unlawful action that may occur while using this toolkit. 

Happy Hacking!
