from __future__ import division
import numpy as np 
import matplotlib.pyplot as plt
from scipy.optimize import minimize, differential_evolution
import seaborn as sns
sns.set_style('whitegrid')

# Set some parameters
K = 975 # capacity, TAF
D = 150 # target yield, TAF
a = 1
b = 2 # cost function parameters

# data setup
Q = np.loadtxt('data/FOL-monthly-inflow-TAF.csv', delimiter=',', skiprows=1, usecols=[1])
T = len(Q)

def simulate(x):
  S = np.zeros(T)
  R = np.zeros(T)
  cost = np.zeros(T)
  h0 = x[0]
  hf = x[1]

  S[0] = K # start simulation full

  for t in range(1,T):

    # new storage: mass balance, max value is K
    S[t] = min(S[t-1] + Q[t-1] - R[t-1], K)

    # determine R from hedging policy
    W = S[t] + Q[t]
    if W > hf:
      R[t] = D
    elif W < h0:
      R[t] = W
    else:
      R[t] = (D-h0)/(hf-h0)*(W-h0)+h0

    shortage = D-R[t]
    cost[t] = a*shortage**b

  return cost.mean()


# to make a contour plot...
h0s = np.arange(0,D,5)
hfs = np.arange(D,K+D,5)

# or, ranges for zoomed in contour plot
# h0s = np.arange(75,78,0.5)
# hfs = np.arange(815,855,0.5)

data = np.zeros((len(h0s),len(hfs)))
i,j = 0,0

for h0 in h0s:
  for hf in hfs:
    data[i,j] = simulate([h0,hf])
    j += 1
  j = 0
  i += 1

X,Y = np.meshgrid(h0s, hfs)
plt.contour(X,Y,data.T, 100, cmap=plt.cm.cool)
plt.colorbar()
plt.title('Average Shortage Cost ("$")')
plt.xlabel(r'$h_0$')
plt.ylabel(r'$h_f$')
plt.show()