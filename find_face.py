import cv2
import face_recognition
import pickle
import matplotlib.pyplot as plt
import os
import numpy as np
from os import listdir
from os.path import join

model_method = 'hog' # cnn, hog
image_type = '.jpg'
encoding_file = '/home/pi/project/server/' + 'encodings.pickle'
data = pickle.loads(open(encoding_file, 'rb').read())
file_name = '/home/pi/project/client/' + 'test/' + 'test_1' + image_type  # test
image = cv2.imread(file_name)
rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
boxe = face_recognition.face_locations(rgb, model=model_method)
encodings = face_recognition.face_encodings(rgb, boxe)
names = []
for encoding in encodings:
  matches = face_recognition.compare_faces(data["encodings"], encoding, 0.4)  # 60% True
  match = face_recognition.face_distance(data['encodings'], encoding)
  name = "Unknown"
  sum_match = 0
  if True in matches:
    matchedIdxs = [i for (i, b) in enumerate(matches) if b]
    counts = {}
    for i in matchedIdxs:
      name = data["names"][i]
      counts[name] = counts.get(name, 0) + 1
    name = max(counts, key=counts.get)
    persent = str(round((1 - min(match)) * 100, 2)) + '%'
    name = 'name : ' + name + '  persent : ' + persent
  names.append(name)

for ((top, right, bottom, left), img_name) in zip(boxe, names):
  cv2.rectangle(image, (left, top), (right, bottom), (0, 255, 0), 3)
  y = top - 15 if top - 15 > 15 else top + 15
  cv2.putText(image, img_name , (left, y), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 3)   # size 0.75, 2

plt.imshow(image)
plt.xticks([]), plt.yticks([])
plt.show()
