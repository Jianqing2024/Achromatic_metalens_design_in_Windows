clear;clc
% 设定参数
nco = 1.4674;
ncl = 1.4607;
R_max = 15;

R_fib = 62.5;
Nx = 101;
Ny = 101;
Nz = 1001;

zmax=500;

delta=(nco^2-ncl^2)/(2*nco^2);
a=4.1;
alphia=(R_max-a)/zmax;

% 坐标轴
x = linspace(-R_max, R_max, Nx);
y = linspace(-R_max, R_max, Ny);
z = linspace(0, zmax, Nz);
R = linspace(a, R_max, Nz);

fid = fopen('new.txt', 'w');

fprintf(fid, '%i %d %d\n', [Nx,-R_max,R_max]);
fprintf(fid, '%i %d %d\n', [Ny,-R_max,R_max]);
fprintf(fid, '%i %d %d\n', [Nz,0,500]);

for i = 1:Nz
    rM = R(i)^2;
    z4 = (a+alphia*z(i))^4;
    for j = 1:Ny
        for k = 1:Nx
            r2 = x(k)^2 + y(j)^2;

            if r2 > R_fib^2
                n = 1;
            elseif r2 < R_fib^2 && r2 >= rM 
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