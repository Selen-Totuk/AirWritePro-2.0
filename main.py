import cv2
import numpy as np
import math
from hand_tracker import HandTracker
from shape_manager import Rectangle, Prism, Triangle, Circle, Cylinder
from calc_manager import EngineeringCalculator

class AirStudioPro:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        self.cap.set(3, 1280); self.cap.set(4, 720)
        self.tracker = HandTracker()
        self.shapes = []
        self.current_draw_type = "RECT" # Varsayılan çizim tipi
        self.selected_shape = None
        self.engineering_calculator = EngineeringCalculator()

        # Sol menü butonlarının tanımlanması (x, y, w, h, label, shape_type)
        self.menu_buttons = [
            (20, 50, 160, 60, "KARE", "RECT"),
            (20, 130, 160, 60, "PRİZMA", "PRISM"),
            (20, 210, 160, 60, "ÜÇGEN", "TRIANGLE"),
            (20, 290, 160, 60, "DAİRE", "CIRCLE"),
            (20, 370, 160, 60, "SİLİNDİR", "CYLINDER"),
            (20, 450, 160, 60, "HESAPLA", "CALC"),
            (20, 530, 160, 60, "TEMİZLE", "CLEAR")
        ]
        self.last_click_time = 0 # Buton spam'ini engellemek için

    def draw_sidebar(self, frame):
        cv2.rectangle(frame, (0, 0), (200, 720), (30, 30, 30), -1)
        cv2.line(frame, (200, 0), (200, 720), (100, 100, 100), 2)
        
        for (x, y, w, h, label, type) in self.menu_buttons:
            color = (0, 180, 0) if self.current_draw_type == type else (60, 60, 60)
            if type == "CALC" and self.engineering_calculator.is_visible: color = (0, 255, 255) # Hesap makinesi açıksa

            cv2.rectangle(frame, (x, y), (x + w, y + h), color, -1)
            cv2.putText(frame, label, (x + 20, y + 40), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

    def run(self):
        while True:
            success, frame = self.cap.read()
            if not success: break
            frame = cv2.flip(frame, 1)
            lms = self.tracker.process(frame)
            self.draw_sidebar(frame)

            finger_x, finger_y = 0, 0
            fingers = [0]*5

            if lms:
                finger_x, finger_y = lms[8][0], lms[8][1] # İşaret parmağı ucu
                fingers = self.tracker.fingers_up()

                current_time = cv2.getTickCount() / cv2.getTickFrequency()
                
                # --- Buton Hover ve Tıklama (İşaret + Orta parmak birleşikse) ---
                if fingers[1] and fingers[2] and (current_time - self.last_click_time) > 0.3: # Spam koruması
                    for (bx, by, bw, bh, label, type) in self.menu_buttons:
                        if bx < finger_x < bx + bw and by < finger_y < by + bh:
                            if type == "CALC":
                                self.engineering_calculator.is_visible = not self.engineering_calculator.is_visible
                            elif type == "CLEAR":
                                self.shapes = []
                                self.engineering_calculator.reset()
                                self.engineering_calculator.is_visible = False
                            else:
                                self.current_draw_type = type
                            self.last_click_time = current_time
                            break # Tek bir butona tıkla

                # --- HESAP MAKİNESİ ETKİLEŞİMİ (Sadece İşaret parmağı ile) ---
                if self.engineering_calculator.is_visible and fingers[1] and not any(fingers[0,2:]):
                    self.engineering_calculator.handle_click(finger_x, finger_y)


                # --- ÇİZİM ALANI (Sağ taraf - Sadece İşaret parmağı) ---
                if not self.engineering_calculator.is_visible and finger_x > 200:
                    if fingers[1] and not any([fingers[0], fingers[2], fingers[3], fingers[4]]): # Sadece işaret
                        if not self.selected_shape or self.selected_shape.type != self.current_draw_type:
                            shape_class = {
                                "RECT": Rectangle, "PRISM": Prism, "TRIANGLE": Triangle, 
                                "CIRCLE": Circle, "CYLINDER": Cylinder
                            }.get(self.current_draw_type)
                            if shape_class:
                                self.selected_shape = shape_class(finger_x, finger_y)
                                self.shapes.append(self.selected_shape)
                        else:
                            self.selected_shape.update(finger_x, finger_y)
                    else:
                        self.selected_shape = None # Çizim bitti

                    # --- BÜYÜTME / KÜÇÜLTME (Yumruk vs El Açık) ---
                    # Yumruk (tüm parmaklar aşağıda)
                    if sum(fingers) == 0 and len(self.shapes) > 0:
                        for s in self.shapes:
                            s.x2 = int(s.x1 + (s.x2 - s.x1) * 0.98)
                            s.y2 = int(s.y1 + (s.y2 - s.y1) * 0.98)
                    # El Açık (tüm parmaklar yukarıda)
                    elif sum(fingers) == 5 and len(self.shapes) > 0:
                        for s in self.shapes:
                            s.x2 = int(s.x1 + (s.x2 - s.x1) * 1.02)
                            s.y2 = int(s.y1 + (s.y2 - s.y1) * 1.02)

            # --- TÜM ÇİZİMLERİ YAP ---
            for s in self.shapes:
                s.draw(frame)
            
            # --- HESAP MAKİNESİ ÇİZİMİ VE ETKİLEŞİMİ ---
            self.engineering_calculator.draw(frame, finger_x, finger_y)


            cv2.imshow("AirStudio Pro - Sanal Mühendislik İstasyonu", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'): break

        self.cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    app = AirStudioPro()
    app.run()