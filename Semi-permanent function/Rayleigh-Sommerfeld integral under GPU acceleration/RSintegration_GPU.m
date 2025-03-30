function U=RSintegration_GPU(Ein,lambda,X0,Y0,x,y,z)
k = 2 * pi / lambda;

R = sqrt((X0 - x).^2 + (Y0 - y).^2 + z.^2);
R_gpu = gpuArray(R);

Ein_gpu = gpuArray(Ein);

diffraction_term_gpu = exp(1i * k .* R_gpu) ./ R_gpu;

integral_gpu = (1 / (1i * lambda)) * Ein_gpu .* diffraction_term_gpu;

x_values = X0(1, :);
y_values = Y0(:, 1);

integral_x_gpu = trapz(x_values, integral_gpu, 2);
integral_xy_gpu = trapz(y_values, integral_x_gpu);

U = gather(integral_xy_gpu);
end
