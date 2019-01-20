% server
close all;clear all;clc;
data =imread('4.jpg');
buffersize = 1024;

s = whos('data');
s.size
s.bytes
tcpipServer = tcpip('localhost',1722,'NetworkRole','Server');
set(tcpipServer,'OutputBufferSize',buffersize);
set(tcpipServer,'InputBufferSize',buffersize);
fopen(tcpipServer);

fwrite(tcpipServer,s.size(1),'int16');%hight
fwrite(tcpipServer,s.size(2),'int16');%width

rsdata = []; %flatten data
for i=1:s.size(1)
    for j=1:s.size(2)
        for k=1:s.size(3)
            rsdata(end+1)=data(i,j,k);
        end
    end 
end
%data=data(:);
%
i=1;
while i <= s.bytes
    if i+buffersize-1 >= s.bytes
        fwrite(tcpipServer,rsdata(i:s.bytes),'uint8');%image
    else
        fwrite(tcpipServer,rsdata(i:i+buffersize-1),'uint8');%image
    end
    %recv = fread(tcpipServer,1,'uchar');%concurrent
    i=i+buffersize;
end
%
fclose(tcpipServer);