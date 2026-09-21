"""
vision.py - Real-Time Multimodal Screen & Webcam Vision Engine for JARVIS
"""

import os
from PIL import Image, ImageGrab, ImageDraw

try:
    import cv2
    OPENCV_AVAILABLE = True
except ImportError:
    OPENCV_AVAILABLE = False


class VisionEngine:
    """Multimodal Desktop Screen & Camera Capture Engine."""

    def __init__(self, max_resolution: int = 1024):
        self.max_resolution = max_resolution

    def compress_image(self, pil_image: Image.Image) -> Image.Image:
        """Resize and convert image to RGB for optimal Gemini Vision payload transmission."""
        if not pil_image:
            return None
        
        img = pil_image.convert("RGB")
        width, height = img.size
        
        if max(width, height) > self.max_resolution:
            ratio = self.max_resolution / float(max(width, height))
            new_size = (int(width * ratio), int(height * ratio))
            img = img.resize(new_size, Image.Resampling.LANCZOS)
        
        return img

    def capture_screen(self) -> Image.Image:
        """Capture the primary display desktop screenshot."""
        try:
            screenshot = ImageGrab.grab()
            return self.compress_image(screenshot)
        except Exception as e:
            print(f"[VISION WARNING] Screen capture fallback active: {e}")
            # Generate placeholder canvas image for headless/test environments
            img = Image.new("RGB", (400, 300), color=(30, 30, 30))
            draw = ImageDraw.Draw(img)
            draw.text((20, 140), "JARVIS Screen Capture Placeholder", fill=(255, 255, 255))
            return self.compress_image(img)

    def capture_webcam(self) -> Image.Image:
        """Capture a single frame from the host webcam."""
        if not OPENCV_AVAILABLE:
            print("[VISION WARNING] OpenCV is not installed for webcam capture.")
            return None
        
        try:
            cap = cv2.VideoCapture(0)
            if not cap.isOpened():
                return None
            
            ret, frame = cap.read()
            cap.release()
            
            if ret and frame is not None:
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                pil_img = Image.fromarray(rgb_frame)
                return self.compress_image(pil_img)
            return None
        except Exception as e:
            print(f"[VISION ERROR] Webcam capture failed: {e}")
            return None


# Global singleton instance
vision_engine = VisionEngine()


def get_screen_image() -> Image.Image:
    """Helper to capture compressed desktop image."""
    return vision_engine.capture_screen()


def get_webcam_image() -> Image.Image:
    """Helper to capture compressed webcam image."""
    return vision_engine.capture_webcam()
