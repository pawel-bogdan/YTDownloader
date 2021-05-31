def resize_image(image, new_size):
    """
    Function resizes image to new size.
    :param image: Image which will be resized.
    :param new_size: Tuple which contains two values: width and height of new size
    :return: Resized image
    """
    return image.resize(new_size)
