import numpy as np
import soundcard as sc
from faster_whisper import WhisperModel
from PyQt6.QtCore import QThread, pyqtSignal, QThreadPool, QRunnable

SAMPLE_RATE = 16000  # Faster Whisper expects 16 kHz
CHUNK_SEC = 2  # Reduce latency (1-second chunks)
MODEL_CACHE = {}  # Cache for loaded models

def get_whisper_model(model_name: str = "medium"):
    """Load the Faster Whisper model and cache it to avoid reloading."""
    if model_name not in MODEL_CACHE:
        MODEL_CACHE[model_name] = WhisperModel(model_name, device="cuda", compute_type="float16")
    return MODEL_CACHE[model_name]

class TranscriptionTask(QRunnable):
    """Runs Faster Whisper transcription in a separate thread."""
    def __init__(self, model, chunk, signal, **settings):
        super().__init__()
        self.model = model
        self.chunk = chunk  # Process a single chunk at a time
        self.signal = signal

        self.language = settings.get("language", None)
        self.task = settings.get("task", "transcribe")
        self.multilingual = settings.get("multilingual", False)

    def run(self):
        """Process and transcribe the audio chunk immediately."""
        try:
            segments, _ = self.model.transcribe(
                self.chunk,
                language=self.language,
                task=self.task,
                without_timestamps=True,
                beam_size=5,
                best_of=5,
                temperature=[0.0, 0.2, 0.4, 0.6, 0.8, 1.0],
                multilingual=self.multilingual,
                word_timestamps=False
            )

            text = " ".join(segment.text.strip() for segment in segments if segment.text)
            if text:
                self.signal.emit(text)

        except Exception as e:
            print(f"Error in transcription: {e}")

class AudioStreamer(QThread):
    """Threaded audio recording and transcription."""
    new_text_signal = pyqtSignal(str)

    def __init__(self, model_name: str = "medium", **settings):
        super().__init__()
        self.model = get_whisper_model(model_name)  # Use cached model
        self.thread_pool = QThreadPool.globalInstance()
        self.running = True  # Flag for stopping the thread
        self.settings = settings

    def run(self):
        """Continuously capture and process system audio."""
        try:
            mic = sc.get_microphone(
                id=str(sc.default_speaker().name),
                include_loopback=True
            )

            with mic.recorder(samplerate=SAMPLE_RATE) as recorder:
                while self.running:
                    data = recorder.record(numframes=int(SAMPLE_RATE * CHUNK_SEC))

                    if data.ndim > 1:  # Convert stereo to mono
                        data = np.mean(data, axis=1).astype(np.float32)

                    chunk = data.astype(np.float32)

                    # Process transcription immediately
                    task = TranscriptionTask(self.model, chunk, self.new_text_signal, **self.settings)
                    self.thread_pool.start(task)

        except Exception as e:
            print(f"Error in audio streaming: {e}")

    def stop(self):
        """Stop the audio recording and ensure resources are released."""
        self.running = False  # Stop the loop
        self.thread_pool.waitForDone()  # Wait for all tasks to finish
        print("Audio streaming stopped.")
