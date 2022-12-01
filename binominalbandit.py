# Python implementation of:

# Lotze, T., & Loecher, M. (2014, November 1). bandit: Functions for simple A/B split test and multi-armed bandit analysis. Retrieved from https://cran.r-project.org/web/packages/bandit/index.html.
# Scott, S. L. (2010). A modern Bayesian look at the multi-armed bandit. Applied Stochastic Models in Business and Industry, 26(6), 639-658. doi:10.1002/asmb.874

import pandas as pd
from datetime import datetime, timedelta
from scipy.integrate import quad
import collections
from datetime import date



# Calculates the density/point estimate of the Beta-distribution
def dbeta(x,shape1,shape2):
    """
    Calculates the density/point estimate of the Beta-distribution
    """
    from scipy.stats import beta
    result=beta.pdf(x=x,a=shape1,b=shape2,loc=0,scale=1)
    return result

# Calculates the cumulative of the Beta-distribution
def pbeta(q,shape1,shape2):
    """
    Calculates the cumulative of the Beta-distribution
    """
    from scipy.stats import beta
    result=beta.cdf(x=q,a=shape1,b=shape2,loc=0,scale=1)
    return result


# Calculates the Bayesian probability (i.e. the bandit recommendation)
def binominal_bandit(x, n, alpha=1, beta=1):
    ans = []
    k = len(x)
    l = list(range(0, k))
    for i in l:
        excluded_index = i
        indx = l[:excluded_index] + l[excluded_index + 1:]

        def f(z):
            r = dbeta(z, x[i] + alpha, n[i] - x[i] + beta)
            for j in indx:
                r = r * pbeta(z, x[j] + alpha, n[j] - x[j] + beta)
            return r

        a = quad(f, 0, 1)[0]
        ans.append(a)

    return ans

# Creating an alias
bb = binominal_bandit
