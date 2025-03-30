function Fwhm=FWHM_Calculation_GPU(Ein,lambda,X,Y,CheckR,CheckPoint,CheckZ)
Ein_GPU = gpuArray(Ein);
lambda_gpu = gpuArray(lambda);
X_gpu = gpuArray(X);
Y_gpu = gpuArray(Y);
CheckR_gpu = gpuArray(CheckR);
CheckPoint_gpu = gpuArray(CheckPoint);
CheckZ_gpu = gpuArray(CheckZ);

CheckX=linspace(-CheckR_gpu,CheckR_gpu,CheckPoint_gpu);

Fwhm=zeros(1,numel(CheckZ_gpu));
for i=1:numel(CheckZ_gpu)
    Z=CheckZ_gpu(i);
    U = RSradial(Ein_GPU,lambda_gpu,X_gpu,Y_gpu,CheckX,Z);
    Fwhm(i)=FWHM(CheckX,U);
end
Fwhm=gather(Fwhm);
end