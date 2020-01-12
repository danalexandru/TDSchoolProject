%% Description
% This method saves the healthy and broken data returned by one of the
% matlab functions
function [] = save_as_csv_files(dict_healthy_data_results, dict_broken_data_results, method)
%% Retrieve file path
path = '.\csvs\Matlab Results\';
healthy_data_folder = [path 'Healthy Data\'];
broken_data_folder = [path 'BrokenTooth Data\'];

%% Save the healthy data results
keys = dict_healthy_data_results.keys;
for i = 1 : length(keys)
    key = keys(i);
    key = key{1, 1};
    csvwrite([healthy_data_folder method '\' key '.csv'], dict_healthy_data_results(key));
end

%% Save the broken data results
keys = dict_broken_data_results.keys;
for i = 1 : length(keys)
    key = keys(i);
    key = key{1, 1};
    csvwrite([broken_data_folder method '\' key '.csv'], dict_broken_data_results(key));
end

end
