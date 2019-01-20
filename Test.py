import socket
import numpy as np
from PIL import Image

sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM) ##TCP
sock.connect(('localhost',1722))
print("socket connected")

higth = int.from_bytes(sock.recv(2), byteorder='big')
width = int.from_bytes(sock.recv(2), byteorder='big')

buffersize = 1024 ## buffer 1024 bytes

print(higth,width,3)
img=[]
for i in range(1,higth*width*3,buffersize):#higth*width*3
    data = sock.recv(buffersize)
    # sock.send('y'.encode()) ## send confirm message
    for j in data:
        img.append(j)
sock.close()
print("socket closed")

img = np.array(img).reshape((higth,width,3))
print(img)
# print(np.array(Image.open('1.jpg')))
Image.fromarray(img.astype('uint8')).convert('RGB').save("test.jpg")