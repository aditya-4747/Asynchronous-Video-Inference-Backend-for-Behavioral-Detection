from ultralytics import YOLO
import cv2

class YoloInferenceService:
    def __init__(self, model_path: str):
        self.model = YOLO(model_path)

    def run(self, video_path: str, frame_interval: int):
        '''
        Docstring for run
        
        :param video_path: URL of the video
        :param frame_interval (30): considers 1 frame for a 30 fps video
        '''
        cap = cv2.VideoCapture(video_path)
        detections = []

        frame_idx = 0
        fps = cap.get(cv2.CAP_PROP_FPS) or 30

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            if frame_idx % frame_interval == 0:
                timestamp = frame_idx/fps
                spitting_instances = []

                results = self.model(frame, verbose=False)

                for r in results:
                    for box in r.boxes:
                        cls_id = int(box.cls[0])
                        conf = float(box.conf[0])
                        x1, y1, x2, y2 = map(int, box.xyxy[0])

                        if cls_id == 0 and conf > 0.6:
                            spitting_instances.append(
                                {"conf": conf, "box": [x1, y1, x2, y2]}
                            )
                
                if spitting_instances:
                    detections.append((timestamp, frame.copy(), spitting_instances))

            frame_idx += 1

        cap.release()
        return detections