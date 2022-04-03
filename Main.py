from Checker import Checker
from Detector import Detector
from Visualizer import Visualizer

import json

FRAME_PATH = "/home/arnaldo/Documents/TEST_FRAMES/test_1.png"

detector = Detector("https://tfhub.dev/tensorflow/efficientdet/lite2/detection/1")
net_out = detector.run(FRAME_PATH)

with open('cam1.json') as json_file:
    web_out = json.load(json_file)

checador = Checker()

alerts = checador.check(net_out=net_out,
                        web_out=web_out,
                        iou_thresh=0.5)

print(alerts)

visualizer = Visualizer(frame_path=FRAME_PATH,
                        net_out=net_out,
                        web_out=web_out)

visualizer.view()

