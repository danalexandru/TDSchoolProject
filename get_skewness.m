%% Description
% This method computes skewness for each sensor of a given dataset
function [skewness_measure] = get_skewness(dataset)
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

skewness_measure = zeros(M, 4);

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
        
        skewness_measure(k + 1, :) = [...
            skewness(group(:, 1)) ...
            skewness(group(:, 2)) ...
            skewness(group(:, 3)) ...
            skewness(group(:, 4)) ...
            ];
    
        %% Debug
        display(strcat('Iteration: ', num2str(k)));
        k = k + 1;
        
    end
else
    %% Ts = 0 cas
    skewness_measure = [...
        skewness(X(:, 1)) ...
        skewness(X(:, 2)) ...
        skewness(X(:, 3)) ...
        skewness(X(:, 4)) ...
        ];
end

end
