import os
import uuid
import tempfile
import librosa
import numpy as np
import onnxruntime as ort
import soundfile as sf

SR = 16000
WINDOW_SEC = 3
N_MFCC = 40

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "audio_classifier.onnx")

# Load model once (important for Azure Functions performance)
session = ort.InferenceSession(
    MODEL_PATH,
    providers=["CPUExecutionProvider"]
)

label_map = {
    0: "speech",
    1: "ivr",
    2: "music",
    3: "ringtone",
    4: "non_speech"
}


# ---------------- FEATURE EXTRACTION ----------------

def extract_features(y):

    mfcc = librosa.feature.mfcc(
        y=y,
        sr=SR,
        n_mfcc=N_MFCC
    )

    target_len = 94

    if mfcc.shape[1] < target_len:
        mfcc = np.pad(mfcc, ((0, 0), (0, target_len - mfcc.shape[1])))
    else:
        mfcc = mfcc[:, :target_len]

    return mfcc


# ---------------- PREDICT SEGMENT ----------------

def predict_segment(y):

    mfcc = extract_features(y)

    input_data = mfcc.astype(np.float32)
    input_data = np.expand_dims(input_data, axis=(0, 1))

    outputs = session.run(None, {"input": input_data})

    logits = outputs[0]

    # Stable softmax
    exp_logits = np.exp(logits - np.max(logits))
    probs = exp_logits / np.sum(exp_logits)

    cls = np.argmax(probs)
    conf = probs[0][cls]

    label = label_map[cls]

    # Optional IVR correction
    if label == "ivr" and conf < 0.75:
        label = "speech"

    return label, float(conf)


# ---------------- PROCESS AUDIO ----------------

def process_audio(file_path):

    # Faster load
    y, sr = librosa.load(file_path, sr=None, mono=True)

    # Resample only if required
    if sr != SR:
        y = librosa.resample(y, orig_sr=sr, target_sr=SR)
        sr = SR

    win = WINDOW_SEC * sr
    audio_len = len(y)

    segments = []

    for start in range(0, audio_len, win):

        end = start + win

        if end > audio_len:
            break

        segment = y[start:end]

        # Skip very quiet segments quickly
        if np.max(np.abs(segment)) < 0.001:
            segments.append((start / sr, end / sr, "non_speech", 1.0))
            continue

        label, conf = predict_segment(segment)

        segments.append((start / sr, end / sr, label, conf))

    cleaned_audio_segments = []

    speech_duration = 0
    non_speech_duration = 0
    conf_sum = 0

    for start, end, label, conf in segments:

        conf_sum += conf

        start_i = int(start * sr)
        end_i = int(end * sr)

        if label == "speech":

            cleaned_audio_segments.append(y[start_i:end_i])
            speech_duration += end - start

        else:

            non_speech_duration += end - start

    # Prevent empty output
    if len(cleaned_audio_segments) == 0:
        cleaned_audio = np.zeros(sr)
    else:
        cleaned_audio = np.concatenate(cleaned_audio_segments)

    base = os.path.splitext(os.path.basename(file_path))[0]

    tmp_dir = tempfile.gettempdir()

    cleaned_file = os.path.join(
        tmp_dir,
        f"{base}_{uuid.uuid4().hex}_cleaned.wav"
    )

    sf.write(cleaned_file, cleaned_audio, sr)

    metadata = {
        "Recording_File_Name": os.path.basename(file_path),
        "Actual_Duration_sec": speech_duration + non_speech_duration,
        "Non_Speech_Duration_sec": non_speech_duration,
        "Cleaned_Duration_sec": speech_duration,
        "CNN_Avg_Confidence": conf_sum / max(len(segments), 1),
        "CNN_Segments": len(segments)
    }

    return cleaned_file, metadata