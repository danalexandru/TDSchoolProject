%% Description
% This method computes the magnitude for each frequency of a given dataset
function [freq_magn] = get_frequencies_magnitude(dataset)
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

freq_magn = zeros(M, 4);

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
        
        frequencies = [...
            fft(group(:, 1)) ...
            fft(group(:, 2)) ...
            fft(group(:, 3)) ...
            fft(group(:, 4)) ...
            ];
        
        freq_magn(k + 1, :) = [...
            norm(frequencies(:, 1)) ...
            norm(frequencies(:, 2)) ...
            norm(frequencies(:, 3)) ...
            norm(frequencies(:, 4)) ...
            ];

        %% Debug
        display(strcat('Iteration: ', num2str(k)));
        k = k + 1;
        
    end
else
    %% Ts = 0 cas
    frequencies = [...
        fft(X(:, 1)) ...
        fft(X(:, 2)) ...
        fft(X(:, 3)) ...
        fft(X(:, 4)) ...
        ];

    freq_magn = [...
        norm(frequencies(:, 1)) ...
        norm(frequencies(:, 2)) ...
        norm(frequencies(:, 3)) ...
        norm(frequencies(:, 4)) ...
        ];
end

end
