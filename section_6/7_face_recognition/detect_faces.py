# -*- coding: utf-8 -*-
# !/usr/bin/env python3

import pathlib
import face_recognition
from PIL import Image


if __name__ == '__main__':
    # load source image
    src_img_path = (pathlib.Path('..') / 'images' / 'meeting.jpg').resolve()
    img = face_recognition.load_image_file(str(src_img_path))

    # detect location of human faces
    face_locations = face_recognition.face_locations(img)
    print('Found: {} faces\n'.format(len(face_locations)))
    for top, right, bottom, left in face_locations:
        # say where the face was found
        print("Found a face at pixel coordinates top: {}, left: {}, "
              "bottom: {}, right: {}".format(top, left, bottom, right))

        # create a Pillow image out of binary data
        face_data_array = img[top:bottom, left:right]
        face_image = Image.fromarray(face_data_array)

        # create target file and save image
        face_img_path = pathlib.Path('{}{}{}{}-face.jpg'.format(
            top, right, bottom, left))
        face_img_path.touch()
        face_image.save(str(face_img_path.resolve()))
