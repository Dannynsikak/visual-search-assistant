from transformers import VisionEncoderDecoderModel, AutoTokenizer, ViTFeatureExtractor
import torch
from PIL import Image

# Load components separately
model = VisionEncoderDecoderModel.from_pretrained("nlpconnect/vit-gpt2-image-captioning")
feature_extractor = ViTFeatureExtractor.from_pretrained("nlpconnect/vit-gpt2-image-captioning")
tokenizer = AutoTokenizer.from_pretrained("nlpconnect/vit-gpt2-image-captioning")

def get_image_description(image_path):
    image = Image.open(image_path).convert("RGB")
    pixel_values = feature_extractor(images=image, return_tensors="pt").pixel_values

    # Generate description with attention mask
    generated_ids = model.generate(pixel_values, attention_mask=torch.ones(pixel_values.shape[:2]), max_new_tokens=20)
    description = tokenizer.decode(generated_ids[0], skip_special_tokens=True)
    return description
