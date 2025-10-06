function Eout = Light_Field_SA_A(Ft, ft, r, single, lambda, U, A)

ft = sort(ft);

F = ft(Ft);

x = linspace(-(r-0.5*single), (r+0.5*single), U);
y = linspace(-(r-0.5*single), (r+0.5*single), U);
[X, Y] = meshgrid(x, y);

R2 = (X).^2 + (Y).^2;

phi_lens = (2*pi/lambda)*(F-sqrt(R2+F.^2));

phi_shift = -pi*Ft*A;

phi = phi_lens+phi_shift;

Eout = exp(1i*phi);

end
