%% Description
% This method combines one healthy dataset with one broken one (considering
% it is a dataset with the training, valid, test split already made
function [data] = combine_datasets(h_data, b_data)
%% Check parameters
if (~strcmp(h_data.name(2:end), b_data.name(2:end)))
    data = {};
    return;
end

%% Combine sets
data = struct;

data.name = strcat('hb', b_data.name(2:end));
data.Ts = b_data.Ts;
data.frequency = b_data.frequency;

%% Combine training sets
data.training = struct;

data.training.X = [h_data.training.X; b_data.training.X];
data.training.y = [h_data.training.y; b_data.training.y];

%% Combine valid sets
data.valid = struct;

data.valid.X = [h_data.valid.X; b_data.valid.X];
data.valid.y = [h_data.valid.y; b_data.valid.y];

%% Combine test sets
data.test = struct;

data.test.X = [h_data.test.X; b_data.test.X];
data.test.y = [h_data.test.y; b_data.test.y];
    
end