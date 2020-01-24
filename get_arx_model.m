%% Description
% This function will return an ARX model based on the given training set
% and the valid set
function [dict_mode_arx] = get_arx_model(training_set, valid_set, Ts)
%% Check input parameters
if (nargin < 3)
    Ts = 30;
end

%% Convert the training set into an iddata mode
training_data = iddata(training_set.y, training_set.X, Ts);
valid_data = iddata(valid_set.y, valid_set.X, Ts);

[~, M] =  size(training_set.X);

%% Initialize model ARX structure
dict_mode_arx = containers.Map;

%% Get the ARX polynomial orders for each sensor
for i = 1 : M
    %% Estimate latency
%     nk = delayest(training_data(:,:,i),2,2,0,5,160000);
    nk = delayest(training_data(:,:,i));
    NN = struc(1:4, 1:4, nk);


    %% Get the ARX polynomial orders
    V = arxstruc(training_data(:,:,i), valid_data(:,:,i), NN);
    order = selstruc(V, 0);

    %% Append the new ARX model to the final result
    str = strcat('sensor_', num2str(i));
    dict_mode_arx(str) = arx(training_data(:,:,i), order);
end

end
