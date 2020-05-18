%%      Magothy Bay code to create parameter file for xbeach
% This code generates parameters for xbeach in 1d. There are 4 transects to
% choose from that represent the real transects out in the field.
% It is similar to the 2d parameter codes created and it uses similar
% settings such as:
%           -   waves
%           -   tide
%           -   vegetation
%           -   wind

% Tyler ( Not Taylor) worked on this script ( Say Thank you ) 
clear all; clc;

%%      Define Path Directory
% This helps with keeping everything in order instead of writing the file
% path multiple times

destin          = 'Z:\Users\Tyler\projects\TNC\2d\test2\';
destin2         = 'Z:\Project_TNC\5_Modeling\Deal_dem\';

xs = importdata('Z:\Project_TNC\5_Modeling\Deal_dem\c_j_transect1_v3.txt');
% B. Model
dxmin           = 2;
dymin           = 2;
outputformat    = 'netcdf';

%%      Call the topo/bathy file 
cd(destin2)
load 'deal_dem_v2.mat'
x2=(output_X);
z2=(output_Z_CRM2);
y2=output_Y;

%%      Plot of the original topo/bathy 
% this may be used to determine the transect points. If it is used you must
% right down the grid in the y component point to have consistancy.
% 
z = squeeze(zb(1,:,:));
figure;
pcolor(x,y,z);hold on
shading interp; colormap jet
colorbar
% title('Bathymetry of Magothy Bay');
[x1,y1]=ginput(1);
close;

[num, idx]=min(abs(x(1,:)-x1));
[num2, idy]=min(abs(y(:,2)-y1)); 

%%      determine the tide either use data files or xbeach default    

tide=importdata('WLFort63.txt');

tide_h(:,1)=tide.textdata(4:2:end,2);
tide_t(:,1)=tide.textdata(3:2:end,2);

tide_height=str2double(tide_h(:,1));
tide_time=str2double(tide_t(:,1));
tide_time(1:end,1)=3600;
for i=1:length(tide_time(1:(end-1),1))
    tide_time(i+1,1)=tide_time(i,1)+3600;
end

%%      Generate the waves 

 xb_wave=xb_generate_waves('Hm0',0.73,'gammajsp',3.3,'s',10,...
                            'mainang',90,'fnyq',.45,'Tp',4.45);   
    
%%    Generate the tide

  xb_tide=xb_generate_tide('time',tide_time,'front',tide_height);    

%%    Generate the settings for xbeach to follow

xb_set=xb_generate_settings('outputformat',outputformat,... 
        'thetamin',180,'thetamax',360,'dtheta',90,'dtheta_s',5,...
        'instat','jons','morfac', 1,'posdwn',-1,'avalanching',0,...
        'morstart', 0,'CFL', 0.4,'front', 'abs_2d','random',0,...
        'back', 'abs_2d','left','neumann','right','neumann','mpiboundary','auto',...
        'thetanaut', 1,'zs0',1.5,'single_dir',0,...
        'tstop', 259201,'tstart', 0,...
        'tint', 259200,'tintm',360,'tintg',259200,'epsi',-1,'facua',0.300,'bedfriction', 'manning',...
        'meanvar',{'zb', 'zs', 'H','u','v','sigm'} ,...
        'globalvar',{'zb', 'zs','H','u','v','sigm'});


%%      Generate the bathy for Tansect 
xb_bathy=xb_generate_bathy('x',x,'y',y,'z',z,'optimize',true,...
    'xgrid',{'dxmin',dxmin},'ygrid',{'dymin',dymin},'crop',false,...
    'world_coordinates',true,'rotate',false,'finalise', {'zmin',-2.5});


x = xs.data(:,1);
z = xs.data(:,2);
z2=z;
plot(x,z)
layer(1:67,1) = 1;
layer(43,1) = 0;
layer(44,1) = 0;
layer(45,1) = 0;
% x(:,1)     = [0:0.5:104];
% z(:,1)     = [0:0.5:104]+0.77;
% x     = fliplr(x);
% z     = fliplr(z);

t1 = importdata([destin2,'c_j_transect1_v3.txt']);
x = t1.data(:,1);
z = t1.data(:,2);
[xgrid,zgrid]=xb_grid_xgrid(x,z,'dxmin',0.5);
layer2(1,1:199) = 1;
layer2(1,69) = 0;
layer2(1,70) = 0;
layer2(1,71) = 0;
layer2(1,72) = 0;

%[xgrid,zgrid]=xb_grid_xgrid(x2,z2);
xb_bathy=xb_generate_bathy('x',xgrid,'y','z',zgrid,...
    'crop',false,'optimize',false,...
    'rotate',false);


%%      Fine tune the grid 
% ygrid2                   = xs_get(xb_bathy,'yfile.yfile');
xgrid2                   = xs_get(xb_bathy,'xfile.xfile');
ygrid2                   = xs_get(xb_bathy,'yfile.yfile');
zgrid2                   = xs_get(xb_bathy,'depfile.depfile');
figure;
pcolor(xgrid2,ygrid2,zgrid2);hold on
shading interp; colormap jet
colorbar

% id1 = find(zgrid2 > 1.5);
% for i = 1:length(id1)
%     zgrid2(id1(i)) = 1.5;
% end
xb_bathy                         = xs_set(xb_bathy, 'yfile.yfile', y);
xb_bathy                         = xs_set(xb_bathy, 'xfile.xfile', x);
xb_bathy                         = xs_set(xb_bathy, 'depfile.depfile', squeeze(zb(1,:,:)));
%%      check with wave height and water celerity graph
Tp=4.45;
zs0=1.5;
[c cg n, k] = wavevelocity(Tp,zs0-zgrid2(1));


%%

 


%%
figure;
plot(xgrid2,zgrid2);%shading flat;colorbar;
%%      Create Vegetation Map
xveg(1:201,1:397) = 0;
for i=1:201
    for ii=1:397
        if zgrid2(i,ii)>.08
            xveg(i,ii)=1;
            veg_h(i,ii)=.4319;
        end
        %if zgrid2(i,ii)>0
        %    xveg(i,ii)=1;
        %    veg_h(i,ii)=.2;
        %end
    end
end

nsec  =   1;               % number of vertical sections (only for mangrroves)
ah    =  [.55];    % vegetation height of each section (m) - [roots -> trunk -> canopy]
bv    =  [.02]; % stem diameter / blade width (m)
N     =  [200];      % density (units/m2)
Cd    =  [-3];


xb_veg=xb_generate_settings('vegetation',1,'veggiefile','vegetation.txt','veggiemapfile','spartina_map.txt');

%%
destout = 'Z:\Project_TNC\5_Modeling\X-Beach\equations\inputs\';
cd(destout)
% wave_h=0;
% tide  = 1.0043;
N = 649.6;
Cd = -6;
ah = 0.4319;
bv    = 0.00438;
tide = 1.5;
lazy = fopen(['Z:\Project_TNC\5_Modeling\X-Beach\equations\inputs', '\copy.sh'],'wt');
lazier = fopen(['Z:\Project_TNC\5_Modeling\X-Beach\equations\inputs', '\auto_simulate.sh'],'wt');
fprintf(lazy,'%s\n','#!bin/bash');
fprintf(lazier,'%s\n','#!bin/bash');


%%      Plot the initial bathy grid with the vegetation
    for ii=1:6
        %tide=tide+.25;
    %    wave_h=0.4290;
    %for iii=1:2

%         wave_h2= wave_h*100;
        Cd2 = Cd*-1;
        str = ([destout,'drag',num2str(Cd2)]);
        str2= (['test','/','drag',num2str(Cd2)]);
        mkdir(str);
%     cd(str)
%         xb_wave=xb_generate_waves('Hm0',wave_h,'gammajsp',3.3,'s',10,'Tp',2.828,...
%                             'mainang',90,'fnyq',.45);   

        xb_set=xb_generate_settings('outputformat',outputformat,... 
        'thetamin',0,'thetamax',180,'dtheta',180,'dtheta_s',5,'xori',0,...
        'instat','jons','taper',1,'morfac', 1,'posdwn',-1,'avalanching',0,...
        'morstart', 0,'CFL', 0.2,'front', 'abs_1d','random',0,...
        'back', 'abs_1d','left','neumann','right','neumann','mpiboundary','auto',...
        'thetanaut', 1,'zs0',tide,'single_dir',0,...
        'tstop', 3601,'tstart', 0,'alpha',0.005,...
        'tintm',1200,'tintg',1200,'epsi',-1,'facua',0.300,'bedfriction', 'manning',...
        'meanvar',{'zb', 'zs', 'H','urms','Cdrag','Qb','E','sigm','Dveg','Df'} ,...
        'globalvar',{'zb', 'zs','H','urms','Cdrag'});

        xb_set                     = xs_set(xb_set, 'bedfricfile', xs_set([], 'bedfricfile', bedfrict)); 

        nsec  =  1;               % number of vertical sections (only for mangrroves)
                                  % vegetation height of each section (m) - [roots -> trunk -> canopy]
                                  % stem diameter / blade width (m)
                                  % density (units/m2)
        drag  = Cd;
        xb_veg=xb_generate_settings('vegetation',1,'veggiefile','vegetation.txt','veggiemapfile','spartina_tran.txt');


        xb_tot=xs_join(xb_bathy,xb_veg,xb_set);
        xb_write_input([destin, '\params.txt'], xb_tot)

        fid = fopen([destin,'\vegetation.txt'],'w');
        fprintf(fid,'%s\n','spartina.txt');
        fclose(fid);

        fid = fopen([destin, '\spartina.txt'],'w');
            fprintf(fid,'%s\n', ['nsec = ', num2str(nsec)]);
            fprintf(fid,'%s\n', ['ah = ',num2str(ah)]);
            fprintf(fid,'%s\n', ['bv = ',num2str(bv)]);
            fprintf(fid,'%s\n', ['N  = ',num2str(N)]);
            fprintf(fid,'%s\n', ['Cd = ',num2str(1)]);
        fclose(fid);

%             fprintf(lazy,'%10s\n',['cp /home/vse/Neptune_work_folder/XBeach/validation/Jose xbeach ','/home/vse/Neptune_work_folder/XBeach/validation/Jose/',str2]);
            fprintf(lazier,'%10s\n',['cd /home/admin/neptune_work/users/tyler/xbeach/juan_eqn_deal/equations/',str2]);
            fprintf(lazier,'%10s\n','/home/admin/neptune_work/realtime/xbeach/trunkv1/src/xbeach/xbeach -n 1');
    
            dlmwrite([destin, '\spartina_tran.txt'],xveg,'precision',3);

            bedfric                   = xs_get(xb_tot,'bedfricfile.bedfricfile');
            dlmwrite([str, '\bedfricfile.txt'],bedfric,'precision',6);
%             if wave_h >= 2
%                 break
%             end
%         wave_h = wave_h+0.001;
%    end
    Cd = Cd + 1;
    end


%%
%   this has been figurered out. Since the way the vegetation is created it
%   is already formatted for the grid. Just adjust the values so the
%   represent the vegetation height!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
water=xgrid2*0+.35;
figure;

plot(xgrid2(1,1:85),water(1,1:85),'c'); hold on
plot(xgrid2,zgrid2,'k');hold on
%axis([1600 2150 -1 2]);
for j = 1:length(xgrid2)
    plot([xgrid2(j),xgrid2(j)],[zgrid2(j) zgrid2(j)+veg_h(j)],'Color',[76 153 0]/255);
end

%%      create bedfriction map
% 
% for i=1
%     for ii=1:732
%         if xveg(i,ii)==1
%             bedfrict(i,ii)=.012;
%         else
%             bedfrict(i,ii)=0.02;
%         end
%     end
% end
bedfrict(1:144,1:353)=0;
for i=1:144
    for ii=1:353
        if zgrid2(i,ii)<0
            bedfrict(i,ii)=.02;
        end
        if zgrid2(i,ii)>=0
            bedfrict(i,ii)=.01;
        end
    end
end

xb_set                     = xs_set(xb_set, 'bedfricfile', xs_set([], 'bedfricfile', bedfrict)); 
%%
[xc yc dim dir idx] = xb_get_coastline(xgrid2, ygrid2, zgrid2);

figure;
plot(xc,yc)
%% Create the Parameter file and any other necessary file to run xbeach
% *reminder a linux system cannot read a map file created by using the
% fprint function instead use the dlmwrite with a precision of 3.
destout = 'Z:\Users\Tyler\projects\TNC\modeling\2d\april23_inputs\';
% cd(destin);
xb_tot=xs_join(xb_bathy,xb_set);
xb_write_input([destout, '\params.txt'], xb_tot)
% fid = fopen([destout,'\filelist.txt'], 'w');
%     fprintf(fid,'%s\n', 'FILELIST');
%         fprintf(fid, '%10i%10.4f%50s\n', 36000, 36000, ('wave001.txt'));      
% fclose(fid);
fid = fopen([destout,'\vegetation.txt'],'w');
    fprintf(fid,'%s\n','spartina.txt');
fclose(fid);
fid = fopen([destout, '\spartina.txt'],'w');
     fprintf(fid,'%s\n', ['nsec = ', num2str(nsec)]);
     fprintf(fid,'%s\n', ['ah = ',num2str(ah)]);
     fprintf(fid,'%s\n', ['bv = ',num2str(bv)]);
     fprintf(fid,'%s\n', ['N  = ',num2str(N)]);
     fprintf(fid,'%s\n', ['Cd = ',num2str(Cd)]);
fclose(fid);
% fid = fopen([destout, '\spartina2.txt'],'w');
%      fprintf(fid,'%s\n', ['npts = ', num2str(npts2)]);
%      fprintf(fid,'%s\n', ['zv = ',num2str(zv2)]);
%      fprintf(fid,'%s\n', ['bv = ',num2str(bv2)]);
%      fprintf(fid,'%s\n', ['N  = ',num2str(N2)]);
%      fprintf(fid,'%s\n', ['Cd = ',num2str(Cd2)]);
xveg2 = single(xveg);
dlmwrite([destout, '\spartina_map.txt'],xveg,'precision',3);
save([destout '\spartina_map2.txt'],'xveg2','-ascii');%
bedfric                   = xs_get(xb_tot,'bedfricfile.bedfricfile');
dlmwrite([destout, '\bedfricfile.txt'],bedfric,'precision',3);


