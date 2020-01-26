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
dict_healthy_arx_model_results = containers.Map;

for i = 1 : length(healthy_data)
    dict_current_arx_models = dict_all_arx_models(strcat('hb', healthy_data(i).files.name(2:end)));
    
    dict_prediction_results = containers.Map;
    for j = 1 : 4
        struct_prediction_results = struct;
        arx_model = dict_current_arx_models(strcat('sensor_', num2str(j)));

        struct_prediction_results.y_predicted = mean(filter(arx_model.B, arx_model.A, healthy_data(i).files.test.X(:, j)));
        struct_prediction_results.y_real = mean(healthy_data(i).files.test.y);
        struct_prediction_results.error = immse(healthy_data(i).files.test.y, filter(arx_model.B, arx_model.A, healthy_data(i).files.test.X(:, j)));
        
        dict_prediction_results(strcat('sensor_', num2str(j))) = struct_prediction_results;
    end
    dict_healthy_arx_model_results(healthy_data(i).files.name) = dict_prediction_results;
end

dict_broken_arx_model_results = containers.Map;
for i = 1 : length(broken_data)
    dict_current_arx_models = dict_all_arx_models(strcat('hb', broken_data(i).files.name(2:end)));

    dict_prediction_results = containers.Map;
    for j = 1 : 4
        struct_prediction_results = struct;
        arx_model = dict_current_arx_models(strcat('sensor_', num2str(j)));

        struct_prediction_results.y_predicted = mean(filter(arx_model.B, arx_model.A, broken_data(i).files.test.X(:, j)));
        struct_prediction_results.y_real = mean(broken_data(i).files.test.y);
        
        struct_prediction_results.error = immse(broken_data(i).files.test.y, filter(arx_model.B, arx_model.A, broken_data(i).files.test.X(:, j)));
        
        dict_prediction_results(strcat('sensor_', num2str(j))) = struct_prediction_results;       
    end
    dict_broken_arx_model_results(broken_data(i).files.name) = dict_prediction_results;
end

%% Plot the Fast Fourier Transform for each sensor of a healthy and broken dataset
dict_fft_data = containers.Map;
for i = 1 : length(broken_data) 
    %% Debug
    h_data = healthy_data(i).files;
    b_data = broken_data(i).files;

    struct_fft_current_data = struct;
    [X_fft_healthy, X_fft_broken] = get_fast_fourier_transform_plot(h_data, b_data);
    struct_fft_current_data.X_healthy = X_fft_healthy;
    struct_fft_current_data.X_broken = X_fft_broken;
    
    dict_fft_data(strcat('hb', b_data.name(2:end))) = struct_fft_current_data;
end

%% Plot the Fast Fourier Transform 2 for each sensor of a healthy and broken dataset
dict_fft_data = containers.Map;
for i = 1 : length(broken_data) 
    %% Debug
    h_data = healthy_data(i).files;
    b_data = broken_data(i).files;

    struct_fft_current_data = struct;
    [X_fft_healthy, X_fft_broken] = get_fast_fourier_transform_2_plot(h_data, b_data);
    struct_fft_current_data.X_healthy = X_fft_healthy;
    struct_fft_current_data.X_broken = X_fft_broken;
    
    dict_fft_data(strcat('hb', b_data.name(2:end))) = struct_fft_current_data;
end

%% Get the skewness for each sensor
dict_healthy_skewness_measure = containers.Map;
dict_broken_skewness_measure = containers.Map;

for i = 1 : length(healthy_data)
    X = [healthy_data(i).files.training.X; healthy_data(i).files.valid.X; healthy_data(i).files.test.X];
    y = [healthy_data(i).files.training.y; healthy_data(i).files.valid.y; healthy_data(i).files.test.y];
    
    healthy_data(i).files.X = X;
    healthy_data(i).files.y = y;
    dict_healthy_skewness_measure(healthy_data(i).files.name) = get_skewness(healthy_data(i).files);
end

for i = 1 : length(broken_data)
    X = [broken_data(i).files.training.X; broken_data(i).files.valid.X; broken_data(i).files.test.X];
    y = [broken_data(i).files.training.y; broken_data(i).files.valid.y; broken_data(i).files.test.y];
    
    broken_data(i).files.X = X;
    broken_data(i).files.y = y;
    dict_broken_skewness_measure(broken_data(i).files.name) = get_skewness(broken_data(i).files);
end

%% Plot the skeweness for each sensor
for i = 1 : length(broken_data)
    %% Debug
    X_healthy = dict_healthy_skewness_measure(healthy_data(i).files.name);
    X_broken = dict_broken_skewness_measure(broken_data(i).files.name);

    get_figures_results_plot(X_healthy, X_broken, broken_data(i).files.name, 'Skeweness');
    
end

%% Plot the histogram for each sensor
for i = 1 : length(broken_data)
    %% Debug
    X_healthy = [healthy_data(i).files.training.X; healthy_data(i).files.valid.X; healthy_data(i).files.test.X];
    X_broken = [broken_data(i).files.training.X; broken_data(i).files.valid.X; broken_data(i).files.test.X];
    
    get_histogram_figure_plot(X_healthy, X_broken, broken_data(i).files.name, 'Histogram');
    
end

%% Get the kurtosis for each sensor
dict_healthy_kustosis_measure = containers.Map;
dict_broken_kustosis_measure = containers.Map;

for i = 1 : length(healthy_data)
    X = [healthy_data(i).files.training.X; healthy_data(i).files.valid.X; healthy_data(i).files.test.X];
    
    dict_healthy_kustosis_measure(healthy_data(i).files.name) = [...
        kurtosis(X(:, 1)) ...
        kurtosis(X(:, 2)) ...
        kurtosis(X(:, 3)) ...
        kurtosis(X(:, 4)) ...
        ];
end

for i = 1 : length(broken_data)
    X = [broken_data(i).files.training.X; broken_data(i).files.valid.X; broken_data(i).files.test.X];
    
    dict_broken_kustosis_measure(broken_data(i).files.name) = [...
        kurtosis(X(:, 1)) ...
        kurtosis(X(:, 2)) ...
        kurtosis(X(:, 3)) ...
        kurtosis(X(:, 4)) ...
        ];
end

save_as_csv_files_2(dict_healthy_kustosis_measure, dict_broken_kustosis_measure, 'kurtosis');

%% Get the skewness for each sensor
dict_healthy_skewness_measure = containers.Map;
dict_broken_skewness_measure = containers.Map;

for i = 1 : length(healthy_data)
    X = [healthy_data(i).files.training.X; healthy_data(i).files.valid.X; healthy_data(i).files.test.X];
    
    dict_healthy_skewness_measure(healthy_data(i).files.name) = [...
        skewness(X(:, 1)) ...
        skewness(X(:, 2)) ...
        skewness(X(:, 3)) ...
        skewness(X(:, 4)) ...
        ];
end

for i = 1 : length(broken_data)
    X = [broken_data(i).files.training.X; broken_data(i).files.valid.X; broken_data(i).files.test.X];
    
    dict_broken_skewness_measure(broken_data(i).files.name) = [...
        skewness(X(:, 1)) ...
        skewness(X(:, 2)) ...
        skewness(X(:, 3)) ...
        skewness(X(:, 4)) ...
        ];
end

save_as_csv_files_2(dict_healthy_skewness_measure, dict_broken_skewness_measure, 'skewness');
end
