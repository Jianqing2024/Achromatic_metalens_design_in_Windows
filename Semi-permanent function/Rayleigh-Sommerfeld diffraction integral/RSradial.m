function U = RSradial(Ein,lambda,X0,Y0,x,z)
U=zeros(1,numel(x));
   for i=1:numel(x)
       X=x(i);
       u=RSintegration(Ein,lambda,X0,Y0,X,0,z);
       U(i)=abs(u)^2;
   end
end