
try:
  import usocket as socket
except:
  import socket

from machine import Pin
import network

import esp
esp.osdebug(None)

import gc
gc.collect()

ssid = 'OpenWrt'
password = 'lembang1945'

station = network.WLAN(network.STA_IF)

station.active(True)
station.connect(ssid, password)

while station.isconnected() == False:
  pass

print('Connection successful')
print(station.ifconfig())

import gc
import os


value = 0
string = "HelloWorld"
firstNum = 0.0
secNum = 0.0
calcNum = 0.0
calcError = ""
extraHTML = '<meta name="viewport" content="width=device-width, initial-scale=1"><link rel="icon" href="data:,"><style>html{font-family: Helvetica; display:inline-block; margin: 0px auto; text-align: center;} h1{color: #0F3376; padding: 2vh;}p{font-size: 1.5rem;}.button{display: inline-block; background-color: #e7bd3b; border: none;  border-radius: 4px; color: white; padding: 16px 40px; text-decoration: none; font-size: 30px; margin: 2px; cursor: pointer;} .button2{background-color: #4286f4;}</style>'

def indexpage():

  def df():
    s = os.statvfs('//')
    return ('{0} MB'.format((s[0]*s[3])/1048576))

  def free(full=False):
    F = gc.mem_free()
    A = gc.mem_alloc()
    T = F+A
    P = '{0:.2f}%'.format(F/T*100)
    if not full: return P
    else : return ('Total:{0} Free:{1} ({2})'.format(T,F,P))
	
  ramrom = "Free Space: " + df() + " Memory Usage: " + free()
  
  html = '<html><head><title>ESP Web Server</title>' + extraHTML +'</head><body><h1>ESP Web Server on Micropython</h1><h6>Original code from <a href="https://randomnerdtutorials.com" target="_blank">randomnerdtutorials.com</a></h6><h3><a href="/test">Goto /test</a></h3>   <p>Memory usage: <strong>' + ramrom + '</strong></p><p>Value: <strong>' + str(value) + '</strong></p><p><a href="/?valueadd"><button class="button">increase</button></a></p><p><a href="/?valuedec"><button class="button button2">Decrease</button></a></p><p>String = <strong>' + string + '</strong></p><input id="txt" type="text" value="' + string +'"><p><a onclick="location.href=\'/?string=\' + document.getElementById(\'txt\').value + \'EndOfStr\';"><button class="button button2">setstring</button></a></p></body></html>'
  return html

def secondpage():
  try:
    calcNum = firstNum * secNum
  except ValueError:
    calcNum = " ValueError Occured"
  html2 = '<html><head><title>FormTest</title>' + extraHTML +'</head><body><h1>Forms Test page gengs</h1><h3><a href="/">Goto /</a></h3><h3></strong>First Number: ' + str(firstNum) + ' </strong></h3><h3></strong>Second Number: ' + str(secNum) + ' </strong></h3><h3></strong>Resulting Number: ' + str(calcNum) + calcError + ' </strong></h3></br><form action="/test">First Number:<br><input type="text" name="firstnum" value="420"><br>Multiplied by<br>Second Number:<br><input type="text" name="secondnum" value="420"><br><br><input type="submit" value="Submit"></form> </body></html>'
  return html2
  
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 80))
s.listen(5)

while True:
  conn, addr = s.accept()
  print('Got a connection from %s' % str(addr))
  request = conn.recv(1024)
  request = str(request)
  print('Content = %s' % request)
  valueadd = request.find('/?valueadd')
  valuedec = request.find('/?valuedec')
  chstring = request.find('/?string=')
  strend = request.find('EndOfStr')
  getFirstNum = request.find('?firstnum=')
  getFirstNumEnd = request.find('&secondnum')
  getSecondNum = request.find('&secondnum=')
  getRequestEnd = request.find(" HTTP/")
  
  if valueadd == 6:
    value += 1
  if valuedec == 6:
    value -= 1
  if chstring == 6:
    string = request[15:int(strend)]
  if getFirstNum == 11:
    try:
      calcError = ""
      diff = getSecondNum + 11
      firstNum = float(request[21:getFirstNumEnd])
      secNum = float(request[diff:getRequestEnd])
    except ValueError: 
      calcError = " ValueError Occured"
  if request[6:11] == "/test":
    response = secondpage()
  else:
    response = indexpage()
	
  conn.send('HTTP/1.1 200 OK\n')
  conn.send('Content-Type: text/html\n')
  conn.send('Connection: close\n\n')
  conn.sendall(response)
  conn.close()