from flask import Flask, render_template, request, jsonify
from transformers import TFMarianMTModel, MarianTokenizer

app = Flask(__name__)

token = "<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>"  # Your Hugging Face token;

def translate_kiswahili_to_english(text):
    model_name = "Helsinki-NLP/opus-mt-swc-en"
    tokenizer = MarianTokenizer.from_pretrained(model_name, revision="main", use_auth_token=token)
    model = TFMarianMTModel.from_pretrained(model_name, revision="main", use_auth_token=token)

    inputs = tokenizer.encode(text, return_tensors="tf")
    outputs = model.generate(inputs, max_length=128, num_beams=4, early_stopping=True)
    translated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)

    return translated_text

def translate_english_to_kiswahili(text):
    model_name = "Helsinki-NLP/opus-mt-en-sw"
    tokenizer = MarianTokenizer.from_pretrained(model_name, revision="main", use_auth_token=token)
    model = TFMarianMTModel.from_pretrained(model_name, revision="main", use_auth_token=token)

    inputs = tokenizer.encode(text, return_tensors="tf")
    outputs = model.generate(inputs, max_length=128, num_beams=4, early_stopping=True)
    translated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)

    return translated_text

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/translate", methods=["POST"])
def translate():
    data = request.get_json()
    text = data.get("text")
    direction = data.get("direction")

    if direction == "kiswahili":
        translated_text = translate_english_to_kiswahili(text)
    elif direction == "english":
        translated_text = translate_kiswahili_to_english(text)
    else:
        return jsonify({"error": "Unsupported translation direction"})

    return jsonify({"translation": translated_text})

if __name__ == "__main__":
    app.run(debug=True)
