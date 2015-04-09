import random
import numpy as np
import statsmodels.api as sm
from statsmodels.tsa.arima_model import _arma_predict_out_of_sample
from statsmodels.tsa.arima_process import arma_generate_sample

np.random.seed(12345)


# Generate some data from an ARMA process:

arparams = np.array([.75, -.25])
maparams = np.array([.65, .35])


# The conventions of the arma_generate function require that we specify a 1 for the zero-lag of the AR and MA parameters and that the AR parameters be negated.
arparams = np.r_[1, -arparams]
maparam = np.r_[1, maparams]
nobs = 250
y = arma_generate_sample(arparams, maparams, nobs)

train = y[: 200]
test = y[200 :240]

y = range(1000)
random.shuffle(y)
#for i in range(1, 250):
#    y[i] += y[i - 1]
train = y[: 500]
test = y[500 :700]

#  Now, optionally, we can add some dates information. For this example, we'll use a pandas time series.
res = sm.tsa.stattools.arma_order_select_ic(train, ic='aic')
arma_mod = sm.tsa.ARMA(train, order=res.aic_min_order)
arma_res = arma_mod.fit(trend='nc', disp=-1)

#print res.params
# get what you need for predicting one-step ahead
params = arma_res.params
residuals = arma_res.resid
p = arma_res.k_ar
q = arma_res.k_ma
k_exog = arma_res.k_exog
k_trend = arma_res.k_trend
steps = 300

print y[700: ]
print _arma_predict_out_of_sample(params, steps, residuals, p, q, k_trend, k_exog, endog=test, exog=None, start=len(test))

#for y1, y2 in zip(y, y_):
#    print '%f\t%f' % (y1, y2)
