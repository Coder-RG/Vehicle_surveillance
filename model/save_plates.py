# remove warning message
import os
import os.path
import sys
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

# required by wpod-net
import cv2
import numpy as np
from local_utils import detect_lp
from os.path import splitext,basename
from tensorflow.keras.models import model_from_json
from imageio import imwrite
import logging
logging.getLogger().setLevel(logging.ERROR)

def load_model(path):
    try:
        path = splitext(path)[0]
        with open('%s.json' % path, 'r') as json_file:
            model_json = json_file.read()
        model = model_from_json(model_json, custom_objects={})
        model.load_weights('%s.h5' % path)
        print("Loading model successfully...")
        return model
    except Exception as e:
        print(e)

wpod_net_path = "wpod-net.json"
wpod_net = load_model(wpod_net_path)

def preprocess_image(image_path,resize=False):
    img = cv2.imread(image_path)
    # cv2.imshow(img)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = img / 255
    if resize:
        img = cv2.resize(img, (224,224))
    return img

def get_plate(image_path, Dmax=608, Dmin = 608):
    vehicle = preprocess_image(image_path)
    ratio = float(max(vehicle.shape[:2])) / min(vehicle.shape[:2])
    side = int(ratio * Dmin)
    bound_dim = min(side, Dmax)
    _ , LpImg, _, cor = detect_lp(wpod_net, vehicle, bound_dim, lp_threshold=0.5)
    return vehicle, LpImg, cor

def delete_prev_plates():
    with os.scandir("plates/") as scanner:
        for plate in scanner:
            os.remove(plate)

def main():
    delete_prev_plates()
    count = 0
    for file in os.listdir("frames/"):
        vehicle, LpImg,cor = get_plate(os.path.join("frames",file))
        for i in LpImg:
            imwrite("plates/LP{}.png".format(count), i)
            count += 1

if __name__ == "__main__":
    main()
