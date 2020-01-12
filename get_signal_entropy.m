%% Description
% This method computes the entropy of the sensors of a given dataset
function [signal_entropy] = get_signal_entropy(dataset)
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

signal_entropy = zeros(M, 4);

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
        
        group_normalized = [...
            group(:, 1)/max(abs(group(:, 1))) ...
            group(:, 2)/max(abs(group(:, 2))) ...
            group(:, 3)/max(abs(group(:, 3))) ....
            group(:, 4)/max(abs(group(:, 4))) ...
            ];
        
        signal_entropy(k + 1, :) = [...
            entropy(group_normalized(:, 1)) ...
            entropy(group_normalized(:, 2)) ...
            entropy(group_normalized(:, 3)) ...
            entropy(group_normalized(:, 4)) ...
            ];

        %% Debug
        display(strcat('Iteration: ', num2str(k)));
        k = k + 1;
        
    end
else
    %% Ts = 0 cas
    group_normalized = [...
        X(:, 1)/max(abs(X(:, 1))) ...
        X(:, 2)/max(abs(X(:, 2))) ...
        X(:, 3)/max(abs(X(:, 3))) ....
        X(:, 4)/max(abs(X(:, 4))) ...
        ];

    signal_entropy = [...
        entropy(group_normalized(:, 1)) ...
        entropy(group_normalized(:, 2)) ...
        entropy(group_normalized(:, 3)) ...
        entropy(group_normalized(:, 4)) ...
        ];
    
end

end
