# -*- coding: utf-8 -*-
# !/usr/bin/env python3

import face_recognition
from PIL import Image, ImageDraw, ImageColor


def show_facial_features(image_path):

    # Load the jpg file into an array
    image = face_recognition.load_image_file(image_path)

    # these are the features that will be detected and shown
    facial_features = [
        'chin',
        'left_eyebrow',
        'right_eyebrow',
        'nose_bridge',
        'nose_tip',
        'left_eye',
        'right_eye',
        'top_lip',
        'bottom_lip']

    blue = ImageColor.getcolor('blue', 'RGB')

    # Find all facial landmarks for all the faces in the image
    face_landmarks_list = face_recognition.face_landmarks(image)
    img_obj = Image.fromarray(image)

    # draw lines upon facial features
    for face_landmarks in face_landmarks_list:
        drawing = ImageDraw.Draw(img_obj)
        for facial_feature in facial_features:
            drawing.line(face_landmarks[facial_feature], width=2, fill=blue)

    # show image
    img_obj.show()
