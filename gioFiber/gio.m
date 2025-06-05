clear;clc
% 设定参数
nco = 1.4674;
ncl = 1.4607;
R_max = 15;

Nx = 101;
Ny = 1001;
Nz = 2;

ymax=500;

delta=(nco^2-ncl^2)/(2*nco^2);
a=4.1;
alphia=(R_max-a)/ymax;

% 坐标轴
x = linspace(-R_max, R_max, Nx);
z = linspace(0, ymax, Nz);
R = linspace(a, R_max, Nz);

fid = fopen('new.txt', 'w');

fprintf(fid, '%i %d %d\n', [Nx,-R_max,R_max]);
fprintf(fid, '%i %d %d\n', [Ny,0,ymax]);
fprintf(fid, '%i %d %d\n', [Nz,0,0]);

for i = 1:Nz
    rM = R(i)^2;
    z4 = (a+alphia*z(i))^4;
    for j = 1:Ny
        for k = 1:Nx
            r2 = x(k)^2 + y(j)^2;

            if r2 < R_fib^2 && r2 >= rM 
                n = ncl;
            else
                n = single(sqrt(nco^2*(1-2*delta*(a^2*r2)/z4)));
            end

            fprintf(fid, '%.8f\n', n);
        end
    end
    fprintf("已进行：%i / %i\n", i, Nz);
end

fclose(fid); 



for i = 1:Nz
    rM = R(i)^2;
    z4 = (a+alphia*z(i))^4;
        for k = 1:Nx
            r2 = x(k)^2;

            if r2 > R_fib^2
                n = 1;
            elseif r2 < R_fib^2 && r2 >= rM 
                n = ncl;
            else
                n = single(sqrt(nco^2*(1-2*delta*(a^2*r2)/z4)));
            end

            fprintf(fid, '%.8f\n', n);
        end
    fprintf("已进行：%i / %i\n", i, Nz);
end

fclose(fid);