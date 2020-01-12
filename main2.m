%% Description
% This is the second version of the main script
function [] = main2()
%% Clear console
clc;
clear;

%% Get all datasets
load('datasets.mat');

%% Get the medium frequencies
dataset = healthy_data{1, 1};
mean_freq = get_medium_frequencies(dataset);

%% Get the frequency magnitude
dataset = healthy_data{1, 1};
freq_magn = get_frequencies_magnitude(dataset);

%% Get the kurtosis for each sensor
dataset = healthy_data{1, 1};
kustosis_measure = get_kurtosis(dataset);

%% Get the skewness for each sensor
dataset = healthy_data{1, 1};
skewness_measure = get_skewness(dataset);

%% Get the entropy of the sensors
dataset = healthy_data{1, 1};
signal_entropy = get_signal_entropy(dataset);

end
