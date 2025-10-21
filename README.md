# YouTube Video Summarizer

A Flask-based web application that summarizes YouTube videos by fetching the transcript and generating a concise extractive summary using TextRank algorithm.

## Features
- Paste a YouTube URL and get a quick summary
- Async form submission with helpful error messages
- TextRank-based extractive summarization using spaCy and pyTextRank
- Clean, modern web interface
- Local development focused (no deployment configuration)

## Project Structure
```
Video Summarization/
├── app.py                 # Main Flask application
├── summarizer.py          # Video summarization logic
├── requirements.txt       # Python dependencies
├── templates/
│   └── index.html        # Web interface
├── static/
│   ├── css/
│   │   └── styles.css    # Styling
│   └── js/
│       └── script.js     # Frontend JavaScript
└── README.md             # This file
```

## Setup (Local)
1. Create and activate a virtual environment
   - Windows (PowerShell):
     ```bash
     python -m venv .venv
     .venv\\Scripts\\Activate.ps1
     ```
   - macOS/Linux:
     ```bash
     python3 -m venv .venv
     source .venv/bin/activate
     ```
2. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```
3. Download spaCy model (first run only)
   ```bash
   python -m spacy download en_core_web_sm
   ```
4. Run the app
   ```bash
   python app.py
   ```
5. Open `http://127.0.0.1:5000` in your browser.

## Dependencies
- **Flask** - Web framework
- **pytube** - YouTube video ID extraction
- **youtube-transcript-api** - Transcript fetching
- **spaCy** - Natural language processing
- **pyTextRank** - TextRank summarization algorithm

## Environment Variables
- None required for basic operation

## Usage
1. Start the application: `python app.py`
2. Open `http://127.0.0.1:5000` in your browser
3. Paste a YouTube URL and click "Summarize"
4. Wait for the summary to be generated

## Notes
- Some videos may not have transcripts or have disabled transcripts; in such cases, the app returns an error
- The app uses TextRank algorithm for extractive summarization
- First run will download the spaCy English model (~50MB)
- Works with various YouTube URL formats (youtube.com, youtu.be, shorts)

## Troubleshooting
- If you get import errors, ensure all dependencies are installed: `pip install -r requirements.txt`
- If spaCy model is missing, run: `python -m spacy download en_core_web_sm`
- For transcript errors, try a different video or check if the video has captions enabled

## License
MIT
