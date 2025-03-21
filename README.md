# Python Speech-to-Text Application

This is a Python desktop application that uses **FasterWhisper** for real-time speech-to-text transcription, with a **PyQt6** interface for displaying the transcribed text. The application processes audio input using **SoundCard** and leverages **NumPy** for efficient data handling.

## 🚀 Features
- 🎤 Real-time **speech recognition** using **FasterWhisper**
- 🖥 **PyQt6 GUI** to display transcribed text
- 🔊 **Microphone input** handling with **SoundCard**
- ⚡ Optimized performance with **NumPy**

## 📦 Installation

### 1️⃣ Prerequisites
Make sure you have **Python 3.8+** installed on your system.

### 2️⃣ Install Dependencies
First, create a virtual environment (optional but recommended):
```sh
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

Then install the required packages from `requirements.txt`:
```sh
pip install -r requirements.txt
```

Or manually install them:
```sh
pip install numpy faster-whisper soundcard PyQt6
```

## 🛠 Usage
Run the application:
```sh
python main.py
```

## 📁 Project Structure
```
.
├── pages/                 # PyQt pages and the transcription logic file
├── requirements.txt       # Dependencies
├── README.md              # Project documentation
└── main.py                # Main application file
```

## ⚙️ Configuration

For **GPU acceleration**, use:
```python
model = WhisperModel("small", device="cuda")
```
### ⚡ GPU Requirements
GPU execution requires the following NVIDIA libraries to be installed:
- **cuBLAS** for CUDA 12
- **cuDNN 9** for CUDA 12

For more information, check the official **FasterWhisper** repository: [SYSTRAN/faster-whisper](https://github.com/SYSTRAN/faster-whisper)

#### Otherwise just use cpu:
```python
model = WhisperModel("small", device="cpu")
```
## ✅ TODOs
- [ ] Implement settings page for more configuration
- [ ] Improve UI design with additional styling
- [ ] Optimize performance for lower latency and better accuracy
- [ ] Fix crash when trying to stop listening
- [ ] Improve listening page so it can be resized and have customizable styling so it can actually work as a subtitle overlay 

## 📝 License
This project is licensed under the **MIT License**.

## 🤝 Contributing
Feel free to **fork** this repository and submit pull requests to improve it!


