import sys
import queue

import sounddevice as sd
import numpy as np
import faster_whisper

VERSION = "base" # "tiny"
DEVICE = "cpu"
model = faster_whisper.WhisperModel(VERSION, device=DEVICE)

SAMPLE_RATE = 16000
SECOND_CHUNKS = 2
BEAM_SIZE = 3
BLOCK_SIZE = int(SAMPLE_RATE * SECOND_CHUNKS)

START_MESSAGE = "Listening...\n"
END_MESSAGE = "\nStopped."

audio_q = queue.Queue()


def callback(indata, frames, time, status):
    # if status:
        # print(status)
    audio_q.put(indata.copy())


def main():
        buffer = np.zeros(0, dtype=np.float32)

        while True:
            data = audio_q.get()
            buffer = np.concatenate((buffer, data[:, 0]))
            
            if len(buffer) > BLOCK_SIZE:
                segment = buffer[:BLOCK_SIZE]
                buffer = buffer[BLOCK_SIZE:]
                
                segments, _ = model.transcribe(segment, beam_size=BEAM_SIZE)
                text = " ".join([s.text for s in segments]).strip()
                if text:
                    #sys.stdout.write(text)
                    print(text, flush=True)


if __name__ == "__main__":
    with sd.InputStream(samplerate=SAMPLE_RATE, channels=1, callback=callback):
        print(START_MESSAGE)
        try:
            main()
        except KeyboardInterrupt:
            print(END_MESSAGE)

