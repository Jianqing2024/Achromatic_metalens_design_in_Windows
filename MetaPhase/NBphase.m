function [Eout, phi] = NBphase(r, single, lambda, l, Fnum, start, stop, singleDownsampling, loop, popnum, Ft, Ft_low)
% NBphase - Achromatic phase optimization using SA2.6 two-stage GA
%   Compatible wrapper: same interface as original NBphase, but uses 
%   SA2.6's binary-amplitude-modulated focal sequence optimization.
%
%   Inputs:
%     r      - metalens radius
%     single - unit cell period
%     lambda - wavelength
%     l      - source-to-lens distance
%     Fnum   - number of focal zones
%     start  - focal range start
%     stop   - focal range end
%     singleDownsampling - downsampled period (unused, kept for compatibility)
%     loop   - iteration count (unused, kept for compatibility)
%     popnum - GA population size
%     Ft     - random zone matrix (full resolution)
%     Ft_low - random zone matrix (downsampled, unused)
%
%   Outputs:
%     Eout - complex emission field
%     phi  - phase distribution

U = int64(r*2/single);

%% Stage 1: Optimize global parameters (A, V, D)
% A: binary amplitude modulation strength
% V: focal spacing growth factor
% D: initial focal spacing

fitnessFcnA = @(x) FitnessA(Ft, x, r, single, lambda, l, Fnum, start, stop, U);

optionsA = optimoptions('ga', ...
    'Display', 'iter', ...
    'PopulationSize', popnum, ...
    'MaxGenerations', 500, ...
    'CrossoverFraction', 0.8);

lbA = [0e-3, 10e-9, 0e-6];
ubA = [20e-3, 80e-9, 40e-6];

fprintf('=== NBphase Stage 1: Optimizing A, V, D ===\n');
[bestA, ~] = ga(fitnessFcnA, 3, [], [], [], [], lbA, ubA, [], optionsA);

A = bestA(1);
V = bestA(2);
D = bestA(3);

fprintf('Stage 1 done: A=%.4e, V=%.2e, D=%.2e\n', A, V, D);

%% Stage 2: Optimize per-zone focal positions (ft) and amplitudes (At)

% Generate initial population from Stage 1 results
Init_ft = Focal_Sequence_Generation(start, Fnum, V, D)';
Init_At = A * ones(1, Fnum);

Init_ft_pop = [Generate_Initial_Population(Init_ft, 500e-9, popnum-1, start-0.1e-3, stop+0.1e-3); Init_ft];
Init_At_pop = [Generate_Initial_Population(Init_At, 1e-3, popnum-1, 0.000, 0.02); Init_At];
Init_pop = [Init_ft_pop, Init_At_pop];

fitnessFcnB = @(x) FitnessB(Ft, x, r, single, lambda, l, Fnum, start, stop, U);

optionsB = optimoptions('ga', ...
    'Display', 'iter', ...
    'InitialPopulationMatrix', Init_pop, ...
    'PopulationSize', popnum, ...
    'MaxGenerations', 500, ...
    'CrossoverFraction', 0.8);

lbB = [(start-0.1e-3)*ones(1,Fnum), 0.1e-3*ones(1,Fnum)];
ubB = [(stop+0.1e-3)*ones(1,Fnum), 20e-3*ones(1,Fnum)];

fprintf('=== NBphase Stage 2: Optimizing ft, At ===\n');
[bestB, ~] = ga(fitnessFcnB, Fnum*2, [], [], [], [], lbB, ubB, [], optionsB);

ft = bestB(1:Fnum);
At = bestB(Fnum+1:end);

fprintf('Stage 2 done.\n');

%% Compute final output field and phase
[Eout, phi] = Light_Field_SA_B(Ft, ft, r, l, single, lambda, U, At);
phi = wrapToPi(phi);

%% Visualization
x_plot = linspace(-(r-0.5*single), (r-0.5*single), U);
y_plot = linspace(-(r-0.5*single), (r-0.5*single), U);
[X_plot, Y_plot] = meshgrid(x_plot, y_plot);

z_plot = linspace(start-20e-6, stop+20e-6, 100);

E_plot = RSaxis_GPU(Eout, lambda, X_plot, Y_plot, z_plot, 1);

f1 = figure(1);
plot(z_plot, normalizeArrayTo01(E_plot));
txt1 = sprintf('Wav = %.0fnm  (SA2.6)', lambda*1e9);
title(txt1);
xlabel('z (m)');
ylabel('Normalized intensity');

txt2 = sprintf('Wav%3.0d.mat', lambda*1e9);
save(txt2, 'phi', 'Eout', 'ft', 'At');

txt3 = sprintf('Wav%3.0d.fig', lambda*1e9);
savefig(f1, txt3);

close all;

end
