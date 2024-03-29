from flask import Flask, request, jsonify
import torch
from torch import nn
from torchvision import transforms
import requests
from transformers import AutoModelForImageClassification
from PIL import Image
import csv
import io
app = Flask(__name__)
classes=[]
animes={}
file = open("classes.csv", "r")
reader = csv.reader(file)
for row in reader:
    #print(row)
    classes.append(row[1])
file.close()
file = open("output.csv", "r")
reader = csv.reader(file)
for row in reader:
    animes[row[0]] = row[1]
file.close()
model = AutoModelForImageClassification.from_pretrained(
    "microsoft/beit-base-patch16-224-pt22k-ft22k",
    image_size=224,
    num_labels=3357,
    ignore_mismatched_sizes=True,
)
weights = torch.load("weights.ckpt", map_location=torch.device("cpu"))["state_dict"]
pp = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.5, 0.5, 0.5], std=[0.5, 0.5, 0.5]),
])
w = {}
for k, v in weights.items():
    #print(k)
    if k.startswith("net"):
        k = k.replace("net"+".", "")
        w[k] = v
    '''
    if "relative_position_bias_table" in k:
        k = k.replace("bias_table", "index")
        w[k] = v
    '''
model.load_state_dict(w, strict=True)

@app.route('/predict', methods=['POST'])
def predict():
    file = request.data
    if file:
        im_data = io.BytesIO(file)
        image = pp(Image.open(im_data).convert("RGB")).unsqueeze(0)
        outputs = model(pixel_values=image)
        logits = outputs.logits
        probs = torch.nn.functional.softmax(logits, dim=-1)
        top5_probs, top5_classes = torch.topk(probs, 5)
        top5_classes=top5_classes[0].tolist()
        #print(top5_classes)
        #print(animes['bocchi_hitori'])
        top5_classes = [classes[idx] for idx in top5_classes]
        top5_animes = [animes[chara] for chara in top5_classes]
        return jsonify({
            'top5_probs': top5_probs[0].tolist(),
            'top5_classes': top5_classes,
            'top5_animes': top5_animes
        })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)