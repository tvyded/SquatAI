import cv2
import mediapipe as mp
import numpy as np

class SquatTracker:
    def __init__(self):
        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose(
            static_image_mode=False,
            model_complexity=1,
            enable_segmentation=False,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        self.draw = mp.solutions.drawing_utils
        self.reps = 0
        self.stage = "UP"
        self.correct_down = False
        self.current_form = "WAITING"
        self.current_angle = 0
        
    def calculate_angle(self, a, b, c):
        a, b, c = np.array(a), np.array(b), np.array(c)
        rad = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
        ang = abs(rad * 180 / np.pi)
        return 360 - ang if ang > 180 else ang
    
    def process_frame(self, frame):
        img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        res = self.pose.process(img)
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        
        if res.pose_landmarks:
            lm = res.pose_landmarks.landmark
            
            hip = [lm[24].x, lm[24].y]
            knee = [lm[26].x, lm[26].y]
            ankle = [lm[28].x, lm[28].y]
            
            self.current_angle = self.calculate_angle(hip, knee, ankle)
            
            if self.stage == "UP" and 80 <= self.current_angle <= 100:
                self.stage = "DOWN"
                self.correct_down = True
            elif self.stage == "DOWN" and self.current_angle > 160:
                self.stage = "UP"
                if self.correct_down:
                    self.reps += 1
                self.correct_down = False
            
            if 80 <= self.current_angle <= 100:
                self.current_form = "GOOD DEPTH"
            elif self.current_angle < 70:
                self.current_form = "TOO DEEP"
            else:
                self.current_form = "BAD FORM"
            
            self.draw.draw_landmarks(img, res.pose_landmarks, self.mp_pose.POSE_CONNECTIONS)
        
        # УБИРАЕМ ВСЕ НАДПИСИ С ВИДЕО!
        # Видео теперь чистое, только скелет
        
        return img
    
    def get_stats(self):
        return {
            'reps': self.reps,
            'form': self.current_form,
            'angle': self.current_angle,
            'stage': self.stage
        }
    
    def reset(self):
        self.reps = 0
        self.stage = "UP"
        self.correct_down = False
        self.current_form = "WAITING"