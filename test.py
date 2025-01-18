import easyocr
from googletrans import Translator
from PIL import Image, ImageDraw, ImageFont

def translate_and_display_image(image_path, target_language):


    # Crée un lecteur OCR avec les langues que tu souhaites utiliser
    reader = easyocr.Reader(['en', 'fr'])

    # Créer un traducteur
    translator = Translator()

    image = Image.open(image_path)
    draw = ImageDraw.Draw(image)

    # Lire l'image avec EasyOCR pour détecter le texte et obtenir les coordonnées
    result = reader.readtext(image_path)

    # Traiter chaque zone de texte détectée
    for detection in result:
        # Extraction des coordonnées et du texte
        top_left, bottom_right, text = detection[0], detection[1], detection[1]

        # Traduction du texte
        translated_text = translator.translate(text, src='en', dest='fr').text

        # Définir la taille et la police du texte traduit
        font = ImageFont.load_default()
        font_size = 30  # Tu peux ajuster la taille de la police
        try:
            font = ImageFont.truetype("arial.ttf", font_size)  # Utiliser une police spécifique (si disponible)
        except IOError:
            font = ImageFont.load_default()  # Police par défaut si "arial" n'est pas trouvé

        # Calculer la taille du texte pour ajuster la position
        text_width, text_height = draw.textsize(translated_text, font=font)

        # Redimensionner le texte pour s'adapter à la boîte de détection
        max_width = bottom_right[0] - top_left[0]
        if text_width > max_width:
            font_size = int(font_size * max_width / text_width)
            font = ImageFont.truetype("arial.ttf", font_size) if font_size < 30 else font

        # Ajouter un fond sous le texte pour améliorer la lisibilité (facultatif)
        background_color = (255, 255, 255)  # Blanc
        text_color = (0, 0, 0)  # Noir

        # Dessiner le texte traduit dans la zone de texte détectée
        draw.rectangle([top_left, bottom_right], outline="red", width=2)  # Dessiner une boîte rouge autour du texte
        draw.text((top_left[0], top_left[1] - 10), translated_text, font=font, fill=text_color)

    # Sauvegarder l'image modifiée
    output_path = 'image_with_translated_text.jpg'
    image.save(output_path)

    # Afficher l'image modifiée
    image.show()

    print(f"L'image avec le texte traduit a été enregistrée sous : {output_path}")

if __name__ == "__main__":
    # Hardcoded image path
    image_path = r"C:\Users\ariel\Downloads\test.jpg"
    target_language = "es"  # Example: 'es' for Spanish

    translate_and_display_image(image_path, target_language)
