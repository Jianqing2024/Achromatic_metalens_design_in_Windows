function Eout = Light_field_regular(r,l,single,lambda,U,f)
k1=2*pi/lambda*1.444;
k2=2*pi/lambda*1.333;

x = linspace(-(r-0.5*single),(r-0.5*single),U);
y = linspace(-(r-0.5*single),(r-0.5*single),U);
[X,Y]=meshgrid(x,y);
x0=0;
y0=0;

Ein=zeros(U,U);
Emiddle=zeros(U,U);
R2=zeros(U,U);

for i=1:U
    for j=1:U
    R2(i,j)=(x(i)-x0)^2+(y(j)-y0)^2;
    Ein(i,j)=(1/sqrt(R2(i,j)+l^2))*exp(1i*k1*sqrt(R2(i,j)+l^2));
    Emiddle(i,j)=k2*(f-sqrt(R2(i,j)+f^2))+k1*(l-sqrt(R2(i,j)+l^2));
    end
end

Emiddle=exp(1i*Emiddle);
Eout=Ein.*Emiddle;

Eout(sqrt(X.^2+Y.^2)>=r)=0;
end