function FIT = FitnessA(Ft, x, r, single, lambda, l, Fnum, start, stop, U)
% FitnessA - Stage 1 fitness: optimize global parameters (A, V, D)
%   Accepts parameters directly (also backwards compatible with parameter_preset)
A = x(1);
V = x(2);
D = x(3);

% Allow fallback to parameter_preset if only 2 args passed
if nargin < 9
    para = parameter_preset();
    r = para.r;
    single = para.single;
    lambda = para.lambda;
    Fnum = para.Fnum;
    l = para.l;
    start = para.start;
    stop = para.stop;
    U = para.U;
end

ft = Focal_Sequence_Generation(start, Fnum, V, D);
Eout = Light_Field_SA_A(Ft, ft, r, l, single, lambda, U, A);

x_coord = linspace(-(r-0.5*single),(r-0.5*single),U);
y_coord = linspace(-(r-0.5*single),(r-0.5*single),U);

[X,Y]=meshgrid(x_coord,y_coord);

z=linspace(start-0.5e-3,stop+0.5e-3,100);

Enormal=normalizeArrayTo01(RSaxis_GPU(Eout, lambda, X, Y, z, 1.333));

Estandard = flat_top_gaussian(z, 1, start, stop, 0.05e-3);
FIT = sum(abs(Enormal-Estandard));

end