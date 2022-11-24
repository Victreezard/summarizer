from dotenv import load_dotenv
from os import getenv
from os.path import abspath, dirname, join
from time import perf_counter
import json
import obspython as obs
import urllib.parse
import urllib.request


current_dir = abspath(dirname(__file__))
load_dotenv(join(current_dir, ".env"))

# ---------------Custom Functions---------------

def call_smmry(text: str) -> str:
    API_KEY = getenv("API_KEY")
    API_ENDPOINT = "https://api.smmry.com"

    # Parameters that go with the URL
    params = {
        "SM_API_INPUT": text,
        "SM_API_KEY": API_KEY,
        "SM_LENGTH": "3",
        "SM_KEYWORD_COUNT": "3",
        # "SM_URL"=X,
        # "SM_WITH_BREAK",
        # "SM_WITH_ENCODE",
        # "SM_IGNORE_LENGTH",
        "SM_QUOTE_AVOID": "",
        "SM_QUESTION_AVOID": "",
        "SM_EXCLAMATION_AVOID": ""
    }
    # Join base URL and params
    params = urllib.parse.urlencode(params)
    url = API_ENDPOINT + "?" + params
    # print(f"{url=}")

    # Encode text as data to trigger POST
    data = urllib.parse.urlencode({"sm_api_input": text}).encode('ascii')

    # SMMRY API call
    with urllib.request.urlopen(url, data) as response:
        # print(f"{response.geturl()=}")
        # print(f"{response.info()=}")
        # print(f"{response.getcode()=}")
        response = response.read().decode("utf-8")
        response = json.loads(response)

    # print(f"{response=}")
    return response["sm_api_content"]


def summarize_pressed(props, prop):
    """Update the Output Text"""
    time_start = perf_counter()

    summary = call_smmry(text)

    time_stop = perf_counter()
    time_elapsed = str(time_stop-time_start)
    obs.obs_data_set_string(settings_copy, "info_text",
                            formatted_time := f"{time_elapsed=!s}")
    obs.obs_data_set_string(settings_copy, "result_text", summary)
    print(formatted_time)

    return True

# ---------------Script Global Functions---------------

def script_description():
    return """Summarizer powered by SMMRY"""


def script_defaults(settings):
    """Sets the default values of the Script's properties when 'Defaults' button is pressed"""
    pass

def script_update(settings):
    global text
    text = obs.obs_data_get_string(settings, "text_input")
    global settings_copy
    settings_copy = settings


def script_properties():
    props = obs.obs_properties_create()
    # Input Text
    obs.obs_properties_add_text(props, "text_input", "Text", obs.OBS_TEXT_MULTILINE)

    # Summarize Button
    obs.obs_properties_add_button(
        props, "button_summarize", "Summarize", summarize_pressed)

    obs.obs_properties_add_text(props, "info_text", "", obs.OBS_TEXT_INFO)
    obs.obs_properties_add_text(props, "result_text", "Result", obs.OBS_TEXT_MULTILINE)

    return props
