# convert an image into a PNG with unique tiles (squares) only

import argparse, os, sys
from collections import OrderedDict
from itertools import chain
try:
    from PIL import Image
except ImportError:
    sys.exit("Pillow module required. See https://python-pillow.org")

# output image settings
BACKGROUND_COLOR = (0xff, 0x00, 0xff)
TILES_PER_ROW = 16

def parse_arguments():
    # parse command line arguments

    parser = argparse.ArgumentParser(
        description="Convert an image into a PNG with distinct tiles only. "
        "See README.md for more info."
    )

    parser.add_argument("--width", type=int, default=8)
    parser.add_argument("--height", type=int, default=8)
    parser.add_argument(
        "--order", choices=("o", "p", "a", "c", "cp", "ca"), default="o"
    )
    parser.add_argument("--outfile", type=str, required=True)
    parser.add_argument("--verbose", action="store_true")

    parser.add_argument("inputfiles", nargs="+")

    args = parser.parse_args()

    if not 1 <= args.width <= 256:
        sys.exit("Tile width must be 1-256.")
    if not 1 <= args.height <= 256:
        sys.exit("Tile height must be 1-256.")

    for file_ in args.inputfiles:
        if not os.path.isfile(file_):
            sys.exit("Input file not found: " + file_)
    if os.path.exists(args.outfile):
        sys.exit("Output file already exists.")

    return args

def get_tiles(handle, tileWidth, tileHeight):
    # generate: tuples of (red, green, blue) tuples in original order

    handle.seek(0)
    image = Image.open(handle)

    if image.width == 0 or image.width % tileWidth:
        sys.exit("Image width is not a multiple of tile width.")
    if image.height == 0 or image.height % tileHeight:
        sys.exit("Image height is not a multiple of tile height.")

    if image.mode in ("L", "P"):
        image = image.convert("RGB")
    elif image.mode != "RGB":
        sys.exit("Unrecognized pixel format (try removing the alpha channel).")

    for y in range(0, image.height, tileHeight):
        for x in range(0, image.width, tileWidth):
            yield tuple(
                image.crop((x, y, x + tileWidth, y + tileHeight)).getdata()
            )

def write_image(handle, uniqueTiles, tileWidth, tileHeight):
    # write unique tiles to an image;
    # uniqueTiles: list of tuples of (red, green, blue) tuples

    width = TILES_PER_ROW * tileWidth
    # height = ceil(len(uniqueTiles) / TILES_PER_ROW) * tileHeight
    height = (
        (len(uniqueTiles) + TILES_PER_ROW - 1) // TILES_PER_ROW * tileHeight
    )
    image = Image.new("RGB", (width, height), BACKGROUND_COLOR)

    # copy pixels to image via temporary image
    tileImage = Image.new("RGB", (tileWidth, tileHeight))
    for (i, tile) in enumerate(uniqueTiles):
        (y, x) = divmod(i, TILES_PER_ROW)
        tileImage.putdata(tile)
        image.paste(tileImage, (x * tileWidth, y * tileHeight))

    handle.seek(0)
    image.save(handle, "png")

def rgb_to_grayscale(red, green, blue):
    return red * 2 + green * 3 + blue

def main():
    args = parse_arguments()

    uniqueTiles = []  # a set wouldn't preserve the order
    for file_ in args.inputfiles:
        try:
            with open(file_, "rb") as handle:
                for tile in get_tiles(handle, args.width, args.height):
                    if tile not in uniqueTiles:
                        uniqueTiles.append(tile)
        except OSError:
            sys.exit("Error reading input file: " + file_)

    if args.verbose:
        print("Unique colors:", len(set(chain.from_iterable(uniqueTiles))))
        print("Unique tiles:", len(uniqueTiles))
        print(
            "Min. unique colors/tile:", min(len(set(t)) for t in uniqueTiles)
        )
        print(
            "Max. unique colors/tile:", max(len(set(t)) for t in uniqueTiles)
        )

    if args.order == "o":
        pass
    elif args.order == "p":
        uniqueTiles.sort(key=lambda t: tuple(rgb_to_grayscale(*p) for p in t))
    elif args.order == "a":
        uniqueTiles.sort(key=lambda t: sum(rgb_to_grayscale(*p) for p in t))
    elif args.order == "c":
        uniqueTiles.sort(key=lambda t: len(set(t)))
    elif args.order == "cp":
        uniqueTiles.sort(key=lambda t: tuple(rgb_to_grayscale(*p) for p in t))
        uniqueTiles.sort(key=lambda t: len(set(t)))
    elif args.order == "ca":
        uniqueTiles.sort(key=lambda t: sum(rgb_to_grayscale(*p) for p in t))
        uniqueTiles.sort(key=lambda t: len(set(t)))
    else:
        sys.exit("Something went wrong.")

    try:
        with open(args.outfile, "wb") as handle:
            write_image(handle, uniqueTiles, args.width, args.height)
    except OSError:
        sys.exit("Error writing output file.")

main()
