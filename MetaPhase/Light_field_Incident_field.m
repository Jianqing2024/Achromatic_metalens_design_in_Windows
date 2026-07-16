function [Eout, phase] = Light_field_Incident_field(r,single,lambda,U,l,w0,n)
lambda = lambda/n;

k = 2*pi/lambda;

x = linspace(-(r-0.5*single),(r-0.5*single),U);
y = linspace(-(r-0.5*single),(r-0.5*single),U);
[X, Y] = meshgrid(x, y);

zR = pi * w0^2 / lambda;

wz = w0 * sqrt(1 + (l / zR)^2);

Rz = l * (1 + (zR / l)^2);

psi = atan(l / zR);

amplitude = (w0 / wz) * exp(-(X.^2 + Y.^2) / wz^2);

phase = k*l + k*(X.^2 + Y.^2)/(2*Rz) - psi;

Eout = amplitude .* exp(1i * phase);

% lambda = lambda/n;
% 
% x = linspace(-(r-0.5*single),(r-0.5*single),U);
% y = linspace(-(r-0.5*single),(r-0.5*single),U);
% [X, Y] = meshgrid(x, y);
% 
% f = pi*w0^2/lambda;
% r2 = X.^2+Y.^2;
% k = 2*pi/lambda;
% w = w0*sqrt(1+(l/f));
% R = l+f^2/l;
% 
% A = 1/w*exp(-r2/(w^2));
% P = exp(-1i*(k*(l+r2/(2*R))-atan(l/f)));
% Eout = A*P;

end