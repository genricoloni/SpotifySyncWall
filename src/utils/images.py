"""
Module for image processing functions.
"""

import math
from PIL import Image, ImageDraw, ImageFont

def paste_and_save_album_image(bg, cover, display, text):
    """
       Paste the album image in the center of the background image and save the final image.
       Args:
           bg (Image): The background image.
           cover (Image): The album image.
           display (tuple): The dimensions of the display.
           text (Image): The text image.
    """

    width = int(display[0])
    height = int(display[1])

    # Calculate the center coordinates for pasting
    center_x = int(width / 2 - cover.width / 2)
    center_y = int(height / 2 - cover.height / 2)

    # Paste the album image in the center
    bg.paste(cover, (center_x, center_y))
    #save the final image

    background = Image.new('RGB', (width, height))
    background.paste(bg, (0, 0))
    background.paste(text, (0, 0), mask = text)

    background.save("ImageCache/finalImage.png")

#pylint: disable=too-many-positional-arguments, too-many-arguments
def generate_text_image(song_title, artist_name, colors, display, position_x=50, position_y=50):
    """
    Generate a text image containing the song title and artist name.

    This function creates an image with the song title and artist name rendered onto it.

    Parameters:
        song_title (str): The title of the song.
        artist_name (str): The name of the artist.
        colors (list): A list of colors to use for the text.
        display (list): The dimensions of the display.
        position_x (int, optional): The x-coordinate of the text. Defaults to 50.
        position_y (int, optional): The y-coordinate of the text. Defaults to 50.

    Returns:
        Image: A new image with the song title and artist name.
    """
    width = int(display[0])
    height = int(display[1])

    text_color = colors[0].rgb

    # Adjust text color to ensure contrast
    if (text_color[0] * 0.299 + text_color[1] * 0.587 + text_color[2] * 0.114) > 186:
        text_color = (0, 0, 0)  # Black text for light backgrounds
    else:
        text_color = (255, 255, 255)  # White text for dark backgrounds

    # Create a new transparent image for the text
    text = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(text)

    # Set font and draw the text
    my_font = ImageFont.truetype("./fonts/Rubik.ttf", 40)
    draw.text((position_x, position_y),
              (song_title + "\n" + artist_name),
              font=my_font, fill=text_color)

    return text


def calculate_contrast_ratio(color1, color2):
    """
    Calculate the contrast ratio between two colors.

    The contrast ratio is calculated using the formula:
    (L1 + 0.05) / (L2 + 0.05), where L1 and L2 are the relative luminances
    of the two colors.

    Parameters:
        color1 (Color): The first color.
        color2 (Color): The second color.

    Returns:
        float: The contrast ratio between the two colors.
    """
    luminance1 = calculate_relative_luminance(color1)
    luminance2 = calculate_relative_luminance(color2)

    # Ensure luminance1 is the higher value
    if luminance2 > luminance1:
        luminance1, luminance2 = luminance2, luminance1

    return (luminance1 + 0.05) / (luminance2 + 0.05)


def calculate_relative_luminance(color):
    """
    Calculate the relative luminance of a color.

    The luminance is calculated using the formula:
    L = 0.2126 * R + 0.7152 * G + 0.0722 * B

    Parameters:
        color (Color): The color object to calculate luminance for.

    Returns:
        float: The relative luminance of the color.
    """
    r, g, b = color.rgb
    return 0.2126 * r + 0.7152 * g + 0.0722 * b

def find_darkest_color(colors):
    """
    Find the darkest color in a list of colors.

    Args:
        colors (list): A list of color objects.

    Returns:
        Color:s: A list of color objects.

    """
    #distance from black
    distance1 = math.sqrt(colors[0].rgb[0]**2 + colors[0].rgb[1]**2 + colors[0].rgb[2]**2)
    distance2 = math.sqrt(colors[1].rgb[0]**2 + colors[1].rgb[1]**2 + colors[1].rgb[2]**2)

    if distance1 > distance2:
        return [colors[0], colors[1]]

    return [colors[1], colors[0]]

# pylint: disable=no-member
def resize_and_center_image(image, target_width, target_height):
    """
    Resizes an image to a target width, and centers it vertically.

    Args:
        image (Image): The image to resize.
        target_width (int): The target width of the image.
        target_height (int): The target height of the image.

    Returns:
        Image: The resized and centered image.
    """
    # Resize with preserved aspect ratio
    aspect_ratio = image.width / image.height
    new_height = target_height
    new_width = int(int(aspect_ratio) * int(new_height))
    resized_image = image.resize((int(new_width), int(new_height)), Image.LANCZOS)

    target_width = int(target_width)
    # Center the image vertically
    if new_width > target_width:
        x_offset = (new_width - target_width) // 2
        resized_and_centered_image = resized_image.crop((
            x_offset, 0, x_offset + target_width, new_height))
    else:
        resized_and_centered_image = resized_image

    return resized_and_centered_image
