# __BEGIN_LICENSE__
# Copyright (C) 2008-2010 United States Government as represented by
# the Administrator of the National Aeronautics and Space Administration.
# All Rights Reserved.
# __END_LICENSE__

import os

from PIL import Image, ImageOps, ImageFilter

DEFAULT_HALO_WIDTH = 0.1


def autocrop(img):
    _, _, _, a = img.split()
    return img.crop(a.getbbox())


def thresholdFunc(v, thresh):
    if v >= thresh:
        return 255
    else:
        return 0


def thresholdImage(img, thresh):
    return img.point(lambda v: thresholdFunc(v, thresh))


def doAddHalo(inPath, outPath, width):
    im = Image.open(inPath)
    im.load()
    n = max(im.size)
    widthPixels = int(n * width)
    padded = ImageOps.expand(im, border=3 * widthPixels)
    _, _, _, paddedA = padded.split()

    halo = paddedA.copy()
    numBlurIterations = int(widthPixels / 2.5 + 0.5)
    for _ in xrange(0, numBlurIterations):
        halo = halo.filter(ImageFilter.BLUR)
        halo = thresholdImage(halo, 20)

    zero = Image.new('L', paddedA.size, 0)
    one = Image.new('L', paddedA.size, 256)
    result = Image.merge('RGBA', [one, zero, zero, halo])
    result.paste(padded, None, padded)

    outDir = os.path.dirname(os.path.abspath(outPath))
    if not os.path.exists(outDir):
        os.makedirs(outDir)

    autocrop(result).save(outPath)


def addHalo(builder, inPath, outPath, width=DEFAULT_HALO_WIDTH):
    """
    Runs a builder rule that reads the image at inPath, which must be an
    RGBA image, adds a red "halo" around the area of the image with
    non-zero alpha, and writes the result to outPath. @width specifies
    very roughly how wide the halo should be as a proportion of the image
    size (0..1).
    """
    builder.applyRule(outPath, [inPath], lambda: doAddHalo(inPath, outPath, width))


def main():
    import optparse
    parser = optparse.OptionParser('usage: %prog <in.png> <out.png>')
    parser.add_option('-w', '--width',
                      type=float, default=DEFAULT_HALO_WIDTH,
                      help='Width of halo as a proportion of the image size (0..1) [%default]')
    opts, args = parser.parse_args()
    if len(args) != 2:
        parser.error('expected exactly 2 args')
    if not (0 < opts.width and opts.width < 1):
        parser.error('width must be in range 0..1')

    from geocamUtil.Builder import Builder
    builder = Builder()

    addHalo(builder, args[0], args[1], opts.width)

if __name__ == '__main__':
    main()
