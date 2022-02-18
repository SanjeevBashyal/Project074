A = np.array([[1,4],[2,5],[1,3],[3,6]])
B = np.array([[1,4],[3,6],[7,8]])

nrows, ncols = A.shape
dtype={'names':['f{}'.format(i) for i in range(ncols)],
       'formats':ncols * [A.dtype]}

C = np.setdiff1d(A.view(dtype), B.view(dtype))

# This last bit is optional if you're okay with "C" being a structured array...
C = C.view(A.dtype).reshape(-1, ncols)