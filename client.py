import socket
import cv2
import os
import matplotlib.pyplot as plt
from os import listdir
from os.path import join

image_type = '.jpg'
IP = ''
PORT = 5123

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((IP, PORT))
os.system('clear')
first_recv = s.recv(1024).decode()
print(first_recv)
test_path = '/home/pi/project/client/test/'
while True:
    test_file = [f for f in listdir(test_path) if join(test_path, f).endswith('.jpg')]
    print(test_file)
    test_image = input('select test image name (not [.jpg]): ')
    test_image_name = test_image + '.jpg'
    if test_image_name in test_file:
        break
    else: 
        os.system('clear')
        print('image name is not in test folder')

file_name = test_path + test_image + image_type  # test
f = open(file_name, 'rb')
l = f.read(1024)
while (l):
    s.sendall(l)
    l = f.read(1024)
f.close()
print('send iamge complete\nface recognition start....')
with open('/home/pi/project/client/recv/' + 'img_file.jpg', 'wb') as f:
    while True:
        data = s.recv(1024)
        if len(data) != 1024:
            f.write(data)
            break
        else: f.write(data)
    f.close()
s.close()
print('converted image received\nimage open')

file_name = '/home/pi/project/client/recv/' + 'img_file.jpg'
image = cv2.imread(file_name)
rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
plt.imshow(rgb)
plt.xticks([]), plt.yticks([])
plt.show()