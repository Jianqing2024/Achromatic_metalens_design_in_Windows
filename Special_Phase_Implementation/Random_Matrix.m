function Ft = Random_Matrix(Fnum, Size)
Ft = zeros(Size,Size);
for i=1:Size
    for j=1:Size
        Ft(i,j) = randi([1, Fnum]);
    end
end
end