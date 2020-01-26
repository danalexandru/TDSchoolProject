%% Description
% This method plots the histogram for each sensor
function [] = get_histogram_figure_plot(X_healthy, X_broken, broken_data_name, method)
%% Plot results
[~, M] = size(X_broken);

for i = 1 : M
    f = figure(i);
    subplot(2, 1, 1);
    histogram(X_healthy(:, i));
    grid on;
    title(strcat(method, ' for healthy dataset: sensor ', num2str(i)));
    
    subplot(2, 1, 2);
    histogram(X_broken(:, i));
    grid on;
    title(strcat(method, ' for broken dataset: sensor ', num2str(i)));
    
    figure_name = strcat('.\pics\', lower(method),'\', lower(method), '_hb', broken_data_name(2:end), '_sensor_', num2str(i), '.jpg');
    saveas(f, figure_name);
end

end
