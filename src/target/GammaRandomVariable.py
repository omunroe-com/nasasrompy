'''
Class for implementing a gamma random variable
'''

import numpy as np
from scipy.stats import gamma as scipygamma

from src.target.RandomVariable import RandomVariable


class GammaRandomVariable(RandomVariable):
    '''
    Class for implementing a gamma random variable
    '''

    def __init__(self, alpha, shift=0, scale=1, max_moment=10):
        '''
        Initialize the gamma random variable with the standard alpha
        shape parameter (follows convention for a in scipy.stats.gamma).
        Optionally specify shift & scale parameters to translate and scale the
        random variable, e.g.:
            new_gamma = shift + scale * standard_gamma.

        Implementation wraps scipy.stats.gamma to get statistics/samples.
        '''

        if alpha < 0:
            raise ValueError("Alpha shape param must be non-negative")
        if scale <= 0:
            raise ValueError("Scale param must be positive")

        self._alpha = alpha
        self._shift = shift
        self._scale = scale
        #set dimension (scalar), min/max
        self._dim = 1
        self._mins = [shift]
        #NOTE Gamma max is technically infinite, do this on variance (3 STDs)?
        self._maxs = [shift + 2*self.get_variance()**0.5]

        #cache moments
        self.generate_moments(max_moment)
        self._max_moment = max_moment

    def get_dim(self):
        return self._dim

    def get_variance(self):
        '''
        Returns variance of gamma random variable
        '''
        return scipygamma.var(self._alpha, self._shift, self._scale)

    def compute_moments(self, max_order):
        '''
        Returns moments up to order 'max_order' in numpy array.
        '''

        #TODO - calculate moments above max_moment on the fly & append to stored
        if max_order <= self._max_moment:
            moments = self._moments[:max_order]
        else:
            raise NotImplementedError("Moment above max_moment not handled yet")

        return moments


    def compute_CDF(self, x_grid):
        '''
        Returns numpy array of gamma CDF values at the points contained in x_grid
        '''

        return scipygamma.cdf(x_grid, self._alpha, self._shift, self._scale)

    def compute_inv_CDF(self, x_grid):
        '''
        Returns np array of inverse gamma CDF values at pts in x_grid
        '''
        return scipygamma.ppf(x_grid, self._alpha, self._shift, self._scale)

    def compute_pdf(self, x_grid):
        '''
        Returns numpy array of gamma pdf values at the points contained in x_grid
        '''
        return scipygamma.pdf(x_grid, self._alpha, self._shift, self._scale)

    def draw_random_sample(self, sample_sz):
        '''
        Draws random samples from the gamma random variable. Returns numpy
        array of length 'sample_size' containing these samples
        '''

        #Use scipy gamma rv to return shifted/scaled samples automatically
        return scipygamma.rvs(self._alpha, self._shift, self._scale, sample_sz)

    def generate_moments(self, max_moment):
        '''
        Calculate & store moments to retrieve more efficiently later
        '''

        self._moments = np.zeros((max_moment, 1))

        #Rely on scipy.stats to return non-central moment
        for i in range(max_moment):
            self._moments[i] = scipygamma.moment(i+1, self._alpha, self._shift,
                                                 self._scale)

