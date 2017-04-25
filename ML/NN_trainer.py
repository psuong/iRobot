#trains NN classifier to distinguish between left, right, forward, back


import cv2
import numpy as numpy


labels = np.load("videolabels.npz")
framedata = np.load("framedata.npz")

print(labels.shape)
print(framedata.shape)

layers = np.int32((307200, 32, 4))

model = cv2.ANN_MLP()
model.create(layers)

criteria = (cv2.TERM_CRITERIA_COUNT | cv2.TERM_CRITERIA_EPS, 500, 0.0001)
criteria2 = (cv2.TERM_CRITERIA_COUNT, 100, 0.001)
params = dict(term_crit = criteria,
              train_method = cv2.ANN_MLP_TRAIN_PARAMS_BACKPROP,
              bp_dw_scale = 0.001,
			  bp_moment_scale = 0.0)
num_iter = model.train(train, train_labels, None, params = params)

model.save('mlp_xml/mlp.xml')