import pyaudio
import wave

def play_sound(path: str):
    CHUNK = 1024

    wf = wave.open(path, 'rb')

    p = pyaudio.PyAudio()

    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)

    data = wf.readframes(CHUNK)

    while data != b'':
        stream.write(data)
        data = wf.readframes(CHUNK)

    stream.stop_stream()
    stream.close()

    p.terminate()

def authorization_sound():
    play_sound('./utils/authorization_sound.wav')

def deny_dues_not_paid_sound():
    play_sound('./utils/deny_dues_not_paid.wav')

def deny_overlap_student_sound():
    play_sound('./utils/deny_overlap_student.wav')

def deny_unknown_student_sound():
    play_sound('./utils/deny_unknown_student.wav')