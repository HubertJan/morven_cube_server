import cv2


def capture_image(camera_id: int) -> cv2.Mat:  # type:ignore
    cam = cv2.VideoCapture(0)
    result = cam.read()
    ret = result[0]
    frame: cv2.Mat = result[1]  # type: ignore
    if not ret:
        raise Exception("Failed to capture an image")
    return frame
