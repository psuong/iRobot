#trains NN classifier to distinguish between left, right, forward, back


import cv2
import numpy as np


labels = np.load("videolabels.npy")
framedata = np.load("framedata.npy")

print(labels.shape)
print(framedata.shape)

print(labels.dtype)
print(framedata.dtype)

layers = np.int32((307200, 32, 4))

model = cv2.ml.ANN_MLP_create()
model.setLayerSizes(layers)

criteria = (cv2.TERM_CRITERIA_COUNT | cv2.TERM_CRITERIA_EPS, 500, 0.0001)
criteria2 = (cv2.TERM_CRITERIA_COUNT, 100, 0.001)
model.setTermCriteria(criteria)
model.setTrainMethod(0)
model.setBackpropWeightScale(0.001)
model.setBackpropMomentumScale(0.0)
model.setActivationFunction(1)

params = dict(term_crit = criteria,
              bp_dw_scale = 0.001,
			  bp_moment_scale = 0.0)
num_iter = model.train(framedata, 0, labels)
model.save('mlp.xml')
print("Done")

print(model.predict(framedata[1:]))
