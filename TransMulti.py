import socket
import numpy as np
from PIL import Image
import time

sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM) ##TCP
sock.connect(('localhost',1722))
print("socket connected")
buffersize = 1024 ## buffer 1024 bytes
batch_size = 10
batch = []

## receive image shape
higth = int.from_bytes(sock.recv(2), byteorder='big')
width = int.from_bytes(sock.recv(2), byteorder='big')
print(higth, width, 3)

# receive image from matlab
start = time.clock()
for n in range(1,batch_size+1):
    print("receiving %s..." % n)
    img=[]
    for i in range(1,higth*width*3,buffersize):#higth*width*3
        data = sock.recv(buffersize)
        for j in data:
            img.append(j)
    img = np.array(img).reshape((higth,width,3))
    batch.append(img)
    # Image.fromarray(img.astype('uint8')).convert('RGB').save("python_receive%s.jpg"%n)
    sock.send(bytes(1))
elapsed = (time.clock() - start)
print("receive from matlab time: ",elapsed)

pass ## your process of img

## send processed img
start = time.clock()
for n in range(1, batch_size+1):
    print("sending %s..."%n)
    img = batch[n-1]
    rsimg=[]
    higth = img.shape[0]
    width = img.shape[1]

    # x = time.clock()
    for k in range(3):
        for j in range(width):
            for i in range(higth):
                 rsimg.append(img[i][j][k])
    # print("reshape time ",time.clock()-x)
    i=0
    # x = time.clock()
    while i < higth*width*3:
        if i+buffersize > higth*width*3:
            sock.send(bytes(rsimg[i:higth*width*3]))
        else:
            sock.send(bytes(rsimg[i:i+buffersize]))
        i = i + buffersize
    # print("send time ", time.clock() - x)
    elapsed = (time.clock() - start)
    sock.recv(1) ## confirm matlab received
print("send to matlab time: ",elapsed)

## close socket
sock.close()
print("socket closed")
