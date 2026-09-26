"""
vad.py - Real-Time Voice Activity Detection (VAD) & Audio Frame Processor for JARVIS
"""

import struct
import math

try:
    import torch
    # Optional Silero VAD
    SILERO_AVAILABLE = True
except ImportError:
    SILERO_AVAILABLE = False


class VoiceActivityDetector:
    """Real-Time Voice Activity Detector with Adaptive Noise Floor Tracking."""

    def __init__(self, sample_rate: int = 16000, sensitivity: float = 2.5):
        self.sample_rate = sample_rate
        self.sensitivity = sensitivity
        self.noise_floor = 100.0  # Initial RMS noise floor estimate
        self.speech_active = False
        self.silence_count = 0
        self.silero_model = None

        if SILERO_AVAILABLE:
            try:
                model, utils = torch.hub.load(
                    repo_or_dir="snakers4/silero-vad",
                    model="silero_vad",
                    force_reload=False,
                    trust_repo=True
                )
                self.silero_model = model
            except Exception as e:
                print(f"⚠️ Silero VAD load fallback: {e}")
                self.silero_model = None

    def calculate_rms(self, pcm_chunk: bytes) -> float:
        """Calculate Root Mean Square (RMS) energy of 16-bit PCM audio bytes."""
        if not pcm_chunk:
            return 0.0

        count = len(pcm_chunk) // 2
        if count == 0:
            return 0.0

        format_str = f"<{count}h"
        try:
            shorts = struct.unpack(format_str, pcm_chunk)
            sum_squares = sum([s * s for s in shorts])
            rms = math.sqrt(sum_squares / count)
            return rms
        except Exception:
            return 0.0

    def is_speech_frame(self, pcm_chunk: bytes) -> bool:
        """Determine if an audio chunk contains human speech."""
        rms = self.calculate_rms(pcm_chunk)

        # Update noise floor adaptively during quiet frames
        if rms < self.noise_floor * 1.5:
            self.noise_floor = 0.95 * self.noise_floor + 0.05 * rms

        threshold = max(self.noise_floor * self.sensitivity, 200.0)
        is_speech = rms > threshold

        if is_speech:
            self.speech_active = True
            self.silence_count = 0
        else:
            self.silence_count += 1
            if self.silence_count > 5:
                self.speech_active = False

        return is_speech

    def process_audio_stream(self, audio_chunks: list[bytes]) -> dict:
        """Process a stream of PCM audio chunks and segment speech boundaries."""
        speech_chunks = []
        total_rms = []

        for chunk in audio_chunks:
            rms = self.calculate_rms(chunk)
            total_rms.append(rms)
            if self.is_speech_frame(chunk):
                speech_chunks.append(chunk)

        avg_rms = sum(total_rms) / len(total_rms) if total_rms else 0.0
        has_speech = len(speech_chunks) > 0

        return {
            "has_speech": has_speech,
            "avg_rms": round(avg_rms, 2),
            "speech_chunks": speech_chunks,
            "speech_ratio": round(len(speech_chunks) / (len(audio_chunks) or 1), 2)
        }


# Global singleton instance
vad_detector = VoiceActivityDetector()


def is_user_speaking(pcm_chunk: bytes) -> bool:
    """Helper function to check if audio chunk contains speech."""
    return vad_detector.is_speech_frame(pcm_chunk)
