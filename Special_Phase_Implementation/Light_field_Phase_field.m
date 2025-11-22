function phi=Light_field_Phase_field(Ft,ft,r,l,single,lambda,U)

x = linspace(-(r-0.5*single),(r-0.5*single),U);
y = linspace(-(r-0.5*single),(r-0.5*single),U);
[X,Y]=meshgrid(x,y);
x0=0;
y0=0;
R2 = (X-x0).^2+(Y-y0).^2;

F = ft(Ft);

[~, phase] = Light_field_Incident_field(r,single,lambda,U,l,4.4e-6,1);

phi=(2*pi/lambda)*(F-sqrt(R2+F.^2))-phase;
end