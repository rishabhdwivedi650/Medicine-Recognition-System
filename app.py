import os

from flask import Flask, render_template, request
from google import genai
from PIL import Image

app = Flask(__name__)

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


@app.route("/", methods=["GET", "POST"])
def home():
    result = None

    if request.method == "POST":
        image_file = request.files.get("image")

        if image_file:
            image = Image.open(image_file)

            prompt = """
            Analyze this medicine-related image and provide:
            1. Visible medicine name, if readable
            2. Basic information visible or reasonably identifiable
            3. A short description

            Do not provide dosage or treatment advice.
            If the medicine cannot be identified reliably, say so clearly.
            """

            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=[prompt, image]
            )

            result = response.text

    return render_template(
        "index.html",
        result=result
    )


if __name__ == "__main__":
    app.run(debug=True)
