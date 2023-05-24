import cv2 as cv
import cvzone
from LaoODetection.data_manipulation import creating_detection_line

total_detected_object = []


class TrackerDetection(object):

    def __init__(self, captured_frame, tracker_outputs):
        self.captured_frame = captured_frame
        self.tracker_outputs = tracker_outputs

    def tracking(self, tracked_object_data):
        # Bounding box location of each tracker from the detection
        x1, y1, x2, y2, object_id = tracked_object_data
        width, height = (x2 - x1), (y2 - y1)
        bounding_box = [int(x1), int(y1), int(width), int(height)]

        # Creating the bounding box and text over the tracker
        cvzone.cornerRect(self.captured_frame, bounding_box, rt=2, l=5, t=2, colorR=(0, 0, 255))
        cvzone.putTextRect(self.captured_frame, text="id: {0}".format(object_id),
                           pos=(int(max(0, x1)), int(max(35, y1))),
                           scale=0.5, colorT=(255, 255, 255), thickness=2, offset=1,
                           font=cv.FONT_HERSHEY_SIMPLEX)
        

        # Finding the center of the tracker for counting when each object has crossed the line
        center_x, center_y = int(x1 + width // 2), int(y1 + height // 2)

        # draw a circle at the center
        cv.circle(self.captured_frame, (center_x, center_y), 5, (0, 255, 0), cv.FILLED)

        return [center_x, center_y, object_id]

    def counting_line_detection(self, detecting_range=(20, 20), COUNTER_line1=None):
        global total_detected_object
        # Tracker operations:
        for tracked_object_data in self.tracker_outputs:
            # Getting the center and id from the tacker and draw bounding box and mark center on the object
            center_x, center_y, object_id = self.tracking(tracked_object_data)

            # start to count when the center of a tracker is in the line's range
            above_line, under_line = detecting_range
            if COUNTER_line1 is not None and COUNTER_line1[0] < center_x < COUNTER_line1[2] \
                    and COUNTER_line1[1] - above_line < center_y < COUNTER_line1[3] + under_line:

                if object_id not in total_detected_object:
                    total_detected_object.append(object_id)
                    # Change the counter line color when an object has crossed the line
                    creating_detection_line(self.captured_frame, COUNTER_line1, color=(0, 255, 0))

            # show the number
            cvzone.putTextRect(self.captured_frame, f"Amount: {len(total_detected_object)}", pos=(50, 80),
                               font=cv.FONT_HERSHEY_SIMPLEX, scale=1.5, colorT=(0, 255, 0), thickness=2)
        # return the amount of detected objects
        return len(total_detected_object)