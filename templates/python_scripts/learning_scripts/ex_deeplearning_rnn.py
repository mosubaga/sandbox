import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import numpy as np
import matplotlib.pyplot as plt
import string
import re
from collections import Counter

# Set random seed for reproducibility
tf.random.set_seed(42)
np.random.seed(42)

print("TensorFlow version:", tf.__version__)
print("GPU Available:", tf.config.list_physical_devices('GPU'))
print()

# =====================================================================
# PART 1: TEXT GENERATION WITH RNN
# =====================================================================

print("=" * 60)
print("PART 1: TEXT GENERATION WITH RNN")
print("=" * 60)

# Sample text data for character-level text generation
sample_text = """
The quick brown fox jumps over the lazy dog. This is a sample text for training our RNN model.
Machine learning is fascinating and can be used to solve many problems. Deep learning networks
like RNNs are particularly good at sequence modeling tasks. They can learn patterns in sequential
data and generate new sequences based on what they have learned. Text generation is one of the
most interesting applications of RNNs. We can train them on any text corpus and they will learn
to generate similar text. The possibilities are endless when it comes to creative applications
of artificial intelligence and machine learning.
"""

# Preprocess the text
def preprocess_text(text):
    # Convert to lowercase and remove extra whitespace
    text = re.sub(r'\s+', ' ', text.lower().strip())
    return text

processed_text = preprocess_text(sample_text)
print(f"Text length: {len(processed_text)} characters")

# Create character mappings
chars = sorted(list(set(processed_text)))
char_to_idx = {char: idx for idx, char in enumerate(chars)}
idx_to_char = {idx: char for idx, char in enumerate(chars)}
vocab_size = len(chars)

print(f"Vocabulary size: {vocab_size}")
print(f"Characters: {chars}")
print()

# Create training sequences
def create_sequences(text, seq_length):
    sequences = []
    targets = []
    
    for i in range(len(text) - seq_length):
        seq = text[i:i + seq_length]
        target = text[i + seq_length]
        sequences.append([char_to_idx[char] for char in seq])
        targets.append(char_to_idx[target])
    
    return np.array(sequences), np.array(targets)

seq_length = 40
X_text, y_text = create_sequences(processed_text, seq_length)
print(f"Training sequences shape: {X_text.shape}")
print(f"Training targets shape: {y_text.shape}")

# Build text generation RNN model
def create_text_generation_model(vocab_size, seq_length, embedding_dim=50, rnn_units=128):
    model = keras.Sequential([
        layers.Embedding(vocab_size, embedding_dim, input_length=seq_length),
        layers.LSTM(rnn_units, return_sequences=True, dropout=0.2, recurrent_dropout=0.2),
        layers.LSTM(rnn_units, dropout=0.2, recurrent_dropout=0.2),
        layers.Dense(vocab_size, activation='softmax')
    ])
    return model

text_model = create_text_generation_model(vocab_size, seq_length)
text_model.compile(
    optimizer='adam',
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)

print("Text Generation Model Architecture:")
text_model.summary()

# Train the text generation model
print("\nTraining text generation model...")
text_history = text_model.fit(
    X_text, y_text,
    batch_size=32,
    epochs=50,
    validation_split=0.2,
    verbose=1
)

# Text generation function
def generate_text(model, seed_text, num_chars=200, temperature=1.0):
    generated = seed_text
    
    for _ in range(num_chars):
        # Prepare input sequence
        input_seq = [char_to_idx.get(char, 0) for char in generated[-seq_length:]]
        input_seq = np.array(input_seq).reshape(1, -1)
        
        # Predict next character
        predictions = model.predict(input_seq, verbose=0)[0]
        
        # Apply temperature for diversity
        predictions = np.asarray(predictions).astype('float64')
        predictions = np.log(predictions + 1e-8) / temperature
        exp_preds = np.exp(predictions)
        predictions = exp_preds / np.sum(exp_preds)
        
        # Sample next character
        next_idx = np.random.choice(len(predictions), p=predictions)
        next_char = idx_to_char[next_idx]
        generated += next_char
    
    return generated

# Generate sample text
print("\nGenerating text with different temperatures:")
seed = "the quick brown"
for temp in [0.5, 1.0, 1.5]:
    generated = generate_text(text_model, seed, num_chars=150, temperature=temp)
    print(f"\nTemperature {temp}:")
    print(generated)

# =====================================================================
# PART 2: SENTIMENT ANALYSIS WITH RNN
# =====================================================================

print("\n" + "=" * 60)
print("PART 2: SENTIMENT ANALYSIS WITH RNN")
print("=" * 60)

# Load IMDB movie reviews dataset
print("Loading IMDB dataset...")
(x_train_imdb, y_train_imdb), (x_test_imdb, y_test_imdb) = keras.datasets.imdb.load_data(num_words=10000)

print(f"Training samples: {len(x_train_imdb)}")
print(f"Test samples: {len(x_test_imdb)}")

# Get word index for IMDB dataset
word_index = keras.datasets.imdb.get_word_index()
reverse_word_index = {value: key for key, value in word_index.items()}

def decode_review(encoded_review):
    return ' '.join([reverse_word_index.get(i - 3, '?') for i in encoded_review])

# Show sample reviews
print("\nSample reviews:")
for i in range(2):
    print(f"\nReview {i+1} (Label: {'Positive' if y_train_imdb[i] else 'Negative'}):")
    print(decode_review(x_train_imdb[i])[:200] + "...")

# Pad sequences to same length
max_length = 500
x_train_padded = keras.preprocessing.sequence.pad_sequences(x_train_imdb, maxlen=max_length)
x_test_padded = keras.preprocessing.sequence.pad_sequences(x_test_imdb, maxlen=max_length)

print(f"\nPadded training data shape: {x_train_padded.shape}")
print(f"Padded test data shape: {x_test_padded.shape}")

# Build sentiment analysis RNN model
def create_sentiment_model(vocab_size=10000, max_length=500, embedding_dim=100):
    model = keras.Sequential([
        layers.Embedding(vocab_size, embedding_dim, input_length=max_length),
        layers.Bidirectional(layers.LSTM(64, dropout=0.3, recurrent_dropout=0.3)),
        layers.Dense(32, activation='relu'),
        layers.Dropout(0.5),
        layers.Dense(1, activation='sigmoid')
    ])
    return model

sentiment_model = create_sentiment_model()
sentiment_model.compile(
    optimizer='adam',
    loss='binary_crossentropy',
    metrics=['accuracy']
)

print("Sentiment Analysis Model Architecture:")
sentiment_model.summary()

# Train sentiment analysis model
print("\nTraining sentiment analysis model...")
sentiment_history = sentiment_model.fit(
    x_train_padded, y_train_imdb,
    batch_size=32,
    epochs=5,  # Reduced for demonstration
    validation_data=(x_test_padded, y_test_imdb),
    verbose=1
)

# Evaluate sentiment model
test_loss, test_accuracy = sentiment_model.evaluate(x_test_padded, y_test_imdb, verbose=0)
print(f"\nSentiment Analysis Test Accuracy: {test_accuracy:.4f}")

# Make predictions on sample reviews
sample_indices = [0, 100, 200, 300, 400]
sample_predictions = sentiment_model.predict(x_test_padded[sample_indices])

print("\nSample Predictions:")
for i, idx in enumerate(sample_indices):
    prediction = sample_predictions[i][0]
    actual = y_test_imdb[idx]
    sentiment = "Positive" if prediction > 0.5 else "Negative"
    confidence = prediction if prediction > 0.5 else 1 - prediction
    
    print(f"\nReview {idx}:")
    print(f"Actual: {'Positive' if actual else 'Negative'}")
    print(f"Predicted: {sentiment} (Confidence: {confidence:.3f})")
    print(f"Review text: {decode_review(x_test_imdb[idx])[:100]}...")

# =====================================================================
# PART 3: VISUALIZATION AND ANALYSIS
# =====================================================================

print("\n" + "=" * 60)
print("PART 3: VISUALIZATION AND ANALYSIS")
print("=" * 60)

# Plot training histories
plt.figure(figsize=(15, 10))

# Text generation model
plt.subplot(2, 3, 1)
plt.plot(text_history.history['loss'], label='Training Loss')
plt.plot(text_history.history['val_loss'], label='Validation Loss')
plt.title('Text Generation - Loss')
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.legend()
plt.grid(True, alpha=0.3)

plt.subplot(2, 3, 2)
plt.plot(text_history.history['accuracy'], label='Training Accuracy')
plt.plot(text_history.history['val_accuracy'], label='Validation Accuracy')
plt.title('Text Generation - Accuracy')
plt.xlabel('Epoch')
plt.ylabel('Accuracy')
plt.legend()
plt.grid(True, alpha=0.3)

# Sentiment analysis model
plt.subplot(2, 3, 4)
plt.plot(sentiment_history.history['loss'], label='Training Loss')
plt.plot(sentiment_history.history['val_loss'], label='Validation Loss')
plt.title('Sentiment Analysis - Loss')
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.legend()
plt.grid(True, alpha=0.3)

plt.subplot(2, 3, 5)
plt.plot(sentiment_history.history['accuracy'], label='Training Accuracy')
plt.plot(sentiment_history.history['val_accuracy'], label='Validation Accuracy')
plt.title('Sentiment Analysis - Accuracy')
plt.xlabel('Epoch')
plt.ylabel('Accuracy')
plt.legend()
plt.grid(True, alpha=0.3)

# Prediction confidence distribution
plt.subplot(2, 3, 3)
all_predictions = sentiment_model.predict(x_test_padded[:1000])
plt.hist(all_predictions, bins=50, alpha=0.7, edgecolor='black')
plt.title('Prediction Confidence Distribution')
plt.xlabel('Prediction Score')
plt.ylabel('Frequency')
plt.grid(True, alpha=0.3)

# Model complexity comparison
plt.subplot(2, 3, 6)
models = ['Text Gen\n(LSTM)', 'Sentiment\n(Bi-LSTM)']
params = [text_model.count_params(), sentiment_model.count_params()]
colors = ['skyblue', 'lightcoral']
plt.bar(models, params, color=colors, edgecolor='black', alpha=0.7)
plt.title('Model Complexity (Parameters)')
plt.ylabel('Number of Parameters')
for i, v in enumerate(params):
    plt.text(i, v + max(params)*0.01, f'{v:,}', ha='center', va='bottom')
plt.grid(True, alpha=0.3, axis='y')

plt.tight_layout()
plt.show()

# =====================================================================
# PART 4: CUSTOM TEXT SENTIMENT ANALYSIS
# =====================================================================

print("\n" + "=" * 60)
print("PART 4: CUSTOM TEXT SENTIMENT ANALYSIS")
print("=" * 60)

def analyze_custom_text(text, model, word_index, max_length=500):
    # Preprocess the text
    words = text.lower().split()
    sequence = [word_index.get(word, 0) for word in words]  # 0 for unknown words
    
    # Pad the sequence
    padded_sequence = keras.preprocessing.sequence.pad_sequences([sequence], maxlen=max_length)
    
    # Make prediction
    prediction = model.predict(padded_sequence)[0][0]
    sentiment = "Positive" if prediction > 0.5 else "Negative"
    confidence = prediction if prediction > 0.5 else 1 - prediction
    
    return sentiment, confidence, prediction

# Test custom texts
custom_texts = [
    "This movie was absolutely fantastic! I loved every minute of it.",
    "The plot was confusing and the acting was terrible. Complete waste of time.",
    "It was an okay movie, nothing special but not bad either.",
    "Amazing cinematography and outstanding performances by all actors!",
    "I fell asleep halfway through. Very boring and predictable."
]

print("Analyzing custom texts:")
for i, text in enumerate(custom_texts):
    sentiment, confidence, score = analyze_custom_text(text, sentiment_model, word_index)
    print(f"\nText {i+1}: \"{text}\"")
    print(f"Sentiment: {sentiment} (Confidence: {confidence:.3f}, Score: {score:.3f})")

print("\n" + "=" * 60)
print("RNN DEMONSTRATION COMPLETED!")
print("=" * 60)
print("\nSummary:")
print("1. Text Generation RNN: Learned to generate text character by character")
print("2. Sentiment Analysis RNN: Classified movie reviews as positive/negative")
print("3. Used different RNN architectures: LSTM and Bidirectional LSTM")
print("4. Demonstrated various RNN applications and techniques")