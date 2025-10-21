# YouTube Summarizer

A Flask-based web application that summarizes YouTube videos by fetching the transcript and generating a concise extractive summary.

## Features
- Paste a YouTube URL and get a quick summary
- Async form submission with helpful error messages
- Simple frequency-based summarization (no external ML services required)
- Production-ready structure with logging and Procfile

## Project Structure
```
youtube-summarizer/
├── app.py
├── summarizer.py
├── templates/
│   └── index.html
├── static/
│   ├── css/
│   │   └── styles.css
│   └── js/
│       └── script.js
├── requirements.txt
├── Procfile
├── .gitignore
└── README.md
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

## Environment Variables
- None required for basic operation. Add any tokens/config your custom summarizer may need via a `.env` and load them in `app.py` as needed.

## Deployment (Heroku)
1. Ensure you have a Heroku app created and the CLI installed.
2. Set Python buildpack automatically by having `requirements.txt`.
3. Push to Heroku:
   ```bash
   git add .
   git commit -m "Deploy YouTube summarizer"
   heroku create
   git push heroku main
   ```
4. (Optional) Pre-download spaCy model during build via release phase or run:
   ```bash
   heroku run python -m spacy download en_core_web_sm
   ```

## Notes
- Some videos may not have transcripts or have disabled transcripts; in such cases, the app returns an error.
- `pytube` is used to robustly parse video IDs from various URL formats.

## License
MIT

