import cv2
import numpy as np
from uuid import uuid1
import os

def get_output_layers(net):
    
    layer_names = net.getLayerNames()
    try:
        output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]
    except:
        output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]

    return output_layers

def draw_prediction(img, class_id, confidence, x, y, x_plus_w, y_plus_h, COLORS, classes):

    label = str(classes[class_id])

    color = COLORS[class_id]

    cv2.rectangle(img, (x,y), (x_plus_w,y_plus_h), color, 2)

    cv2.putText(img, label, (x-10,y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

def main(to_open_image, all=True):
    classes = None
    image = cv2.imread(to_open_image)
    a = cv2.resize(image,(768, 576))
    arr = [a]
    Width = image.shape[1]
    Height = image.shape[0]
    scale = 0.00392
    config= r"L:\Simple-Flask-ML-APP\object-detection-opencv\yolov3.cfg"
    weights = r"L:\Simple-Flask-ML-APP\object-detection-opencv\yolov3.weights"
    to_open_classes = r"L:\Simple-Flask-ML-APP\object-detection-opencv\yolov3.txt"
    with open(to_open_classes, 'r') as f:
        classes = [line.strip() for line in f.readlines()]
    
    COLORS = np.random.uniform(0, 255, size=(len(classes), 3))
    net = cv2.dnn.readNet(weights, config)

    blob = cv2.dnn.blobFromImage(image, scale, (416,416), (0,0,0), True, crop=False)

    net.setInput(blob)

    outs = net.forward(get_output_layers(net))
    
    class_ids = []
    confidences = []
    boxes = []
    conf_threshold = 0.5
    nms_threshold = 0.4
    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.5:
                center_x = int(detection[0] * Width)
                center_y = int(detection[1] * Height)
                w = int(detection[2] * Width)
                h = int(detection[3] * Height)
                x = center_x - w / 2
                y = center_y - h / 2
                class_ids.append(class_id)
                confidences.append(float(confidence))
                boxes.append([x, y, w, h])


    indices = cv2.dnn.NMSBoxes(boxes, confidences, conf_threshold, nms_threshold)
    copy = image.copy()
    for i in indices:
        try:
            box = boxes[i]
        except:
            i = i[0]
            box = boxes[i]
        
        x = box[0]
        y = box[1]
        w = box[2]
        h = box[3]
        if all:
        # extract objects
            try:
                copy_ = copy
                crop_img = copy_[round(y):round(y)+round(h), round(x):round(x+w)]
                crop_img = cv2.resize(crop_img,(768, 576))
                arr.append(crop_img)
            except:
                pass
        draw_prediction(image, class_ids[i], confidences[i], round(x), round(y), round(x+w), round(y+h), COLORS, classes)    
    
    try:
        a = cv2.resize(image,(768, 576))
        arr.append(a)
        cv2.destroyAllWindows()
    
        collage = np.hstack(arr)
    except:
        pass
    return collage    
    