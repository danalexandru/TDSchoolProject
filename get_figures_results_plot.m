%% Description
% This method plots the skeweness for each sensor
function [] = get_figures_results_plot(X_healthy, X_broken, broken_data_name, method)
%% Get dimensions
[Nh, M] = size(X_healthy);
[Nb, ~] = size(X_broken);

%% Plot results
for i = 1 : M
    f = figure(i);
    subplot(2, 1, 1);
    plot(1 : Nh, X_healthy(:, i));
    grid on;
    hold on;
    plot(1 : Nh, ones(Nh, 1)*mean(X_healthy(:, i)));
    hold off;
    title(strcat(method, ' for healthy dataset: sensor ', num2str(i)));
    legend(...
        'Skeweness',...
        strcat('Mean value: ', num2str(mean(X_healthy(:, i))))...
        );
    
    subplot(2, 1, 2);
    plot(1 : Nb, X_broken(:, i));
    grid on;
    hold on;
    plot(1 : Nb, ones(Nb, 1)*mean(X_broken(:, i)));
    hold off;
    title(strcat(method, ' for broken dataset: sensor ', num2str(i)));
    legend(...
        'Skeweness',...
        strcat('Mean value: ', num2str(mean(X_broken(:, i))))...
        );
    
    figure_name = strcat('.\pics\', lower(method),'\', lower(method), '_hb', broken_data_name(2:end), '_sensor_', num2str(i), '.jpg');
    saveas(f, figure_name);
end

end
