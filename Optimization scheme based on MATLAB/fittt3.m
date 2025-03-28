function Targetphi=fittt3(shift)
r=0.25e-3;
single=0.2e-6;
lambda=linspace(0.532e-6,0.8e-6,2);
U=int16(r/single);
f=8.5e-3+shift(3);
x=linspace(0.5*single,(r-0.5*single),U);

shift_phi=shift(1:2);

Targetphi=zeros(numel(lambda),numel(x));
for i=1:numel(lambda)
    Targetphi(i,:)=wrapToPi(Hyperbolic_phase(x,lambda(i),f)+shift_phi(i));
end

end