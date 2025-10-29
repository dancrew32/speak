import queue

import sounddevice as sd
import numpy as np
import faster_whisper

VERSION = "tiny"  # "base"
DEVICE = "cpu"
COMPUTE_TYPE = "int8"
LANGUAGE = "en"

SAMPLE_RATE = 16000
SECOND_CHUNKS = 2
BEAM_SIZE = 2
BLOCK_SIZE = int(SAMPLE_RATE * SECOND_CHUNKS)

START_MESSAGE = "Listening...\n"
END_MESSAGE = "\nStopped."

model = faster_whisper.WhisperModel(VERSION, device=DEVICE, compute_type=COMPUTE_TYPE)
audio_q = queue.Queue(maxsize=8)


def main():
    buffer = np.zeros(0, dtype=np.float32)

    while True:
        data = audio_q.get()
        buffer = np.concatenate((buffer, data[:, 0]))

        if len(buffer) <= BLOCK_SIZE:
            continue

        segment = buffer[:BLOCK_SIZE]
        buffer = buffer[BLOCK_SIZE:]

        segments, _ = model.transcribe(segment, beam_size=BEAM_SIZE, language=LANGUAGE)
        text = " ".join([s.text for s in segments]).strip()
        if text:
            print(text, flush=True)


def input_callback(indata, frames, time, status):
    audio_q.put(indata.copy())


if __name__ == "__main__":
    with sd.InputStream(samplerate=SAMPLE_RATE, channels=1, callback=input_callback):
        print(START_MESSAGE)
        try:
            main()
        except KeyboardInterrupt:
            print(END_MESSAGE)
