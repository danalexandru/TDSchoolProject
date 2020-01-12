%% Description
% This is the second version of the main script
function [] = main2()
%% Clear console
clc;
clear;

%% Get all datasets
[healthy_data, broken_data] = get_all_datasets();

%% Get the medium frequencies
dict_healthy_mean_freq = containers.Map;
dict_broken_mean_freq = containers.Map;

for i = 1 : length(healthy_data)
    dict_healthy_mean_freq(healthy_data(i).files.name) = get_medium_frequencies(healthy_data(i).files);
end

for i = 1 : length(broken_data)
    dict_broken_mean_freq(broken_data(i).files.name) = get_medium_frequencies(broken_data(i).files);
end

save('dict_healthy_mean_freq.mat', 'dict_healthy_mean_freq');
save('dict_broken_mean_freq.mat', 'dict_broken_mean_freq');

%% Get the frequency magnitude
dict_healthy_freq_magn = containers.Map;
dict_broken_freq_magn = containers.Map;

for i = 1 : length(healthy_data)
    dict_healthy_freq_magn(healthy_data(i).files.name) = get_frequencies_magnitude(healthy_data(i).files);
end

for i = 1 : length(broken_data)
    dict_broken_freq_magn(broken_data(i).files.name) = get_frequencies_magnitude(broken_data(i).files);
end

save('dict_healthy_freq_magn.mat', 'dict_healthy_freq_magn');
save('dict_broken_freq_magn.mat', 'dict_broken_freq_magn');

%% Get the kurtosis for each sensor
dict_healthy_kustosis_measure = containers.Map;
dict_broken_kustosis_measure = containers.Map;

for i = 1 : length(healthy_data)
    dict_healthy_kustosis_measure(healthy_data(i).files.name) = get_kurtosis(healthy_data(i).files);
end

for i = 1 : length(broken_data)
    dict_broken_kustosis_measure(broken_data(i).files.name) = get_kurtosis(broken_data(i).files);
end

save('dict_healthy_kustosis_measure.mat', 'dict_healthy_kustosis_measure');
save('dict_broken_kustosis_measure.mat', 'dict_broken_kustosis_measure');

%% Get the skewness for each sensor
dict_healthy_skewness_measure = containers.Map;
dict_broken_skewness_measure = containers.Map;

for i = 1 : length(healthy_data)
    dict_healthy_skewness_measure(healthy_data(i).files.name) = get_skewness(healthy_data(i).files);
end

for i = 1 : length(broken_data)
    dict_broken_skewness_measure(broken_data(i).files.name) = get_skewness(broken_data(i).files);
end

save('dict_healthy_skewness_measure.mat', 'dict_healthy_skewness_measure');
save('dict_broken_skewness_measure.mat', 'dict_broken_skewness_measure');

%% Get the entropy of the sensors
dict_healthy_signal_entropy = containers.Map;
dict_broken_signal_entropy = containers.Map;

for i = 1 : length(healthy_data)
    dict_healthy_signal_entropy(healthy_data(i).files.name) = get_signal_entropy(healthy_data(i).files);
end

for i = 1 : length(broken_data)
    dict_broken_signal_entropy(broken_data(i).files.name) = get_signal_entropy(broken_data(i).files);
end

save('dict_healthy_signal_entropy.mat', 'dict_healthy_signal_entropy');
save('dict_broken_signal_entropy.mat', 'dict_broken_signal_entropy');

%% Get the entropy of the sensors
dict_healthy_iqr_data = containers.Map;
dict_broken_iqr_data = containers.Map;

for i = 1 : length(healthy_data)
    dict_healthy_iqr_data(healthy_data(i).files.name) = get_iqr(healthy_data(i).files);
end

for i = 1 : length(broken_data)
    dict_broken_iqr_data(broken_data(i).files.name) = get_iqr(broken_data(i).files);
end

save('dict_healthy_iqr_data.mat', 'dict_healthy_iqr_data');
save('dict_broken_iqr_data.mat', 'dict_broken_iqr_data');

end
