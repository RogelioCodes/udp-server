from socket import *
import uuid
import sys

serverName = 'localhost'
serverPort = 12000
clientSocket = socket(AF_INET, SOCK_DGRAM)

def getMac():
       return
macAddress =(':'.join(['{:02x}'.format((uuid.getnode() >> ele) & 0xff) 
    for ele in range(0,8*6,8)][::-1]))


macAddress =(':'.join(['{:02x}'.format((uuid.getnode() >> ele) & 0xff) 
for ele in range(0,8*6,8)][::-1]))
print ("CLIENT: Your MAC address: " , macAddress)
message = input('Input a MAC address:')
macAddress = message

print("CLIENT: SENDING DISCOVER MESSAGE TO SERVER")
message = 'DISCOVER,' + macAddress 
clientSocket.sendto(message.encode(),(serverName, serverPort))
   
message, serverAddress = clientSocket.recvfrom(2048)
if 'OFFER' in message.decode():
       print("CLIENT: RECEIVED OFFER MESSAGE")
       msg_type, payload,ip = message.decode().split(' ')
       client_mac = payload
       ip = ip
       if client_mac == macAddress:
              print("CLIENT: SENDING REQUEST MESSAGE")
              print("CLIENT_MAC:",client_mac)
              print("CLIENT_IP:",ip)
              message = "REQUEST," + client_mac + "," + ip
              clientSocket.sendto(message.encode(),(serverName, serverPort))
       else:
              print("CLIENT: MAC ADDRESS DONT MATCH.\nTERMINATING PROGRAM")
              sys.exit()
       message, serverAddress = clientSocket.recvfrom(2048)
if 'ACK' in message.decode():
       print("CLIENT: RECEIVED ACK MESSAGE")
       msg_type, payload,ip = message.decode().split(' ')
       client_mac = payload
       ip = ip
       if client_mac == macAddress:
              print("CLIENT: GOT AN IP ADDRESS")
              print("CLIENT_MAC:",client_mac)
              print("CLIENT_IP:",ip)
       else:
              print("CLIENT: MAC ADDRESS DONT MATCH.\nTERMINATING PROGRAM")
              sys.exit() 
else:
       print(message.decode())
#MENU
choice = ''
while choice.upper != 'C':
    print ("----- MENU -----")
    print ("A. Release")
    print ("B. Renew")
    print ("C. Quit")
    choice = input("Choose an option: ")
    if 'SERVER' in message.decode():
        print(message.decode())
    
    if choice.upper() == "A":
        print("CLIENT: SENDING RELEASE MESSAGE")
        release = "RELEASE"
        clientSocket = socket(AF_INET, SOCK_DGRAM)
        clientSocket.sendto(release.encode(),(serverName, serverPort))
        message, serverAddress = clientSocket.recvfrom(2048)
        print(message.decode())
    if choice.upper() == "B":
        print("CLIENT: SENDING RENEW MESSAGE")
        renew = "RENEW"
        clientSocket = socket(AF_INET, SOCK_DGRAM)
        clientSocket.sendto(renew.encode(),(serverName, serverPort))
        message, serverAddress = clientSocket.recvfrom(2048)
        
        if 'OFFER' in message.decode():
               print("CLIENT: RECEIVED OFFER, SENDING REQUEST")
               print("CLIENT_MAC:",client_mac)
               print("CLIENT_IP:",ip)
               request = 'REQUEST,' + client_mac + "," + ip
               clientSocket = socket(AF_INET, SOCK_DGRAM)
               clientSocket.sendto(request.encode(),(serverName, serverPort))
               message, serverAddress = clientSocket.recvfrom(2048)
               if 'ACK' in message.decode():
                  print("CLIENT: RECEIVED ACK")
                  msg_type, payload,ip = message.decode().split(' ')
                  client_mac = payload
                  ip = ip
                  print("CLIENT_MAC:" ,client_mac)
                  print("CLIENT_IP:", ip)
        else:
               print("here:",message.decode())  
    if choice.upper() == "C":
        print("TERMINATING PROGRAM")
        sys.exit()
       
