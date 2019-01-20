import socket
import numpy as np
from PIL import Image
import time

sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM) ##TCP
sock.connect(('localhost',1722))
print("socket connected")

# receive image from matlab
start = time.clock()
higth = int.from_bytes(sock.recv(2), byteorder='big')
width = int.from_bytes(sock.recv(2), byteorder='big')
buffersize = 1024 ## buffer 1024 bytes
print(higth,width,3)
img=[]
for i in range(1,higth*width*3,buffersize):#higth*width*3
    data = sock.recv(buffersize)
    for j in data:
        img.append(j)

img = np.array(img).reshape((higth,width,3))
# print(img)
# Image.fromarray(img.astype('uint8')).convert('RGB').save("test.jpg")
elapsed = (time.clock() - start)
print("receive from matlab time: ",elapsed)

pass ## your process of img

## send processed img
start = time.clock()
rsimg=[]
for k in range(3):
    for j in range(width):
        for i in range(higth):
             rsimg.append(img[i][j][k])

i=0
while i < higth*width*3:
    if i+buffersize > higth*width*3:
        sock.send(bytes(rsimg[i:higth*width*3]))
    else:
        sock.send(bytes(rsimg[i:i+buffersize]))
    i = i + buffersize
elapsed = (time.clock() - start)
print("send to matlab time: ",elapsed)
## close socket
sock.close()
print("socket closed")
