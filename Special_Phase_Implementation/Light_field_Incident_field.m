function [Eout, phase] = Light_field_Incident_field(r,single,lambda,U,l,w0,n)
lambda = lambda/n;

k = 2*pi/lambda;

x = linspace(-(r-0.5*single),(r-0.5*single),U);
y = linspace(-(r-0.5*single),(r-0.5*single),U);
[X, Y] = meshgrid(x, y);

phase = zeros(U, U);

amplitude = ones(U, U);

Eout = amplitude .* exp(1i * phase);

end