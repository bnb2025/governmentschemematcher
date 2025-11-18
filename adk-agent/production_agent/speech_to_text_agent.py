"""
Voice-Enabled Government Scheme Assistant
Combines real-time speech recognition with BigQuery agent for natural language queries
"""

import os
import json
import logging
import warnings
import sys
import threading
import queue
from pathlib import Path
from dotenv import load_dotenv

# Google Cloud imports
import google.auth
from google.cloud import speech_v1
from google.oauth2 import service_account
from google.adk.tools.bigquery import BigQueryToolset, BigQueryCredentialsConfig
from google.adk.agents import LlmAgent

# Audio imports
import pyaudio

# Silence warnings
warnings.filterwarnings("ignore")

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)

# Audio recording parameters
RATE = 16000
CHUNK = int(RATE / 10)
CHANNELS = 1


class VoiceAgent:
    """Voice-enabled agent that combines speech recognition with BigQuery querying."""
    
    def __init__(self, credentials_path: str):
        """
        Initialize the voice-enabled agent.
        
        Args:
            credentials_path: Path to Google Cloud credentials JSON file
        """
        self.credentials_path = credentials_path
        self.speech_client = None
        self.agent = None
        self.audio_queue = queue.Queue()
        self.is_listening = False
        
        # Initialize components
        self._setup_credentials()
        self._setup_agent()
        self._setup_speech_client()
        
    def _setup_credentials(self):
        """Set up Google Cloud credentials."""
        if not os.path.exists(self.credentials_path):
            raise FileNotFoundError(f"Credentials file not found at {self.credentials_path}")
        
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = self.credentials_path
        logger.info("Credentials configured")
    
    def _setup_agent(self):
        """Initialize the BigQuery agent."""
        try:
            creds, project = google.auth.load_credentials_from_file(
                self.credentials_path,
                scopes=["https://www.googleapis.com/auth/cloud-platform"],
            )
            logger.info(f"Loaded credentials for project: {project}")
            
            credentials_config = BigQueryCredentialsConfig(credentials=creds)
            
            bigquery_toolset = BigQueryToolset(
                credentials_config=credentials_config,
                tool_filter=[
                    "list_datasets_ids",
                    "get_dataset_info",
                    "list_table_ids",
                    "get_table_info",
                    "execute_sql",
                    "run_query",
                ],
            )
            
            self.agent = LlmAgent(
                name="voice_bigquery_agent",
                description="Voice-activated agent for government scheme queries",
                instruction=(
                    "You are a friendly government scheme assistant. "
                    "Answer user questions about government schemes using BigQuery data. "
                    "Data is in project_id=gokul-harsh-bnb2025, dataset=governmentschemes, table=schemecollection. "
                    "Provide concise, accurate, and helpful responses. "
                    "Focus on scheme benefits, eligibility criteria, and relevant details. "
                    "Keep responses conversational and easy to understand."
                ),
                tools=[bigquery_toolset],
                model="gemini-2.5-flash",
            )
            
            logger.info("Agent initialized successfully")
            
        except Exception as e:
            logger.exception("Failed to initialize agent")
            raise
    
    def _setup_speech_client(self):
        """Initialize Google Cloud Speech-to-Text client."""
        self.speech_client = speech_v1.SpeechClient()
        logger.info("Speech client initialized")
    
    def _audio_generator(self, stream):
        """Generate audio chunks from the microphone stream."""
        while self.is_listening:
            try:
                chunk = stream.read(CHUNK, exception_on_overflow=False)
                yield speech_v1.StreamingRecognizeRequest(audio_content=chunk)
            except Exception as e:
                logger.error(f"Error reading audio: {e}")
                break
    
    def process_query(self, query: str):
        """
        Process a text query through the agent.
        
        Args:
            query: The user's question in natural language
            
        Returns:
            The agent's response
        """
        try:
            logger.info(f"Processing query: {query}")
            
            # Use run_live method which is available in LlmAgent
            result = self.agent.run_live(query)
            
            # The result is typically an iterator/generator of responses
            # Collect all responses
            responses = []
            for response in result:
                if hasattr(response, 'text'):
                    responses.append(response.text)
                elif hasattr(response, 'content'):
                    responses.append(response.content)
                elif isinstance(response, str):
                    responses.append(response)
                else:
                    responses.append(str(response))
            
            # Join all responses
            final_response = '\n'.join(responses) if responses else "No response generated."
            return final_response
                
        except Exception as e:
            logger.exception("Error processing query")
            return f"Sorry, I encountered an error: {str(e)}"
    
    def start_listening(self, language_code: str = "en-US"):
        """
        Start listening for voice input and process queries in real-time.
        
        Args:
            language_code: Language code for transcription (default: English US)
        """
        # Audio configuration
        config = speech_v1.RecognitionConfig(
            encoding=speech_v1.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=RATE,
            language_code=language_code,
            enable_automatic_punctuation=True,
        )
        
        streaming_config = speech_v1.StreamingRecognitionConfig(
            config=config,
            interim_results=True,
        )
        
        print("\n" + "=" * 60)
        print("🎤 Voice-Enabled Government Scheme Assistant")
        print("=" * 60)
        print("\nListening for your questions...")
        print("Examples:")
        print("  - 'What schemes are available for farmers?'")
        print("  - 'Tell me about education schemes'")
        print("  - 'What are the eligibility criteria for housing schemes?'")
        print("\nPress Ctrl+C to stop.\n")
        
        try:
            self.is_listening = True
            
            # Initialize PyAudio
            audio = pyaudio.PyAudio()
            stream = audio.open(
                format=pyaudio.paInt16,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK,
            )
            
            # Start streaming recognition
            requests = self._audio_generator(stream)
            responses = self.speech_client.streaming_recognize(streaming_config, requests)
            
            # Process responses
            current_transcript = ""
            for response in responses:
                if not response.results:
                    continue
                
                result = response.results[0]
                
                if result.alternatives:
                    transcript = result.alternatives[0].transcript
                    
                    if result.is_final:
                        print(f"\n📝 You said: {transcript}")
                        print("🤔 Processing...\n")
                        
                        # Process the query through the agent
                        agent_response = self.process_query(transcript)
                        
                        print("🤖 Assistant:")
                        print("-" * 60)
                        print(agent_response)
                        print("-" * 60)
                        print("\n🎤 Listening for next question...\n")
                        
                        current_transcript = ""
                    else:
                        # Show interim results
                        if transcript != current_transcript:
                            print(f"💬 {transcript}", end="\r")
                            current_transcript = transcript
            
            # Cleanup
            stream.stop_stream()
            stream.close()
            audio.terminate()
            
        except KeyboardInterrupt:
            print("\n\n👋 Voice assistant stopped. Goodbye!")
            self.is_listening = False
        except Exception as e:
            logger.exception("Error in voice listening")
            print(f"\n❌ Error: {e}")
            self.is_listening = False
    
    def query_text(self, query: str):
        """
        Process a text query (for testing without voice).
        
        Args:
            query: The user's question
        """
        print(f"\n📝 Query: {query}")
        response = self.process_query(query)
        print(f"\n🤖 Response:\n{response}\n")


def main():
    """Main function to run the voice-enabled agent."""
    
    # Load environment variables
    dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
    load_dotenv(dotenv_path=dotenv_path)
    
    # Credentials path
    credentials_path = r"C:\workspace\GovernmentSchemeMatcher\gokul-harsh-bnb2025-4b6b290f0621.json"
    
    try:
        # Initialize voice agent
        voice_agent = VoiceAgent(credentials_path)
        
        # Check if user wants text mode or voice mode
        if len(sys.argv) > 1 and sys.argv[1] == "--text":
            # Text mode for testing
            print("Running in text mode. Enter your queries:")
            while True:
                query = input("\nYour question (or 'quit' to exit): ")
                if query.lower() in ['quit', 'exit', 'q']:
                    break
                voice_agent.query_text(query)
        else:
            # Voice mode (default)
            voice_agent.start_listening()
            
    except Exception as e:
        logger.exception("Failed to start voice agent")
        print(f"\n❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()