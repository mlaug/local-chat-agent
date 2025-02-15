from flow.FlowStep import FlowStep
import soco
import os

class PlayAudioOnSonos(FlowStep):
    # Expects audio data (bytes) and returns a status message (string).
    expected_input_types = (str,)
    output_type = str

    def execute(self, input_data):
        ip = os.getenv("LOCAL_IP")
        sonos = soco.SoCo(os.getenv("SONOS_IP"))
        audio_url = f"http://{ip}/tmp/{input_data}"
        sonos.play_uri(audio_url)
        print(f"Playing {audio_url} on Sonos")
