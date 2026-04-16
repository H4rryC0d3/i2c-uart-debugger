from luma.core.interface.serial import i2c
from luma.oled.device import ssd1306
from PIL import Image, ImageDraw, ImageFont
from config import OLED_ADDR


try:
    font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 18)
except:
    font = ImageFont.load_default()

def show(msg):
    serial = i2c(port=1, address=OLED_ADDR)
    device = ssd1306(serial)

    image = Image.new("1", (128, 64))
    draw = ImageDraw.Draw(image)

    msg = msg.encode('ascii', 'ignore').decode()

    try:
        bbox = font.getbbox(msg)
        w = bbox[2] - bbox[0]
        h = bbox[3] - bbox[1]
    except AttributeError:
        w, h = draw.textsize(msg, font=font)

    x = (128 - w) // 2
    y = (64 - h) // 2

    draw.text((x, y), msg, font=font, fill=255)
    device.display(image)
