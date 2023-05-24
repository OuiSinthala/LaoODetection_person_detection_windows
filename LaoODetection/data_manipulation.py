import numpy as np
import torch
import cv2 as cv


def get_data_from_gpu(detected_object_data: list, tracker_info: np.array, ):
    """Note: we want a numpy array from the model, but we are using the gpu to run the model
    with pytorch which the output array that we want also called tensor is located in the gpu memory
    while numpy ar ray is located in cpu memory.
    Therefore, we have to convert the tensor to normal numpy array."""
    current_detected_object_from_gpu = torch.tensor(detected_object_data).cuda()
    current_detected_object_from_gpu_to_cpu = current_detected_object_from_gpu.cpu()
    current_detected_object = np.array(current_detected_object_from_gpu_to_cpu)
    tracker_info = np.vstack((tracker_info, current_detected_object))
    return tracker_info


def get_data_from_cpu(detected_object_data: list, tracker_info: np.array):
    tracker_info = np.vstack((tracker_info, detected_object_data))
    return tracker_info


def creating_detection_line(captured_frame, counter_line, color=(0, 0, 255), thickness=5):
    # Counter line:
    cv.line(captured_frame, (counter_line[0], counter_line[1]),
            (counter_line[2], counter_line[3]), color, thickness)
