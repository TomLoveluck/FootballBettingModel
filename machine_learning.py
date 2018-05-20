import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

# file paths
FEATURE_FP = "data/Features.csv"

# read in data and produce train, test sets
df = pd.read_csv(FEATURE_FP)
train_set = df[(df.Date > '2010-12-01') & (df.Date <= '2016-08-01')].copy().fillna(0)
test_set = df[(df.Date > '2016-08-01') & (df.Date <= '2017-08-01')].copy().fillna(0)

# feature and target columns
feature_cols = ['home_team_goals_scored_sd_mean',
                'home_goals_conceded_sd_mean',
                'away_team_goals_scored_sd_mean',
                'away_team_goals_conceded_sd_mean',
                'home_team_last_home_score',
                'home_team_last_away_score',
                'away_team_last_home_score',
                'away_team_last_away_score']

target_col = 'HomeResult'

# train linear regression model
linear_reg = LinearRegression()
linear_reg.fit(train_set[feature_cols], train_set[target_col])


# predict on train and test set
train_set.loc[:, 'HomePredictionLR'] = linear_reg.predict(X=train_set[feature_cols])
test_set.loc[:, 'HomePredictionLR'] = linear_reg.predict(X=test_set[feature_cols])

# calculate on MSE of linear regression model
mse_lin_train = mean_squared_error(train_set['HomeResult'], train_set['HomePredictionLR'])
mse_lin_test = mean_squared_error(test_set['HomeResult'], test_set['HomePredictionLR'])

# calculate on MSE of constant prediction
test_set.loc[:, 'HomeNaivePrediction'] = train_set['HomeResult'].mean()
mse_nai = mean_squared_error(test_set['HomeResult'], test_set['HomeNaivePrediction'])


# print results to console
print("Linear regression: MSE on train set = {}".format(mse_lin_train))
print("Linear regression: MSE on test set= {}".format(mse_lin_test))
print("Constant prediction benchmark: MSE = {}".format(mse_nai))

print(len(train_set))
print(len(test_set))

