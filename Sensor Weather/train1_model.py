import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import tensorflow as tf
import joblib
import os

# ➤ Load the dataset from a CSV file
data = pd.read_csv("weather_data.csv")

# ➤ Select features (input variables) and target (output variable)
X = data[["humidity", "pressure", "rainfall1h", "temperature"]]  # Input features
y = data["rain"]  # Target label (rain: 0 or 1)

# ➤ Normalize the features to have zero mean and unit variance
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# ➤ Split the dataset into training (80%) and testing (20%) sets
X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y, test_size=0.2, random_state=42
)

# ➤ Define the neural network model architecture
model = tf.keras.Sequential([
    tf.keras.layers.Input(shape=(4,)),        # Input layer for 4 features
    tf.keras.layers.Dense(8, activation='relu'),  # Hidden layer with 8 neurons
    tf.keras.layers.Dense(4, activation='relu'),  # Hidden layer with 4 neurons
    tf.keras.layers.Dense(1, activation='sigmoid') # Output layer for binary classification (0 or 1)
])

# ➤ Compile the model specifying optimizer, loss function and metrics
model.compile(
    optimizer='adam',
    loss='binary_crossentropy',
    metrics=['accuracy']
)

# ➤ Train the model on the training data for 100 epochs, no verbose output
model.fit(X_train, y_train, epochs=100, verbose=0)

# ➤ Evaluate the model performance on the test set
loss, acc = model.evaluate(X_test, y_test)
print(f"Accuracy: {acc*100:.2f}%")

# ➤ Save the trained Keras model to an HDF5 file
model.save("rain_model.h5")
print("Saved Keras model as rain_model.h5")

# ➤ Load the saved model (without compiling it again)
loaded_model = tf.keras.models.load_model("rain_model.h5", compile=False)

# ➤ Convert the loaded Keras model to TensorFlow Lite format for edge deployment
converter = tf.lite.TFLiteConverter.from_keras_model(loaded_model)
tflite_model = converter.convert()

# ➤ Save the TensorFlow Lite model to disk
tflite_path = "/home/pi/rain_predict.tflite"
with open(tflite_path, "wb") as f:
    f.write(tflite_model)
print(f"Conversion complete: {tflite_path} created.")

# ➤ Save the scaler object using joblib for future data preprocessing consistency
scaler_path = "scaler.save"
joblib.dump(scaler, scaler_path)
print(f"Scaler saved as: {scaler_path}")
