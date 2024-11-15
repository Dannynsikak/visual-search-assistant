<<<<<<< HEAD
from transformers import VisionEncoderDecoderModel, AutoTokenizer, ViTImageProcessor
=======
from transformers import VisionEncoderDecoderModel, AutoTokenizer, ViTFeatureExtractor
>>>>>>> 221de2e8fc6779426901f2f3eb86618b73e0c2c2
import torch
from PIL import Image, UnidentifiedImageError

# Load the model, feature extractor, and tokenizer
model = VisionEncoderDecoderModel.from_pretrained("nlpconnect/vit-gpt2-image-captioning")
<<<<<<< HEAD
feature_extractor = ViTImageProcessor.from_pretrained("nlpconnect/vit-gpt2-image-captioning")
=======
feature_extractor = ViTFeatureExtractor.from_pretrained("nlpconnect/vit-gpt2-image-captioning")
>>>>>>> 221de2e8fc6779426901f2f3eb86618b73e0c2c2
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
        
<<<<<<< HEAD
        # Create an attention mask
        attention_mask = torch.ones(inputs['pixel_values'].shape[:-1], dtype=torch.long).to(device)

        # Generate caption using the model with attention mask
        outputs = model.generate(
            inputs['pixel_values'], 
            attention_mask=attention_mask,
            max_length=50 if mode == "summary" else 100
        )
=======
        # Generate caption using the model
        outputs = model.generate(**inputs, max_length=50 if mode == "summary" else 100)
>>>>>>> 221de2e8fc6779426901f2f3eb86618b73e0c2c2
        
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

