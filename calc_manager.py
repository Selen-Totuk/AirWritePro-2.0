import cv2
import math

class EngineeringCalculator:
    def __init__(self):
        self.is_visible = False
        self.display_text = ""
        self.current_input = ""
        self.last_result = 0.0
        self.last_operator = None

        # Hesap Makinesi Butonları (x, y, w, h, label)
        self.buttons = [
            # Sayılar
            (700, 300, 70, 70, "7"), (780, 300, 70, 70, "8"), (860, 300, 70, 70, "9"),
            (700, 380, 70, 70, "4"), (780, 380, 70, 70, "5"), (860, 380, 70, 70, "6"),
            (700, 460, 70, 70, "1"), (780, 460, 70, 70, "2"), (860, 460, 70, 70, "3"),
            (700, 540, 70, 70, "0"), (780, 540, 70, 70, "."),
            # Operatörler
            (940, 300, 70, 70, "/"), (940, 380, 70, 70, "*"), (940, 460, 70, 70, "-"),
            (940, 540, 70, 70, "+"),
            # Fonksiyonlar
            (700, 220, 70, 70, "C"), (780, 220, 70, 70, "="), 
            (860, 220, 70, 70, "sin"), (940, 220, 70, 70, "cos"),
            (700, 620, 150, 70, "PI"), (860, 620, 150, 70, "KAPAT")
        ]

    def draw(self, img, finger_x, finger_y):
        if not self.is_visible: return

        # Hesap Makinesi Arka Planı
        cv2.rectangle(img, (680, 200), (1030, 700), (50, 50, 50), -1)
        
        # Ekran
        cv2.rectangle(img, (700, 220), (1010, 280), (80, 80, 80), -1)
        cv2.putText(img, self.display_text, (710, 260), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

        for (bx, by, bw, bh, label) in self.buttons:
            # Buton rengini parmak üzerindeyse değiştir
            btn_color = (120, 120, 120)
            if bx < finger_x < bx + bw and by < finger_y < by + bh:
                btn_color = (0, 200, 0) # Yeşil vurgu
            
            cv2.rectangle(img, (bx, by), (bx + bw, by + bh), btn_color, -1)
            cv2.putText(img, label, (bx + 10, by + 45), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

    def handle_click(self, finger_x, finger_y):
        if not self.is_visible: return None

        for (bx, by, bw, bh, label) in self.buttons:
            if bx < finger_x < bx + bw and by < finger_y < by + bh:
                if label == "KAPAT":
                    self.is_visible = False
                    self.reset()
                    return None
                elif label == "C":
                    self.reset()
                elif label == "=":
                    self._perform_calculation()
                elif label == "sin":
                    self._apply_function(math.sin)
                elif label == "cos":
                    self._apply_function(math.cos)
                elif label == "PI":
                    self.current_input = str(math.pi)
                    self.display_text = self.current_input
                elif label in ["+", "-", "*", "/"]:
                    if self.current_input:
                        self._perform_calculation(operator=label)
                    else:
                        self.last_operator = label
                else: # Sayılar ve nokta
                    self.current_input += label
                    self.display_text = self.current_input
                return label # Hangi butona basıldığını döndür

    def _perform_calculation(self, operator=None):
        try:
            if self.last_operator and self.current_input:
                num2 = float(self.current_input)
                if self.last_operator == "+": self.last_result += num2
                elif self.last_operator == "-": self.last_result -= num2
                elif self.last_operator == "*": self.last_result *= num2
                elif self.last_operator == "/": 
                    if num2 != 0: self.last_result /= num2
                    else: self.display_text = "Hata: Bolme 0"
                self.display_text = str(round(self.last_result, 4))
                self.current_input = ""
            elif self.current_input and not self.last_operator: # İlk sayı girişi
                self.last_result = float(self.current_input)
                self.display_text = self.current_input
                self.current_input = ""

            self.last_operator = operator if operator else None

        except ValueError:
            self.display_text = "Hata"
        except Exception as e:
            self.display_text = f"Hata: {e}"

    def _apply_function(self, func):
        try:
            if self.current_input:
                value = float(self.current_input)
                self.last_result = func(math.radians(value)) # Trigonometrik fonksiyonlar için dereceyi radyana çevir
                self.display_text = str(round(self.last_result, 4))
                self.current_input = ""
            elif self.last_result is not None:
                self.last_result = func(math.radians(self.last_result))
                self.display_text = str(round(self.last_result, 4))
        except Exception as e:
            self.display_text = f"Hata: {e}"

    def reset(self):
        self.display_text = ""
        self.current_input = ""
        self.last_result = 0.0
        self.last_operator = None