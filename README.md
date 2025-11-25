# Automated Lane Barrier Control System �

An intelligent **computer vision-based automated barrier control system** that detects vehicle movement across a designated lane using YOLOv8 and automatically controls the opening/closing of lane barriers without requiring any physical sensors.

## 🎯 Overview

This project is designed to **automatically control lane/road barriers** by monitoring vehicle movement through computer vision. When a vehicle is detected crossing a virtual tripwire line, the system determines if the vehicle is within the barrier zone and sends a control signal to:

- **OPEN the barrier** (Status = 1): When vehicle is detected inside the barrier zone → **BARRIER OPEN🔴**
- **CLOSED the barrier** (Status = 0): When vehicle moves out of the barrier zone → **BARRIER CLOSED 🟢**

This eliminates the need for physical sensors (IR sensors, pressure plates, etc.) by using AI-powered computer vision instead!

## 🚀 Key Features

✅ **Automatic Barrier Control** - Opens/closes lane barriers without human intervention  
✅ **Real-time Vehicle Detection** - Uses YOLOv8 for accurate vehicle detection  
✅ **Intelligent Tracking** - Maintains persistent object tracking across frames  
✅ **Virtual Tripwire** - Detects when vehicles cross a defined barrier detection line  
✅ **Zone Monitoring** - Monitors vehicle presence within the barrier zone  
✅ **No Physical Sensors** - Purely computer vision-based (no IR/pressure sensors needed)  
✅ **Live Visualization** - Real-time video feed with detection boxes and barrier status  
✅ **Easy Integration** - Status output can connect to barrier motor control systems  

## 📋 System Logic

1. **Video Input** → Process video frames from camera/file
2. **Object Detection** → YOLO detects vehicles (trucks)
3. **Tripwire Crossing** → Detects when vehicle crosses virtual line
4. **Zone Monitoring** → Checks if vehicle is inside the barrier region
5. **Status Output** → Outputs barrier control signal (OPEN/CLOSED)

### Detection Regions:
- **Red Rectangle**: Barrier zone (monitoring area)
- **Purple Line**: Tripwire (crossing detection line)
- **Bounding Boxes**: Detected vehicles with tracking IDs

## 💻 Requirements

- Python 3.8 or higher
- OpenCV (computer vision processing)
- YOLOv8 (vehicle detection)
- PyTorch (deep learning framework)
- NumPy (numerical operations)

## 📦 Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/Lane_Barrier.git
   cd Lane_Barrier
   ```

2. **Create a virtual environment (recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Download YOLOv8 model:**
   - The model will be automatically downloaded on first run, or
   - Pre-download: `yolov8m.pt` (included in repository)

## 🎬 Usage

### Basic Run:
```bash
python Cam1_Lane_Barrier.py
```

### Customization:

Edit the following constants in `Cam1_Lane_Barrier.py` to adjust for your camera setup:

```python
# Video resolution
TARGET_WIDTH, TARGET_HEIGHT = 640, 480

# Tripwire line coordinates (start point and end point)
TRIPWIRE_START = (117, 328)
TRIPWIRE_END = (26, 475)

# Barrier zone region (top-left and bottom-right corners)
REGION_TOP_LEFT = (190, 4)
REGION_BOTTOM_RIGHT = (634, 473)

# Video source
cap = cv2.VideoCapture("video.mp4")  # Change to 0 for webcam
```

### Exit:
Press **'q'** to quit the application.

## � Live Demo

**Check out the Lane Barrier Detection System in action:**

[![Lane Barrier Detection Demo](https://img.shields.io/badge/📹%20Watch%20Demo-Click%20Here-blue?style=for-the-badge)](./Demo.mp4)

**[Demo.mp4](./Demo.mp4)** - See real-time vehicle detection, tripwire crossing, and automatic barrier status control

### What to Look For in the Demo:
- 🟢 **Green Bounding Boxes** - Vehicle detected outside barrier zone (Status: 1 - OPEN)
- 🔴 **Red Bounding Boxes** - Vehicle detected inside barrier zone (Status: 0 - CLOSED)
- 🟣 **Purple Line** - Virtual tripwire crossing detection line
- 🟡 **Yellow Rectangle** - Barrier monitoring zone
- 📊 **Status Display** - "Lane Barrier: 0" or "Lane Barrier: 1" shown in top-left

## �📊 Output

The system displays:
- **Bounding boxes** around detected vehicles
- **Tracking IDs** for each vehicle
- **Barrier status**: "Lane Barrier: 1" (OPEN) or "Lane Barrier: 0" (CLOSED)
- **Color-coded indicators**:
  - 🟢 **Green**: Vehicle outside zone (OPEN)
  - 🔴 **Red**: Vehicle inside zone (CLOSED)

## 🔧 Configuration

### Vehicle Detection:
By default, the system detects **trucks**. To change the target vehicle class:

```python
TANKER_NAME = "truck"  # Change to: "car", "bus", "motorcycle", etc.
```

Supported classes depend on the COCO dataset labels.

### Model Selection:
Available YOLOv8 models:
- `yolov8n.pt` - Nano (fastest, least accurate)
- `yolov8s.pt` - Small
- `yolov8m.pt` - Medium (current, balanced)
- `yolov8l.pt` - Large
- `yolov8x.pt` - Extra Large (slowest, most accurate)

## 📝 Project Structure

```
Lane_Barrier/
├── Cam1_Lane_Barrier.py      # Main barrier control script
├── yolov8m.pt               # Pre-trained YOLOv8 vehicle detection model
├── requirements.txt         # Python dependencies
├── README.md               # Project documentation
├── Demo.mp4                # Demo video showing barrier control in action
└── video.mp4               # Input video file (or use webcam with index 0)
```

## 🎓 How It Works

### Tripwire Detection Algorithm:
Uses cross-product calculation to detect when a tracked object crosses a virtual line:
```
side = (xB - xA) * (cy - yA) - (yB - yA) * (cx - xA)
```
If `side` changes sign, the vehicle has crossed the tripwire.

### Zone Detection:
Checks if the vehicle's center point (cx, cy) lies within the rectangular barrier zone using bounding box comparison.

## ⚙️ System Requirements

- **CPU**: Intel i5/Ryzen 5 or better (recommended)
- **GPU**: NVIDIA GPU with CUDA support (optional, for faster processing)
- **RAM**: Minimum 4GB, recommended 8GB+
- **Storage**: ~100MB for model files

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| Model not downloading | Install with `pip install --upgrade ultralytics` |
| Poor detection accuracy | Adjust tripwire/zone coordinates; ensure proper lighting |
| Slow performance | Use lighter model (`yolov8n.pt`) or lower resolution |
| Tracking ID resets | Increase persistence or reduce frame rate fluctuations |

## 🚀 Future Enhancements

- 📡 Integration with physical barrier control systems (GPIO/Serial)
- 🎥 Multi-camera support
- 📊 Data logging and statistics
- 🤖 ML-based zone optimization
- 📱 Web dashboard for monitoring
- 🔔 Alert system for unauthorized entries

## 📄 License

MIT License - Feel free to use and modify for your projects.

## 📞 Support

For issues, questions, or contributions:
- Open an issue on GitHub
- Submit a pull request
- Contact: fzkn1998@gmail.com

---

**Made with Python 🐍 + YOLOv8 🤖 + OpenCV 📷**
