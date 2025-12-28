clear;clc;close all
r = 1.8e-3;
single = 0.4e-6;
lambda = 0.532e-6;
U = int64(r/single*2);
l = 25e-3;

[Ein, phase] = Light_field_Incident_field(r,single,lambda,U,l,1.8e-6,1);

imagesc(abs(Ein).^2)
axis equal
axis off