%% Description
% This method retrieves the training, valid and test sets returned by the
% python 'Dataset' class
function [dict_training_set, dict_valid_set, dict_test_set] = get_training_valid_test_sets()
%% Load training set
load('training_set.mat');
dict_training_set = containers.Map;
dict_training_set('X') = X;
dict_training_set('y') = y;

%% Load valid set
load('valid_set.mat');
dict_valid_set = containers.Map;
dict_valid_set('X') = X;
dict_valid_set('y') = y;

%% Load test set
load('test_set.mat');
dict_test_set = containers.Map;
dict_test_set('X') = X;
dict_test_set('y') = y;

end
