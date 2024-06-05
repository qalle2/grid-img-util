# resize the grid of a grid-based image

import argparse, os, sys
try:
    from PIL import Image, UnidentifiedImageError
except ImportError:
    sys.exit("Pillow module required. See https://python-pillow.org")

def decode_color_code(colorStr):
    # decode a hexadecimal RRGGBB color code into (red, green, blue)
    try:
        color = int(colorStr, 16)
        if not 0 <= color <= 0xffffff:
            raise ValueError
    except ValueError:
        sys.exit("Unrecognized color code: " + colorStr)
    return tuple((color >> s) & 0xff for s in (16, 8, 0))

def parse_arguments():
    # parse command line arguments

    parser = argparse.ArgumentParser(
        description="Enlarge the grid of a grid-based image. See README.md "
        "for more info."
    )

    parser.add_argument("--iw", type=int, default=8)
    parser.add_argument("--ih", type=int, default=8)
    parser.add_argument("--ow", type=int, default=9)
    parser.add_argument("--oh", type=int, default=9)
    parser.add_argument("--bgcolor", type=str, default="000000")

    parser.add_argument("inputfile")
    parser.add_argument("outputfile")

    args = parser.parse_args()

    intArgValues = (args.iw, args.ih, args.ow, args.oh)
    if min(intArgValues) < 1 or max(intArgValues) > 256:
        sys.exit("Tile widths and heights must be 1-256.")

    if args.ow == args.iw and args.oh == args.ih:
        sys.exit(
            "Output tile size must be different from input tile size in at "
            "least one dimension."
        )

    decode_color_code(args.bgcolor)  # just validate for now

    if not os.path.isfile(args.inputfile):
        sys.exit("Input file not found.")
    if os.path.exists(args.outputfile):
        sys.exit("Output file already exists.")

    return args

def convert_image(source, args):
    # source: source image
    # return: target image

    if source.width == 0 or source.width % args.iw:
        sys.exit("Image width is not a multiple of input tile width.")
    if source.height == 0 or source.height % args.ih:
        sys.exit("Image height is not a multiple of input tile height.")

    if source.mode in ("L", "P"):
        source = source.convert("RGB")
    elif source.mode != "RGB":
        sys.exit(
            "Unsupported input pixel format (try removing the alpha channel)."
        )

    # input image width & height in tiles
    tileColumns = source.width  // args.iw
    tileRows    = source.height // args.ih

    # create output image
    target = Image.new(
        "RGB", (tileColumns * args.ow, tileRows * args.oh),
        decode_color_code(args.bgcolor)
    )

    # create a temporary image for copying each tile
    tileWidth  = min(args.iw, args.ow)
    tileHeight = min(args.ih, args.oh)
    tileImage = Image.new(
        "RGB", (tileWidth, tileHeight), decode_color_code(args.bgcolor)
    )

    for ty in range(tileRows):
        for tx in range(tileColumns):
            # copy tile from input image to temporary image
            x = tx * args.iw
            y = ty * args.ih
            tile = tuple(
                source.crop((x, y, x + tileWidth, y + tileHeight)).getdata()
            )
            tileImage.putdata(tile)
            # copy temporary image to top left corner of corresponding tile in
            # output image
            target.paste(tileImage, (tx * args.ow, ty * args.oh))

    return target

def main():
    args = parse_arguments()

    try:
        with open(args.inputfile, "rb") as source, \
        open(args.outputfile, "wb") as target:
            source.seek(0)
            sourceImage = Image.open(source)
            targetImage = convert_image(sourceImage, args)
            target.seek(0)
            targetImage.save(target, "png")
    except UnidentifiedImageError:
        sys.exit("Unrecognized input image format.")
    except OSError:
        sys.exit("Error reading/writing files.")

main()
