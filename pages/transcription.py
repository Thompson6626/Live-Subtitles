import numpy as np
import soundcard as sc
from faster_whisper import WhisperModel
from PyQt6.QtCore import QThread, pyqtSignal, QThreadPool, QRunnable
from typing_extensions import override

SAMPLE_RATE = 16000  # Faster Whisper expects 16 kHz
CHUNK_SEC = 1  # Reduce latency (1-second chunks)
BUFFER_LIMIT = 5  # Store 5 chunks before processing
MODEL_CACHE = {}  # Cache for loaded models

def get_whisper_model(model_name: str):
    """Load the Faster Whisper model and cache it to avoid reloading."""
    if model_name not in MODEL_CACHE:
        MODEL_CACHE[model_name] = WhisperModel(model_name, device="cuda", compute_type="float16")
    return MODEL_CACHE[model_name]

class TranscriptionTask(QRunnable):
    """Runs Faster Whisper transcription in a separate thread."""
    def __init__(self, model, chunk, signal):
        super().__init__()
        self.model = model
        self.chunk = chunk  # Process a single chunk at a time
        self.signal = signal

    @override
    def run(self):
        """Process and transcribe the audio chunk immediately."""

        # If language not given ,it will be guessed on the first 30 seconds
        # TODO Add multilingual gui

        segments, _ = self.model.transcribe(
            self.chunk,
            language="en",
            task="transcribe",
            without_timestamps=True,
            beam_size=5,
            best_of=5,
            temperature=[0.0, 0.2, 0.4, 0.6, 0.8, 1.0],
            vad_filter=True,
            multilingual=False,
            log_progress=False,
            word_timestamps=False,
            condition_on_previous_text=True
        )

        text = " ".join(segment.text.strip() for segment in segments if segment.text)
        if text:
            self.signal.emit(text)

class AudioStreamer(QThread):
    """Threaded audio recording and transcription."""
    new_text_signal = pyqtSignal(str)

    def __init__(self, model_name: str = "medium"):
        super().__init__()
        self.model_name = model_name
        self.model = get_whisper_model(self.model_name)  # Use cached model
        self.thread_pool = QThreadPool.globalInstance()
        self.running = True  # Flag for stopping the thread

    @override
    def run(self):
        """Continuously capture and process system audio."""
        try:
            with sc.get_microphone(
                    id=str(
                        sc.default_speaker().name
                    ),
                    include_loopback=True
            ).recorder(
                samplerate=SAMPLE_RATE
            ) as mic:
                while self.running:
                    data = mic.record(numframes=int(SAMPLE_RATE * CHUNK_SEC))

                    if data.ndim > 1:  # Convert stereo to mono properly
                        data = np.mean(data, axis=1, dtype=np.float32)

                    chunk = data.astype(np.float32)

                    # Process transcription immediately instead of waiting
                    task = TranscriptionTask(self.model, chunk, self.new_text_signal)
                    self.thread_pool.start(task)

        except Exception as e:
            print(f"Error in audio streaming: {e}")

    def stop(self):
        """Stop the audio recording and ensure resources are released."""
        self.running = False  # Stop the loop

        # Close the microphone stream safely
        if hasattr(self, "stream") and self.stream is not None:
            self.stream.stop_stream()
            self.stream.close()

        # Wait for any remaining tasks to finish
        if self.thread_pool:
            self.thread_pool.waitForDone()

        print("Audio streaming stopped.")



