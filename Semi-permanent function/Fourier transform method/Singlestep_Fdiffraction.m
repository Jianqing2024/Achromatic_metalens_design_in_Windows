function [x2,y2,Uout] = Singlestep_Fdiffraction(Uin, lambda, single, d) 
N = size(Uin, 1);
k = 2*pi/lambda;
[x1,y1] = meshgrid((-N/2 : 1 : N/2 - 1) * single);
[x2,y2] = meshgrid((-N/2 : N/2-1) / (N*single)*lambda*d);
Uout=1/(1i*lambda*d).*exp(1i*k/(2*d)*(x2.^2+y2.^2)).*ft2(Uin.*exp(1i*k/(2*d).*(x1.^2+y1.^2)),single);
end
