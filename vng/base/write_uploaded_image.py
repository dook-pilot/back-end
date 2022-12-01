from uuid import uuid4

def get_image(file):
    image_name = str(uuid4())+".jpg"
    image_bytes = file.read()
    with open(image_name, "wb") as img:
        img.write(image_bytes)
    return (image_name, image_bytes)