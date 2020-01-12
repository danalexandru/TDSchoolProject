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

end
