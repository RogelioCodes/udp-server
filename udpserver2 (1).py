from socket import *
import uuid, struct
import ipaddress


def ipRange(start_ip, end_ip):
   start = list(map(int, start_ip.split(".")))
   end = list(map(int, end_ip.split(".")))
   temp = start
   ip_range = []
   
   ip_range.append(start_ip)
   while temp != end:
      start[3] += 1
      for i in (3, 2, 1):
         if temp[i] == 256:
            temp[i] = 0
            temp[i-1] += 1
      ip_range.append(".".join(map(str, temp)))    
      
   return ip_range
   
allIps=[]   
 #sample usage 
ip_range = ipRange("192.168.1.1", "192.168.1.254")
for ip in ip_range:
   allIps.append(ip)

#print (allIps)
client_mac_list = []
ip_address_pool= []
totalList = [client_mac_list,ip_address_pool]

counter = 0 

serverPort = 12000
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(('', serverPort))
print ('The server is ready to receive')

listCounter = 0

def get_ip_address():
   print("SERVER: GETTING IP")
   counter = len(ip_address_pool)
   ip_address_pool.append(allIps[counter])
   counter+=1
   return ip_address_pool[counter-1]
def findip(client_mac):
   x = 0
   for client_mac in client_mac_list:
      x+=1
      if client_mac in client_mac_list:
       print( "SERVER: FOUND MAC ADDRESS")
       return ip_address_pool[x-1]
      else:
       print("SERVER: DID NOT FIND MAC ADDRESS")


def recv_discover():
    if client_mac in client_mac_list:
        ip = findip(client_mac)
        sentMessage = "SERVER: " + ip + " has already been assigned to this client."
        serverSocket.sendto(sentMessage.encode(), clientAddress)
    else:
        client_mac_list.append(client_mac)
        if len(ip_address_pool) < 255:
            print("SENDING OFFER")
            client_ip = get_ip_address()
            print("CLIENT_MAC:",client_mac)
            print("CLIENT_IP:",client_ip)
            sentMessage = "OFFER " + client_mac  + " " + client_ip
            serverSocket.sendto(sentMessage.encode(), clientAddress)
        else:
            sentMessage = "DECLINE: Request declined. There is no available IP address."
            serverSocket.sendto(sentMessage.encode(), clientAddress)

while 1:
   message, clientAddress = serverSocket.recvfrom(2048)
   if 'DISCOVER' in message.decode():
      msg_type, payload = message.decode().split(',')
   if 'REQUEST' in message.decode():
      msg_type, payload,ip = message.decode().split(',')
   if 'RELEASE' in message.decode():
      msg_type = 'RELEASE'
   if 'RENEW' in message.decode():
      msg_type = 'RENEW' 
   if msg_type == 'DISCOVER':
       print("SERVER: RECEIVED DISCOVER MESSAGE")
       client_mac = payload
       recv_discover()
   if msg_type == 'REQUEST':
       print("SERVER: RECEIVED REQUEST MESSAGE")
       if ip in ip_address_pool:
          client_mac = payload
          client_ip = ip
       else:
          client_ip = get_ip_address()
       print("SERVER: SENDING ACK MESSAGE")
       print("CLIENT_MAC:",client_mac)
       print("CLIENT_IP:",client_ip)
       sentMessage = "ACK " + client_mac +" " + client_ip
       serverSocket.sendto(sentMessage.encode(), clientAddress)
   if msg_type == 'RELEASE':
       print("SERVER: RECEIVED RELEASE MESSAGE")
       if client_ip in ip_address_pool:
          print("SERVER: RELEASING IP")
          ip_address_pool.remove(client_ip)
          client_mac_list.remove(client_mac)
          sentMessage = "SERVER: REMOVED CLIENT MAC AND CORRESPONDING IP FROM DIRECTORY"
          serverSocket.sendto(sentMessage.encode(), clientAddress)
       else:
          print("SERVER: ALREADY REMOVED CLIENT MAC AND CORRESPONDING IP FROM DIRECTORY")
          sentMessage = "SERVER: ALREADY REMOVED CLIENT MAC AND CORRESPONDING IP FROM DIRECTORY"
          serverSocket.sendto(sentMessage.encode(), clientAddress)
   if msg_type == 'RENEW':
      print("SERVER: RECEIVED RENEW MESSAGE")
      if client_ip in ip_address_pool and client_mac in client_mac_list:
         sentMessage = "CLIENT: CLIENT ALREADY HAS IP AND THE IP IS " + client_ip
         serverSocket.sendto(sentMessage.encode(), clientAddress)
      else:
         client_mac_list.append(client_mac)
         if len(ip_address_pool) < 255:
            print("SENDING OFFER")
            client_ip = get_ip_address()
            print("CLIENT_MAC:",client_mac)
            print("CLIENT_IP:",client_ip)
            sentMessage = "OFFER " + client_mac  + " " + client_ip
            serverSocket.sendto(sentMessage.encode(), clientAddress)
         else:
            print("Request declined. There is no available IP address.")
            sentMessage = "Request declined. There is no available IP address."
            serverSocket.sendto(sentMessage.encode(), clientAddress)
         
   
       
