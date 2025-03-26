clear;clc
conn = sqlite('nanostructures.db');

specific_wavelengths1 = 0.532e-6;  

wavelength_list = join(string(specific_wavelengths1), ",");

query1 = sprintf( ...
    "SELECT n.structure_info, m.wavelength, m.phase_shift, m.transmission "+...
    "FROM measurements m "+...
    "JOIN nanostructures n ON m.structure_id = n.id "+...
    "WHERE m.wavelength IN (%s) "+...
    "ORDER BY n.structure_info;",wavelength_list);

data1 = fetch(conn, query1);

specific_wavelengths2 = 0.8e-6;  

wavelength_list = join(string(specific_wavelengths2),",");

query2 = sprintf( ...
    "SELECT n.structure_info, m.wavelength, m.phase_shift, m.transmission "+...
    "FROM measurements m "+...
    "JOIN nanostructures n ON m.structure_id = n.id "+...
    "WHERE m.wavelength IN (%s) "+...
    "ORDER BY n.structure_info;",wavelength_list);

data2 = fetch(conn, query2);

% 显示数据
disp(data1);
disp(data2);

close(conn);

D(1,:)=table2array(data1(:,"phase_shift"));
D(2,:)=table2array(data2(:,"phase_shift"));
%% 目标计算
r=12e-6;
single=0.4e-6;
lambda=linspace(0.532e-6,0.8e-6,2);
U=int16(r/single*2);
f=24e-6;
x=linspace(-(r-0.5*single),(r-0.5*single),U);
y=linspace(-(r-0.5*single),(r-0.5*single),U);
[X,Y]=meshgrid(x,y);
radiusSquared=(X).^2+(Y).^2;
radius=sqrt(radiusSquared);

phi=zeros(numel(lambda),numel(x));
for i=1:numel(lambda)
    Lambda=lambda(i);
    phi(i,:)=Hyperbolic_phase(x,Lambda,f);
end

%%
for i=1:60
    phi_target=phi(:,i);
    for j=1:60
        StrPhi=D(:,j);
        interpolation(j)=sum(abs(phi_target-StrPhi))/10;
    end
    idx=find(interpolation==min(interpolation,[],"all"));
    idx=idx(1);
    P(:,i)=D(:,idx);
end

%% function
function phi=Hyperbolic_phase(r,lambda,f)
phi=-2*pi/lambda*(sqrt(r.^2+f^2)-f);
end