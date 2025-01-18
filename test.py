import cv2
import easyocr
from googletrans import Translator

def translate_and_display_image(image_path, target_language):
    # Initialize EasyOCR reader
    reader = easyocr.Reader(['en', 'es'])  # Add more languages as needed

    # Perform OCR
    results = reader.readtext(image_path, detail=0)
    extracted_text = "\n".join(results)
    print("Extracted Text:", extracted_text)  # Optional: Debugging purposes

    # Translate text
    translator = Translator()
    translated_text = translator.translate(extracted_text, dest=target_language).text

    # Load the image with OpenCV
    image = cv2.imread(image_path)

    # Overlay translated text on the image
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 0.5
    font_thickness = 1
    color = (0, 255, 0)  # Green text
    x, y = 10, 30  # Starting position for text

    for i, line in enumerate(translated_text.split("\n")):
        cv2.putText(image, line, (x, y + i * 20), font, font_scale, color, font_thickness)
    print(type(image))

    from matplotlib import pyplot as plt
    plt.imshow(image, interpolation='nearest')
    plt.show()

if __name__ == "__main__":
    # Hardcoded image path
    image_path = r"C:\Users\joewo\OneDrive\Pictures\Screenshots\test.png"
    target_language = "es"  # Example: 'es' for Spanish

    translate_and_display_image(image_path, target_language)
