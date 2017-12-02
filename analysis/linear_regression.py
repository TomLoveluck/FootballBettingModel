import pandas as pd
from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn.metrics import mean_squared_error

# filepaths
FEATURE_FP = "../data/Features.csv"

# read in data and produce train, test sets
df = pd.read_csv(str(FEATURE_FP))
train_set = df[(df.Date > '2011-10-01') & (df.Date <= '2012-03-01')].copy()
test_set = df[(df.Date > '2012-03-01') & (df.Date <= '2012-05-01')].copy()

# feature and target columns
feature_cols = ['home_goals_td_mean',
                'home_goals_sd_mean',
                'away_goals_td_mean',
                'away_goals_sd_mean',
                'home_team_last_home_score',
                'home_team_last_away_score',
                'away_team_last_home_score',
                'away_team_last_away_score']

target_col = 'HomeResult'

# train linear regression model
linear_reg = LinearRegression()
linear_reg.fit(train_set[feature_cols], train_set[target_col])

# predict on test set
test_set.loc[:,'HomePrediction'] = linear_reg.predict(test_set[feature_cols])
print(test_set[['HomeResult','HomePrediction']].head(20))

# calculate on MSE
mse_lin = mean_squared_error(test_set['HomeResult'],test_set['HomePrediction'])
print("Linear regression: MSE = {}".format(mse_lin))
