%% Description
% This function will return an ARX model based on the given training set
% and the valid set
function [mode_arx] = get_arx_model(dict_training_set, dict_valid_set, Ts)
%% Check input parameters
if (nragin < 3)
    Ts = 0.5;
end

%% Convert the training set into an iddata mode
training_data = iddata(dict_training_set('y'), dict_training_set('X'), Ts);
valid_data = iddata(dict_valid_set('y'), dict_valid_set('X'), Ts);

training_data_m = misdata(training_data);
valid_data_m = misdata(valid_data);

% trend = getTrend(training_data_m);
% training_data_m = detrend(training_data_m, trend);
% 
% trend = getTrend(valid_data_m);
% valid_data_m = detrend(valid_data_m, trend);

%% Estimate latency
% nk = delayest(training_data_m,2,2,0,5,160000);
NN = struc(1:4, 1:4, 0);

%% Get the ARX polynomial orders
V = arxstruc(training_data_m, valid_data_m, NN);
order = selstruc(V, 0);

mode_arx = arx(training_data_m, order);

end
