from tqdm import tqdm

import ImageHelper
import LayerHandler as LayerHandler
import Metadata

UniqueNfts = []
NUMBER_OF_NFT = 10


def main() -> None:
    for i in tqdm(range(NUMBER_OF_NFT)):
        generate(i)
    print('saving metadata...')
    Metadata.create()


def generate(index: int) -> None:
    layers = LayerHandler.generate_layers()
    while True:
        token_id = layers[2]
        if token_id in UniqueNfts:
            layers = LayerHandler.generate_layers()
        else:
            ImageHelper.save_image(layers, index + 1)
            UniqueNfts.append(token_id)
            break
    Metadata.calculate_rarity(layers, index + 1)


if __name__ == '__main__':
    main()
