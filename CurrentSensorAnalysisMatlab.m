cd_init = cd; % Initial directory

filter = {'*.csv','CSV Python Output Files (*.csv)'};

% This gets the file data for the sample.
[file,path,fileTypeIndex] = uigetfile(filter,'Select file(s) to import:','MultiSelect','off');
cd_load = path;

opts = delimitedTextImportOptions("NumVariables", 6);
opts.DataLines = [2, Inf];
opts.Delimiter = ",";
opts.VariableNames = ["Time (s)", "Bus Voltage (V)", "Shunt Voltage (mV)", "Load Voltage (V)", "Current (mA)", "Power (mW)"];
opts.VariableTypes = ["double", "double", "double", "double", "double", "double"];
opts.ExtraColumnsRule = "ignore";
opts.EmptyLineRule = "read";
opts.VariableNamingRule =  'preserve';
TableOuput = readtable(fullfile(path,file), opts);
clear opts

%%
clc
close all
TableArray = table2array(TableOuput(:,:));

cutOff = 502; % cut-off time
if isempty(cutOff)
    warning('No cut off value chosen...');
else
    [~, cutOff_index] = min(abs(cutOff-TableArray(:,1)));
    TableArray = TableArray(1:cutOff_index,:);
end


[N,edges,bin] = histcounts(TableArray(:,4),(0:1:ceil(max(TableArray(:,4)))));

windowstate = 'normal';

figure('WindowState',windowstate);

% subplot(1,2,1);
x = TableArray(:,4);
y = TableArray(:,5);
sz = 25;
c = linspace(1,length(x),length(x));
colormap cool;
IV_raw = scatter(x,y,sz,c,'s');
IV_raw.DisplayName = 'Raw';
title('Raw');
xlabel('Voltage (V)');
ylabel('Current (mA)');

% subplot(1,2,2);
hold on
x = TableArray(:,4);
kb = 2;
kf = 5;
y = movmean(TableArray(:,5),[kb,kf]);
sz = 30;
c = linspace(1,length(x),length(x));
colormap cool;
IV_movmean = scatter(x,y,sz,c,'filled');
IV_movmean.DisplayName = 'Mov. Ave.';
% hold on
% plot(x,y,'r');
title(sprintf('Moving Average - kb %d, & kf %d',kb,kf));
xlabel('Voltage (V)');
ylabel('Current (mA)');

hcb = colorbar;
hcb.Title;
hcb.Title.String = "Time (s)";
legend('Location','SouthEast');



figure('WindowState',windowstate);
subplot(2,1,1);
x = TableArray(:,1);
y = TableArray(:,5);
sz = 25;
c = linspace(1,10,length(x));
colormap cool;
scatter(x,y,sz,c,'filled');
title('I vs t');
xlabel('Time (s)');
ylabel('Current (mA)');

subplot(2,1,2);
x = TableArray(:,1);
y = TableArray(:,4);
sz = 25;
c = linspace(1,10,length(x));
colormap cool;
scatter(x,y,sz,c,'filled');
title('V vs t');
xlabel('Time (s)');
ylabel('Voltage (V)');

% Y = discretize(X,edges)