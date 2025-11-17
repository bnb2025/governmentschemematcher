# Quick Start Guide

## Setup Instructions

### Step 1: Clone the Repository
```bash
git clone https://github.com/bnb2025/governmentschemematcher.git
cd governmentschemematcher
```

### Step 2: Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Setup Google Cloud Credentials
1. Create a service account in Google Cloud Console
2. Download the JSON key file
3. Set the environment variable:
   ```bash
   set GOOGLE_APPLICATION_CREDENTIALS=C:\path\to\your\key.json
   ```
4. Or create `.env` file:
   ```bash
   cp .env.example .env
   # Edit .env with your credentials
   ```

### Step 5: Run the Application
```bash
python main.py
```

## Features Overview

### 1. Speech-to-Text
- Real-time audio capture from microphone
- Automatic transcription using Google Cloud Speech-to-Text
- Support for multiple languages

### 2. NLP Processing
- Intent detection (search, list, statistics, etc.)
- Entity extraction (scheme names, categories)
- Query parsing and normalization

### 3. BigQuery Integration
- Query government schemes database
- Search by criteria (category, eligibility, etc.)
- Get statistics and analytics

### 4. Text-to-Speech
- Convert responses to natural-sounding speech
- Multiple voice options
- Adjustable speaking rate

## Module Structure

```
┌─────────────────────────────────────────────┐
│         main.py (Entry Point)               │
└────┬─────────────────────────────────────────┘
     │
     ├─→ SpeechProcessor (src/speech_processor.py)
     │   └─ Handles STT conversion
     │
     ├─→ NLPEngine (src/nlp_engine.py)
     │   └─ Intent & entity extraction
     │
     ├─→ BigQueryAnalytics (src/bigquery_analytics.py)
     │   └─ Database queries
     │
     └─→ TextToSpeechProcessor (src/text_to_speech.py)
         └─ Handles TTS conversion
```

## Common Use Cases

### Use Case 1: Find Education Schemes
```
User: "Find education schemes"
→ NLP extracts intent: search_scheme
→ BigQuery returns matching schemes
→ Response converted to speech
```

### Use Case 2: Get Statistics
```
User: "Show me statistics"
→ NLP extracts intent: statistics
→ BigQuery returns aggregated data
→ Response with numbers played as speech
```

### Use Case 3: Search by Category
```
User: "Agricultural schemes"
→ NLP extracts entity: category=agriculture
→ BigQuery filtered results
→ Results spoken back to user
```

## Key Configuration Files

- `config/gcp_config.py` - Google Cloud configuration
- `.env.example` - Environment variables template
- `requirements.txt` - Python dependencies

## Environment Variables

```
GCP_PROJECT_ID              - Your GCP project ID
GOOGLE_APPLICATION_CREDENTIALS - Path to service account key
BIGQUERY_DATASET            - BigQuery dataset name
BIGQUERY_TABLE              - BigQuery table name
SPEECH_LANGUAGE_CODE        - Language for STT (default: en-US)
TTS_LANGUAGE_CODE          - Language for TTS (default: en-US)
TTS_VOICE_NAME             - TTS voice (default: en-US-Neural2-C)
```

## API Documentation

### SpeechProcessor
- `transcribe_streaming()` - Real-time microphone input
- `transcribe_audio_file(file_path)` - Transcribe saved audio

### NLPEngine
- `extract_intent(text)` - Detect query intent
- `extract_entities(text)` - Extract relevant entities
- `parse_query(text)` - Full query parsing

### BigQueryAnalytics
- `get_scheme_info(scheme_name)` - Get scheme details
- `search_schemes_by_criteria(criteria)` - Filter schemes
- `get_scheme_statistics()` - Get aggregate stats

### TextToSpeechProcessor
- `synthesize_speech(text, output_file)` - Generate speech
- `get_available_voices()` - List available voices

## Troubleshooting

### Issue: "No module named 'google.cloud'"
**Solution:** Install required packages
```bash
pip install -r requirements.txt
```

### Issue: "GOOGLE_APPLICATION_CREDENTIALS not found"
**Solution:** Set the environment variable
```bash
set GOOGLE_APPLICATION_CREDENTIALS=path/to/key.json
```

### Issue: "PyAudio error"
**Solution:** Install PortAudio headers
```bash
# macOS
brew install portaudio

# Ubuntu/Debian
sudo apt-get install portaudio19-dev

# Windows (from wheels)
pip install pipwin
pipwin install pyaudio
```

## Next Steps

1. ✅ Setup Google Cloud Project
2. ✅ Install dependencies
3. ✅ Configure credentials
4. ✅ Prepare BigQuery dataset
5. ✅ Run the application
6. 📖 Read full README.md for advanced features

## Support

- 📚 See README.md for detailed documentation
- 🐛 Report issues on GitHub Issues
- 💡 Suggest features via Discussions
- 🤝 Contribute via Pull Requests

---

**Ready to start?** Run: `python main.py`
