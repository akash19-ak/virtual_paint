
# 🖌️ Virtual Painter using Hand Gestures

This is a computer vision project that turns your hand into a virtual paintbrush! Using **OpenCV** and **MediaPipe**, you can draw on the screen by just moving your finger in front of your webcam. No mouse or touch required — just gestures!

---

## 🚀 Features

- 👆 Draw using your **index finger**
- 🎨 Choose colors: **Purple**, **Green**, **Red**
- 🧽 Use the **Eraser**
- 🗑️ Clear the canvas with one gesture
- 🖐️ Real-time **hand tracking** using MediaPipe

---

## 📷 Demo

https://user-images.githubusercontent.com/your_video_link.mp4 *(Add your screen recording here if available)*

---

## 🛠️ Technologies Used

- **Python 3**
- **OpenCV** – for capturing webcam and drawing
- **MediaPipe** – for real-time hand detection and landmark tracking
- **NumPy** – for managing the canvas as an image array

---

## 📦 Installation

1. **Clone the repository**

```bash
git clone https://github.com/yourusername/virtual-painter-hand-gestures.git
cd virtual-painter-hand-gestures
```

2. **Install the dependencies**

Make sure Python is installed, then run:

```bash
pip install opencv-python mediapipe numpy
```

3. **Run the application**

```bash
python virtual_painter.py
```

> Press `ESC` to exit the app.

---

## ✋ How to Use

- **Use only one hand** (for best results).
- Raise your **index finger** to draw.
- Tap the top buttons with your index finger to:
  - **Change color**
  - **Use eraser**
  - **Clear the screen**
- Lower your finger to **stop drawing**.

---

## 📁 File Structure

```
virtual-painter/
├── virtual_painter.py   # Main application script
├── README.md            # Project documentation
```

---

## 🙋‍♂️ Future Improvements

- Add **save drawing to file** option
- Add **brush thickness** control
- Support for **multi-hand drawing**
- Add **gesture-based undo** functionality

---

## 📸 Screenshot

*(Add a screenshot here of your application running)*

---

## 🧠 Credits

- **MediaPipe** by Google for hand tracking
- OpenCV community for powerful computer vision tools

---

## 📜 License

This project is open-source and free to use under the [MIT License](LICENSE).
