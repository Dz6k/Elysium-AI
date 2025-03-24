from utils import config
import supervision as sv
    
byte_tracker = sv.ByteTrack()

class ProcessImg:
    def process(self, model, image):
        return byte_tracker.update_with_detections(
            sv.Detections.from_ultralytics(
                model(
                    source=image,
                    conf=config.confidence,
                    imgsz=640,
                    iou=0.7,
                    nms = False,
                    classes=[0],
                    max_det=3,
                    agnostic_nms=False,
                    augment=False   ,
                    vid_stride=True,
                    visualize=False,
                    verbose=False,
                    show_boxes=False,
                    show_labels=False, 
                    show_conf=False,
                    save=False,  
                    show=False,
                )[0]
            )
        )
        
