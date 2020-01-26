%% Description
% This method saves the healthy and broken data returned by one of the
% matlab functions
function [] = save_as_csv_files_2(dict_healthy_data_results, dict_broken_data_results, method)
%% Retrieve file path
path = '.\csvs\Matlab Results\Signal Processing\';

%% Create matrix results
keys_length = (length(dict_healthy_data_results.keys) + length(dict_broken_data_results.keys))/2;

healthy_keys = dict_healthy_data_results.keys;
broken_keys = dict_broken_data_results.keys;

matrix_result = [];
for i = 1 : keys_length
    healthy_key = healthy_keys(i);
    broken_key = broken_keys(i);

    healthy_key = healthy_key{1, 1};
    broken_key = broken_key{1, 1};
    
    matrix_result = [...
        matrix_result;...
        [(i - 1) dict_healthy_data_results(healthy_key)];...
        [(i - 1) dict_broken_data_results(broken_key)]...
        ];
end

%% Save as csv
csvwrite([path method '.csv'], matrix_result);

end
