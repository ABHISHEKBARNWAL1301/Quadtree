from PIL import Image
from quadtree import QuadTree
import logging


# Set up logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def build_quadtree(image_path):
    """Build a QuadTree from an image."""
    image = Image.open(image_path)
    width, height = image.size
    qt = QuadTree(max(width.bit_length(), height.bit_length()))
    pixels = image.load()  # Load the pixel data
    for y in range(height):
        for x in range(width):
            color = pixels[x, y]  # Get the pixel color (as an RGB tuple)
            qt.set(x, y, x + 1, y + 1, color)  # Set each pixel in the QuadTree
    return qt


def compress_image(image_path):
    qt_original = build_quadtree(image_path)  # Build the quadtree
    original_size = qt_original.count_nodes()  # Count nodes in the original quadtree

    # Now we will reduce the original quadtree
    qt_original.reduce()  # Reduce the quadtree to merge nodes
    reduced_size = qt_original.count_nodes()  # Count nodes in the reduced quadtree

    # Output the size difference
    print(f"Original Quadtree size: {original_size} nodes")
    print(f"Reduced Quadtree size: {reduced_size} nodes")
    print(f"Size difference: {original_size - reduced_size} nodes")


# def invert_image(image_path):
#     """Invert an image using the QuadTree and save the result."""
#     # Build the quadtree from the original image
#     qt = build_quadtree(image_path)

#     # Invert the colors in the quadtree
#     qt.complement()  # Assuming you have a complement method to toggle pixel colors
#     print("Image inverted")

#     # Create an empty image to hold the inverted pixel values
#     inverted_image = Image.new("RGB", (2 ** qt.s, 2 ** qt.s))
#     pixels = inverted_image.load()

#     # Retrieve pixel values from the quadtree and set them in the new image
#     for y in range(inverted_image.height):
#         for x in range(inverted_image.width):
#             # Get the inverted color from the quadtree
#             inverted_color = qt.get(x, y)  # Assuming this returns the inverted color
#             pixels[x, y] = tuple(inverted_color)  # Set the pixel color in the inverted image

#     # Save the inverted image to a file
#     inverted_image_path = image_path.replace(".png", "_inverted.png")
#     inverted_image.save(inverted_image_path)
#     logging.info(f"Inverted image saved as {inverted_image_path}")


if __name__ == "__main__":
    compress_image('/Users/abhishek2.barnwal/Desktop/self/Quadtree/image.png')  # Compress the image
    # invert_image('/Users/abhishek2.barnwal/Desktop/self/Quadtree/image.png')  # Invert the image
