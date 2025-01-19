import cv2
import easyocr
from pygoogletranslation import Translator


translator = Translator()
reader = easyocr.Reader(["en"])


def translate_image(image, target_language):
    results, translated_text = get_information(image, target_language)
    return apply_information(image, results, translated_text)

def get_information(image, target_language):
    # Perform OCR
    results = reader.readtext(image)
    if results:
        translated_text = translator.translate("\n".join([res[1] for res in results]), dest=target_language).text.split("\n")
    else:
        translated_text = []
    return results, translated_text

def apply_information(image, results, translated_text):
    for (bbox, text, prob) in results:
        if prob > 0.5:
            (tl, tr, br, bl) = bbox
            tl = (int(tl[0]), int(tl[1]))
            tr = (int(tr[0]), int(tr[1]))
            br = (int(br[0]), int(br[1]))
            bl = (int(bl[0]), int(bl[1]))
            cv2.rectangle(image, tl, br, (255, 255, 255), -1)

    i = 0
    for (bbox, text, prob) in results:
        if prob > 0.5:
            (tl, tr, br, bl) = bbox
            tl = (int(tl[0]), int(tl[1]))
            tr = (int(tr[0]), int(tr[1]))
            br = (int(br[0]), int(br[1]))
            bl = (int(bl[0]), int(bl[1]))
            cv2.putText(image, translated_text[i], (tl[0], bl[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 1)
        i += 1

    return image
