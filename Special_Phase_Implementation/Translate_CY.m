clear;clc
load Phase.mat
phi = readmatrix('gkj_cylinder.txt');

r = linspace(0.25,0.55,100);

for i=1:400
    for j=1:400
        phase = Phase(i,j);

        if phase == 0
            radius(i,j) = nan;
        else
            for k=1:100
                diff(k) = abs(phase-phi(k));
            end
            [~, index] = min(diff);
            radius(i,j) = r(index);
        end
    end
end

save radius.mat radius