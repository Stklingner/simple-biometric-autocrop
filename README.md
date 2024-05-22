```markdown
# Biometric Passport Photo Processor

This Python CLI program processes an image file to detect a face, crops it to conform to biometric passport photo standards, and reports the DPI and dimensions of the cropped image.

## Features

- Detects face in an image using the `face_recognition` library.
- Crops the image based on the detected face to create a proportional passport photo.
- Allows customization of the crop through a head scaling factor.
- Reports the DPI and dimensions of the cropped image.

## Requirements

- Python 3.6+
- Pillow
- face_recognition
- face_recognition_models
- cmake (for dlib)

## Installation

1. Clone the repository:
   ```sh
   git clone https://github.com/yourusername/biometric-photo-processor.git
   cd biometric-photo-processor
   ```

2. Create and activate a virtual environment:
   ```sh
   python3 -m venv venv
   source venv/bin/activate  # Unix/MacOS
   # .\venv\Scripts\activate  # Windows
   ```

3. Install the required packages:
   ```sh
   pip install --upgrade setuptools
   pip install pillow face_recognition cmake
   pip install git+https://github.com/ageitgey/face_recognition_models
   ```

## Usage

1. Place your image file in the directory or provide the path to your image file.

2. Run the script with the path to your image file:
   ```sh
   python passport_photo.py path/to/your/image.jpg
   ```

3. You can customize the head scaling factor by modifying the script:
   ```python
   # Define the head scaling factor (magnitude, bias)
   head_scaling_factor = (1.5, 1.0)  # Example values: 1.5x scaling, centered bias
   ```

## Example

Given an image `example.jpg`, run:
```sh
python passport_photo.py example.jpg
```

This will:
- Detect the face in `example.jpg`.
- Crop the image proportionally based on the face landmarks and head scaling factor.
- Save the cropped image as `proportional_passport_photo.jpg`.
- Print the new DPI and dimensions of the cropped image.

## Script Details

### `passport_photo.py`

This script includes the following key functions:

- `get_image_info(image_path)`: Retrieves the DPI and dimensions of the image.
- `detect_face(image_path)`: Detects face landmarks in the image.
- `get_nose_bridge_center(face_landmarks)`: Calculates the center of the nose bridge from face landmarks.
- `create_proportional_crop(image_path, face_landmarks, head_scaling_factor)`: Crops the image proportionally based on the face landmarks and head scaling factor.
- `calculate_new_dpi(original_dpi, original_size, new_size)`: Calculates the new DPI after cropping.
- `main(image_path)`: Main function to process the image.

## License

This project is licensed under the MIT License.

## Acknowledgments

- [face_recognition](https://github.com/ageitgey/face_recognition)
- [Pillow](https://python-pillow.org/)
- [dlib](http://dlib.net/)

## Contributing

Feel free to submit issues, fork the repository, and make pull requests. Contributions are welcome!
```