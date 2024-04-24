function phi_obj= TIE_unwrapping(phase1);
I1= exp(j*phase1);
I2=fftshift(fft2(fftshift(I1)));
[rows, cols] = size(I1); 
%figure, imshow(abs(I2), []);

%system parameter%
lambda= 660e-9;
p= 6.5e-6;
k = 2*pi/lambda;
z = 0e-3;
dz = 10e-9;
[x y] = ndgrid(-(rows/2):(rows/2)-1, -cols/2:cols/2-1);
x = x * p;
y = y * p;


[fx fy] = ndgrid(-1/2/p:1/p/rows:1/2/p-1, -1/2/p:1/p/cols:1/2/p-1);





%Angular spectrum transfer function%
f= (fx.^2)+ (fy.^2);
h= sqrt((k.^2)- (4*pi^2).*(f));
H_positive = exp(j*(z+dz)*h);
H_negative = exp(j*(z-dz)*h);
% figure, imagesc(abs(H_negative));
% figure, imagesc(abs(H_positive));


%convolution operation%
I3 = fftshift(ifft2(ifftshift(I2 .* H_positive)));
I4 = fftshift(ifft2(ifftshift(I2 .* H_negative)));
% figure, imagesc(abs(I3));
% figure, imagesc(abs(I4));



%% %%
I2_1=fftshift(ifft2(ifftshift(I2)));
%  figure, imshow(angle(I3), []);
%  figure, imshow(angle(I4), []);
%  figure, imshow(angle(I2_1), []);
% I2_1_1= I2_1(180, 796)
% I3= I3(180, 796)
% I4= I4(180, 796)

%% %%

%Derivative of intensity%;
I_deri= ((abs(I3.^2)- abs(I4.^2))./ (2.*dz));
%figure,imagesc(abs(I_deri));

D0 = -4*pi^2*(fx.^2 + fy.^2);
D = D0 ./ ( D0.^2 + eps);

I5 = fftshift(fft2(ifftshift(I_deri)));


phi_obj = -k*real(fftshift(ifft2(ifftshift(I5 .* D))));
phi_obj = phi_obj - min(phi_obj(:));
phi_obj= phi_obj;