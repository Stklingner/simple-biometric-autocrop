import argparse
from PIL import Image
import face_recognition
import sys

try:
    import face_recognition_models
except ImportError:
    print("face_recognition_models is not installed. Please install it using:")
    print("pip install git+https://github.com/ageitgey/face_recognition_models")
    sys.exit(1)

def get_image_info(image_path):
    with Image.open(image_path) as img:
        dpi = img.info.get('dpi', (72, 72))  # Default DPI is 72 if not found
        width, height = img.size
        return dpi, width, height

def detect_face(image_path):
    image = face_recognition.load_image_file(image_path)
    face_landmarks_list = face_recognition.face_landmarks(image)

    if not face_landmarks_list:
        raise ValueError("No face detected in the image")

    # Assuming the first detected face is the one we want
    return face_landmarks_list[0]

def get_nose_bridge_center(face_landmarks):
    nose_bridge = face_landmarks['nose_bridge']
    nose_bridge_center = nose_bridge[len(nose_bridge) // 2]  # Approximate center of the nose bridge
    return nose_bridge_center

def create_proportional_crop(image_path, face_landmarks, head_scaling_factor=(2.5,1.1)):
    # Get nose bridge center
    nose_bridge_center = get_nose_bridge_center(face_landmarks)
    nose_x, nose_y = nose_bridge_center

    # Calculate top and bottom based on the chin and forehead (estimated from eyes)
    chin = face_landmarks['chin']
    left_eye = face_landmarks['left_eye']
    right_eye = face_landmarks['right_eye']

    chin_bottom = max([point[1] for point in chin])
    eye_top = min([point[1] for point in left_eye + right_eye])

    face_height = chin_bottom - eye_top

    # Using a 4:5 aspect ratio (35mm x 45mm)
    aspect_ratio = 35 / 45

    # Apply head scaling factor
    scaling_magnitude, scaling_bias = head_scaling_factor

    # Calculate new crop height with scaling
    crop_height = face_height * scaling_magnitude
    crop_width = crop_height * aspect_ratio

    # Calculate the new top and bottom positions with bias
    bias_adjustment = (scaling_bias - 1) * face_height * 0.5
    new_top = max(nose_y - (crop_height / 2) + bias_adjustment, 0)
    new_bottom = min(nose_y + (crop_height / 2) + bias_adjustment, Image.open(image_path).height)
    new_left = max(nose_x - (crop_width / 2), 0)
    new_right = min(nose_x + (crop_width / 2), Image.open(image_path).width)

    with Image.open(image_path) as img:
        proportional_crop = img.crop((int(new_left), int(new_top), int(new_right), int(new_bottom)))
        return proportional_crop


def calculate_new_dpi(original_dpi, original_size, new_size):
    original_width, original_height = original_size
    new_width, new_height = new_size

    new_dpi_x = (new_width / original_width) * original_dpi[0]
    new_dpi_y = (new_height / original_height) * original_dpi[1]

    return new_dpi_x, new_dpi_y

def main(image_path):
    dpi, width, height = get_image_info(image_path)
    print(f"Original Image DPI: {dpi}")
    print(f"Original Image Dimensions: {width} x {height}")

    face_landmarks = detect_face(image_path)
    print(f"Face landmarks detected: {face_landmarks.keys()}")

    proportional_crop = create_proportional_crop(image_path, face_landmarks)
    new_width, new_height = proportional_crop.size
    new_dpi = calculate_new_dpi(dpi, (width, height), (new_width, new_height))

    output_path = "proportional_passport_photo.jpg"
    proportional_crop.save(output_path)
    print(f"Proportional passport photo saved as {output_path}")
    print(f"New Image DPI: {new_dpi}")
    print(f"New Image Dimensions: {new_width} x {new_height}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process an image to create a proportional passport photo.")
    parser.add_argument("image", help="Path to the image file (jpeg, png, tiff)")
    args = parser.parse_args()

    main(args.image)
