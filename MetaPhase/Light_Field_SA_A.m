function Eout = Light_Field_SA_A(Ft, ft, r, l, single, lambda, U, A)

Ft = double(Ft);
ft = sort(ft);

F = ft(Ft);

x = linspace(-(r-0.5*single), (r+0.5*single), U);
y = linspace(-(r-0.5*single), (r+0.5*single), U);
[X, Y] = meshgrid(x, y);

R2 = (X).^2 + (Y).^2;

[Ein, phase] = Light_field_Incident_field(r,single,lambda,U,l,4.5e-6,1.447);

phi_lens = (2*pi/lambda*1.333)*(F-sqrt(R2+F.^2))-phase;

phi_shift = -pi*Ft*A;

phi = phi_lens+phi_shift;

Eout = Ein.*exp(1i*phi);

end
