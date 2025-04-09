clear;clc
array=randi(100,100);
[E532,E800]=function1(array);

function [E532,E800]=function1(array)
dbFile = 'structures.db';
conn = sqlite(dbFile, 'readonly');

[sizeX,sizeY]=size(array);

Phi532=zeros(sizeX,sizeY);
Phi800=zeros(sizeX,sizeY);
for i=1:sizeX
    for j=1:sizeY
        ID=array(i,j);
        query=sprintf('SELECT %s, %s FROM structures WHERE id = %d', "angleIn532", "angleIn800", ID);
        data=fetch(conn,query);
        data=table2array(data);
        Phi532(i,j)=data(1);
        Phi800(i,j)=data(2);
    end
end

close(conn);
E532=exp(1i*Phi532);
E800=exp(1i*Phi800);
end