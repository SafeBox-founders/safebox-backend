from datetime import datetime, timedelta


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
        return datetime.strptime(time_str, '%m/%d/%y %H:%M:%S')

    def check(self, net_out, web_out):
        check_output = {}

        now = datetime.now()
        current_time = now.strftime("%m/%d/%y %H:%M:%S")
        current_date = now.strftime("%m/%d/%y")

        for box in web_out:
            start = web_out[box]['start']
            end = web_out[box]['end']
            min = web_out[box]['min']
            max = web_out[box]['max']


            safebox = (int(web_out[box]['x1']), int(web_out[box]['y1']), int(web_out[box]['x2']), int(web_out[box]['y2']))
            person_count = 0
            for out in net_out:
                detection = (int(net_out[out]['x1']), int(net_out[out]['y1']), int(net_out[out]['x2']), int(net_out[out]['y2']))
                if self.__iou(safebox, detection) != 0:
                    person_count += 1

            # gambiarra (s/n)
            end_date = current_date
            if self.__str_to_time(current_time) > self.__str_to_time(current_date+" "+end):
                end_date = end_date.split('/')
                end_date[1] = str(int(end_date[1])+1)
                end_date = '/'.join(end_date)

            if self.__str_to_time(current_date+" "+start) < self.__str_to_time(current_time) < self.__str_to_time(end_date+" "+end):
                tmp = current_time.split(" ")

                if person_count < int(min):
                    check_output[box] = {'alert': 'min',
                                         'date': tmp[0],
                                         'time': tmp[1]}

                if person_count > int(max):
                    check_output[box] = {'alert': 'max',
                                         'date': tmp[0],
                                         'time': tmp[1]}


        return check_output




