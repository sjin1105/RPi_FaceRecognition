import cv2
import face_recognition
import pickle
import os
from os import listdir
from os.path import join

dataset_paths = ['/home/pi/project/server/chang/', '/home/pi/project/server/lee/'] #
names = ['chang', 'lee'] #
image_type = '.jpg'
encoding_file = 'encodings.pickle' #output file
model_method = 'cnn' # cnn, hog
knownEncodings = []
knownNames = []

for (i, dataset_path) in enumerate(dataset_paths):
  print('file')
  name = names[i]
  f_dir = dataset_path + name + '/'
  if not os.path.exists(f_dir):
    os.mkdir(f_dir)

  jpg_path = dataset_path 
  jpg_file = [f for f in listdir(jpg_path) if join(jpg_path, f).endswith('.jpg')]
  number_images = len(jpg_file)   # 

  for idx in range(number_images):
    file_name = dataset_path + name + '_' + str(idx+1) + image_type
    image = cv2.imread(file_name)
    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  #opencv BGR  face_recognition RGB
    boxes = face_recognition.face_locations(rgb, model=model_method)
    encodings = face_recognition.face_encodings(rgb, boxes)

    for encoding in encodings:
      knownEncodings.append(encoding)
      knownNames.append(name)

    for (top, right, bottom, left) in boxes:
      cv2.rectangle(image, (left, top), (right, bottom), (0, 255, 0), 4)
      f_name_path = f_dir + name + '_' + str(idx+1) + '.jpg'
      image = cv2.resize(image, (400, 400))
      #cv2_imshow(image)
      cv2.imwrite(f_name_path, image)
    
data = {"encodings": knownEncodings, "names": knownNames}
f = open(encoding_file, "wb")
f.write(pickle.dumps(data))
f.close()