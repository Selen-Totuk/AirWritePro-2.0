import cv2
import numpy as np
import math

class Shape:
    def __init__(self, x, y, color=(0, 255, 0)):
        self.x1, self.y1 = x, y
        self.x2, self.y2 = x, y
        self.color = color
        self.type = "GENERIC"

    def update(self, x, y):
        self.x2, self.y2 = x, y

    def get_info(self):
        w_px = abs(self.x2 - self.x1)
        h_px = abs(self.y2 - self.y1)
        # 1 cm = 38 pixel varsayımı
        return w_px / 38.0, h_px / 38.0

    def draw(self, img):
        pass # Alt sınıflar implement edecek

class Rectangle(Shape):
    def __init__(self, x, y, color=(0, 255, 0)):
        super().__init__(x, y, color)
        self.type = "RECT"
    
    def draw(self, img):
        cv2.rectangle(img, (self.x1, self.y1), (self.x2, self.y2), self.color, 2)
        w, h = self.get_info()
        cv2.putText(img, f"A: {w*h:.1f} cm2", (self.x1, self.y1 - 10), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, self.color, 1)

class Prism(Shape):
    def __init__(self, x, y, color=(255, 100, 0)):
        super().__init__(x, y, color)
        self.type = "PRISM"

    def draw(self, img):
        w = abs(self.x2 - self.x1)
        h = abs(self.y2 - self.y1)
        d = min(w, h) // 4 # Derinlik
        
        # Ön yüz
        cv2.rectangle(img, (self.x1, self.y1), (self.x2, self.y2), self.color, 2)
        # Arka yüz
        cv2.rectangle(img, (self.x1 + d, self.y1 - d), (self.x2 + d, self.y2 - d), self.color, 2)
        # Bağlantılar
        cv2.line(img, (self.x1, self.y1), (self.x1 + d, self.y1 - d), self.color, 2)
        cv2.line(img, (self.x2, self.y1), (self.x2 + d, self.y1 - d), self.color, 2)
        cv2.line(img, (self.x1, self.y2), (self.x1 + d, self.y2 - d), self.color, 2)
        cv2.line(img, (self.x2, self.y2), (self.x2 + d, self.y2 - d), self.color, 2)
        
        # Hacim gösterimi (varsayılan derinlik 1 birim)
        w_cm, h_cm = self.get_info()
        volume = w_cm * h_cm * (d / 38.0) # Derinliği de cm'ye çevir
        cv2.putText(img, f"V: {volume:.1f} cm3", (self.x1, self.y1 - 10), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, self.color, 1)

class Triangle(Shape):
    def __init__(self, x, y, color=(0, 255, 255)):
        super().__init__(x, y, color)
        self.type = "TRIANGLE"

    def draw(self, img):
        x_mid = (self.x1 + self.x2) // 2
        pts = np.array([[x_mid, self.y1], [self.x1, self.y2], [self.x2, self.y2]], np.int32)
        cv2.polylines(img, [pts], True, self.color, 2)
        # Alan hesaplama
        base = abs(self.x2 - self.x1) / 38.0
        height = abs(self.y2 - self.y1) / 38.0
        area = 0.5 * base * height
        cv2.putText(img, f"A: {area:.1f} cm2", (self.x1, self.y1 - 10), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, self.color, 1)

class Circle(Shape):
    def __init__(self, x, y, color=(255, 0, 0)):
        super().__init__(x, y, color)
        self.type = "CIRCLE"
        self.radius = 0

    def update(self, x, y):
        super().update(x, y)
        self.radius = int(math.hypot(x - self.x1, y - self.y1))

    def draw(self, img):
        cv2.circle(img, (self.x1, self.y1), self.radius, self.color, 2)
        # Alan hesaplama
        r_cm = self.radius / 38.0
        area = math.pi * (r_cm ** 2)
        cv2.putText(img, f"A: {area:.1f} cm2", (self.x1 - self.radius, self.y1 - self.radius - 10), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, self.color, 1)

class Cylinder(Shape):
    def __init__(self, x, y, color=(0, 0, 255)):
        super().__init__(x, y, color)
        self.type = "CYLINDER"
        self.radius = 0
        self.height = 0

    def update(self, x, y):
        super().update(x, y)
        self.radius = int(abs(x - self.x1) / 2) # X ekseninde yarıçap
        self.height = abs(y - self.y1) # Y ekseninde yükseklik

    def draw(self, img):
        # Üst elips
        cv2.ellipse(img, (self.x1, self.y1), (self.radius, int(self.radius * 0.3)), 0, 0, 360, self.color, 2)
        # Alt elips
        cv2.ellipse(img, (self.x1, self.y1 + self.height), (self.radius, int(self.radius * 0.3)), 0, 0, 360, self.color, 2)
        # Yan çizgiler
        cv2.line(img, (self.x1 - self.radius, self.y1), (self.x1 - self.radius, self.y1 + self.height), self.color, 2)
        cv2.line(img, (self.x1 + self.radius, self.y1), (self.x1 + self.radius, self.y1 + self.height), self.color, 2)
        
        # Hacim hesaplama
        r_cm = self.radius / 38.0
        h_cm = self.height / 38.0
        volume = math.pi * (r_cm ** 2) * h_cm
        cv2.putText(img, f"V: {volume:.1f} cm3", (self.x1 - self.radius, self.y1 - 10), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, self.color, 1)