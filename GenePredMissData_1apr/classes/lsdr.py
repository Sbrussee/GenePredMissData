import numpy as np
import scipy.linalg as la

class PLST:

	#Principle label space transformation, Tai & Lin 2010
	def __init__(self):
		#transformation matrix
		self.w = np.array([])
		#inverse map
		self.winv = np.array([])

		self.bias = np.array([])
		self.sigma = np.array([])
		self.varianceExplained = 0.0


	def fit(self, Y, **kwargs):
		#Y: #objects x #labels

		try:
			var_correction = kwargs.pop('var_correction')

		except KeyError:
			var_correction = False


		try:
			ndims =  kwargs.pop('ndims')

			dim = True

			if kwargs:
				raise TypeError('Unexpected **kwargs: %r' % kwargs)

		except KeyError:

			var =  kwargs.pop('var')

			dim = False

			if kwargs:
				raise TypeError('Unexpected **kwargs: %r' % kwargs)


		if dim and ndims > Y.shape[1]:
			raise ValueError('Invalid number of dimensions specified')
		if not dim and (var < 0.0 or var > 1.0):
			raise ValueError('Invalid variance fraction specified')


		self.bias = np.mean(Y, axis=0)

		Y = Y - np.tile(self.bias, [Y.shape[0], 1])

		if var_correction:
			self.sigma = np.std(Y, axis=0)

			for i in range(self.sigma.shape[0]):
				if self.sigma[i] == 0:
					self.sigma[i] = 1


			Y = Y / np.tile(self.sigma, (Y.shape[0],1))

		else:
			self.sigma = np.ones((Y.shape[1],))


		#print np.sum(np.isnan(Y).astype(int))

		[U, s, VT] = la.svd(Y)


		totalVariance = np.sum(s)

		if dim:
			self.w = VT[:ndims,:].T

			self.winv = self.w.T

			self.varianceExplained = np.sum(s[:ndims]) / totalVariance

		else:

			variances = np.cumsum(s) / totalVariance

			found = False
			i = 0

			ndims = -1

			while not found and i != variances.shape[0]:
				if variances[i] > var:
					found = True
					ndims = i + 1
				i += 1

			if not found:
				ndims = Y.shape[1]

			print (ndims)

			self.w = VT[:ndims,:].T

			self.winv = self.w.T

			self.varianceExplained = np.sum(s[:ndims]) / totalVariance

		return Y.dot(self.w)


	def inverseMap(self, Yprime):

		Yrec = Yprime.dot(self.winv) * np.tile(self.sigma, [Yprime.shape[0], 1])

		Yrec = Yrec + np.tile(self.bias, [Yprime.shape[0], 1])

		return Yrec

