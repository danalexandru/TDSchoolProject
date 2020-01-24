%% Description
% This method returns all the healthy and broken datasets from the
% 'datasets'.mat file
function [healthy_data, broken_data] = get_all_datasets(dataset_name)
%% Check parameters
if (nargin < 1)
    dataset_name = 'all_datasets.mat';
end

%% Load the dataset 
S = load(dataset_name);

%% Split the dataset 
healthy_data = S.healthy_data;
broken_data = S.broken_data;

%% Split the dataset into broken/healthy subsets
healthy_data = cell2struct(healthy_data, {'files'}, 1);
broken_data = cell2struct(broken_data, {'files'}, 1);

end
