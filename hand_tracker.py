import cv2
import mediapipe as mp

class HandTracker:
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.5
        )
        self.mp_draw = mp.solutions.drawing_utils
        self.lm_list = []

    def process(self, img):
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = self.hands.process(img_rgb)
        self.lm_list = []
        if results.multi_hand_landmarks:
            for hand_lms in results.multi_hand_landmarks:
                for id, lm in enumerate(hand_lms.landmark):
                    h, w, c = img.shape
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    self.lm_list.append([cx, cy])
                self.mp_draw.draw_landmarks(img, hand_lms, self.mp_hands.HAND_CONNECTIONS)
        return self.lm_list

    def fingers_up(self):
        fingers = []
        if len(self.lm_list) < 21: return [0,0,0,0,0]
        # Baş parmak (x eksenine göre)
        if self.lm_list[4][0] > self.lm_list[3][0]: fingers.append(1)
        else: fingers.append(0)
        # Diğer 4 parmak (y eksenine göre)
        for tip in [8, 12, 16, 20]:
            if self.lm_list[tip][1] < self.lm_list[tip - 2][1]: fingers.append(1)
            else: fingers.append(0)
        return fingers