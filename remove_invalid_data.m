%% Description
% This method is used in order to remove any invalid data from the sendors data 
function [A] = remove_invalid_data(A)
nan_rows = any(isnan(A), 2);
minus_inf_rows = any(A == -inf, 2);
plus_inf_rows = any(A == inf, 2);
bad_rows = nan_rows | minus_inf_rows | plus_inf_rows;
A(bad_rows, :) = [];
end
