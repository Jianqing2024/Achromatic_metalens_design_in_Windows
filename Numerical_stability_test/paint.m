clear;clc
load lum_l.mat
load py_l_532.mat
load py_l_800.mat
p_m_l_532=phase532_py;
p_f_l_532=wrapToPi(p532);
t_m_l_532=trans532_py;
t_f_l_532=t532;

p_m_l_800=phase800_py;
p_f_l_800=wrapToPi(p800);
t_m_l_800=trans800_py;
t_f_l_800=t532;

l=linspace(0.25,0.4,10);

figure(1);
subplot(2,2,1)
plot(l,p_f_l_532,'-r', l,p_m_l_532,'-b')
subplot(2,2,2)
plot(l,t_f_l_532,'-r', l,t_m_l_532,'-b')
subplot(2,2,3)
plot(l,p_f_l_800,'-r', l,p_m_l_800,'-b')
subplot(2,2,4)
plot(l,t_f_l_800,'-r', l,t_m_l_800,'-b')

%%
load lum_w.mat
load py_w_532.mat
load py_w_800.mat

p_m_w_532=phase532_py;
p_f_w_532=wrapToPi(p532);
t_m_w_532=trans532_py;
t_f_w_532=t532;

p_m_w_800=phase800_py;
p_f_w_800=wrapToPi(p800);
t_m_w_800=trans800_py;
t_f_w_800=t532;

w=linspace(0.1,0.2,10);

figure(2);
subplot(2,2,1)
plot(w,p_f_w_532,'-r', w,p_m_w_532,'-b')
subplot(2,2,2)
plot(w,t_f_w_532,'-r', w,t_m_w_532,'-b')
subplot(2,2,3)
plot(w,p_f_w_800,'-r', w,p_m_w_800,'-b')
subplot(2,2,4)
plot(w,t_f_w_800,'-r', w,t_m_w_800,'-b')

%%
% load lum_r.mat
% load py_r_532.mat
% load py_r_800.mat