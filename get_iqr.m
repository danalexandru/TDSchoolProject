%% Description
% This method computes the Interquartile range for each sensor of a given dataset
function [iqr_data] = get_iqr(dataset)
%% Get all necessary values from the dataset
X = dataset.X;

Ts = dataset.Ts;
freq = dataset.frequency;

X = remove_invalid_data(X);

%% Initialize the mean_freq variable
N = length(X);
if (Ts ~= 0)
    M = ceil(N / Ts);
else
    M = 1;
end

iqr_data = zeros(M, 4);

%% Get the medium frequency
if (Ts ~= 0)
    %% Ts ~= 0 case
    k = 0;
    while (k < M)
        begin = k*Ts + 1;
        if ((k + 1)*Ts < N)
            finish = (k + 1)*Ts;
        else
            finish = N;
        end
        
        group = X(begin : finish, :);
        
        iqr_data(k + 1, :) = [...
            iqr(group(:, 1)) ...
            iqr(group(:, 2)) ...
            iqr(group(:, 3)) ...
            iqr(group(:, 4)) ...
            ];
    
        %% Debug
        display(strcat('Iteration: ', num2str(k)));
        k = k + 1;
        
    end
else
    %% Ts = 0 cas
    iqr_data = [...
        iqr(X(:, 1)) ...
        iqr(X(:, 2)) ...
        iqr(X(:, 3)) ...
        iqr(X(:, 4)) ...
        ];
end

end
