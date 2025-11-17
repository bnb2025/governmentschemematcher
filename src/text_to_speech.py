"""
Text-to-Speech Module - Converts text responses to speech
"""

from typing import Optional
from google.cloud import texttospeech_v1
from config.gcp_config import gcp_config


class TextToSpeechProcessor:
    """Handles text-to-speech conversion"""
    
    def __init__(
        self,
        language_code: Optional[str] = None,
        voice_name: Optional[str] = None
    ):
        """
        Initialize Text-to-Speech Processor
        
        Args:
            language_code: Language code for TTS (default: en-US)
            voice_name: Voice name for TTS (default: en-US-Neural2-C)
        """
        self.client = texttospeech_v1.TextToSpeechClient()
        self.language_code = language_code or gcp_config.TTS_LANGUAGE_CODE
        self.voice_name = voice_name or gcp_config.TTS_VOICE_NAME
    
    def synthesize_speech(
        self,
        text: str,
        output_file: Optional[str] = None,
        speaking_rate: float = 1.0
    ) -> Optional[bytes]:
        """
        Synthesize speech from text
        
        Args:
            text: Text to convert to speech
            output_file: Optional file path to save audio
            speaking_rate: Speaking rate (0.25 to 4.0)
            
        Returns:
            Audio content as bytes
        """
        try:
            # Prepare synthesis input
            synthesis_input = texttospeech_v1.SynthesisInput(text=text)
            
            # Prepare voice selection
            voice = texttospeech_v1.VoiceSelectionParams(
                language_code=self.language_code,
                name=self.voice_name,
            )
            
            # Prepare audio configuration
            audio_config = texttospeech_v1.AudioConfig(
                audio_encoding=texttospeech_v1.AudioEncoding.MP3,
                speaking_rate=speaking_rate,
            )
            
            # Synthesize speech
            response = self.client.synthesize_speech(
                input=synthesis_input,
                voice=voice,
                audio_config=audio_config,
            )
            
            # Save to file if specified
            if output_file:
                with open(output_file, "wb") as f:
                    f.write(response.audio_content)
                print(f"✓ Audio saved to: {output_file}")
            
            return response.audio_content
            
        except Exception as e:
            print(f"❌ Error synthesizing speech: {e}")
            raise
    
    def get_available_voices(self) -> list:
        """Get list of available voices"""
        try:
            response = self.client.list_voices()
            return [
                {
                    "name": voice.name,
                    "language_codes": voice.language_codes,
                    "ssml_gender": voice.ssml_gender,
                    "natural_sample_rate_hertz": voice.natural_sample_rate_hertz,
                }
                for voice in response.voices
                if self.language_code in voice.language_codes
            ]
        except Exception as e:
            print(f"❌ Error fetching voices: {e}")
            return []
