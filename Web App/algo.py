import warnings
from pandas import read_csv
import numpy as np
from pandas import datetime
from matplotlib import pyplot
from statsmodels.tsa.arima_model import ARIMA
from sklearn.metrics import mean_squared_error

def rspm_facc(file):
    predicts = {}
    target = ['NO2', 'SO2', 'AQI']
    lst = []
    for i in range(len(target)):
        series = read_csv(file, header=0, index_col=0)
        series = series.dropna()

        series = series.iloc[:, [i]]
        X = series.values

        size = int(len(X) * 0.96)
        train, test = X[0:size], X[size:len(X)]
        history = [x for x in train]
        predictions = list()
        err = []
        for t in range(7):
            model = ARIMA(history, order=(5, 1, 0))
            model_fit = model.fit(disp=0)
            output = model_fit.forecast()
            yhat = output[0]
            predictions.append(yhat)
            obs = yhat
            history.append(yhat)

        #         print('predicted=%f, expected=%f' % (yhat, obs))

        predicts[i] = predictions

        # pyplot.plot(predictions, color='red')
        # pyplot.ylabel("AQI", fontsize=22)
        #
        # pyplot.show()
    d = {}

    for i in range(1, 8):
        lst = [predicts[0][i-1][0], predicts[1][i-1][0], predicts[2][i-1][0]]
        d[i] = lst


    return d

def run(file):
    warnings.filterwarnings('ignore')
    return rspm_facc(file)
