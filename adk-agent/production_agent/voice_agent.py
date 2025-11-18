import time
import traceback

# Import the transcribe function from the production speech file
from adk_agent.production_agent.speech_to_text import transcribe_streaming

# Import the root agent defined in `agent.py`
try:
    from agent import root_agent
except Exception:
    root_agent = None


def send_to_agent(prompt: str):
    """Send the prompt to the configured agent and return/print the response.

    This tries a few common method names so it works with different agent APIs.
    """
    if root_agent is None:
        print("No `root_agent` available from `agent.py`. Please import or initialize your agent first.")
        return

    try:
        # Common method names used by agent wrappers
        for method in ("run", "respond", "execute", "call", "invoke", "__call__"):
            if hasattr(root_agent, method):
                fn = getattr(root_agent, method)
                if callable(fn):
                    response = fn(prompt)
                    print("Agent response:\n", response)
                    return response

        # If the agent object itself is callable
        if callable(root_agent):
            response = root_agent(prompt)
            print("Agent response:\n", response)
            return response

        print("root_agent does not expose a runnable API. Inspect `agent.py` to find the correct call.")
    except Exception:
        print("Error sending prompt to agent:")
        traceback.print_exc()


def main():
    print("Starting voice -> agent bridge. Speak to send prompts to the agent.")

    def on_final(transcript: str):
        print(f"\n[Voice] Final transcript received: {transcript}")
        send_to_agent(transcript)

    # Start the real-time transcription; final transcripts will be forwarded to the agent
    try:
        transcribe_streaming(callback=on_final)
    except KeyboardInterrupt:
        print("Stopped by user.")


if __name__ == "__main__":
    main()
