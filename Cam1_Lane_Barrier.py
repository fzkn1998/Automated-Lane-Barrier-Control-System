import os
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"
from ultralytics import YOLO
import cv2
import numpy as np

# Constants
TARGET_WIDTH, TARGET_HEIGHT = 640, 480
TRIPWIRE_START = (117, 328)
TRIPWIRE_END = (26, 475)
REGION_TOP_LEFT = (190, 4)
REGION_BOTTOM_RIGHT = (634, 473)

TANKER_NAME = "truck"
model = YOLO("yolov8m.pt")
TANKER_ID = [k for k, v in model.names.items() if v == TANKER_NAME][0]

cap = cv2.VideoCapture("video.mp4")

# Har track_id ke liye state: {'crossed': bool, 'inside': bool, 'prev_side': float}
track_states = {}

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.resize(frame, (TARGET_WIDTH, TARGET_HEIGHT))
    results = model.track(frame, persist=True)[0]

    status = 0
    cv2.rectangle(frame, REGION_TOP_LEFT, REGION_BOTTOM_RIGHT, (255, 255, 0), 2)
    cv2.line(frame, TRIPWIRE_START, TRIPWIRE_END, (255, 0, 255), 2)

    for box in results.boxes:
        cls_id = int(box.cls)
        if cls_id != TANKER_ID:
            continue

        x1, y1, x2, y2 = map(int, box.xyxy[0])
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

        track_id = int(box.id) if box.id is not None else None
        if track_id is None:
            continue

        # Tripwire crossing logic
        xA, yA = TRIPWIRE_START
        xB, yB = TRIPWIRE_END
        side = (xB - xA)*(cy - yA) - (yB - yA)*(cx - xA)

        if track_id not in track_states:
            track_states[track_id] = {'crossed': False, 'inside': False, 'prev_side': side}
        else:
            prev_side = track_states[track_id]['prev_side']
            if not track_states[track_id]['crossed'] and side * prev_side < 0:
                track_states[track_id]['crossed'] = True  # Tripwire crossed
            track_states[track_id]['prev_side'] = side

        # Zone logic (only after tripwire crossed)
        inside_roi = (REGION_TOP_LEFT[0] <= cx <= REGION_BOTTOM_RIGHT[0]) and \
                     (REGION_TOP_LEFT[1] <= cy <= REGION_BOTTOM_RIGHT[1])

        if track_states[track_id]['crossed']:
            if inside_roi:
                color = (0, 0, 255)  # Red
                status = 1
                track_states[track_id]['inside'] = True
            else:
                color = (0, 255, 0)  # Green
                status = 0
                track_states[track_id]['inside'] = False
        else:
            color = (0, 255, 0)  # Green
            status = 0

        cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
        cv2.circle(frame, (cx, cy), 4, color, -1)
        cv2.putText(frame, f'ID: {track_id}', (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

    cv2.putText(frame, f"Lane Barrier: {status}", (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
    cv2.imshow("Lane_Barrier_Task", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()