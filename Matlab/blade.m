
function New=blade(sections,profile_name,alpha,c,r,c_max)
%Author: Aymara Baumann Duran
%% Change Angle of Attack of a 2D airfoil
%% Loading the txt file
fileID = fopen(profile_name,'r');
formatSpec = '%d %f %f';
sizeA = [3 Inf];
A = fscanf(fileID,formatSpec,sizeA);
A(4,:)=zeros;
A = A';
%% Change twist
%alpha=12; %AOA in degrees
%c=5; %Chord in m
%r=14.2; %Radius in m

R = rotz(alpha);

A(:,2)=[A(:,2)-1/4]; %aerodynamic centre in c/4

B(:,1)=[A(:,2)];
B(:,2)=[A(:,3)];
B(:,3)=[A(:,4)];
Puntos_rotados(:,:)=R*transpose(B(:,:));
Puntos_rotados=Puntos_rotados';

New(:,2)=c*(Puntos_rotados(:,1)+1/4);
New(:,3)=c*Puntos_rotados(:,2);
%New(:,4)=c*A(:,4);
New(:,1)=r;
%% Show new geometry
figure(1)
% plot(c*A(:,2),c*A(:,3),'-b')
hold on
plot(New(:,2),New(:,3),'-r')
xlim([-c_max c_max+8])
ylim([-4-c_max c_max+4])
legend('Rotated Airfoil')

%% Output points to new txt
% open a file for writing
fid = fopen(sections, 'w');
% print a title
fprintf(fid, 'StartCurve\n');
% print values in column order
% Three values appear on each row of the file
for i=4:395
fprintf(fid, '%f %f %f\n', New(i,:));
end
fprintf(fid, '%f %f %f\n', New(4,:));
fprintf(fid, 'EndCurve\n');
fclose(fid);

%writematrix(New,sections,'Delimiter',' ');
%type tabledata.txt
end