import socket
import face_recognition
import pickle
import matplotlib.pyplot as plt
import cv2
import os

image_type = '.jpg'
IP = ''
PORT = 5123

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 5)
s.bind((IP, PORT))
s.listen(True)
conn, addr = s.accept()

conn.sendall('server connected'.encode('utf-8'))
os.system('clear')
print('client connected')
with open('/home/pi/project/server/recv/' + 'img_file.jpg', 'wb') as f:
    while True:
        data = conn.recv(1024)
        if len(data) != 1024:
            f.write(data)
            break
        else: f.write(data)
    f.close()
print('img recv from client')
model_method = 'hog' # cnn, hog
image_type = '.jpg'
encoding_file = '/home/pi/project/server/' + 'encodings.pickle'
data = pickle.loads(open(encoding_file, 'rb').read())
print('algorithm : ' + model_method + '\nencoding file : ' + encoding_file)
file_name = '/home/pi/project/server/recv/' + 'img_file' + image_type  # test.
image = cv2.imread(file_name)
rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
print('image read....\nimage convert color BGR to RGB....\nfind face location....')
boxe = face_recognition.face_locations(rgb, model=model_method)
encodings = face_recognition.face_encodings(rgb, boxe)
names = []
print('start compare faces...')
for encoding in encodings:
  matches = face_recognition.compare_faces(data["encodings"], encoding, 0.4)  # 60% True 0.6
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
    name = 'name : ' + name + '  pers : ' + persent
  names.append(name)
print('write name on face')
for ((top, right, bottom, left), img_name) in zip(boxe, names):
  cv2.rectangle(image, (left, top), (right, bottom), (0, 255, 0), 3)
  y = top - 15 if top - 15 > 15 else top + 15
  cv2.putText(image, img_name , (left, y), cv2.FONT_HERSHEY_SIMPLEX, 1.1, (0, 255, 0), 3)   # size 0.75, 2

cv2.imwrite('/home/pi/project/server/recv/face_recognition.jpg', image)
print('save finished image')
file_name = '/home/pi/project/server/recv/' + 'face_recognition.jpg' # test send

f = open(file_name, 'rb')
l = f.read(1024)
print('send converted image')
while (l):
    conn.sendall(l)
    l = f.read(1024)
f.close()
conn.close()
s.close()
print('server closed')