function Emiddle=Light_field_Phase_field(Ft,ft,r,l,single,lambda,U)
k1=2*pi/lambda*1.444;
k2=2*pi/lambda;

x = linspace(-(r-0.5*single),(r-0.5*single),U);
y = linspace(-(r-0.5*single),(r-0.5*single),U);
[X,Y]=meshgrid(x,y);
x0=0;
y0=0;

for i=1:U
    for j=1:U
        index=Ft(i,j);
        Ft(i,j)=ft(index);
    end
end

Emiddle=zeros(U,U);
R2=zeros(U,U);

for i=1:U
    for j=1:U
    R2(i,j)=(x(i)-x0)^2+(y(j)-y0)^2;
    % Emiddle(i,j)=k*(Ft(i,j)+l-sqrt(R2(i,j)+Ft(i,j)^2)-sqrt(R2(i,j)+l^2));
    Emiddle(i,j)=k2*(Ft(i,j)-sqrt(R2(i,j)+Ft(i,j)^2))+k1*(l-sqrt(R2(i,j)+l^2));
    end
end
Emiddle=wrapTo2Pi(Emiddle);
Emiddle(sqrt(X.^2+Y.^2)>=r)=0;

end