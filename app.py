import logging
from flask import Flask, render_template, request, jsonify
from summarizer import summarize_youtube_video


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s - %(message)s",
)
logger = logging.getLogger(__name__)


app = Flask(__name__)


@app.route("/")
def home():
    """Render the main page"""
    return render_template("index.html")


@app.route("/summarize", methods=["POST"])
def summarize():
    """Handle YouTube URL submission and return summary"""
    try:
        data = request.get_json(silent=True) or {}
        youtube_url = data.get("url", "").strip()

        logger.info("Summarize request received: %s", youtube_url)

        if not youtube_url:
            logger.warning("No URL provided in request body")
            return jsonify({"error": "No URL provided", "status": 400}), 400

        summary = summarize_youtube_video(youtube_url)

        if not summary:
            logger.warning("Empty summary returned for URL: %s", youtube_url)
            return jsonify({"error": "Could not generate summary", "status": 404}), 404

        logger.info("Summary generated successfully (%d chars)", len(summary))
        return jsonify({"summary": summary, "status": 200})

    except Exception as exc:  # pylint: disable=broad-except
        logger.exception("Unhandled error while summarizing video")
        return jsonify({"error": str(exc), "status": 500}), 500


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)


