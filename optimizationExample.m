clear;clc
nvars = 3;
lb = [-pi,-pi,-0.1e-3];   % 下界
ub = [pi,pi,0.1e-3];    % 上界
options = optimoptions('ga', 'PopulationSize', 40, 'MaxGenerations', 20000, 'FunctionTolerance', 1e-8);

tic;
[x_opt, fval] = ga(@fittt, nvars, [], [], [], [], lb, ub, [], options);
toc;
%%
[Phase_spectrum,str]=fittt2(x_opt);
Targetphi=fittt3(x_opt);

%%
[row,col]=size(Phase_spectrum);
lambda=linspace(0.532e-6,0.8e-6,2);

r=0.25e-3;
single=0.2e-6;
U=int16(r/single);
R=linspace(0.5*single,(r-0.5*single),U);

figure(1);
t = tiledlayout(row, 1, 'Padding', 'tight', 'TileSpacing', 'compact');

% 添加全局标题和坐标轴标签
title(t, '拟合结果', 'FontSize', 14);
xlabel(t, 'R/\mum');
ylabel(t, 'Phi');

ax = gobjects(row, 1);

for i = 1:row
    ax(i) = nexttile; 
    
    plot(R, Targetphi(i,:));
    hold on;
    set(gca, 'TickLength', [0 0]);

    scatter(R, Phase_spectrum(i,:), 8); 
    hold off;
    title(sprintf('Lambda = %.4f $\\mu$m', lambda(i) * 1e6), 'Interpreter', 'latex');
end
%%
% r=0.25e-3;
% single=0.4e-6;
% lambda=linspace(0.4e-6,0.6e-6,10);
% U=int16(r/single*2);
% f=1e-3;
% x=linspace(-(r-0.5*single),(r-0.5*single),U);
% y=linspace(-(r-0.5*single),(r-0.5*single),U);
% [X,Y]=meshgrid(x,y);
% radiusSquared=(X).^2+(Y).^2;
% radius=sqrt(radiusSquared);
% 
% load SweepPhi.mat
% 
% for i=1:5
%     Phi=SweepPhi{i};
%     for j=1:12
%         p{(i-1)*12+j}=Phi(:,j);
%     end
% end
% 
% chazhi=zeros(numel(R),1);
% UsedStr=zeros(U,U);
% for i=1:U
%     for j=1:U
%         if radius(i,j)>r
%             continue
%         end
%         for k=1:numel(R)
%             chazhi(k)=abs(radius(i,j)-R(k));
%         end
%         idx=find(chazhi==min(chazhi,[],"all"),1);
%         UsedStr(i,j)=str(idx);
%         for l=1:numel(lambda)
%             PPP(i,j)=p{UsedStr(i,j)}(l);
%             phi{l}=PPP;
%         end
%     end
% end