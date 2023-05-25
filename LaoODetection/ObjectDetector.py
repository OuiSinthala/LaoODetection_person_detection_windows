# Other modules
import math
from ultralytics import YOLO
import cvzone
import threading

# Modules inside this package
from LaoODetection.sound_config import play_sound
from LaoODetection.ObjectNames import object_names
from LaoODetection.ObjectTracker import TrackerDetection
from LaoODetection.data_manipulation import *
from LaoODetection.sort import *

# Important object:
tracker = Sort(max_age=60, min_hits=3, iou_threshold=0.3)


class ObjectDetector:

    def __init__(self, target_object="person"):
        self.model = YOLO("LaoODetection/yoloV8_Models/yoloV8n.pt")
        self.target_object = target_object
        self.number_of_detected_objects = 0

    def object_detection(self, video_capture):
        total_detected_object = []
        while True:
            # Read the frame from video stream
            success_status, captured_frame = video_capture.read()

            # If there are no more frames, break out of the loop
            if not success_status:
                print("Error!! : There is no input source")
                break

            # Use YOLO model to detect objects in the frame
            results = self.model(captured_frame, stream=True)

            # Get list of detected objects on this frame
            detected_objects = self.detected_object_data_in_each_frame(results, captured_frame)

            # Update the tracker with detected objects and get the tracked objects on this frame
            tracked_objects = tracker.update(detected_objects)

            # Create a TrackerDetection object with current frame and tracked objects
            counter = TrackerDetection(captured_frame, tracked_objects)

            # Keep track of active object IDs
            active_object_ids = []

            # Loop over the tracked objects
            for tracked_object in tracked_objects:
                # Get the center and ID of the tracked object and draw bounding box and center on the object
                center_x, center_y, object_id = counter.tracking(tracked_object)
                
                
                # If this is a new object, add it to the list of total detected objects
                if object_id not in total_detected_object:
                    total_detected_object.append(object_id)
                    print("Hello") 
                    if len(total_detected_object) <= 1:
                        # Threading
                        sound_thread = threading.Thread(target=play_sound)
                        sound_thread.start()
                    
                    
                    
                # If the object is within the frame, add its ID to the list of active object IDs
                if 0 <= center_x <= captured_frame.shape[1] and 0 <= center_y <= captured_frame.shape[0]:
                    active_object_ids.append(object_id)
                    

            # Get the IDs of inactive objects and remove from the total detected objects by taking only the object that
            # is not in the inactive objects
            inactive_object_ids = set(total_detected_object) - set(active_object_ids)
            total_detected_object = [obj_id for obj_id in total_detected_object if obj_id not in inactive_object_ids]

            # Update the count of detected objects
            self.number_of_detected_objects = len(total_detected_object)

            # Display the count of detected objects
            cvzone.putTextRect(captured_frame, f"Amount: {self.number_of_detected_objects}",
                               pos=(50, 80),
                               font=cv.FONT_HERSHEY_SIMPLEX, scale=1.5, colorT=(0, 255, 0), thickness=2)

            # Display the current frame
            cv.imshow("captured image", captured_frame)
            # Wait for key press
            key = cv.waitKey(1)
            # Quit if the user presses 'q'
            if key == ord('q'):
                break

        # Release resources
        video_capture.release()
        cv.destroyAllWindows()

    def detected_object_data_in_each_frame(self, results, captured_frame) -> list:
        # Creating an empty list for a tracker
        tracker_info = np.empty((0, 5))
        for a_frame in results:
            boxes = [box for box in a_frame.boxes]
            for box in boxes:
                # Getting the position of a bounding box on an object
                x1, y1, x2, y2 = box.xyxy[0]
                x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                # Getting important values from the bounding box of a detected object
                confidence = math.ceil((box.conf[0] * 100))
                object_name_index = int(box.cls[0])
                current_detected_object = object_names[object_name_index]

                # Detect only specific objects and put a tracker on a detected object
                is_target_object_detected = current_detected_object in self.target_object
                is_confident_enough = confidence > 60
                is_valid_index = object_name_index < len(object_names)

                if is_target_object_detected and is_confident_enough and is_valid_index:
                    detected_object_data = [x1, y1, x2, y2, confidence]
                    if torch.__version__ == "2.0.0+cu117":
                        tracker_info = get_data_from_gpu(detected_object_data, tracker_info)
                        cv.rectangle(captured_frame, pt1=(x1, y1), pt2=(x2, y2), color=[0, 255, 255])
                    else:
                        tracker_info = get_data_from_cpu(detected_object_data, tracker_info)

        return tracker_info

    def object_line_counter(self, video_capture, region_of_interest,
                            detecting_range=(20, 20), counter_line1=None, ):
        while True:
            # Getting input
            success_status, captured_frame = video_capture.read()
            try:
                # Preprocessing the image (this should be changed to fit your need)
                captured_frame_region = cv.bitwise_and(captured_frame, region_of_interest)
            except cv.error as e:
                print("ERROR detect!!!!:{}".format(e))
                break

            # Using the YOLO model to detect objects on each frame
            results = self.model(captured_frame_region, stream=True)
            # Getting a list of data of detected objects on each frame into tracker_info
            # for keep tracking the object status
            tracker_info = self.detected_object_data_in_each_frame(results, captured_frame)

            # Getting information from trackers that are tracking objects from frames
            tracker_outputs = tracker.update(tracker_info)

            # Counter line before detect something for checking status of the line whether it count or not:
            if counter_line1 is not None:
                creating_detection_line(captured_frame, counter_line1)

            # Counting the tracker on each object
            if isinstance(detecting_range, tuple) and len(detecting_range) == 2:
                detecting_range = detecting_range
            else:
                raise Exception("the argument must be a tuple with 2 items ")

            counter = TrackerDetection(captured_frame, tracker_outputs)
            self.number_of_detected_objects = counter.counting_line_detection(detecting_range, counter_line1)

            # show each frame FROM the video
            cv.imshow("captured frame", captured_frame)

            # Video Stream control
            # cv.waitKey(0)  # for debugging purpose
            # Wait for key press
            key = cv.waitKey(1)
            # Quit if the user presses 'q'
            if key == ord('q'):
                break
            # Pause if the user presses 'space'
            elif key == ord(' '):
                while True:
                    key = cv.waitKey(1)
                    if key == ord(' '):
                        break

            # Release resources
        video_capture.release()
        cv.destroyAllWindows()
