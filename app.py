from flask import render_template, Flask, request, jsonify

import tensorflow as tf

from PIL import Image
import io
from io import BytesIO
import base64
import numpy as np

app = Flask(__name__)

split_to = 256
y_t = 0
x_t = 0

model = None

def load_model():
    global model
    model = tf.keras.models.load_model('my_saved_model/model_onehot_10')

color_dict = {0: (0, 0, 0),
              1: (0, 125, 0),
              2: (150, 80, 0),
              3: (255, 255, 0),
              4: (100, 100, 100),
              5: (0, 255, 0),
              6: (0, 0, 150),
              7: (150, 150, 255),
              8: (255, 255, 255)}

def join_image(batch, x_t, y_t):
  y_list = []

  for i in range(0, x_t):
    current_batch = np.concatenate([batch[(i * y_t) + j] for j in range(0, y_t)], axis=0)

    y_list.append(current_batch)
  
  final_image = np.concatenate([y_list[j] for j in range(0, x_t)], axis=1)

  return final_image

def onehot_to_rgb(onehot, color_dict):
    single_layer = np.argmax(onehot, axis=-1)
    output = np.zeros(onehot.shape[:2] + (3,))

    for k in color_dict.keys():
        output[single_layer==k] = color_dict[k]
        
    return np.uint8(output)

def join_onehot_image(batch, color_dict, x_t, y_t):
  y_list = []

  for i in range(0, x_t):
    current_batch = np.concatenate([onehot_to_rgb(batch[(i * y_t) + j], color_dict) for j in range(0, y_t)], axis=0)

    y_list.append(current_batch)
  
  final_image = np.concatenate([y_list[j] for j in range(0, x_t)], axis=1)

  return final_image

def get_batch(image):
    global y_t
    y_t = int(image.shape[0] / split_to)
    global x_t
    x_t = int(image.shape[1] / split_to)

    # Split batch
    test_batch = []

    for i_x in range(0, x_t):
        x = split_to * i_x
        x2 = split_to * (i_x + 1)

        for i_y in range(0, y_t):
            y = split_to * i_y
            y2 = split_to * (i_y + 1)

            test_batch.append(image[y:y2, x:x2])
    
    test_batch = np.array(test_batch)
    return test_batch

def load_request_batch(image):
    image = Image.open(BytesIO(image))

    if image.mode != "RGB":
        image = image.convert("RGB")

    image = tf.keras.preprocessing.image.img_to_array(image, dtype="uint8")

    batch = get_batch(image)
    print(batch.shape)

    return batch

def predict_batch(batch):
    results = model.predict(batch, verbose=0)
    final_image = join_onehot_image(results, color_dict, x_t, y_t)

    print(final_image.shape)
    return final_image

@app.route('/')
def index():
    return render_template('index.html')

@app.route("/predict", methods=["POST"])
def predict():
    image = request.files["image"].read()
    batch = load_request_batch(image)
    final_image = predict_batch(batch)

    print("Prediction Done")

    img = Image.fromarray(final_image)
    img.convert("RGB")
    rawBytes = io.BytesIO()
    img.save(rawBytes, "JPEG")
    rawBytes.seek(0)
    img_base64 = base64.b64encode(rawBytes.read())

    return jsonify({'final_image': str(img_base64)})
    
if __name__ == "__main__":
    load_model()
    app.run(debug = False, threaded = False)

if __name__ == "app":
    load_model()