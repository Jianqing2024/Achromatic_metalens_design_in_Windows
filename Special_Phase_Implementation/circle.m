function c=circle(r,x0,y0,m)
theta = linspace(0, 2*pi, m + 1); 
theta(end) = [];
x_circle = r * cos(theta) + x0;
y_circle = r * sin(theta) + y0;
c = [x_circle',y_circle'];
end