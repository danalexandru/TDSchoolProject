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

end
