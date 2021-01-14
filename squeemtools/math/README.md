## Math
### FCM.py:
#### FCM(data,c,m,maxiter,genCentroids,distFunc)
Class for Fuzzy C-Means. Currently works with Pandas DataFrames
- data is the data to cluster on
- c is the number of clusters
- m is the fuzzifier
  - Default: 2
- maxiter is the maximum number of items the algorithm should run
  - Default: 100
- genCentroids is whether or not the class should generate the samples or they are provided by the users
  - Default: False
- distFunc is the distance function to use when calculating distance, must be callable
  - Default: False (uses np.linalg.norm)
 
Class Methods: 
fcm.fit()
- Runs the Bezdek Algorithm on the data. Uses the distance function
- Sets the centroids in self._centroids and returns them