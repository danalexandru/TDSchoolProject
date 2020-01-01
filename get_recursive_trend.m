%% Description 
% This metod returns the trend of a given training dataset
function[dict_ps_output] = get_recursive_trend(dict_training_set, p)
%% Convert the training set into an iddata mode
training_data = iddata(dict_training_set('y'), dict_training_set('X'), 1);
training_data = misdata(training_data);

%% Retrieve dataset features and targets
X = training_data.InputData;
y = training_data.OutputData;

%% Step 0: Initialize parameters
[N, M] = size(X);

yT = zeros(N, 1);

M1 = p + 1;

%% Step 1: Estimate the vector parameters tetaNp by implementing the MCMMP
theta = [];
for j = 1 : M
    tn = X(:, j);
    
    RN = zeros(p + 1);
    rN = zeros(p + 1, 1);
    BM = zeros(p + 1);
    for k = 1 : p + 1
        for i = 1 : k
            RN(i, k) = (1/N)*sum(tn.^(i - 1 + k - 1));
            RN(k, i) = RN(i, k);
        end
        rN(k) = (1/N)*((tn.^(k - 1))'*y);
        BM(k, k) = 1/(((M1)^(k - 1))*sqrt(M1));
    end
    
    
    thetaNp = BM*((BM*RN*BM)^(-1))*BM*rN;
    theta = [theta thetaNp];
    
end

%% Step 2: Evaluate the efective model of the trend on the measurement horison
for j = 1 : M
    tn = X(:, j);
    thetaNp = theta(:, j);
    
    for i = 1 : p + 1
        yT = yT + thetaNp(i)*(tn.^(i - 1));
    end
end

%% Map the results in the (0, 1) interval
% m = mean(yT);
% for i = 1 : length(yT)
%     if (yT(i) >= m)
%         yT(i) = 1;
%     else
%         yT(i) = 0;
%     end
% end

yT = (yT-min(yT))/(max(yT)-min(yT));

%% Create dictionary
dict_ps_output = containers.Map;

dict_ps_output('theta') = theta;
dict_ps_output('trend') = yT;
end