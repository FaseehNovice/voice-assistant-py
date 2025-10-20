import os
from dotenv import load_dotenv

from types import SimpleNamespace # helps create simple objects with dynamic attributes

load_dotenv()

AGENT_ID = os.getenv("AGENT_ID")
API_KEY = os.getenv("API_KEY")

# the main client to interact with ElevenLabs services.
from elevenlabs.client import ElevenLabs

# handles a live AI conversation session.
from elevenlabs.conversational_ai.conversation import Conversation

# enables microphone and speaker usage for real-time talking/listening.
from elevenlabs.conversational_ai.default_audio_interface import DefaultAudioInterface

# holds configuration data for the AI conversation (like prompts, variables, etc.).
from elevenlabs.types import ConversationConfig

user_name = "Shabana G"
agent_name = "Momo"
agent_gender = "female"
schedule = "Parlor Bhi jana hai 9 bajay ; Meetup with Rukhsana"
prompt = f"You are {agent_name} who is my assistant. Your Gender is {agent_gender}.Your interlocutor has the following schedule: {schedule}."
first_message = f"Hello {user_name}, Kidhar Hain aap?"

conversation_override = {
    "agent": {
        "__name__":agent_name,
        "prompt": {
            "prompt": prompt,
        },
        "first_message": first_message,
    },
}

config = ConversationConfig(
    conversation_config_override=conversation_override,
    extra_body={},
    dynamic_variables={},
    id=None,
)


# converts the configuration object into a dictionary.
# converts that dictionary into an object with attributes
# (so you can access values like config.prompt instead of config['prompt']).
config = SimpleNamespace(**config.model_dump())
config.user_id = None

client = ElevenLabs(api_key=API_KEY)

def print_agent_response(response):
    print(f"Agent: {response}")


def print_interrupted_response(original, corrected):
    print(f"Agent interrupted, truncated response: {corrected}")


def print_user_transcript(transcript):
    print(f"User: {transcript}")


conversation = Conversation(
    client,
    AGENT_ID,
    config=config,
    requires_auth=True,
    audio_interface=DefaultAudioInterface(),
    callback_agent_response=print_agent_response,
    callback_agent_response_correction=print_interrupted_response,
    callback_user_transcript=print_user_transcript,
)

conversation.start_session()