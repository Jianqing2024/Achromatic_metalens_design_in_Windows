function Eout = Light_field_Control(r,single,lambda,U,f,w0)
k=2*pi/lambda;

x = linspace(-(r-0.5*single),(r-0.5*single),U);
y = linspace(-(r-0.5*single),(r-0.5*single),U);

[X, Y] = meshgrid(x, y);

zR = pi * w0^2 / lambda;

wz  = w0 * sqrt(1 + (f / zR)^2);
Rz  = -f * (1 + (zR / f)^2);
psi = -atan(f / zR);

Xc = X;
Yc = Y;

amplitude = (w0 / wz) * exp( - (Xc.^2 + Yc.^2) / wz^2 );
phase = exp(1i * k * (Xc.^2 + Yc.^2) / (2 * Rz) - 1i * psi);

Eout = amplitude .* phase;

% Eout(sqrt(X.^2+Y.^2)>=r)=0;
end