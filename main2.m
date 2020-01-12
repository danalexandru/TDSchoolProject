%% Description
% This is the second version of the main script
function [] = main2()
%% Clear console
clc;
clear;

%% Get all datasets
[healthy_data, broken_data] = get_all_datasets();

%% Get the medium frequencies
dataset = healthy_data(1).files;
mean_freq = get_medium_frequencies(dataset);

%% Get the frequency magnitude
dataset = healthy_data(1).files;
freq_magn = get_frequencies_magnitude(dataset);

%% Get the kurtosis for each sensor
dataset = healthy_data(1).files;
kustosis_measure = get_kurtosis(dataset);

%% Get the skewness for each sensor
dataset = healthy_data(1).files;
skewness_measure = get_skewness(dataset);

%% Get the entropy of the sensors
dataset = healthy_data(1).files;
signal_entropy = get_signal_entropy(dataset);

%% Get the entropy of the sensors
dataset = healthy_data(1).files;
iqr_data = get_iqr(dataset);

end
