clear;clc
% 使用present变量和ifempty解决问题
global data
data=linspace(1,10,20);

x=linspace(1,20,30);
y=fu(x);

function y=fu(x)
global data
y=sum(data)*x;
end
