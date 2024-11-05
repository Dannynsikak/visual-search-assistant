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

def get_image_description(image_path: str, mode: str = "summary") -> str:
    """
    Generates a description for the image based on the specified mode.

    Parameters:
        image_path (str): The path to the image file.
        mode (str): The mode for description; could be 'summary' or 'detailed'.

    Returns:
        str: The generated description.
    """
    try:
        # Load the image and preprocess it for the model
        image = Image.open(image_path)
        inputs = feature_extractor(images=image, return_tensors="pt").to(device)
        
        # Generate caption using the model
        outputs = model.generate(**inputs, max_length=50 if mode == "summary" else 100)
        
        # Decode the generated caption
        description = tokenizer.decode(outputs[0], skip_special_tokens=True)
        
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
# description = get_image_description("path/to/image.jpg", mode="detailed")
# print(description)
