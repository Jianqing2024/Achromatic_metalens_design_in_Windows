function ft = Focal_Sequence_Generation(f1, Fnum, V, D)
ft = zeros(Fnum, 1);
for k = 1:Fnum
    ft(k) = f1 + (k - 1)*(D + V*(k - 1));
end
end