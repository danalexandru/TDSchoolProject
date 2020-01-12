%% Description
% This method computes the medium frequency of a given dataset
function [mean_freq] = get_medium_frequencies(dataset)
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

mean_freq = zeros(M, 4);

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
        
        mean_freq(k + 1, :) = [...
            medfreq(group(:, 1), freq) ...
            medfreq(group(:, 2), freq) ...
            medfreq(group(:, 3), freq) ...
            medfreq(group(:, 4), freq) ...
            ];
    
        %% Debug
        display(strcat('Iteration: ', num2str(k)));
        k = k + 1;
        
    end
else
    %% Ts = 0 cas
    mean_freq = [...
        medfreq(X(:, 1), freq) ...
        medfreq(X(:, 2), freq) ...
        medfreq(X(:, 3), freq) ...
        medfreq(X(:, 4), freq) ...
        ];
end

end
