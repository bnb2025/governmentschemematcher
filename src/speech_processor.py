"""
Speech Processing Module - Handles real-time speech-to-text conversion
"""

import os
from typing import Optional, Generator
import pyaudio
from google.cloud import speech_v1
from config.gcp_config import gcp_config


class SpeechProcessor:
    """Handles audio input and speech-to-text conversion"""
    
    def __init__(self, language_code: Optional[str] = None):
        """
        Initialize the Speech Processor
        
        Args:
            language_code: Language code for speech recognition (default: en-US)
        """
        self.client = speech_v1.SpeechClient()
        self.language_code = language_code or gcp_config.SPEECH_LANGUAGE_CODE
        self.rate = gcp_config.SAMPLE_RATE_HERTZ
        self.chunk = gcp_config.AUDIO_CHUNK_SIZE
        
    def _create_config(self) -> speech_v1.RecognitionConfig:
        """Create speech recognition configuration"""
        return speech_v1.RecognitionConfig(
            encoding=speech_v1.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=self.rate,
            language_code=self.language_code,
            enable_automatic_punctuation=True,
        )
    
    def _audio_generator(self, stream) -> Generator:
        """Generator that yields audio chunks"""
        while True:
            try:
                chunk = stream.read(self.chunk, exception_on_overflow=False)
                if not chunk:
                    break
                yield speech_v1.StreamingRecognizeRequest(audio_content=chunk)
            except Exception as e:
                print(f"Error reading audio chunk: {e}")
                break
    
    def transcribe_streaming(self, timeout: Optional[float] = None) -> Optional[str]:
        """
        Transcribe audio from microphone stream in real-time
        
        Args:
            timeout: Timeout for transcription in seconds
            
        Returns:
            Transcribed text from the audio
        """
        try:
            config = self._create_config()
            streaming_config = speech_v1.StreamingRecognitionConfig(
                config=config,
                interim_results=True,
            )
            
            # Initialize PyAudio
            audio = pyaudio.PyAudio()
            stream = audio.open(
                format=pyaudio.paInt16,
                channels=1,
                rate=self.rate,
                input=True,
                frames_per_buffer=self.chunk,
            )
            
            print("🎤 Listening... (press Ctrl+C to stop)")
            
            requests = self._audio_generator(stream)
            responses = self.client.streaming_recognize(
                streaming_config, 
                requests,
                timeout=timeout
            )
            
            final_transcript = ""
            for response in responses:
                if not response.results:
                    continue
                
                result = response.results[0]
                if result.alternatives:
                    transcript = result.alternatives[0].transcript
                    
                    if result.is_final:
                        final_transcript = transcript
                        print(f"\n✓ Final: {transcript}")
                    else:
                        print(f"→ Interim: {transcript}", end="\r")
            
            stream.stop_stream()
            stream.close()
            audio.terminate()
            
            return final_transcript
            
        except KeyboardInterrupt:
            print("\n⊘ Transcription stopped by user.")
            return None
        except Exception as e:
            print(f"❌ Error in transcription: {e}")
            raise
    
    def transcribe_audio_file(self, file_path: str) -> Optional[str]:
        """
        Transcribe audio from a file
        
        Args:
            file_path: Path to the audio file
            
        Returns:
            Transcribed text
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Audio file not found: {file_path}")
        
        try:
            with open(file_path, "rb") as audio_file:
                content = audio_file.read()
            
            config = self._create_config()
            audio = speech_v1.RecognitionAudio(content=content)
            
            response = self.client.recognize(config=config, audio=audio)
            
            if response.results:
                return response.results[0].alternatives[0].transcript
            return None
            
        except Exception as e:
            print(f"❌ Error transcribing file: {e}")
            raise
