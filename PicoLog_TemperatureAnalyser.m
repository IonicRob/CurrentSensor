%% T Logger Analysis
% By Robert J Scales
% Uses the txt files from the Pico T logger software to 
clear
TimeInSecOrHrs = input('Type in 1/0 for time axis in seconds/minutes: ');
TInCOrK = input('Type in 1/0 for T axis in Celcius/Kelvin: ');
%% Importer
opts = delimitedTextImportOptions("NumVariables", 2);
% Specify range and delimiter
opts.DataLines = [4, Inf];
opts.Delimiter = "\t";
% Specify column names and types
opts.VariableNames = ["Time", "Temperature"];
opts.VariableTypes = ["double", "double"];
% Specify file level properties
opts.ExtraColumnsRule = "ignore";
opts.EmptyLineRule = "read";
% Import the data
[file,path]=uigetfile('*.txt','Select the txt file for the logged data...');
filename=fullfile(path,file);
tloggertable = readtable(filename, opts);
tloggertable = table2array(tloggertable);
clear opts
disp('Data imported!');

%% Plotter
close all
if TimeInSecOrHrs==0
    X = tloggertable(:,1)/60;
    XLabel = 'Time (min)';
else
    X = tloggertable(:,1)/1;
    XLabel = 'Time (s)';
end
if TInCOrK==0
    Y = tloggertable(:,2)-(273.15);
    YLabel = 'Temperature (^{\circ}K)';
else
    Y = tloggertable(:,2)-0;
    YLabel = 'Temperature (^{\circ}C)';
end
FigTvst = figure('WindowState','Maximized');
figure(FigTvst);
YAx_U = round(max(Y),0)+1;
YAx_L = round(min(Y),0)-1;
Plot_Tvst = plot(X,Y,'x');
PlotMean = input('Type 1 to plot the mean value across all of the data: ');
PlotMovAvg = input('Type the number for the range of the the moving average; 0 to not have one: ');
if PlotMean==1
    disp('Select by clicking 2 points graphically the range to mean: ');
    [mean_x1 ,~] =ginput(1);
    [~,index1] = min(abs(X - mean_x1),[],'linear');
    hold on
    plot(X(index1),Y(index1),'rx');
    [mean_x2 ,~] =ginput(1);
    [~,index2] = min(abs(X - mean_x2),[],'linear');
    hold on
    plot(X(index2),Y(index2),'rx');
    hold on
    MeanT = mean(Y(index1:index2));
    Plot_Mean = yline(MeanT);
    Plot_Mean.Color = 'r';
    Plot_Mean.LineStyle = '--';
end
if PlotMovAvg~=0
    hold on
    MovingAvg = movmean(Y,PlotMovAvg);
    Plot_MovAvg = plot(X,MovingAvg,'b');
end
xlabel(XLabel);
ylabel(YLabel);
ylim([YAx_L,YAx_U]);
disp('Plotter done!');