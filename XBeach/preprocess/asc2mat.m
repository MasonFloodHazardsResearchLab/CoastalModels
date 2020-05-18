%% XBeach JIP tutorial: how to set-up a storm-impact model? 
% v0.1 Nov-15
clear all, close all, clc


%% 0. Define
destin = '/Users/tmiesse/work/FHRL/eeslr/modelling/gis/';

% Determine area of interest (not boundaries from XBeach grid, but close)
output_lon_w        = -75.968433; 
output_lon_e        = -75.960112;  
output_lat_n        =  37.125594;  
output_lat_s        =  37.1109013;  
output_delta_x      = .00001;
output_delta_y      = .00001;
% Determine size of grid cells
% output_delta_x      = 1;
% output_delta_y      = 1;
[output_X,output_Y] = meshgrid(output_lon_w:output_delta_x:output_lon_e, output_lat_n:-output_delta_y:output_lat_s);

%% 1. Load CRM

[input_Z_CRM, R_CRM]            = arcgridread_v2([destin,'mgb_es.asc']); % 

% Get grid information from input dataset     
[input_n_y, input_n_x]           = size(input_Z_CRM);
input_delta_x                   = R_CRM(2,1);
input_delta_y                   = R_CRM(1,2);
input_lon_w                     = R_CRM(3,1);
input_lon_e                     = R_CRM(3,1)+input_delta_x*(input_n_x-1);
input_lat_n                     = R_CRM(3,2);
input_lat_s                     = R_CRM(3,2)+input_delta_y*(input_n_y-1);
[input_X_CRM, input_Y_CRM]          = meshgrid(input_lon_w:R_CRM(2,1):input_lon_e,input_lat_n:R_CRM(1,2):input_lat_s);
% Griddata to output grid
output_Z_CRM                     = griddata(input_X_CRM, input_Y_CRM,input_Z_CRM, output_X, output_Y);


%%

figure; pcolor(input_X_CRM ,input_Y_CRM , input_Z_CRM); shading interp;  

figure;pcolor(output_X,output_Y,output_Z_CRM);shading interp;


%%

long = reshape(output_X2,[300*1697,1]);
lat = reshape(output_Y2,[300*1697,1]);
elev = reshape(output_Z_CRM2,[300*1697,1]);

TX=[long lat elev];

save MGB.dat TX -ascii -double




%%
%save(['Z:\Project_NFWF\3_Modeling\2_xBeach\magothy_bay_attempt\MGB_bathy.mat_files\','mgb_bathy_standard_real.mat'],
%('output_X2'),('output_Y2'),('output_Z_CRM2'));

%%
