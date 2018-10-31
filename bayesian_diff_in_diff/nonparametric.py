from bayesian_bootstrap.bootstrap import mean
import numpy as np
from matplotlib import pyplot as plt
import seaborn as sns

class NonparametricDiffInDiff(object):
    def __init__(self, data, time_col, intervention_col, observation_col, n_samples):
        """
        A Difference in difference estimator which calculates uncertainty with a Bayesian Bootstrap.

        Params:
        data: A Pandas dataframe with the data set.
        time_col: The column containing the time indicator (0 or 1, for before and after, respectively)
        intervention_col: The column containing the group indicator (0 or 1, where the group with the label 1 received the treatment at T=1)
        observation_col: The column with the observed values.
        n_samples: The number of bootstramp resamples to perform.
        """
        self._validate_input(data, time_col, intervention_col, observation_col)
        self.group_mean_samples = self._run_sampling(data, time_col, intervention_col, observation_col, n_samples)
        self.treatment_effect_samples = (self.group_mean_samples[0, 0] - self.group_mean_samples[1, 0]) - (self.group_mean_samples[0, 1] - self.group_mean_samples[1, 1 ]) 
        
    def _validate_input(self, data, time_col, intervention_col, observation_col):
        pass
        
    def _run_sampling(self, data, time_col, intervention_col, observation_col, n_samples):
        posterior_samples = {}
        for group, group_df in data.groupby([time_col, intervention_col]):
            posterior_samples[group] = np.array(mean(group_df[observation_col], n_samples))
        return posterior_samples
            
    def print_summary(self):
        print(np.mean(self.treatment_effect_samples))

    def plot_means(self):
        plt.plot([0, 1], [np.mean(self.group_mean_samples[0,0]), np.mean(self.group_mean_samples[1, 0])], marker='o', label='Group 0')
        plt.plot([0, 1], [np.mean(self.group_mean_samples[0,1]), np.mean(self.group_mean_samples[1, 1])], marker='o', label='Group 1, observed')
        plt.plot([0, 1], [np.mean(self.group_mean_samples[0,1]), np.mean(self.group_mean_samples[1, 1] - self.treatment_effect_samples)], marker='o', linestyle='dotted', label='Group 1, counterfactual')
        plt.legend()
