import time
import json
import os

from Checker import Checker
from Detector import Detector
from Visualizer import Visualizer

FRAME_PATH = "/home/arnaldo/SafeBox/projetao/frame.png"
JSON_PATH = "/home/arnaldo/SafeBox/projetao/jsons/"

detector = Detector("https://tfhub.dev/tensorflow/efficientdet/lite2/detection/1")
checador = Checker()

listing = os.listdir(JSON_PATH)

while True:
    for cam in listing:
        if cam != '.gitkeep':
            with open(JSON_PATH+cam) as json_file:
                time.sleep(18)

                net_out = detector.run(FRAME_PATH)
                web_out = json.load(json_file)

                alerts = checador.check(net_out=net_out,
                                        web_out=web_out)

                with open(os.path.join(JSON_PATH, 'alerts.json'), "w") as out_file:
                    json.dump(alerts, out_file, indent=2)





