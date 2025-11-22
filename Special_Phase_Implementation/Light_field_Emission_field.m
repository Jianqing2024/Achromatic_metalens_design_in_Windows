function Eout=Light_field_Emission_field(Ft,ft,r,l,single,lambda,U)

x = linspace(-(r-0.5*single),(r-0.5*single),U);
y = linspace(-(r-0.5*single),(r-0.5*single),U);
[X,Y]=meshgrid(x,y);
x0=0;
y0=0;
R2 = (X-x0).^2+(Y-y0).^2;

F = ft(Ft);

[Ein, phase] = Light_field_Incident_field(r,single,lambda,U,l,4.4e-6,1);

Emiddle=(2*pi/lambda)*(F-sqrt(R2+F.^2))-phase;

Emiddle=exp(1i*Emiddle);
Eout=Ein.*Emiddle;

Eout(sqrt(X.^2+Y.^2)>=r)=0;
end