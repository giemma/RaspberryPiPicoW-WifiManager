import os
import machine
import network
import socket
import time

import wifimanager.htmlmanager as htmlmanager
import wifimanager.credentialsutility as Credentials
import displaycolors as Colors
import wifimanager.requestutility as Req

version = '0.2 alpha'
ssid = 'PicoW2'
password = '12345678'

class WiFiManager():
    
    def __init__(self, display):
        self._display=display
        
        if Credentials.Founds():
            credentials = Credentials.Read()
            n_name=credentials[0]
            n_password=credentials[1]
            
            n_name=n_name.replace('\n','')
            n_password=n_password.replace('\n','')
            self._display.WriteLines(["Credentials","founds","", "Connecting..."], color=Colors.BLACK, background=Colors.GREEN)
            self._sub_connect_to_network(n_name,n_password)
        else:
            self._display.WriteLines(["Credentials","NOT","founds"], color=Colors.BLACK, background=Colors.RED)
            
            self._sub_start_portal()         

    def _sub_start_portal(self):
        html = htmlmanager.HTMLMANAGER('Titolo')
        htmlDropdownNetworks='<option></option>'
        
        wlan = network.WLAN()
        wlan.active(True)
        networks = wlan.scan()
        i=0
        networks.sort(key=lambda x:x[3],reverse=True) # sorted on RSSI (3)
        for w in networks:
            i+=1
            htmlDropdownNetworks+="<option value='" + w[0].decode() +"'>" + w[0].decode() +"</option>"
            print(i,w[0].decode())
        
        css = htmlmanager.GetCss()
        htmlMain = html.GetIndexPage('Wi-Fi Configuration', htmlDropdownNetworks)    
        htmlInfo = html.GetInfoPage('Info', version, os.uname().version, os.uname().machine )    
        htmlPasswordOk = html.GetPasswordOkPage('Password saved')    
        htmlShutdown = html.GetStoppedPage('Stopped')    
        htmlRestarting = html.GetRestartingPage('Restarting')
        
        ap = network.WLAN(network.AP_IF)
        ap.config(essid=ssid, password=password)
        ap.active(True)

        while ap.active() == False:
            pass

        print('Connection successful')
        status = ap.ifconfig()
        print(ap.ifconfig())
        
        addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
        s = socket.socket()
        s.bind(addr)
        s.listen(1)

        print('listening on', addr)        
        
        self._display.WriteLines(["Connect on", ssid +"." ,"Navigate on", str(status[0]), "Password:", "12345678" ], color=Colors.BLACK, background=Colors.YELLOW)
        
        # Listen for connections
        while True:
         
            try:
                cl, addr = s.accept()
                #print('client connected from', addr)            
                request = cl.recv(1024)
                print('----------- START RAW -----------')
                print(request)
                print('----------- END RAW -----------')
                requestString = request.decode('utf-8')
                
                if request.startswith('POST'):                              
                    n=Req.GetParameterValue(requestString,'txtnetwork=')                
                    p=Req.GetParameterValue(requestString,'txtpassword=')
                                    
                    Credentials.Save(n,p)
                    
                    cl.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
                    cl.send(htmlPasswordOk)
                    
                    self._display.WriteLines(["Informations", "saved." ,"Restart","the device"])
                    
                else:                  
                    requestedPage = Req.GetRequestPageGet(requestString)             
                            
                    if requestedPage == '/' or requestedPage == '':
                        cl.send(htmlMain)
                        cl.close()
                    elif requestedPage == '/style.css':
                        cl.send(css)
                        cl.close()    
                    elif requestedPage == '/info':                    
                        cl.send(htmlInfo)
                        cl.close()                
                    elif requestedPage == '/server/restart':
                        print('Restarting...')
                        self._display.WriteLine('Restarting...')
                        cl.send(htmlRestarting)
                        cl.close()
                        machine.reset()                                 
                            
                    else:
                        print('Page not found')
                        self._display.WriteLine('404: ' + requestedPage)
                        cl.send('HTTP/1.0 404 OK\r\nContent-type: text/html\r\n\r\n')
                        cl.close()

            except OSError as e:
                cl.close()
                
                print('connection closed')

    def _sub_connect_to_network(self, n_name,n_password):
        wlan = network.WLAN(network.STA_IF)
        wlan.active(True)
        wlan.connect(n_name,n_password)
        max_wait = 10
        while max_wait > 0:
            if wlan.status() < 0 or wlan.status() >= 3:
                break
        max_wait -= 1
        time.sleep(1)
        
        if wlan.status() != 3:
            Credentials.Clear()
            print('network connection failed. Network name:' + n_name) 
            machine.reset()

        status = wlan.ifconfig()
        print('Connected!')
        
        self._display.WriteLines(["Connected to", n_name, 'my ip is', status[0]], color=Colors.BLACK, background=Colors.GREEN)

        time.sleep(1)
        
        return 

    def ClearCredentials(self):
        Credentials.Clear()