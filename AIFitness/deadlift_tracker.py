import cv2
import mediapipe as mp
import numpy as np

class DeadliftTracker:
    def __init__(self, side='right', lower_thresh=0.65, raise_thresh=0.55,
                 too_deep_thresh=0.72, back_angle_thresh=70):
        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose(
            static_image_mode=False,
            model_complexity=1,
            enable_segmentation=False,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        self.draw = mp.solutions.drawing_utils
        self.side = side
        self.lower_thresh = lower_thresh
        self.raise_thresh = raise_thresh
        self.too_deep_thresh = too_deep_thresh
        self.back_angle_thresh = back_angle_thresh
        self.reps = 0
        self.stage = "UP"
        self.good_form = True
        self.current_form = "WAITING"
        self.current_angle = 0
        self.hip_y = 0

    def calculate_angle(self, a, b, c):
        a = np.array([a.x, a.y])
        b = np.array([b.x, b.y])
        c = np.array([c.x, c.y])
        rad = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
        ang = abs(rad * 180 / np.pi)
        return 360 - ang if ang > 180 else ang

    def process_frame(self, frame):
        frame = cv2.flip(frame, 1)  # зеркалим для удобства
        img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        res = self.pose.process(img)
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

        if res.pose_landmarks:
            lm = res.pose_landmarks.landmark

            # выбор стороны
            if self.side == 'right':
                shoulder = lm[12]
                hip = lm[24]
                knee = lm[26]
            else:
                shoulder = lm[11]
                hip = lm[23]
                knee = lm[25]

            self.back_angle = self.calculate_angle(shoulder, hip, knee)
            self.hip_y = hip.y

            # логика повторений
            if self.stage == "UP" and self.hip_y > self.lower_thresh:
                self.stage = "DOWN"
                self.good_form = True
            elif self.stage == "DOWN" and self.hip_y < self.raise_thresh:
                self.stage = "UP"
                if self.good_form:
                    self.reps += 1

            # оценка формы
            if self.hip_y > self.too_deep_thresh:
                self.current_form = "TOO DEEP"
                self.good_form = False
            elif self.hip_y < self.raise_thresh:
                self.current_form = "TOO HIGH"
                # не сбрасываем good_form, т.к. в начале подхода это нормально
            else:
                if self.back_angle < self.back_angle_thresh:
                    self.current_form = "ROUND BACK"
                    self.good_form = False
                else:
                    self.current_form = "GOOD FORM"

            self.draw.draw_landmarks(img, res.pose_landmarks, self.mp_pose.POSE_CONNECTIONS)

        return img

    def get_stats(self):
        return {
            'reps': self.reps,
            'form': self.current_form,
            'back_angle': self.back_angle if hasattr(self, 'back_angle') else 0,
            'hip_y': self.hip_y,
            'stage': self.stage
        }

    def reset(self):
        self.reps = 0
        self.stage = "UP"
        self.good_form = True
        self.current_form = "WAITING"