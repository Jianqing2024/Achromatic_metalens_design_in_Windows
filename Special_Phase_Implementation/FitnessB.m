function FIT = FitnessB(Ft, para, List)
r=para.r;
single=para.single;
lambda=para.lambda;

start=para.start;
stop=para.stop;

U=para.U;
Fnum=para.Fnum;

ft=List(1:Fnum);
At=List(Fnum+1:end);

Eout = Light_Field_SA_B(Ft, ft, r, single, lambda, U, At);

x = linspace(-(r-0.5*single),(r-0.5*single),U);
y = linspace(-(r-0.5*single),(r-0.5*single),U);

[X,Y]=meshgrid(x,y);

l = stop-start;

z=linspace(start-0.25*l,stop+0.25*l,100);

Enormal=normalizeArrayTo01(RSaxis_GPU(Eout, lambda, X, Y, z, 1));

Estandard = flat_top_gaussian(z, 1, start, stop, 0.05e-3);
FIT = sum(abs(Enormal-Estandard));

end