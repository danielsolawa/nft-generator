from PIL import Image
from PIL.Image import Resampling

import LayerHandler

OUTPUT_DIRECTORY = "output"


def save_image(layers: any, i: int) -> None:
    bg = Image.open(layers[0][LayerHandler.FULL_PATH])
    for layer in layers[1]:
        if layer[LayerHandler.INDEX] == -1:
            continue
        full_path = layer[LayerHandler.FULL_PATH]
        img = Image.open(full_path).convert("RGBA").resize((500, 500), resample=Resampling.NEAREST)
        bg.paste(img, (0, 0), img)
    bg.save(OUTPUT_DIRECTORY + LayerHandler.SLASH + str(i) + '.png', 'png', quality=95)
