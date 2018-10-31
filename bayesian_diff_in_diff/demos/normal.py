import unittest
from bayesian_bootstrap.bootstrap import mean
import numpy as np
from matplotlib import pyplot as plt
import seaborn as sns
from bayesian_diff_in_diff.nonparametric import NonparametricDiffInDiff
import pandas as pd

samples_per_group = 5000
sigma = 1
z = 1

y11, y01, y10, y00 = 4, 3, 2, 1

y00_observed = np.random.normal(y00, sigma, samples_per_group)
y01_observed = np.random.normal(y01, sigma, samples_per_group)
y10_observed = np.random.normal(y10, sigma, samples_per_group)
y11_observed = np.random.normal(y11 + z, sigma, samples_per_group)

y_observed = np.concatenate([y00_observed, y01_observed, y10_observed, y11_observed])
T_observed = [0]*samples_per_group + [0]*samples_per_group + [1]*samples_per_group + [1]*samples_per_group
S_observed = [0]*samples_per_group + [1]*samples_per_group + [0]*samples_per_group + [1]*samples_per_group

print((y00 - y10) - (y01 - (y11 + z)))

df = pd.DataFrame({'y':y_observed, 't':T_observed, 's':S_observed})

did = NonparametricDiffInDiff(df, 't', 's', 'y', 5000)
did.plot_means()
plt.show()
