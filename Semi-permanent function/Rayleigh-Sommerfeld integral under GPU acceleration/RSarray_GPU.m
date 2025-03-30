function U = RSarray_GPU(Ein,lambda,X0,Y0,x,y,z)
[xx,~]=size(x);
[~,yy]=size(x);

Ein_GPU = gpuArray(Ein);
lambda_gpu = gpuArray(lambda);
X0_gpu = gpuArray(X0);
Y0_gpu = gpuArray(Y0);
x_gpu = gpuArray(x);
y_gpu = gpuArray(y);
xx_gpu = gpuArray(xx);
yy_gpu = gpuArray(yy);
z_gpu = gpuArray(z);

U=zeros(xx_gpu,yy_gpu);

for i=1:xx_gpu
   for j=1:yy_gpu
       X=x_gpu(i,j);
       Y=y_gpu(i,j);
       u=RSintegration(Ein_GPU,lambda_gpu,X0_gpu,Y0_gpu,X,Y,z_gpu);
       U(i,j)=abs(u)^2;
   end
end
U=gather(U);
end