%%
clear; clc;


%% Load model results


root = 'Z:\Project_TNC\5_Modeling\X-Beach\equations\outputs\drag3\';
xbo=xb_read_output(root);
d1 = xb_read_output('Z:\Project_TNC\5_Modeling\X-Beach\equations\outputs\drag1\');
d3 = xb_read_output('Z:\Project_TNC\5_Modeling\X-Beach\equations\outputs\drag3\');
d4 = xb_read_output('Z:\Project_TNC\5_Modeling\X-Beach\equations\outputs\drag4\');
d5 = xb_read_output('Z:\Project_TNC\5_Modeling\X-Beach\equations\outputs\drag5\');
d6 = xb_read_output('Z:\Project_TNC\5_Modeling\X-Beach\equations\outputs\drag6\');
d7 = xb_read_output('Z:\Project_TNC\5_Modeling\X-Beach\equations\outputs\no_veg\');
xbo2=xbo.data(1).value;
t           =squeeze(xbo2.data(21).value);
t_length    =length(t);
t_end       =3;
%%
 for ii=t_end
     H          =squeeze(xbo.data(21).value(ii,:));
     zs         =squeeze(xbo.data(43).value(2,:));
     zb         =squeeze(xbo.data(38).value(ii,:));
%      sigm       =squeeze(xbo.data(14).value(ii,:));
     cd       =squeeze(xbo.data(4).value(ii,:));
     x          =squeeze(xbo2.data(18).value);
     y          =squeeze(xbo2.data(19).value);

 end
h1 = squeeze(d1.data(21).value(t_end,:));
h3 = squeeze(d3.data(21).value(t_end,:));
h4 = squeeze(d4.data(21).value(t_end,:));
h5 = squeeze(d5.data(21).value(t_end,:));
h6 = squeeze(d6.data(21).value(t_end,:));
h7 = squeeze(d7.data(21).value(t_end,:));
%zs = squeeze(d1.data(21).value(t_end,:));
x_loc1      =18;   % staiton 2
x_loc2      =30;   % staiton 2
x_loc3      =45;   % station 3
x_loc4      =79;   % station 4
for i=1
    for ii=1:90
        if fliplr(zb(i,ii))>.03
            veg_h(i,ii)=.4227;
        end
        if fliplr(zb(i,ii))>0 && fliplr(zb(i,ii))<.25
            veg_h(i,ii)=.3;
        end
        if fliplr(zb(i,ii))<=0
            veg_h(i,ii)=0;
        end
        if fliplr(zb(i,ii))>1.25
            veg_h(i,ii)=.1;
        end
    end
end
station = [102/255 153/255 153/255];
baseline=-2;
index=1:90;
brown= [191/255 128/255 64/255];
green = [51/255 102/255 0];
purple = [153/255,0,1];
C=figure;
B(1)=subplot(2,1,1)
    C(1)=plot(x,h1,'-b'); hold on
    C(2)=plot(x,h3,'-c'); hold on
    C(3)=plot(x,h4,'-r'); hold on
    C(4)=plot(x,h5,'-g'); hold on
    C(5)=plot(x,h6,'-m'); hold on
    C(20) = plot(x,h7,'Color',green); hold on
    C(6)=plot(x(1,x_loc1),0.194,'.','Color',purple,'MarkerSize',20); hold on 
    text(x(1,x_loc1)-2.5,0.2+0.01,'Station 1')
%     C(3)=plot(x(1,x_loc2),fliplr(zb(1,x_loc2)),'* r'); hold on 
    C(7)=plot(x(1,x_loc2),0.192,'.','Color',purple,'MarkerSize',20); hold on 
    text(x(1,x_loc2)-3,0.187,'Station 2')
    C(8)=plot(x(1,x_loc4),0.0041,'.','Color',purple,'MarkerSize',20); hold on 
    text(x(1,x_loc4)-1.5,0.0041+0.04,'Station 4')
    ylabel('H_{S} (m)')
    title('September 18, 2018')
    set(gca,'xtick',[])
    set(findall(gca, 'Type', 'Line'),'LineWidth',1.5);
    set(gca,'LooseInset',get(gca,'TightInset')); 
    set(gcf,'color','w');
    axis([10 95 -0.001 0.35]);
B(2)=subplot(2,1,2)
    C(9)=plot(fliplr(x),fliplr(zb(1,:)),'Color',brown);hold on
    C(12)=plot(fliplr(x),fliplr(zs(1,:)),'Color', [0 0.6 1]);hold on
    C(11)=fill(fliplr(x(index([1 1:end end]))),...
                [baseline fliplr(zs(index)) baseline],...
                [0, 0.6, 1],'EdgeColor','none');
    C(9)=fill(fliplr(x(index([1 1:end end]))),...
                [baseline fliplr(zb(index)) baseline],...
                brown,'EdgeColor','none'); hold on
    ylabel('Elevation at NAVD88 (m)')
    for j = 1:length(x)
        C(10)=plot([fliplr(x(j)),fliplr(x(j))],[fliplr(zb(j)) fliplr(zb(j))+veg_h(j)],'Color',[76 180 0]/255);hold on
        set(C(10),'LineWidth',1.15);
    end
    set(findall(gca, 'Type', 'Line'),'LineWidth',1.5);
    set(gca,'LooseInset',get(gca,'TightInset')); 
    set(gcf,'color','w');
    axis([10 95 -2 2]);
    legend([C(1),C(2),C(3),C(4),C(5),C(20)],'Ozeren','Juan Qre','Juan Qkc','Anderson and Smith','Jadhav','No vegetation','Location','NorthEast');
    xlabel('Cross Shore Distance (m)')
	set(B(1),'Position', [0.05 0.525 .9425 .45]);
	set(B(2),'Position', [0.05 0.061 .9425 .45]);




%%
date1=datetime('now');

delta_t=datenum(date1);
delta_t=delta_t-hours(2);
delta_t2(1:216)=delta_t+minutes(1:20:4320);
%date2=date1-hours(1:2);
datestr(delta_t2(1:216),'mm/dd/yyyy HH:MM');

%%
 for ii=1
     H          =squeeze(xbo.data(9).value(ii,:));
     zs         =squeeze(xbo.data(34).value(ii,:));
     zb         =squeeze(xbo.data(29).value(ii,:));
     sigm       =squeeze(xbo.data(14).value(ii,:));
     Dveg       =squeeze(xbo.data(4).value(ii,:));
     x          =squeeze(xbo2.data(18).value);
     y          =squeeze(xbo2.data(19).value);
     t          =squeeze(xbo2.data(21).value);
 end
%%
baseline=-2;
index=1:90;
brown= [.8 .8 0.6];
blue2=[0 0.3 1];
C=figure;
    C(1)=plot(x,H,'c');  hold on
    C(2)=plot(x,zs,'b'); hold on
    C(3)=plot(x,zb,'k'); hold on
    C(4)=fill(x(index([ 1 1:end end])),...
                [baseline H(index) baseline],...
                blue2,'EdgeColor','none');
    C(5)=fill(x(index([ 1 1:end end])),...
                [baseline zs(index) baseline],...
                'b','EdgeColor','none');
    C(6)=fill(x(index([1 1:end end])),...
                [baseline zb(index) baseline],...
                brown,'EdgeColor','none');
    
 axis([-90 0 -1.5 2]);

 
 
 
 %%
  veg_input=input('input 1 if there is vegetation or 0 if there is not: ');
if veg_input==1
for i=1
    for ii=1:90
        if fliplr(zb(i,ii))>.03
            veg_h(i,ii)=.4227;
        end
        if fliplr(zb(i,ii))>0 && fliplr(zb(i,ii))<.25
            veg_h(i,ii)=.3;
        end
        if fliplr(zb(i,ii))<=0
            veg_h(i,ii)=0;
        end
        if fliplr(zb(i,ii))>1.25
            veg_h(i,ii)=.1;
        end
    end
end
end
 
%%


%   Call the individual outputs from xbo 

        
% vid_path=('Z:\Project_NFWF\3_Modeling\2_xBeach\magothy_bay_attempt\Calibration_figures\');
% cd(vid_path);
% video=VideoWriter('scale_correction','MPEG-4');
% video.FrameRate=4;
% open(video);
% t_end=length(t);
switch veg_input
    case 1
         for i=50:55
          baseline=-2;
            index=1:90;
            brown= [0.6 0.4 .25];
            blue2=[0 0.2 .8];   
         if i<3030
            H1          =squeeze(xbo.data(9).value(i,:));
            zs1         =squeeze(xbo.data(34).value(i,:));
            zb1         =squeeze(xbo.data(29).value(i,:));
            sigm1         =squeeze(xbo.data(14).value(i,:));
            Dveg1          =squeeze(xbo.data(4).value(i,:));
            x1          =squeeze(xbo2.data(18).value);
            y1          =squeeze(xbo2.data(19).value);
            waves = (H1+zs1);

        A=figure('units','normalized','outerposition',[0 0 1 1]);
        
        A(1)=plot(x1,H1+zs1,'c'); hold on
        A(2)=plot(x1,zs1,'b'); hold on
%         A(3)=plot(x1,sqrt(u1.^2+v1.^2),'r');hold on
        A(4)=plot(x1,zb1,'k'); hold on
        for j = 1:length(x1)
            A(5)=plot([x1(j),x1(j)],[zb1(j) zb1(j)+veg_h(j)],'Color',[76 180 0]/255);
            set(A(5),'LineWidth',1.15);
        end
        A(6)=fill(x1(index([ 1 1:end end])),...
                [baseline waves(index) baseline],...
                 blue2,'EdgeColor','none'); alpha(.5)                     
        A(7)=fill(x1(index([ 1 1:end end])),...
                [baseline zs1(index) baseline],...
                'b','EdgeColor','none'); alpha(.5)                
        A(8)=fill(x1(index([1 1:end end])),...
                [baseline zb1(index) baseline],...
                brown,'EdgeColor','none');
            
%        A(9)=plot(x1,sqrt(u2.^2+v2.^2),'r');hold on
        %set(findall(gca, 'Type', 'Line'),'LineWidth',1.25);
        legend([A(1),A(2),A(4), A(5)],'waves','tide','total velocity','bathymetry','vegetation','Location','NorthWest');
        set(A(1),'LineWidth',1.75);
        set(A(2),'LineWidth',1.75);
%        set(A(3),'LineWidth',1.75);
        set(A(4),'LineWidth',1.75);
 %       set(A(9),'LineWidth',1.75);
 axis([-90 0 -1.5 2]);
        xlabel('length (m)');
        ylabel('elevation (m)');
%         ax =gca;
%         outerpos = ax.OuterPosition;
%         ti = ax.TightInset;
%         left = outerpos(2) + ti(1);
%         bottom = outerpos(2)*(5/2) + ti(2);
%         ax_width = outerpos(3) - ti(2);
%         ax_height = outerpos(3)*(10/11) - ti(4);
%         ax.Position = [left bottom ax_width ax_height];
%         str=strcat({'mgb'; datestr(delta_t2(i),'mm-dd-yyyy HH')});
%         title(str,'FontSize',16,'Fontweight','bold');
%         F(i)=getframe(i);
%         writeVideo(video,F(i));
         else
             break;
         end
         end
end
%close(video);

%%
fig=figure('units','normalized','outerposition',[0 0 1 1]);
movie(fig,F,1000);

