import json
import time

import cv2 as cv
import tensorflow as tf
import tensorflow_hub as hub
import pandas as pd


class Detector:
    def __init__(self, net, write_output=False):
        self.net = hub.load(net)
        self.write_output = write_output
        self.labels = pd.read_csv('labels.csv', sep=';', index_col='ID')
        self.labels = self.labels['OBJECT (2017 REL.)']

    def run(self, frame_path):
        frame = cv.imread(frame_path)

        rgb_tensor = tf.convert_to_tensor(frame, dtype=tf.uint8)
        rgb_tensor = tf.expand_dims(rgb_tensor, 0)

        boxes, scores, classes, num_detections = self.net(rgb_tensor)

        pred_labels = classes.numpy().astype('int')[0]
        pred_labels = [self.labels[i] for i in pred_labels]

        pred_boxes = boxes.numpy()[0].astype('int')
        pred_scores = scores.numpy()[0]

        output = {}

        for i, (score, (y1, x1, y2, x2), label) in enumerate(zip(pred_scores, pred_boxes, pred_labels)):

            if score < 0.3 or label != 'person':
                continue


            output[i] = {'label': label,
                         'y1': str(y1),
                         'x1': str(x1),
                         'y2': str(y2),
                         'x2': str(x2)
                         }


        if self.write_output:
            with open('output.json', 'w') as out_file:
                json.dump(output, out_file, indent=2)

        return output


if __name__ == '__main__':
    detector = Detector("https://tfhub.dev/tensorflow/efficientdet/lite2/detection/1")
    #start = time.time()
    detector.run("/home/arnaldo/Documents/TEST_FRAMES/test_1.png")
    #end = time.time()
    #print(end - start)