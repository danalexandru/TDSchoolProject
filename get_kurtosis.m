%% Description
% This method computes kurtosis for each sensor of a given dataset
function [kustosis_measure] = get_kurtosis(dataset)
%% Get all necessary values from the dataset
X = dataset.X;

Ts = dataset.Ts;
freq = dataset.frequency;


%% Initialize the mean_freq variable
N = length(X);
if (Ts ~= 0)
    M = ceil(N / Ts);
else
    M = 1;
end

kustosis_measure = zeros(M, 4);

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
        
        kustosis_measure(k + 1, :) = [...
            kurtosis(group(:, 1)) ...
            kurtosis(group(:, 2)) ...
            kurtosis(group(:, 3)) ...
            kurtosis(group(:, 4)) ...
            ];
    
        %% Debug
        display(strcat('Iteration: ', num2str(k)));
        k = k + 1;
        
    end
else
    %% Ts = 0 cas
    kustosis_measure = [...
        kurtosis(X(:, 1)) ...
        kurtosis(X(:, 2)) ...
        kurtosis(X(:, 3)) ...
        kurtosis(X(:, 4)) ...
        ];
end

end
