import cv2

class Sidebar:
    def __init__(self):
        self.width = 200
        self.buttons = [
            {"label": "RECT", "type": "SHAPE", "y_range": (100, 160)},
            {"label": "PRISM", "type": "SHAPE", "y_range": (180, 240)},
            {"label": "CALC", "type": "TOOL", "y_range": (260, 320)},
            {"label": "UNIT", "type": "TOOL", "y_range": (340, 400)},
            {"label": "CLEAR", "type": "ACTION", "y_range": (420, 480)}
        ]
        self.colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (0, 255, 255)] # RGB

    def draw(self, frame):
        # Sol Panel Arka Planı
        cv2.rectangle(frame, (0, 0), (self.width, 720), (40, 40, 40), -1)
        cv2.line(frame, (self.width, 0), (self.width, 720), (200, 200, 200), 2)

        for btn in self.buttons:
            y1, y2 = btn["y_range"]
            cv2.rectangle(frame, (20, y1), (180, y2), (80, 80, 80), -1)
            cv2.putText(frame, btn["label"], (50, y1 + 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

    def check_click(self, x, y):
        if x < self.width:
            for btn in self.buttons:
                y1, y2 = btn["y_range"]
                if y1 < y < y2:
                    return btn
        return None