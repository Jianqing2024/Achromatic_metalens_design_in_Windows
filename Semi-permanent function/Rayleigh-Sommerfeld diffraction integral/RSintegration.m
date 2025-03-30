function U=RSintegration(Ein,lambda,X0,Y0,x,y,z)
k=2*pi/lambda;
R=sqrt((X0-x).^2+(Y0-y).^2+z^2);
diffraction_term=exp(1i*k.*R)./R;
integral=(1/(1i*lambda))*Ein.*diffraction_term;

x=X0(1,:);
y=Y0(:,1);
integral_x=trapz(x,integral, 2);
integral_xy=trapz(y, integral_x);

U=integral_xy;
% U=abs(integral_xy)^2;
end
