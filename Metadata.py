import json
from datetime import datetime

import LayerHandler

DATE_TIME_FORMAT = "%d%m%Y_%H%M%S"
ASSETS = "assets"
FILE_NAME = "file_name"
RarityDict = {}
Nft_Dict = {}


def create() -> None:
    now = datetime.now().strftime(DATE_TIME_FORMAT)
    metadata_file_name = "metadata/{}.json".format(now)
    metadata_dict = {}
    for key in Nft_Dict:
        nft = Nft_Dict[key]
        metadata = {}
        for asset in nft[ASSETS]:
            name = asset[LayerHandler.NAME]
            final_name = split_camel_case(name)
            rarity_value = RarityDict[name] / len(Nft_Dict) * 100
            metadata[final_name] = "{}%".format(rarity_value)
        metadata_dict[nft[FILE_NAME]] = metadata
    save_metadata(metadata_dict, metadata_file_name)


def save_metadata(metadata_dict: any, metadata_file_name: str) -> None:
    with open(metadata_file_name, "w") as file:
        json.dump(metadata_dict, file, indent=4)


def split_camel_case(input_str: str) -> str:
    result = ""
    for i in range(0, len(input_str)):
        current_char = input_str[i]
        result += " {}".format(current_char.lower()) if current_char.isupper() else current_char
    return result


def calculate_rarity(layers: any, file_number: int) -> None:
    normalized_layers = layers[1].copy()
    normalized_layers.insert(0, layers[0])
    token_id = layers[2]
    assets = []
    for layer in normalized_layers:
        if layer[LayerHandler.INDEX] == -1:
            continue
        assets.append(layer)
        name = layer[LayerHandler.NAME]
        RarityDict[name] = RarityDict[name] + 1 if name in RarityDict else 1
    Nft_Dict[token_id] = {FILE_NAME: str(file_number) + ".png", ASSETS: assets}
