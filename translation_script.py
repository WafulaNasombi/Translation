
from transformers import TFMarianMTModel, MarianTokenizer
token= "<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>" # Your Hugging Face token;

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

# Example usage
kiswahili_text = "Habari za leo?"
english_translation = translate_kiswahili_to_english(kiswahili_text)
print(english_translation)

english_text = "Hello, how are you?"
kiswahili_translation = translate_english_to_kiswahili(english_text)
print(kiswahili_translation)
