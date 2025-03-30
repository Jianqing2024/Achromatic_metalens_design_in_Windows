function U = RSarray(Ein,lambda,X0,Y0,x,y,z)
[xx,~]=size(x);
[~,yy]=size(x);
U=zeros(xx,yy);
for i=1:xx
   for j=1:yy
       X=x(i,j);
       Y=y(i,j);
       u=RSintegration(Ein,lambda,X0,Y0,X,Y,z);
       U(i,j)=abs(u)^2;
   end
end

end