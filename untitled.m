clc
% load dataPhase.mat
lambda = linspace(0.5e-6, 0.8e-6, 5);
z = linspace(120e-6, 1200e-6, 100);

ZZ{1} = RSaxis(exp(1i*phase0),lambda(1), X, Y, z);
ZZ{2} = RSaxis(exp(1i*phase1),lambda(2), X, Y, z);
ZZ{3} = RSaxis(exp(1i*phase2),lambda(3), X, Y, z);
ZZ{4} = RSaxis(exp(1i*phase3),lambda(4), X, Y, z);
ZZ{5} = RSaxis(exp(1i*phase4),lambda(5), X, Y, z);

fig1 = figure(1);
tiledlayout("vertical")

nexttile
plot(z, ZZ{1})

nexttile
plot(z, ZZ{2})

nexttile
plot(z, ZZ{3})

nexttile
plot(z, ZZ{4})

nexttile
plot(z, ZZ{5})
