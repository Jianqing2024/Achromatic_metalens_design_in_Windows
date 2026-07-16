function FIT = FitnessB(Ft, List, r, single, lambda, l, Fnum, start, stop, U)
% FitnessB - Stage 2 fitness: optimize per-zone focal positions and amplitudes
%   Accepts parameters directly (also backwards compatible with parameter_preset)

% Allow fallback to parameter_preset if only 2 args passed
if nargin < 9
    para = parameter_preset();
    r = para.r;
    single = para.single;
    lambda = para.lambda;
    l = para.l;
    start = para.start;
    stop = para.stop;
    U = para.U;
    Fnum = para.Fnum;
end

ft=List(1:Fnum);
At=List(Fnum+1:end);

[Eout, ~] = Light_Field_SA_B(Ft, ft, r, l, single, lambda, U, At);

x_coord = linspace(-(r-0.5*single),(r-0.5*single),U);
y_coord = linspace(-(r-0.5*single),(r-0.5*single),U);

[X,Y]=meshgrid(x_coord,y_coord);

z=linspace(start-0.5e-3,stop+0.5e-3,100);

Enormal=normalizeArrayTo01(RSaxis_GPU(Eout, lambda, X, Y, z, 1.333));

Estandard = flat_top_gaussian(z, 1, start, stop, 0.05e-3);
FIT = sum(abs(Enormal-Estandard));

end