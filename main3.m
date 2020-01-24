%% Description
% This is the second version of the main script
function [] = main3()
%% Clear console
clc;
clear;

%% Get all datasets

filename = 'split_datasets.mat';
[healthy_data, broken_data] = get_all_datasets(filename);

%% Get ARX Model
dict_all_arx_models = containers.Map;

for i = 1 : length(broken_data)
    data = combine_datasets(healthy_data(i).files, broken_data(i).files);
    dict_all_arx_models(data.name) = get_arx_model(data.training, data.valid, data.Ts);
end

end
