import os
import torch
import torchaudio
from speechbrain.inference.TTS import Tacotron2
from speechbrain.inference.vocoders import HIFIGAN

class PodcastGenerator:
    def __init__(self):
        self.tacotron2 = Tacotron2.from_hparams(
            source="speechbrain/tts-tacotron2-ljspeech",
            savedir="tmp_tts",
            run_opts={"device": "cpu"}  # Use "cuda" if available
        )
        self.hifi_gan = HIFIGAN.from_hparams(
            source="speechbrain/tts-hifigan-ljspeech",
            savedir="tmp_vocoder",
            run_opts={"device": "cpu"}  # Use "cuda" if available
        )
    
    def text_to_podcast(self, text: str, style: str = "neutral") -> str:
        # Adjust prosody based on style
        if style == "academic":
            text = "Using an academic tone: " + text
        
        # Generate mel spectrogram
        mel_output, mel_length, _ = self.tacotron2.encode_text(text)
        
        # Synthesize waveform
        waveforms = self.hifi_gan.decode_batch(mel_output)
        
        # Save output
        os.makedirs("outputs/podcasts", exist_ok=True)
        output_path = f"outputs/podcasts/podcast_{hash(text)}.wav"
        torchaudio.save(output_path, waveforms.squeeze(1), 22050)
        
        return output_path