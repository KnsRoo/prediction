

from pandas import read_csv, DataFrame
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.figure as fig
import statsmodels.api as sm
from statsmodels.iolib.table import SimpleTable
from sklearn.metrics import r2_score
import ml_metrics as metrics
from sklearn.linear_model import LinearRegression
import csv
from itertools import zip_longest
import seaborn as sns
import os

class RegressionModel:
    prediction = []
    r_sq = 0

    def __init__(self, dataset, pred, date1, date2):
        otg2 = DataFrame(dataset['eff'])
        x = np.array(dataset['sum']).reshape((-1, 1))
        y = np.array(dataset['eff'])
        model = LinearRegression().fit(x, y)
        self.r_sq = model.score(x, y)
        x = np.array(pred).reshape((-1,1))
        self.prediction = model.predict(x)

        data = [[date1, date2], self.prediction]
        export_data = zip_longest(*data, fillvalue = '')
        with open('temp/mycsvfile.csv', 'w', newline='') as file:
            w = csv.writer(file)
            w.writerow(('date', 'eff'))
            w.writerows(export_data)

        otg3 = read_csv('temp/mycsvfile.csv',',', index_col=['date'], parse_dates=['date'], dayfirst=True)
        fig, ax = plt.subplots(figsize=(9, 4))

        # plot desired quantities; note the `ax=ax` in both
        otg2.plot(ax=ax)
        otg3.plot(ax=ax, style="--r")
        plt.savefig("temp/regr.png")

    def get_rsq(self):
        return 'R^2 = ' + str(self.r_sq)

    def get_prediction(self):
        return self.prediction

class ArimaModel:
    prediction = []
    itog = ''
    stat = ''
    summary = ''
    V = 0
    
    def __init__(self, dataset, date1, date2):
        otg = DataFrame(dataset['sum'])
        otgR = otg.resample('A').mean()
        itog = otgR.describe()
        row =  [u'JB', u'p-value', u'skew', u'kurtosis']
        jb_test = sm.stats.stattools.jarque_bera(otg)
        a = np.vstack(jb_test)
        otg1diff = otgR.diff(periods=1).dropna()
        fig = plt.figure(figsize=(9,4))
        ax1 = fig.add_subplot(211)
        fig = sm.graphics.tsa.plot_acf(otg1diff.values.squeeze(), lags=10, ax=ax1)
        ax2 = fig.add_subplot(212)
        fig = sm.graphics.tsa.plot_pacf(otg1diff, lags=4, ax=ax2)
        self.stat = DataFrame(a, index=row).T
        self.itog = itog.T
        self.V = 'V = %f' % (self.itog['std']/self.itog['mean'])

        src_data_model = otg['sum']
        model = sm.tsa.ARIMA(src_data_model, order=(1,1,1)).fit()   
        self.summary = model.summary().as_text()
        self.prediction = model.predict(date1, date2, typ='levels')

        otg.plot(figsize=(9,4))
        ax = self.prediction.plot(style='r--')
        ax.figure.savefig("temp/arima.png")

    def get_itog_table(self):
        return self.itog
        
    def get_prediction(self):
        return self.prediction

    def get_V(self):
        return self.V

    def get_summary(self):
        return self.summary

class Corr:
    def __init__(self, dataset):
        sns.set(rc={'figure.figsize':(9,4)})
        sns_plot = sns.regplot(x=dataset["sum"], y=dataset["eff"])
        fig = sns_plot.get_figure()
        fig.savefig("temp/corr.png")


class Model:
    dataset = []
    def __init__(self, filepath, date1, date2):
        self.file = filepath
        self.dataset = dataset = read_csv(self.file, ',', index_col=['date'], parse_dates=['date'], dayfirst=True)
        self.corr = Corr(dataset)
        self.arima = ArimaModel(dataset, date1, date2)
        self.linreg = RegressionModel(dataset, self.arima.get_prediction(), date1, date2)

    def get_rsq(self):
        return self.linreg.get_rsq()

    def get_V(self):
        return self.arima.get_V()

    def get_itog_table(self):
        return self.arima.itog

    def get_summary(self):
        return self.arima.get_summary()