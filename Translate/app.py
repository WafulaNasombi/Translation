import os
from flask import Flask, request, jsonify
import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

app = Flask(__name__)

# Load the saved model and tokenizer
current_directory = os.getcwd()
save_path = os.path.join(current_directory, "LuoTOEng-model")
model = AutoModelForSeq2SeqLM.from_pretrained(save_path)
tokenizer = AutoTokenizer.from_pretrained(save_path)

# Define a route for translation
@app.route('/translate', methods=['POST'])
def translate_sentence():
    # Get the input sentence from the request
    input_sentence = request.json['input_sentence']
    
    # Tokenize the input sentence
    tokenized_input = tokenizer(input_sentence, return_tensors="pt")
    
    # Generate the translated sentence
    with torch.no_grad():
        model.eval()
        output = model.generate(**tokenized_input, max_length=50)
    
    # Decode the output and remove special tokens
    translated_sentence = tokenizer.decode(output[0], skip_special_tokens=True)
    
    # Return the translated sentence in JSON format
    return jsonify({'translated_sentence': translated_sentence})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
