%% Description
% This is the main script from which the methods will be called
function [] = main()
%% Clear console
clc;
clear;

%% Get the training, valid and test sets
[dict_training_set, dict_valid_set, dict_test_set] = get_training_valid_test_sets();

%% Get sygnal processing method output
dict_ps_output = get_recursive_trend(dict_training_set, 5);

end
