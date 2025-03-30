function U=RSaxis_Par(Ein,lambda,X0,Y0,z)
U=zeros(1,numel(z));

parfor i=1:numel(z)
    Z=z(i);
    u=RSintegration(Ein,lambda,X0,Y0,0,0,Z);
    U(i)=abs(u)^2;
end
end