from datetime import datetime

class Checker:
    def __init__(self):
        pass

    def __iou(self, a, b):
        xa = max(a[0], b[0])
        ya = max(a[1], b[1])
        xb = min(a[2], b[2])
        yb = min(a[3], b[3])

        inter_area = max(0, xb - xa + 1) * max(0, yb - ya + 1)

        a_area = (a[2] - a[0] + 1) * (a[3] - a[1] + 1)
        b_area = (b[2] - b[0] + 1) * (b[3] - b[1] + 1)

        iou = inter_area / float(a_area + b_area - inter_area)

        return iou

    def __str_to_time(self, time_str):
        return datetime.strptime(time_str, '%H:%M:%S').time()

    def check(self, net_out, web_out, iou_thresh=0.5):
        check_output = []

        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")

        for box in web_out:
            start = web_out[box]['start']
            end = web_out[box]['end']
            min = web_out[box]['min']
            max = web_out[box]['max']

            safebox = (int(web_out[box]['x1']), int(web_out[box]['y1']), int(web_out[box]['x2']), int(web_out[box]['y2']))
            person_count = 0
            for out in net_out:
                detection = (int(net_out[out]['x1']), int(net_out[out]['y1']), int(net_out[out]['x2']), int(net_out[out]['y2']))
                if self.__iou(safebox, detection) > iou_thresh:
                    person_count += 1

            if self.__str_to_time(start) < self.__str_to_time(current_time) < self.__str_to_time(end):
                if person_count < int(min):
                    check_output.append("Min alert in {} - {}".format(box, current_time))
                if person_count > int(max):
                    check_output.append("Max alert in {} - {}".format(box, current_time))

        return check_output




