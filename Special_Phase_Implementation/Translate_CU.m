clear;clc
load Phase.mat
phi = readmatrix('gkj_MiniCube.txt');
phi = wrapTo2Pi(phi);

h = linspace(2,4,100);

for i=1:600
    for j=1:600
        phase = Phase(i,j);

        if phase == 0
            height(i,j) = nan;
        else
            for k=1:100
                diff(k) = abs(phase-phi(k));
            end
            [~, index] = min(diff);
            height(i,j) = h(index);
        end
    end
end

save height.mat height