from transformers import VisionEncoderDecoderModel, AutoTokenizer, ViTFeatureExtractor
import torch
from PIL import Image, UnidentifiedImageError

# Load the model, feature extractor, and tokenizer
model = VisionEncoderDecoderModel.from_pretrained("nlpconnect/vit-gpt2-image-captioning")
feature_extractor = ViTFeatureExtractor.from_pretrained("nlpconnect/vit-gpt2-image-captioning")
tokenizer = AutoTokenizer.from_pretrained("nlpconnect/vit-gpt2-image-captioning")

# Check if GPU is available
device = "cuda" if torch.cuda.is_available() else "cpu"
model.to(device)

def get_image_description(image_path):
    """
    Processes an image to generate a descriptive caption.
    """
    try:
        # Load and preprocess the image
        image = Image.open(image_path).convert("RGB")
        
        # Extract pixel values (feature_extractor includes resizing and normalization)
        pixel_values = feature_extractor(images=image, return_tensors="pt").pixel_values.to(device)
        
        # Generate a caption for the image
        generated_ids = model.generate(
            pixel_values, 
            max_length=40, 
            num_beams=5, 
            no_repeat_ngram_size=2, 
            early_stopping=True
        )
        
        # Decode the caption
        description = tokenizer.decode(generated_ids[0], skip_special_tokens=True)
        
        # Return the text description
        return description

    except UnidentifiedImageError:
        error_message = "Invalid image format. Please provide a valid image file."
        print(error_message)
        return error_message
    except Exception as e:
        error_message = "An error occurred during image processing."
        print(f"{error_message}: {e}")
        return error_message

# Example usage
# description = get_image_description("path/to/image.jpg")
# print(description)
