# Binominal Bandit Application: How to Cold Call Firms? An Application of Multi-Armed Bandit Optimization in Corporate Web Surveys
This repo corresponds to the paper: How to Cold Call Firms? An Application of Multi-Armed Bandit Optimization in Corporate Web Surveys, by Johannes Gaul, Thomas Simon, Davud Rostam-Afschar.

The code displayed is a python implementation of the R-package provided originally by Lotze and Loecher (2014). The code they provide was established by Scott (2010). It is also used as an example for a Multi-Armed Bandit application in Kaibel and Biemann (2021). This part of the code is contained in binominal_bandit.py.

The second file in the repository (distribution.py) contains the request implementations for the Qualtrics API we utilize to access the server and setup our distributions in a automatic fashion, retreive contact information, randomly allocate contacts to samples, retreive distribution histories etc.

## References

Kaibel, C., and T. Biemann (2021): “Rethinking the gold standard with multi-armed bandits:
machine learning allocation algorithms for experiments,” Organizational Research Methods, 24(1),
78–103. 

Lotze, T., & Loecher, M. (2014, November 1). bandit: Functions for simple A/B split test and multi-armed bandit analysis. Retrieved from https://cran.r-project.org/web/packages/bandit/index.html. 

Scott, S. L. (2010). A modern Bayesian look at the multi-armed bandit. Applied Stochastic Models in Business
and Industry, 26(6), 639-658. doi:10.1002/asmb.874.
