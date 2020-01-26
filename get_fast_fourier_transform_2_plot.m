%% Description
% This method gets the fast fourier transform for each sensor of a healthy
% and broken dataset and plots the results
function [X_fft_healthy, X_fft_broken] = get_fast_fourier_transform_2_plot(h_data, b_data)
%% Get features and targets for the healthy dataset
X_healthy = [h_data.training.X; h_data.valid.X; h_data.test.X];

% X_healthy = h_data.training.X;

%% Get features and targets for the broken dataset
X_broken = [b_data.training.X; b_data.valid.X; b_data.test.X];

% X_healthy = b_data.training.X;

%% Get the fast fourier transform
[Nh, M] = size(X_healthy);
[Nb, ~] = size(X_broken);

X_fft_healthy = zeros(Nh, M);
X_fft_broken = zeros(Nb, M);

for i = 1 : M
    X_fft_healthy(:, i) = fft(X_healthy(:, i));
    X_fft_broken(:, i) = fft(X_broken(:, i));
    
    X_fft_healthy(:, i) = X_fft_healthy(:, i).*conj(X_fft_healthy(:, i));
    X_fft_broken(:, i) = X_fft_broken(:, i).*conj(X_fft_broken(:, i));
end

%% Plot results
for i = 1 : M
    f = figure(i);
    %% Plot the healthy data
    subplot(2, 1, 1);
    plot(1 : Nh, X_fft_healthy(:, i));
    grid on;
    hold on;
    plot(find(X_fft_healthy(:, i) == max(X_fft_healthy(:, i))), max(X_fft_healthy(:, i)), 'ro');
    plot(1 : Nh, (ones(Nh, 1))*mean(X_fft_healthy(:, i)), '-r');
    hold off;
    title(strcat('Fast Fourier Transform for the healthy dataset: sensor ', num2str(i)));
    legend('Fast Fourier Transform', ...
        strcat('Max value: ', num2str(max(X_fft_healthy(:, i)))),...
        strcat('Mean value: ', num2str(mean(X_fft_healthy(:, i))))...
        );
    
    %% Plot the broken data
    subplot(2, 1, 2);
    plot(1 : Nb, X_fft_broken(:, i));
    grid on;
    hold on;
    plot(find(X_fft_broken(:, i) == max(X_fft_broken(:, i))), max(X_fft_broken(:, i)), 'ro');
    plot(1 : Nb, (ones(Nb, 1))*mean(X_fft_broken(:, i)), '-r');
    hold off;
    title(strcat('Fast Fourier Transform for the broken dataset: sensor ', num2str(i)));
    legend('Fast Fourier Transform', ...
        strcat('Max value: ', num2str(max(X_fft_broken(:, i)))),...
        strcat('Mean value: ', num2str(mean(X_fft_broken(:, i))))...
        );
    
    figure_name = strcat('.\pics\fft2\fft_2_hb', b_data.name(2:end), '_sensor_', num2str(i), '.jpg');
    saveas(f, figure_name);
end

end
