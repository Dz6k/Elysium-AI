from datetime import datetime
# credits: Aimmy // https://discord.com/invite/aimmy // https://github.com/Babyhamsta
class Wise:
    class WiseDetect:
        def __init__(
            self, 
            x: int,
            y: int,
            # time: datetime = None 
        ):
            self.x = x
            self.y = y
      
            
    def __init__(self) -> None:
        self.last_update_time = None
        self.alpha = 1.2  # Smoothing factor, adjust as necessary
        self.ema_x = None
        self.ema_y = None

    def update_detection(self, detection: WiseDetect) -> None:
        if self.last_update_time is None:
            self.ema_x = detection.x
            self.ema_y = detection.y
        else:
            self.ema_x = self.alpha * detection.x + (1 - self.alpha) * self.ema_x
            self.ema_y = self.alpha * detection.y + (1 - self.alpha) * self.ema_y
        
        self.last_update_time = datetime.utcnow()

    def get_estimated_position(self) -> WiseDetect:
        return self.WiseDetect(int(self.ema_x), int(self.ema_y))


WiseManager = Wise()
