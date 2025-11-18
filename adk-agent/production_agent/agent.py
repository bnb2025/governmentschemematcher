import json
import os
import logging
import warnings
from dotenv import load_dotenv
from pathlib import Path
import google.auth
from google.cloud import secretmanager
from google.oauth2 import service_account
from google.adk.tools import google_search
from google.adk.tools.bigquery import BigQueryToolset, BigQueryCredentialsConfig
from google.adk.agents import Agent, LlmAgent,SequentialAgent



# Silence specific ADK experimental warnings
warnings.filterwarnings("ignore")

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)

# Load environment variables from the .env file located next to this script.
# Using an explicit path avoids issues when the process is started from a different CWD.
dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
# Load environment variables
root_dir = Path(__file__).parent.parent
#gcloud secrets list --project=gokul-harsh-bnb2025dotenv_path = root_dir / ".env"
loaded = load_dotenv(dotenv_path=dotenv_path)

if loaded:
    logger.info("Loaded environment variables from %s", dotenv_path)
else:
    logger.warning(".env not found at %s; environment variables may be missing or empty", dotenv_path)

# Configure Google Cloud
try:
    _, project_id = google.auth.default()
    os.environ.setdefault("GOOGLE_CLOUD_PROJECT", project_id)
except Exception:
    pass

            #try:
            # Create the Secret Manager client.
            #client = secretmanager.SecretManagerServiceClient()

            # Access the secret version.
            #response = client.access_secret_version(request={"name": secret_version_name})

            # Extract the payload as a string.
            #payload = response.payload.data.decode("UTF-8")
            
            # The payload is the service account JSON key.
            # We can load the credentials directly from the string.
            #payload=os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
            # ---------- Credentials ----------
credentials_path = r"C:\workspace\google_flash_agent\adk-agent\production_agent\gokul-harsh-bnb2025-4b6b290f0621.json"
try:
    creds, project = google.auth.load_credentials_from_file(
        credentials_path,
        scopes=["https://www.googleapis.com/auth/cloud-platform"],
    )
    logger.info("Loaded credentials for project: %s", project)
except Exception as e:
    logger.exception("Failed to load credentials from Secret Manager.")
    raise

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

bq_agent = LlmAgent(
            name="bigquery_agent",
            description="An agent that can interact with BigQuery to fetch and analyze data related to government schemes.",
            instruction=(
                "You are a data science agent with access to several BigQuery tools. "
                "Make use of those tools to answer the user's questions. Reply in a concise manner. "
                "Data is in project_id=gokul-harsh-bnb2025, dataset=governmentschemes, table=schemecollection."
                "A production-ready conversational assistant powered by CPU-accelerated GEMINI FLASH 2.5 LITE."
                "a friendly, knowledgeable, and enthusiastic government scheme guide.Your main goal is to make"  
                "conversation engaging accurate and to the point for every government scheme for guests by answering their questions based on their eligiblity criterion."

            "You can provide general information and benefits and eligibility criterion, such as:"
            "- The schemes offered and stored in database and how to apply for them."
            "- Typical benefits and eligibility criteria."
            "- Conservation status and unique characteristics."

            "IMPORTANT: You do NOT have access to any tools. This means you cannot look up real-time, specific information about THIS SCHEME. You cannot provide:"
            "- YOU CAN NOT RETRAIN USING USERS DATA OR STORE BUT YOU CAN ASK."
            "- HALLUCINATE SHOULD NOT OCCUR."
            "Keep your tone cheerful, engaging, and welcoming for visitors of all ages."
            ),
            tools=[bigquery_toolset],
            model="gemini-2.5-flash",
        )
logger.info("Agent initialized: %s", bq_agent.name)

root_agent = bq_agent
        