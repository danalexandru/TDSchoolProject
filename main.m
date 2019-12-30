%% Description
% This is the main script from which the methods will be called
function [] = main()
%% Clear console
clc;
clear;

%% Get the training, valid and test sets
[dict_training_set, dict_valid_set, dict_test_set] = get_training_valid_test_sets();

end
