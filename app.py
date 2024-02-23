from flask import (
    Flask,
    Response,
    request,
    render_template,
    session,
    redirect,
    url_for,
)
from dotenv import load_dotenv
import os
from openai import OpenAI
import requests

load_dotenv()
elevenlabs_api_key = os.getenv("ELEVENLABS_API_KEY")

client = OpenAI()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

system_message = {
    "role": "system",
    "content": "You are my William Crompton, my father. I am your son, Teed. Please provide short, concise answers.",
}


@app.route("/", methods=("GET", "POST"))
def prompt():
    if "conversation" not in session:
        session["conversation"] = []

    if request.method == "POST":
        if request.form.get("action") == "Reset Conversation":
            session.pop("conversation", None)  # Clear the conversation
            return redirect(url_for("prompt"))  # Redirect to clear POST data

        user_prompt = request.form["prompt"]
        session["conversation"].append({"role": "user", "content": user_prompt})

        prompt = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[system_message] + session["conversation"],
            max_tokens=50,
        )

        assistant_response = prompt.choices[0].message.content
        session["conversation"].append(
            {"role": "assistant", "content": assistant_response}
        )

        session.modified = True

    # Pass the entire conversation to the template as 'conversation'
    conversation = session["conversation"]

    # For debugging
    print("Conversation:", conversation, end='\n')
    # Pass only the assistant's most recent message to the template as 'result'
    result = session["conversation"][-1]["content"] if session["conversation"] else None

    return render_template("prompt.html", result=result, conversation=conversation)


@app.route("/stream_audio/<text>")
def stream_audio(text):
    headers = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": elevenlabs_api_key,
    }

    data = {
        "text": text,
        "model_id": "eleven_monolingual_v1",
        "voice_settings": {"stability": 0.5, "similarity_boost": 0.5},
    }

    response = requests.post(
        "https://api.elevenlabs.io/v1/text-to-speech/NsManPzvLKKRvmmOUBOo/stream",
        json=data,
        headers=headers,
        stream=True,
    )

    def generate():
        for chunk in response.iter_content(chunk_size=1024):
            yield chunk

    return Response(generate(), mimetype="audio/mpeg")

# Run locally on any port above 1024
# if __name__ == "__main__":
#     app.run(debug=True, host='0.0.0.0', port=5000)


# Run on port 80 for production
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
