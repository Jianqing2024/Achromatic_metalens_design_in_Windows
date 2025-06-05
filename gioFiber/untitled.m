clear;clc
% 设定参数
nco = 1.4674;
ncl = 1.4607;
R_max = 15;

Nx = 200;
Ny = 20000;
Nz = 2;

ymid=250;
ymax=1000;

delta=(nco^2-ncl^2)/(2*nco^2);
a=4.1;
alphia=(R_max-a)/ymax;

% 坐标轴
x = linspace(-R_max, R_max, Nx);
y = linspace(0, ymax, Ny);
z = linspace(-100, 100, Nz);
R = [linspace(a, R_max, 5000), R_max*ones(1, 15000)];

fid = fopen('new.txt', 'w');

fprintf(fid, '%i %d %d\n', [Nx,-R_max,R_max]);
fprintf(fid, '%i %d %d\n', [Ny,0,ymax]);
fprintf(fid, '%i %d %d\n', [Nz,0,1]);

for i = 1:Nz
    for j = 1:Ny
        rM = R(j)^2;

        if y(j) < ymid
            y4 = (a+alphia*y(j))^4;
        else
            y4 = (a+alphia*ymid)^4;
        end

        for k = 1:Nx
            r2 = x(k)^2;

            if r2 >= rM
                n = ncl;
            else
                n = single(sqrt(nco^2*(1-2*delta*(a^2*r2)/y4)));
            end

            fprintf(fid, '%.8f\n', n);
        end
    end
    fprintf("已进行：%i / %i\n", i, Nz);
end

fclose(fid);