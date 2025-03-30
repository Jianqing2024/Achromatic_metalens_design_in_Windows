function [Efficiency,fwhm]=Focus_on_efficiency_lowSampling_GPU(E1,X1,Y1,E0,lambda,Focus_position,fwmhCheckPoint,fwmhCheckRadius,Sampling)
% 基于瑞利—索末菲衍射积分算法制定的聚焦效率/光斑半高全宽计算函数，用于计算光斑较小（即光斑处采样低）情况下的聚焦效率。
% 在这种情况下，单步傅里叶变换的菲涅尔衍射积分由于其固有的采样率问题，导致整个焦点及附近区域坍缩成一个像素，计算不精确

xx=linspace(-fwmhCheckRadius,fwmhCheckRadius,fwmhCheckPoint);
U=RSradial_GPU(E1,lambda,X1,Y1,xx,Focus_position);
fwhm = FWHM(xx, U);

Calculation_region=fwhm/2*4;
Calculation_point=round(Calculation_region/Sampling*2);

if mod(Calculation_point, 2) == 0
    Calculation_point=Calculation_point+1;
end

xx=linspace(-Calculation_region,Calculation_region,Calculation_point);
yy=linspace(-Calculation_region,Calculation_region,Calculation_point);
[XX,YY]=meshgrid(xx,yy);

U1=RSarray_GPU(E1,lambda,X1,Y1,XX,YY,Focus_position);

integral_x = trapz(XX(1,:), U1, 2);
U_out = trapz(YY(:,1), integral_x);

integral_x = trapz(X1(1,:), abs(E0).^2, 2);
U_in = trapz(Y1(:,1), integral_x);

Efficiency=U_out/U_in;

end