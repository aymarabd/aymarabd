%Author: Aymara Baumann Duran
%%
clear all;clc
%f=blade('sections','airfoil_name.txt',twist,c,r)
%%
n=17;
sections=['a':'q'];
airfoil    = ['DU C1.txt' 'DU C2.txt' 'DU C2.txt' 'DU 40.txt' 'DU 40.txt' 'DU 35.txt' 'DU 35.txt' 'DU 30.txt' 'DU 30.txt' 'DU 25.txt' 'DU 21.txt' 'DU 21.txt' 'DU 21.txt' 'NA CA.txt' 'NA CA.txt' 'NA CA.txt' 'NA CA.txt'];
twist      =[13.31        13.31       14          10          7           4           2           1            0.8        0.3         0           -0.3         -1          -1.53      -2           -3         -4];
c          =[3.0975       3.3687      3.6487      7.9800      8.1375      7.8050      7.4375      7.0175       6.5625     6.1250      5.7050      5.2675       4.8300      4.4100      4.0425      3.6575     2.4850];
r          =[5.0225       9.8000      14.5775     20.5625     27.7375     34.9125     42.0875     49.2625      56.4375    63.6125     70.7875     77.9625      85.1375     92.3125     98.2975     103.0750   107.8525];
c_max=c(4);
figure(2)
plot(r(:),c(:),'-');
xlim([0 110])
ylim([0 110])

fid = fopen('complete_blade', 'w');
for i=1:3
New=(Copy_of_blade(sections(i),airfoil(1,1+9*(i-1):9+9*(i-1)),c(i),r(i),c_max));


% print to file
fprintf(fid, 'StartCurve\n');
 for i=4:395
   fprintf(fid, '%f %f %f\n', New(i,:));
 end
fprintf(fid, '%f %f %f\n', New(4,:));
fprintf(fid, 'EndCurve\n');

end



for i=4:n
New=(blade(sections(i),airfoil(1,1+9*(i-1):9+9*(i-1)),twist(i),c(i),r(i),c_max));

% print to file
fprintf(fid, 'StartCurve\n');
 for i=4:395
   fprintf(fid, '%f %f %f\n', New(i,:));
 end
fprintf(fid, '%f %f %f\n', New(4,:));
fprintf(fid, 'EndCurve\n');

end

fclose(fid);

