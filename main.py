"""
Main application - Conversational Analytics Platform
Combines speech input, NLP processing, BigQuery queries, and speech output
"""

import os
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from src.speech_processor import SpeechProcessor
from src.text_to_speech import TextToSpeechProcessor
from src.bigquery_analytics import BigQueryAnalytics
from src.nlp_engine import NLPEngine
from config.gcp_config import gcp_config


class ConversationalAnalyticsPlatform:
    """Main conversational analytics platform"""
    
    def __init__(self):
        """Initialize the platform"""
        self.speech_processor = SpeechProcessor()
        self.tts_processor = TextToSpeechProcessor()
        self.analytics = BigQueryAnalytics()
        self.nlp_engine = NLPEngine()
        self.conversation_history = []
    
    def setup_credentials(self) -> bool:
        """Setup and verify Google Cloud credentials"""
        credentials_path = gcp_config.GCP_CREDENTIALS_PATH
        
        if not os.path.exists(credentials_path):
            print(f"⚠️  Credentials file not found at: {credentials_path}")
            print("Please set GOOGLE_APPLICATION_CREDENTIALS environment variable")
            print("or place your service account key at the above path")
            return False
        
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials_path
        print(f"✓ Credentials loaded from: {credentials_path}")
        return True
    
    def process_user_query(self, user_input: str) -> str:
        """
        Process user query and return response
        
        Args:
            user_input: User's natural language query
            
        Returns:
            Response string
        """
        print(f"\n📝 Processing query: {user_input}")
        
        # Parse the query
        parsed_query = self.nlp_engine.parse_query(user_input)
        intent = parsed_query["intent"]
        entities = parsed_query["entities"]
        
        print(f"  Intent: {intent}")
        print(f"  Entities: {entities}")
        
        # Execute appropriate action based on intent
        results = None
        
        if intent == "search_scheme":
            scheme_name = entities["scheme_names"][0] if entities["scheme_names"] else user_input
            results = self.analytics.get_scheme_info(scheme_name)
        
        elif intent == "list_schemes":
            results = self.analytics.get_scheme_info()
        
        elif intent == "statistics":
            results = self.analytics.get_scheme_statistics()
        
        elif intent == "scheme_details":
            if entities["scheme_names"]:
                results = self.analytics.get_scheme_info(entities["scheme_names"][0])
        
        # Format response
        response = self.nlp_engine.format_results(results, intent) if results else \
                   "I couldn't process your request. Please try again."
        
        # Store in conversation history
        self.conversation_history.append({
            "user": user_input,
            "response": response,
            "intent": intent
        })
        
        return response
    
    def speak_response(self, text: str, output_file: str = "response.mp3") -> None:
        """
        Convert response to speech and play
        
        Args:
            text: Text to speak
            output_file: Output audio file path
        """
        print(f"\n🔊 Converting response to speech...")
        try:
            self.tts_processor.synthesize_speech(
                text=text,
                output_file=output_file,
                speaking_rate=1.0
            )
            print(f"✓ Audio file saved: {output_file}")
            print("  You can play this file with your media player")
        except Exception as e:
            print(f"❌ Error in speech synthesis: {e}")
    
    def run_interactive_session(self) -> None:
        """Run interactive conversational session"""
        print("\n" + "=" * 60)
        print("🎯 Conversational Government Schemes Analytics Platform")
        print("=" * 60)
        print("\nWelcome! I can help you find government schemes.")
        print("You can:")
        print("  • Ask about specific schemes")
        print("  • List available schemes")
        print("  • Get statistics")
        print("  • Type 'exit' to quit\n")
        
        session_count = 0
        
        while True:
            try:
                # Get user input (text for now)
                user_input = input("You: ").strip()
                
                if not user_input:
                    continue
                
                if user_input.lower() == "exit":
                    print("\n👋 Thank you for using the Conversational Analytics Platform!")
                    break
                
                # Process query
                response = self.process_user_query(user_input)
                print(f"\nAssistant: {response}")
                
                # Ask if user wants speech output
                speak = input("\nWould you like to hear this response? (yes/no): ").strip().lower()
                if speak == "yes":
                    output_file = f"response_{session_count}.mp3"
                    self.speak_response(response, output_file)
                
                session_count += 1
                
            except KeyboardInterrupt:
                print("\n\n⊘ Session interrupted by user")
                break
            except Exception as e:
                print(f"❌ Error: {e}")
    
    def run_speech_mode(self) -> None:
        """Run fully conversational mode with speech input and output"""
        print("\n" + "=" * 60)
        print("🎙️  Speech-Based Conversational Analytics")
        print("=" * 60)
        print("Using speech input and output\n")
        
        session_count = 0
        
        while True:
            try:
                print("Listening for your query...")
                
                # Get speech input
                user_input = self.speech_processor.transcribe_streaming(timeout=30)
                
                if not user_input:
                    continue
                
                print(f"\n✓ You said: {user_input}\n")
                
                # Process query
                response = self.process_user_query(user_input)
                print(f"Assistant: {response}")
                
                # Output as speech
                output_file = f"response_{session_count}.mp3"
                self.speak_response(response, output_file)
                
                session_count += 1
                
                # Ask for next query
                continue_query = input("\nAnother query? (yes/no): ").strip().lower()
                if continue_query != "yes":
                    print("\n👋 Thank you for using the platform!")
                    break
                    
            except KeyboardInterrupt:
                print("\n\n⊘ Session interrupted")
                break
            except Exception as e:
                print(f"❌ Error: {e}")


def main():
    """Main entry point"""
    platform = ConversationalAnalyticsPlatform()
    
    # Setup credentials
    if not platform.setup_credentials():
        print("Setup incomplete. Exiting.")
        return
    
    # Test BigQuery connection
    print("\n🔗 Testing BigQuery connection...")
    if not platform.analytics.test_connection():
        print("⚠️  BigQuery connection failed. Some features may not work.")
    
    # Run interactive session
    mode = input("Select mode:\n1. Text mode (type queries)\n2. Speech mode (use microphone)\nChoice (1/2): ").strip()
    
    if mode == "2":
        platform.run_speech_mode()
    else:
        platform.run_interactive_session()


if __name__ == "__main__":
    main()
