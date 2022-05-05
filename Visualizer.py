import cv2 as cv


class Visualizer:
    def __init__(self, frame_path, net_out, web_out):
        self.frame_path = frame_path
        self.net_out = net_out
        self.web_out = web_out

    def view(self):
        frame = cv.imread(self.frame_path)

        for out in self.net_out:
            img_boxes = cv.rectangle(frame, (int(self.net_out[out]['x1']), int(self.net_out[out]['y2'])),
                                     (int(self.net_out[out]['x2']), int(self.net_out[out]['y1'])),
                                     (0, 255, 0), 2)

        for out in self.web_out:
            img_boxes = cv.rectangle(frame, (int(self.web_out[out]['x1']), int(self.web_out[out]['y2'])),
                                     (int(self.web_out[out]['x2']), int(self.web_out[out]['y1'])),
                                     (0, 0, 255), 2)

        cv.imwrite('safeboxes.png', img_boxes)
