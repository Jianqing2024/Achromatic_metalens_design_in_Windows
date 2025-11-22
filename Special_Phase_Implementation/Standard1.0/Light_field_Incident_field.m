function E=Light_field_Incident_field(r,l,single,lambda,U)
k=2*pi/lambda*1.444;

x = linspace(-(r-0.5*single),(r-0.5*single),U);
y = linspace(-(r-0.5*single),(r-0.5*single),U);
[X,Y]=meshgrid(x,y);
x0=0;
y0=0;

E=zeros(U,U);
R2=zeros(U,U);

for i=1:U
    for j=1:U
    R2(i,j)=(x(i)-x0)^2+(y(j)-y0)^2;
    E(i,j)=(1/sqrt(R2(i,j)+l^2))*exp(1i*k*sqrt(R2(i,j)+l^2));
    end
end

E(sqrt(X.^2+Y.^2)>=r)=0;
end