# TODO: from dotenv import load_dotenv
import json
import obspython as obs
import tkinter as tk
import tkinter.scrolledtext as st
import urllib.parse
import urllib.request


# ---------------Custom Functions---------------

def call_smmry(text: str) -> str:
    # TODO: Use env file
    API_KEY = "E59E875EE2"
    API_ENDPOINT = "https://api.smmry.com"

    # Parameters that go with the URL
    params = {
        # "sm_api_input": input_text,
        "SM_API_INPUT": text,
        "SM_API_KEY": API_KEY,
        "SM_LENGTH": "3",
        "SM_KEYWORD_COUNT": "3"
        # "SM_URL"=X,
        # "SM_WITH_BREAK",
        # "SM_WITH_ENCODE",
        # "SM_IGNORE_LENGTH",
        # "SM_QUOTE_AVOID",
        # "SM_QUESTION_AVOID",
        # "SM_EXCLAMATION_AVOID"
    }
    # Join base URL and params
    params = urllib.parse.urlencode(params)
    url = API_ENDPOINT + "?" + params

    # Encode text as data to trigger POST
    data = urllib.parse.urlencode({"sm_api_input": text}).encode('ascii')

    # SMMRY API call
    with urllib.request.urlopen(url, data) as response:
        # print(response.geturl())
        # print(response.info())
        # print(response.getcode())
        response = response.read().decode("utf-8")
        response = json.loads(response)
    # print(response)
    print(response["sm_api_content"])

    return response["sm_api_content"]


def show_window(text: str):
    # Creating tkinter window
    win = tk.Tk()
    win.title("Summary")

    # Creating scrolled text area
    # widget with Read only by
    # disabling the state
    text_area = st.ScrolledText(win, width=30, height=8, font=("Arial", 15) )

    text_area.grid(column=0, pady=10, padx=10)

    # Inserting Text which is read only
    text_area.insert(tk.INSERT, text)

    # Making the text read only
    text_area.configure(state='disabled')
    win.mainloop()


def summarize_pressed(props, prop):
    """Update the Output Text"""
    show_window( call_smmry(text) )


# ---------------Script Global Functions---------------

def script_description():
    return """Summarizer powered by SMMRY"""


def script_defaults(settings):
    """Sets the default values of the Script's properties when 'Defaults' button is pressed"""
    pass

def script_update(settings):
    global text
    text = obs.obs_data_get_string(settings, "text_input")


def script_properties():
    props = obs.obs_properties_create()
    # Input Text
    obs.obs_properties_add_text(props, "text_input", "Text", obs.OBS_TEXT_MULTILINE)

    # Summarize Button
    obs.obs_properties_add_button(
        props, "button_summarize", "Summarize", summarize_pressed)

    return props
