clear;clc
load Parameter.mat
x = [-fliplr(R), R];
y = x;
[X, Y] = meshgrid(x, y);