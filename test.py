import pdf2image
from pdf2image import convert_from_path
import matplotlib.pyplot as plt

# Path to the PDF file
pdf_path = "C:/Users/joewo/Downloads/2324-0185-recruitment-activity-handout-card-6X4-proof2.pdf"

# Convert PDF to images
images = convert_from_path(pdf_path)

# Display each page using imshow
for i, image in enumerate(images):
    plt.figure(figsize=(10, 10))  # Set figure size for display
    plt.imshow(image)
    plt.axis("off")  # Hide axes
    plt.title(f"Page {i + 1}")  # Add a title for the page
    plt.show()  # Display the image
