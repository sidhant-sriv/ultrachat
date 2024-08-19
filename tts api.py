import os

from gradio_client import Client, file
from dotenv import load_dotenv


load_dotenv()
client = Client(os.getenv("TTS_PORT"))

class TTS:
    def __init__(self, client):
        self.client = client

    def reload(self):
        client.predict(
            api_name="/reload_tts"
        )

	def update_latents(self, voice):
            result = client.predict(
                voice,  # Literal['random', 'microphone'] in 'Voice' Dropdown component
                api_name="/update_baseline_for_latents_chunks"
            )

    def rvc_config(self, voice, index, voice_pitch = 0, index_rate = 0, filer_radius = 3, resampling_sample_rate = 48000, rms_mix_rate = 0.25, protect_consonents = 0.33):
        if voice_pitch > 24: voice_pitch = 24
        if voice_pitch < -24: voice_pitch = -24

        if index_rate > 1: index_rate = 1
        if index_rate <0: index_rate = 0

        if filer_radius > 7: filer_radius = 7
        if filer_radius < 0: filer_radius = 0

        if resampling_sample_rate < 0: resampling_sample_rate = 0
        if resampling_sample_rate > 48000: resampling_sample_rate = 48000

        if rms_mix_rate < 0: rms_mix_rate = 0
        if rms_mix_rate > 1: rms_mix_rate = 1

        if protect_consonents < 0: protect_consonents = 0
        if protect_consonents > 1: protect_consonents = 1


        result = client.predict(
            voice,  # Literal[] in 'RVC Voice Model' Dropdown component
            voice_pitch,  # float (numeric value between -24 and 24)

            index,  # Literal[] in 'RVC Index File' Dropdown component
            index_rate,  # float (numeric value between 0 and 1)

            filer_radius,  # float (numeric value between 0 and 7)

            resampling_sample_rate,  # float (numeric value between 0 and 48000)

            rms_mix_rate,  # float (numeric value between 0 and 1)

            protect_consonents,  # float (numeric value between 0 and 0.5)

            api_name = "/update_rvc_settings_proxy"
            )

        def set_tts_model(self, model):
            client.predict(
                model, # Literal['auto', './models/tortoise/autoregressive.pth'] in 'Autoregressive Model' Dropdown component
                api_name="/set_autoregressive_model"
            )

        def read_generate_settings_proxy(self, ):
            print("Reading generator settings proxy not implemented...")

        def generate(self, prompt ):
            result = client.predict(
                prompt,  # str in 'Input Prompt' Textbox component
                "Hello!!",  # str in 'Line Delimiter' Textbox component
                "Happy",
                # Literal['Happy', 'Sad', 'Angry', 'Disgusted', 'Arrogant', 'Custom', 'None'] in 'Emotion' Radio component
                "Hello!!",  # str in 'Custom Emotion' Textbox component
                "random",  # Literal['random', 'microphone'] in 'Voice' Dropdown component
                file('https://github.com/gradio-app/gradio/raw/main/test/test_files/audio_sample.wav'),
                # filepath in 'Microphone Source' Audio component
                3,  # float in 'Voice Chunks' Number component
                1,  # float (numeric value between 1 and 6)

                3,  # float in 'Seed' Number component
                2,  # float (numeric value between 2 and 512)

                0,  # float (numeric value between 0 and 512)

                0,  # float (numeric value between 0 and 1)

                "P",  # Literal['P', 'DDIM'] in 'Diffusion Samplers' Radio component
                1,  # float (numeric value between 1 and 32)

                0,  # float (numeric value between 0 and 1)

                0,  # float (numeric value between 0 and 1)

                0,  # float (numeric value between 0 and 1)

                0,  # float (numeric value between 0 and 8)

                0,  # float (numeric value between 0 and 8)

                0,  # float (numeric value between 0 and 4)

                ["Half Precision"],  # List[Literal['Half Precision', 'Conditioning-Free']] in 'Experimental Flags' Checkboxgroup component
                True,  # bool in 'Use Original Latents Method (AR)' Checkbox component
                True,  # bool in 'Use Original Latents Method (Diffusion)' Checkbox component
                api_name = "/generate"
                )