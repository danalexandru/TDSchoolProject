%% Description
% This function will return the state space model based on the given training set
% and the valid set
function [sys] = get_state_space_model(training_set, valid_set, Ts)
%% Check input parameters
if (nargin < 3)
    Ts = 30;
end

%% Convert the training set into an iddata mode
training_data = iddata(training_set.y, training_set.X, Ts);
valid_data = iddata(valid_set.y, valid_set.X, Ts);

%% Get state space
nx = 1;
sys = ssest(training_data, nx);

%% Compare training data
figure(1);
compare(training_data, sys);
grid on;

%% Compare valid data
figure(2);
compare(valid_data, sys);
grid on;

end
