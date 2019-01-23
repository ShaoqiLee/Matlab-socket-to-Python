% server
close all;clear all;clc;
buffersize = 1024;
batch_size = 10;
tcpipServer = tcpip('localhost',1722,'NetworkRole','Server');
set(tcpipServer,'OutputBufferSize',buffersize);
set(tcpipServer,'InputBufferSize',buffersize);
fopen(tcpipServer);

hight=107;
width=107;
fwrite(tcpipServer,hight,'int16');%hight
fwrite(tcpipServer,width,'int16');%width

for n=1:batch_size
    n
    data = imread('1.jpg');%sprintf('%s.jpg',num2str(n))
    data = imresize(data,[107,107]);
    bytes = hight*width*3;

    rsdata = []; %flatten data
    for i=1:hight
        for j=1:width
            for k=1:3
                rsdata(end+1)=data(i,j,k);
            end
        end 
    end
    %data=data(:);
    %
    i=1;
    while i <= bytes
        if i+buffersize-1 >= bytes
            fwrite(tcpipServer,rsdata(i:bytes),'uint8');%image
        else
            fwrite(tcpipServer,rsdata(i:i+buffersize-1),'uint8');%image
        end
        i=i+buffersize;
    end
    %confirm python received
    fread(tcpipServer,1,'uint8');
end

%%% receive image from python
for n=1:batch_size
    n
    i=1;
    img=[];
    bytes = hight*width*3;
    %
    t1=clock;
    while i <= bytes
        if i+buffersize-1 >= bytes
            img = [img;fread(tcpipServer,bytes-i+1,'uint8')];%image
        else
            img = [img;fread(tcpipServer,buffersize,'uint8')];%image
        end
        i=i+buffersize;
    end
    t2=clock;
    etime(t2,t1)
    %}
    rsimg = reshape(img,[hight,width,3]);
    %imwrite(uint8(rsimg),sprintf('matlab_receive%s.jpg',num2str(n)));
    %confirm received
    fwrite(tcpipServer,1,'uint8');
end
