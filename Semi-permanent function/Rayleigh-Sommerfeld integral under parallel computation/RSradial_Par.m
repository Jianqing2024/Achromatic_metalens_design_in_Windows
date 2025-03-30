function U = RSradial_Par(Ein,lambda,X0,Y0,x,z)
U=zeros(1,numel(x));
parfor i=1:numel(x)
   X=x(i);
   u=RSintegration(Ein,lambda,X0,Y0,X,0,z);
   U(i)=abs(u)^2;
end
end