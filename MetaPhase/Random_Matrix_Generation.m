function Ft = Random_Matrix_Generation(U,Fnum)
xb = int16(U / sqrt(Fnum));
PB = cell(xb,xb);

for i=1:xb
    for j=1:xb
        randomNumbers= randperm(Fnum);
        PB{i,j}= reshape(randomNumbers, [sqrt(Fnum), sqrt(Fnum)]);
    end
end

Ft=cell2mat(PB);
end