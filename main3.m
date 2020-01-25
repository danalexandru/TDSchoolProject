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

%% Test ARX Model 
for i = 1 : length(healthy_data)

end


%% Plot the Fast Fourier Transform for each sensor of a healthy and broken dataset
dict_fft_data = containers.Map;
for i = 1 : length(broken_data) 
    %% Debug
%     i = 10;
    h_data = healthy_data(i).files;
    b_data = broken_data(i).files;

    struct_fft_current_data = struct;
    [X_fft_healthy, X_fft_broken] = get_fast_fourier_transform_plot(h_data, b_data);
    struct_fft_current_data.X_healthy = X_fft_healthy;
    struct_fft_current_data.X_broken = X_fft_broken;
    
    dict_fft_data(strcat('hb', b_data.name(2:end))) = struct_fft_current_data;
end

end
