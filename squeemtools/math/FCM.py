import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from scipy.stats import entropy

class FCM(object):
    '''Class for Fuzzy C-Means. Currently best suited with Pandas DataFrames for data.'''
    def __init__(self,data,c,m=2,maxiter=100,genCentroids=False,distFunc=False):
        '''data is data you want to cluster, c is number of clusters, m is dimensionality of data'''
        self._data = data        # Data to cluster on
        self._iter = maxiter     # Max iterations
        self._c = c              # Number of clusters
        self._n = len(data)      # Number of items in data set
        self._m = m              # Fuzzifier
        self._A = np.zeros((self._n,self._c)) # Membership matrix

        # Get dimensionality of data set
        if isinstance(data,pd.DataFrame):
            self._dim = len(data.iloc[0])
        elif isinstance(data,np.ndarray):
            self._dim = len(data[0])

        # Sample centroids from data
        if isinstance(genCentroids,bool):
            if self._c <= len(self._data):
                if genCentroids == True and type(self._data) == pd.DataFrame:
                    self._centroids = data.sample(self._c).copy()
                    self._centroids.reset_index(drop=True,inplace=True)
                elif genCentroids == False:
                    self._centroids = pd.DataFrame([np.random.uniform(0,1,self._dim) for x in range(self._c)],columns=self._data.columns)
            else:
                self._centroids = pd.DataFrame([np.random.uniform(0,1,self._dim) for x in range(self._c)],columns=self._data.columns)
        elif isinstance(genCentroids,list):
            self._centroids = pd.DataFrame(genCentroids)
        elif isinstance(genCentroids,pd.DataFrame):
            self._centroids = genCentroids

        # Function for calculating distance between elements
        if callable(distFunc):
            self._distFunc = distFunc
        else:
            self._distFunc = FCM.__l2Distance

    # Run FCM on the data
    def fit(self):
        '''Runs the algorithm on the data provided during construction. Uses the distance function to calculate distance. Returns the centroids'''
        with np.errstate(divide='ignore',invalid='ignore'):
            exponent = (2/(self._m-1))
            for iteration in range(self._iter):
                #Assignment Step
                DTC = np.zeros((self._n,self._c))
                for k in range(self._n):
                    for i in range(self._c):
                        #calculate distance
                        DTC[k,i] = self._distFunc(self._data.iloc[k],self._centroids.iloc[i]) #dimensionality m
                #Update A with membership
                for i in range(self._c):
                    for k in range(self._n):
                        sum = 0
                        for j in range(self._c):
                            sum += (DTC[k,i]/DTC[k,j]) ** exponent #parameter m
                        self._A[k,i] = 1/sum
                self._A[np.isnan(self._A)] = 0
                #Update
                for i in range(self._c):
                    sumnum = np.zeros(self._dim) #dimensionality m
                    sumden = 0
                    for k in range(self._n):
                        sumnum += (self._A[k,i] ** self._m) * self._data.iloc[k].values #parameter m
                        sumden += self._A[k,i] ** self._m #parameter m
                    self._centroids.iloc[i] = sumnum/sumden
        return self._centroids

    # Plotting the data and centroids
    def plot(self):
        '''Rudimentally plots the data using PyPlot for 2d.'''
        if self._dim == 2:
            fig = plt.figure(figsize=(8,8))
            columns = self._data.columns
            plt.scatter(self._data[columns[0]],self._data[columns[1]])
            columns = self._centroids.columns
            plt.scatter(self._centroids[columns[0]],self._centroids[columns[1]])
            plt.show()
            plt.close(fig)

    # De-Fuzzify the data and assign each point to a centroid
    def classify(self,how='max',threshold='.6'):
        '''Classify each point in the data set with it's membership to the centroids'''
        return np.array([list(self._A[x]).index(max(self._A[x])) for x in range(self._n)])

    def calculate_entropy(self):
        '''Calculates how much entropy there is in the membership matrix'''
        amounts = {'<.5' : 0, '<1' : 0, '>1' : 0, '>1.5' : 0}
        ent = np.array([entropy(x,base=2) for x in self._A])
        for e in ent:
            if e <= .5:
                amounts['<.5'] += 1
            elif e <= 1 and e > .5:
                amounts['<1'] += 1
            elif e > 1 and e < 1.5:
                amounts['>1'] += 1
            elif e > 1.5:
                amounts['>1.5'] += 1
        return ent.mean(), amounts

    def __l2Distance(a,b):
        '''Calculates l2 distance between a and b'''
        return np.linalg.norm(a-b)
