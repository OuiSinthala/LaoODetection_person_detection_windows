import cv2 as cv
from LaoODetection import ObjectDetector

def main():
    # Note you can change the input source to be a webcam
    # Input source: Video
    video_capture = cv.VideoCapture(0)

    # Running the object detection algorithm
    detector = ObjectDetector(target_object="person")
    detector.object_detection(video_capture)

    print("Detected: {0} people.".format(detector.number_of_detected_objects))


if __name__ == "__main__":
    main()
