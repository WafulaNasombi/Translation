import tensorflow as tf
from tensorflow.keras.layers import Embedding, GRU, Dense, Input
from tensorflow.keras.losses import SparseCategoricalCrossentropy
from tensorflow.keras.optimizers import Adam
from sklearn.model_selection import train_test_split
import numpy as np
import re

# Data Preprocessing
def preprocess_sentence(sentence):
    # Lowercase the sentence
    sentence = sentence.lower().strip()
    # Remove punctuation
    sentence = re.sub(r"[^\w\s]", "", sentence)
    return sentence

def load_dataset(kikuyu_path, english_path):
    # Load kikuyu and english sentences
    with open(kikuyu_path, encoding='utf-8') as f:
        kikuyu_lines = f.read().splitlines()
    with open(english_path, encoding='utf-8') as f:
        english_lines = f.read().splitlines()
    return kikuyu_lines, english_lines

def tokenize_data(kikuyu_lines, english_lines):
    # Tokenize kikuyu sentences
    tokenizer_kikuyu = tf.keras.preprocessing.text.Tokenizer(filters='')
    tokenizer_kikuyu.fit_on_texts(kikuyu_lines)
    # Tokenize english sentences
    tokenizer_english = tf.keras.preprocessing.text.Tokenizer(filters='')
    tokenizer_english.fit_on_texts(english_lines)
    return tokenizer_kikuyu, tokenizer_english

def create_dataset(kikuyu_lines, english_lines, tokenizer_kikuyu, tokenizer_english):
    # Convert sentences to sequences of integers
    input_sequences_kikuyu = tokenizer_kikuyu.texts_to_sequences(kikuyu_lines)
    output_sequences_english = tokenizer_english.texts_to_sequences(english_lines)
    # Pad sequences to same length
    input_sequences_kikuyu = tf.keras.preprocessing.sequence.pad_sequences(input_sequences_kikuyu, padding='post')
    output_sequences_english = tf.keras.preprocessing.sequence.pad_sequences(output_sequences_english, padding='post')
    return input_sequences_kikuyu, output_sequences_english

# Build Model
def build_model(input_vocab_size, output_vocab_size, embedding_dim, units):
    # Encoder
    encoder_input = Input(shape=(None,))
    encoder_embedding = Embedding(input_vocab_size, embedding_dim)(encoder_input)
    encoder_output, encoder_state = GRU(units, return_state=True)(encoder_embedding)
    # Decoder
    decoder_input = Input(shape=(None,))
    decoder_embedding = Embedding(output_vocab_size, embedding_dim)(decoder_input)
    decoder_output = GRU(units, return_sequences=True)(decoder_embedding, initial_state=encoder_state)
    decoder_output = Dense(output_vocab_size, activation='softmax')(decoder_output)
    # Model
    model = tf.keras.models.Model([encoder_input, decoder_input], decoder_output)
    return model

# Train Model
def train_model(model, X_train, y_train, X_valid, y_valid, batch_size, epochs):
    model.compile(optimizer=Adam(), loss=SparseCategoricalCrossentropy(), metrics=['accuracy'])
    model.fit([X_train[:, :-1], X_train[:, 1:]], y_train, validation_data=([X_valid[:, :-1], X_valid[:, 1:]], y_valid), batch_size=batch_size, epochs=epochs)

# Translation
def translate(sentence, tokenizer_kikuyu, tokenizer_english, model, from_lang, to_lang):
    # Tokenize input sentence
    sentence = preprocess_sentence(sentence)
    if from_lang == 'kikuyu':
        sequence = tokenizer_kikuyu.texts_to_sequences([sentence])
        sequence = tf.keras.preprocessing.sequence.pad_sequences(sequence, maxlen=25, padding='post')
        tokenizer = tokenizer_english
    elif from_lang == 'english':
        sequence = tokenizer_english.texts_to_sequences([sentence])
        sequence = tf.keras.preprocessing.sequence.pad_sequences(sequence, maxlen=25, padding='post')
        tokenizer = tokenizer_kikuyu
    else:
        raise ValueError("Unsupported from_lang, choose either 'kikuyu' or 'english'")

    # Translate using the model
    decoded_sentence = ''
    encoder_output, encoder_state = model.layers[0](sequence)
    decoder_state = encoder_state
    decoder_input = np.zeros((1, 1))
    decoder_input[0, 0] = tokenizer.word_index['<sos>']
    for i in range(25):
        decoder_output, decoder_state = model.layers[1](decoder_input, initial_state=decoder_state)
        decoder_input = np.argmax(decoder_output, axis=-1)
        if decoder_input[0, 0] == tokenizer.word_index['<eos>']:
            break
        decoded_sentence += tokenizer.index_word[decoder_input[0, 0]] + ' '
    return decoded_sentence.strip()

# Main
def main():
    # Load and preprocess dataset
    kikuyu_path = r'C:\Users\ADMIN\Downloads\en-ki.txt\NLLB.en-ki.ki'
    english_path = r'C:\Users\ADMIN\Downloads\en-ki.txt\NLLB.en-ki.en'
    kikuyu_lines, english_lines = load_dataset(kikuyu_path, english_path)
    
    # Tokenize data
    tokenizer_kikuyu = tf.keras.preprocessing.text.Tokenizer(filters='')
    tokenizer_english = tf.keras.preprocessing.text.Tokenizer(filters='')

    # Check vocabulary size
    vocab_size_kikuyu = len(tokenizer_kikuyu.word_index)
    vocab_size_english = len(tokenizer_english.word_index)
    
    # Print vocabulary size for inspection
    print("Vocabulary size (Kikuyu):", vocab_size_kikuyu)
    print("Vocabulary size (English):", vocab_size_english)


    print("Wĩmenyerere ndũkahĩtũkwo rũciũ rũkĩte:", kikuyu_lines[2200619])
    print("You'll read their texts over and over again:", english_lines[2200618])


    
    
    # Ensure tokenizers have the same vocabulary size
    if vocab_size_kikuyu != vocab_size_english:
        raise ValueError("Vocabulary sizes are different for Kikuyu and English")
    
    
   # Create and Split datasets
    X_kikuyu, y_english = create_dataset(kikuyu_lines, english_lines, tokenizer_kikuyu, tokenizer_english)
    X_train_kikuyu, X_valid_kikuyu, y_train_english, y_valid_english = train_test_split(X_kikuyu, y_english, test_size=0.2, random_state=42)

    X_english, y_kikuyu = create_dataset(english_lines, kikuyu_lines, tokenizer_english, tokenizer_kikuyu)
    X_train_english, X_valid_english, y_train_kikuyu, y_valid_kikuyu = train_test_split(X_english, y_kikuyu, test_size=0.2, random_state=42)
    
    # Build models
    model_kikuyu_to_english = build_model(len(tokenizer_kikuyu.word_index)+1, len(tokenizer_english.word_index)+1, embedding_dim=256, units=1024)
    model_english_to_kikuyu = build_model(len(tokenizer_english.word_index)+1, len(tokenizer_kikuyu.word_index)+1, embedding_dim=256, units=1024)
    
    # Train models
    train_model(model_kikuyu_to_english, X_train_kikuyu, y_train_english, X_valid_kikuyu, y_valid_english, batch_size=64, epochs=10)
    train_model(model_english_to_kikuyu, X_train_english, y_train_kikuyu, X_valid_english, y_valid_kikuyu, batch_size=64, epochs=10)
    # Translation
    sentence_kikuyu = "Ndi mwega."
    translation_english = translate(sentence_kikuyu, tokenizer_kikuyu, tokenizer_english, model_kikuyu_to_english, 'kikuyu', 'english')
    print("Kikuyu Input sentence:", sentence_kikuyu)
    print("English Translated sentence:", translation_english)

    sentence_english = "I am fine."
    translation_kikuyu = translate(sentence_english, tokenizer_kikuyu, tokenizer_english, model_english_to_kikuyu, 'english', 'kikuyu')
    print("English Input sentence:", sentence_english)
    print("Kikuyu Translated sentence:", translation_kikuyu)

if __name__ == '__main__':
    main()