from sktime.forecasting.all import *
from loadData import *

# y = load_airline()
y = first_array
y_train, y_test = temporal_train_test_split(y)
fh = ForecastingHorizon(y_test.index, is_relative=False)
forecaster = ThetaForecaster(sp=12)
forecaster.fit(y_train)
y_pred=forecaster.predict(fh)
print(smape_loss(y_test,y_pred))
