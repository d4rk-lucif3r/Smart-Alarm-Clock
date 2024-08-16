"""
This module is responsible for playing text to speech messages.
"""

import requests

def tts(text: str) -> None:
    """
    This function takes in a message and plays it using a text-to-speech service.
    It requires a parameter string which is to be played when 
    function is called.
    """
    # Advanced TTS engine integration example with an external TTS service
    response = requests.post(
        'https://api.external-tts-service.com/v1/synthesize',
        json={'text': text, 'voice': 'en-US-Wavenet-D'},
        headers={'Authorization': 'Bearer YOUR_API_KEY'}
    )
    if response.status_code == 200:
        with open("/tmp/tts_output.mp3", "wb") as out_f:
            out_f.write(response.content)
        # Code to play the mp3 file can be inserted here, for example using `playsound` module
        # from playsound import playsound
        # playsound("/tmp/tts_output.mp3")
    else:
        print("Error in TTS synthesis: ", response.status_code, response.text)