# grid-img-util
Command line utilities for editing grid-based (tile-based) images. Both programs require Python and the [Pillow module](https://python-pillow.org).

Table of contents:
* [a note about the files](#a-note-about-the-files)
* [unique-tiles](#unique-tiles)
* [resize-grid](#resize-grid)

## a note about the files
These files are only meant to be used by the author:
* `*-test.sh` (test scripts; they delete files so don't run them without reading them first)
* `*-test.md5` (hashes of correct output files)
* `test-in/*.png` (test images to be read)

## unique-tiles
Reads one or more images and writes a PNG image with distinct tiles (rectangles of specified size) only.

Some of the sample images are from *Commander Keen: Secret of the Oracle* and *Wolfenstein 3D* by id Software.

### Command line arguments
*options* *inputFiles*
* *options* are any number of these, separated by spaces:
  * `--width N`: The width of each tile, in pixels. `N` is 1 to 256. The default is 8.
  * `--height N`: The height of each tile, in pixels. `N` is 1 to 256. The default is 8.
  * `--order V`: Order of tiles in the output image. `V` is one of these:
    * `o`: original (the first tile to occur in the first input file will occur first in *outputFile*; this is the default)
    * `p`: first by brightnesses of pixels, top left pixel first, then by original order
    * `a`: first by average brightness of each tile, then by original order
    * `c`: first by number of unique colors, then by original order
    * `cp`: first by number of unique colors, then by brightnesses of pixels, then by original order
    * `ca`: first by number of unique colors, then by average brightness of each tile, then by original order
  * `--verbose`: Print information.
  * `--outfile F`: The PNG file to write. `F` is the filename.
    * Required.
    * Will contain every distinct tile in the input files once.
    * The width will be 16 times the tile size.
    * The height will be a multiple of the tile size.
* *inputFiles*: Image files (e.g. PNG) to read.
  * One or more filenames separated by spaces.
  * At least one is required.
  * The width of each image must be a multiple of the tile width.
  * The height of each image must be a multiple of the tile height.
  * The files must not have an alpha channel.

### Example
`python3 uniquetiles.py --outfile wolf3d-uniquetiles.png wolf3d.png`

Before and after:

![Wolfenstein 3D title screen](test-in/wolf3d.png)
![unique tiles in Wolfenstein 3D title screen](uniquetiles-wolf3d.png)

## resize-grid
A command line tool that reads a grid-based image and writes a PNG image with a grid of different size. Each tile (rectangle) in the grid will be padded to the new size by adding the specified background color to the right and bottom edges, or cropped to the new size by cutting off the right and bottom edges.

### Command line arguments
*options* *inputFile* *outputFile*
* *options* are any number of these, separated by spaces:
  * `--iw N`: Width of each tile in input file, in pixels. `N` is 1 to 256. The default is 8.
  * `--ih N`: Height of each tile in input file, in pixels. `N` is 1 to 256. The default is 8.
  * `--ow N`: Width of each tile in output file, in pixels. `N` is 1 to 256. The default is 9.
  * `--oh N`: Height of each tile in output file, in pixels. `N` is 1 to 256. The default is 9.
  * `--bgcolor C`: Background color in output file. Hexadecimal RRGGBB code, `000000`&ndash;`ffffff`. The default is `000000` (black).
* *inputFile*: Image file to read (e.g. PNG).
  * Required.
  * The width must be a multiple of input tile width.
  * The height must be a multiple of input tile height.
  * No alpha channel.
* *outputFile*: PNG file to write.
  * Required.
  * The width will be (input image width) / (input tile width) &times; (output tile width).
  * The height will be (input image height) / (input tile height) &times; (output tile height).

### Example
`python3 resizegrid.py resizegrid-before.png resizegrid-after.png --iw 8 --ih 8 --ow 10 --oh 12 --bgcolor 0000ff`

Before and after:

![four letters in a two-by-two grid, with only a little space in between](resizegrid-before.png)
![four letters in a two-by-two grid, with more space in between horizontally and even more vertically](resizegrid-after.png)

(The images were actually 16&times;16 and 20&times;24 pixels; they've been resized to 5x their original size afterwards.)
