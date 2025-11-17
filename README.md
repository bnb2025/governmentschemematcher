# Conversational Government Schemes Analytics Platform

A comprehensive Python application that combines Google Cloud services (Speech-to-Text, Text-to-Speech, and BigQuery) to provide a conversational interface for government scheme analytics.

## Features

- 🎤 **Real-time Speech Recognition** - Convert spoken queries to text using Google Cloud Speech-to-Text
- 🔊 **Text-to-Speech Output** - Receive responses as natural-sounding speech
- 💾 **BigQuery Integration** - Query government schemes database
- 🧠 **NLP Engine** - Intent detection and entity extraction
- 💬 **Conversational Interface** - Interactive text or speech-based sessions
- 📊 **Analytics Capabilities** - Search, filter, and analyze schemes

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│        User Input (Speech or Text)                      │
└────────────────┬────────────────────────────────────────┘
                 │
        ┌────────▼──────────┐
        │ Speech Processor  │
        │ (STT)             │
        └────────┬──────────┘
                 │
        ┌────────▼──────────┐
        │   NLP Engine      │
        │ (Intent & Entity) │
        └────────┬──────────┘
                 │
        ┌────────▼──────────┐
        │ BigQuery          │
        │ Analytics         │
        └────────┬──────────┘
                 │
        ┌────────▼──────────┐
        │ Text-to-Speech    │
        │ (TTS)             │
        └────────┬──────────┘
                 │
        ┌────────▼──────────┐
        │  User Output      │
        │  (Speech or Text) │
        └────────────────────┘
```

## Prerequisites

- Python 3.8+
- Google Cloud Project with:
  - Speech-to-Text API enabled
  - Text-to-Speech API enabled
  - BigQuery API enabled
- Service Account credentials (JSON key file)
- PyAudio (requires PortAudio development headers)

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/bnb2025/governmentschemematcher.git
cd governmentschemematcher
```

### 2. Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Setup Google Cloud Credentials

```bash
# Set environment variable
export GOOGLE_APPLICATION_CREDENTIALS="path/to/your/service-account-key.json"

# Or create .env file
echo "GOOGLE_APPLICATION_CREDENTIALS=path/to/your/key.json" > .env
echo "GCP_PROJECT_ID=your-project-id" >> .env
echo "BIGQUERY_DATASET=government_schemes" >> .env
```

## Configuration

Edit `config/gcp_config.py` or create a `.env` file:

```env
GCP_PROJECT_ID=your-gcp-project-id
GOOGLE_APPLICATION_CREDENTIALS=/path/to/service-account-key.json
BIGQUERY_DATASET=government_schemes
BIGQUERY_TABLE=scheme_data
SPEECH_LANGUAGE_CODE=en-US
TTS_LANGUAGE_CODE=en-US
TTS_VOICE_NAME=en-US-Neural2-C
```

## Usage

### Interactive Text Mode

```bash
python main.py
# Select option 1 for text mode
# Type your queries or 'exit' to quit
```

### Speech Mode (with Microphone)

```bash
python main.py
# Select option 2 for speech mode
# Speak your queries
```

### Example Queries

- "Find education schemes"
- "Show me all available schemes"
- "Tell me about agricultural schemes"
- "What are the eligibility criteria?"
- "List employment schemes"

### Programmatic Usage

```python
from main import ConversationalAnalyticsPlatform

# Initialize platform
platform = ConversationalAnalyticsPlatform()
platform.setup_credentials()

# Process a query
response = platform.process_user_query("Find education schemes")
print(response)

# Convert to speech
platform.speak_response(response, "output.mp3")
```

## Module Details

### `src/speech_processor.py`
Handles audio input and speech-to-text conversion using Google Cloud Speech-to-Text API.

**Key Methods:**
- `transcribe_streaming()` - Real-time transcription from microphone
- `transcribe_audio_file()` - Transcribe existing audio file

### `src/text_to_speech.py`
Converts text responses to natural-sounding speech using Google Cloud Text-to-Speech API.

**Key Methods:**
- `synthesize_speech()` - Convert text to speech
- `get_available_voices()` - List available voices

### `src/bigquery_analytics.py`
Queries government schemes data from BigQuery.

**Key Methods:**
- `execute_query()` - Run custom SQL queries
- `get_scheme_info()` - Retrieve scheme information
- `search_schemes_by_criteria()` - Filter schemes
- `get_scheme_statistics()` - Get aggregated statistics

### `src/nlp_engine.py`
Processes natural language queries and formats responses.

**Key Methods:**
- `extract_intent()` - Determine query intent
- `extract_entities()` - Extract relevant entities
- `parse_query()` - Parse complete query structure
- `format_results()` - Format results into natural language

## Testing

```bash
python -m pytest tests/ -v

# Or run specific tests
python -m unittest tests.test_analytics
```

## BigQuery Dataset Setup

Create a BigQuery table for government schemes:

```sql
CREATE TABLE `project.government_schemes.scheme_data` (
  scheme_id STRING,
  scheme_name STRING,
  description STRING,
  category STRING,
  eligibility STRING,
  benefits STRING,
  application_url STRING
);
```

## Troubleshooting

### 1. Audio/Microphone Issues
```bash
# Install PortAudio (macOS)
brew install portaudio

# Install PortAudio (Ubuntu/Debian)
sudo apt-get install portaudio19-dev
```

### 2. Google Cloud Credentials Error
- Verify service account key file exists
- Check GOOGLE_APPLICATION_CREDENTIALS environment variable
- Ensure APIs are enabled in GCP console

### 3. BigQuery Connection Issues
- Verify project ID is correct
- Ensure BigQuery API is enabled
- Check dataset and table names in config

## Project Structure

```
governmentschemematcher/
├── src/
│   ├── __init__.py
│   ├── speech_processor.py      # Speech-to-Text
│   ├── text_to_speech.py        # Text-to-Speech
│   ├── bigquery_analytics.py    # BigQuery queries
│   └── nlp_engine.py            # NLP processing
├── config/
│   ├── __init__.py
│   └── gcp_config.py            # GCP configuration
├── tests/
│   ├── __init__.py
│   └── test_analytics.py        # Unit tests
├── main.py                      # Main application
├── requirements.txt             # Python dependencies
├── .gitignore
└── README.md
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

MIT License - see LICENSE file for details

## Acknowledgments

- Google Cloud Platform documentation
- Government of India Digital Services
- Open source community

## Contact & Support

For issues, questions, or suggestions:
- GitHub Issues: [Create an issue](https://github.com/bnb2025/governmentschemematcher/issues)
- Email: support@governmentschemematcher.com

---

**Last Updated:** November 17, 2025
