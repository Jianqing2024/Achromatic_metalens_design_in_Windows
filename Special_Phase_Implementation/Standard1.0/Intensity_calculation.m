function E=Intensity_calculation(Eout,lambda,r,single,z)

xmin=-(r-0.5*single);
xmax=(r-0.5*single);
ymin=-(r-0.5*single);
ymax=(r-0.5*single);

[x,y]=size(Eout);
x0=linspace(xmin,xmax,x);
y0=linspace(ymin,ymax,y);
[X,Y]=meshgrid(x0,y0);

E=RSaxis_GPU(Eout,lambda,X,Y,z);
%E=RSaxis(Eout,lambda,X,Y,z);
end