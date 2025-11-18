"""
Real-time Speech to Text using Google Cloud Speech-to-Text API
This script captures audio from your microphone and transcribes it in real-time.
"""

import os
import json
from google.cloud import speech_v1
from google.oauth2.service_account import Credentials
import pyaudio
import sys

# Audio recording parameters
RATE = 16000  # Sampling rate
CHUNK = int(RATE / 10)  # 100ms chunks
CHANNELS = 1  # Mono audio


def transcribe_streaming(callback=None, language_code: str = "en-US"):
    """
    Transcribes speech from the microphone stream in real-time.
    
    Args:
        language_code: Language code for transcription (default: English US)
    """
    
    # Initialize the Speech-to-Text client
    # Credentials resolution: prefer `GOOGLE_APPLICATION_CREDENTIALS`, otherwise fall back to a repo-local key.
    credentials_env = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
    if credentials_env and os.path.exists(credentials_env):
        client = speech_v1.SpeechClient()
    else:
        fallback = os.path.join(os.path.dirname(__file__), "gokul-harsh-bnb2025-4b6b290f0621.json")
        if os.path.exists(fallback):
            os.environ.setdefault("GOOGLE_APPLICATION_CREDENTIALS", fallback)
            client = speech_v1.SpeechClient()
        else:
            # Let the client try application default credentials; if none available, an error will be raised
            client = speech_v1.SpeechClient()
    
    # Audio configuration
    config = speech_v1.RecognitionConfig(
        encoding=speech_v1.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=RATE,
        language_code=language_code,
        enable_automatic_punctuation=True,
    )
    
    # Streaming configuration
    streaming_config = speech_v1.StreamingRecognitionConfig(
        config=config,
        interim_results=True,  # Show intermediate results
    )
    
    print("Starting real-time speech recognition...")
    print("Speak 'Hello World' or whatever you want to say.")
    print("Press Ctrl+C to stop.\n")
    
    try:
        # Initialize PyAudio
        audio = pyaudio.PyAudio()
        stream = audio.open(
            format=pyaudio.paInt16,
            channels=CHANNELS,
            rate=RATE,
            input=True,
            frames_per_buffer=CHUNK,
        )
        
        # Generator to yield audio chunks
        def audio_generator():
            while True:
                try:
                    chunk = stream.read(CHUNK, exception_on_overflow=False)
                except Exception:
                    # on overflow or audio error, continue and try again
                    continue
                if not chunk:
                    break
                yield speech_v1.StreamingRecognizeRequest(audio_content=chunk)
        
        # Call the streaming recognize API
        requests = audio_generator()
        responses = client.streaming_recognize(streaming_config, requests)
        
        # Process responses
        for response in responses:
            if not response.results:
                continue

            result = response.results[0]

            if result.alternatives:
                transcript = result.alternatives[0].transcript

                if result.is_final:
                    print(f"\nFinal: {transcript}")
                    # Call the callback (if provided) with the final transcript
                    try:
                        if callback:
                            callback(transcript)
                    except Exception as cb_err:
                        print(f"Callback error: {cb_err}")
                else:
                    print(f"Interim: {transcript}", end="\r")
        
        stream.stop_stream()
        stream.close()
        audio.terminate()
        
    except KeyboardInterrupt:
        print("\n\nTranscription stopped by user.")
    except Exception as e:
        print(f"\nError occurred: {e}")
        raise


def main():
    """Main function to run the speech-to-text demo."""
    
    # Prefer existing environment credentials; fall back to a repo-local key if present.
    credentials_env = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
    if credentials_env and os.path.exists(credentials_env):
        print(f"Using credentials from environment: {credentials_env}")
    else:
        fallback = os.path.join(os.path.dirname(__file__), "gokul-harsh-bnb2025-4b6b290f0621.json")
        if os.path.exists(fallback):
            os.environ.setdefault("GOOGLE_APPLICATION_CREDENTIALS", fallback)
            print(f"Using fallback credentials: {fallback}")
        else:
            print("No credentials found in environment or fallback path. The client may fail to initialize.")

    print("=" * 50)
    print("Google Cloud Speech-to-Text Real-time Demo")
    print("=" * 50)
    print()

    # Run the transcription; you can pass a callback to handle final transcripts.
    transcribe_streaming()


if __name__ == "__main__":
    main()
