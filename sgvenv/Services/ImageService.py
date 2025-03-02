import cv2
import io
from PIL import Image

def get_latest_drawn_image_bytes():
    image = load_image("DrawnImages/drawing_output.png")

    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    pil_image = Image.fromarray(image_rgb)

    img_byte_array = io.BytesIO()
    pil_image.save(img_byte_array, format='PNG')
    img_byte_array.seek(0)

    return img_byte_array

def load_image(img_path):
    image = cv2.imread(img_path)
    
    return image

def load_image_greyscale(img_path):
    image = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
    
    return image