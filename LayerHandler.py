import random
from pathlib import Path

ASSETS_DIRECTORY = "assets"
PROBABILITY = "probability"
INDEX = "index"
NAME = "name"
FULL_PATH = "fullPath"
EMPTY_STR = ""
SLASH = "/"
DOT = "."
UNDER_SCORE = "_"
LayerDict = {}
NonEmptyLayers = ["0"]


def get_asset_dict() -> any:
    p = Path(ASSETS_DIRECTORY)
    sub_directories = [str(x) for x in p.iterdir() if x.is_dir()]
    layers_dict = {}
    for sub in sub_directories:
        sub_path = Path(sub)
        key = str(sub_path).replace(ASSETS_DIRECTORY + SLASH, EMPTY_STR)
        layers_dict[key] = {}
        for f in sub_path.iterdir():
            if not f.is_dir():
                f_str = str(f)
                sub = f_str[f_str.rindex(SLASH) + 1: f_str.index(DOT)]
                f_attrs = sub.split(UNDER_SCORE)
                if len(f_attrs) < 3:
                    continue
                layers_dict[key][f_attrs[0]] = get_layer_obj(f_attrs[1], f_attrs[2], f_str, f_attrs[0])
        add_empty_asset(key, layers_dict)
    return layers_dict


def add_empty_asset(key: str, layers_dict: any) -> None:
    if key in NonEmptyLayers:
        return
    layers_dict[key][str(-1)] = get_layer_obj(str(random.randrange(1, 10)), EMPTY_STR, EMPTY_STR)


def get_layer_obj(probability: str, name: str, full_path: str, index: str = "-1") -> any:
    return {INDEX: int(index), PROBABILITY: probability, NAME: name, FULL_PATH: full_path}


def get_indices_and_probabilities(asset_layer: any) -> any:
    indices = set()
    probabilities = set()
    for x in asset_layer:
        indices.add(int(x))
        add_probability(asset_layer, probabilities, x)
    return list(indices), list(probabilities)


def add_probability(asset_layer: any, probabilities: any, x: str) -> None:
    input_probability = int(asset_layer[x][PROBABILITY])
    while input_probability in probabilities:
        input_probability = random.randrange(1, 10)
    probabilities.add(input_probability)


def get_random_asset(layer: any) -> any:
    indices_and_probabilities = get_indices_and_probabilities(layer)
    result = random.choices(indices_and_probabilities[0], indices_and_probabilities[1])
    return retrieve_asset(layer, result[0])


def retrieve_asset(layer_dict: any, index: int) -> any:
    return layer_dict[str(index)]


def get_non_bg_layers(other_assets_dict: any) -> any:
    def get_random(i):
        random_asset = get_random_asset(other_assets_dict[str(i)])
        return random_asset if random_asset[INDEX] != -1 else {INDEX: -1}

    return [get_random(i) for i in range(1, len(other_assets_dict))]


def generate_token_id(bg_layer: any, non_bg_layers: any) -> str:
    new_non_bg_layers = non_bg_layers.copy()
    new_non_bg_layers.insert(0, bg_layer)
    return ''.join([str(x[INDEX]) for x in new_non_bg_layers])


def generate_layers() -> any:
    assets_dict = get_asset_dict()
    bg_layer = get_random_asset(assets_dict["0"])
    non_bg_layers = get_non_bg_layers(assets_dict)
    token_id = generate_token_id(bg_layer, non_bg_layers)
    return bg_layer, non_bg_layers, token_id
