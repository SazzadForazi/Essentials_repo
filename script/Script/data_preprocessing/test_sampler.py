import numpy as np

# def augment_sample(I, pts, dim):
def augment_sample():
	maxsum, maxangle = 120, np.array([80., 80., 45.])
	angles = np.random.rand(1) * maxangle
	if angles.sum() > maxsum:
		angles = (angles / angles.sum()) * (maxangle / maxangle.sum())
	return angles

for i in range(1, 100):
	print(augment_sample())