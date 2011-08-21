# __BEGIN_LICENSE__
# Copyright (C) 2008-2010 United States Government as represented by
# the Administrator of the National Aeronautics and Space Administration.
# All Rights Reserved.
# __END_LICENSE__

from PIL import Image, ImageOps, ImageFilter

HALO_PAD_WIDTH=32

def autocrop(img):
    r, g, b, a = img.split()
    return img.crop(a.getbbox())

def thresholdFunc(v, thresh):
    if v >= thresh:
        return 255
    else:
        return 0

def thresholdImage(img, thresh):
    return img.point(lambda v: thresholdFunc(v, thresh))

def doAddHalo(inPath, outPath, threshold):
    im = Image.open(inPath)
    im.load()
    r, g, b, a = im.split()
    paddedA = ImageOps.expand(a, border=HALO_PAD_WIDTH)
    blur = paddedA.filter(ImageFilter.BLUR)
    halo = thresholdImage(blur, threshold)
    zero = Image.new('L', paddedA.size, 0)
    one = Image.new('L', paddedA.size, 256)
    result = Image.merge('RGBA', [one, zero, zero, halo])
    padded = ImageOps.expand(im, border=HALO_PAD_WIDTH)
    result.paste(padded, None, padded)
    autocrop(result).save(outPath)

def addHalo(builder, inPath, outPath, threshold=30):
    """
    Runs a builder rule that reads the image at inPath, which must be an
    RGBA image, adds a red "halo" around the area of the image with
    non-zero alpha, and writes the result to outPath. @threshold is a
    crude control on the width of the halo (0-255, lower values make a
    wider halo).
    """
    builder.applyRule(outPath, [inPath], lambda: doAddHalo(inPath, outPath, threshold))

def main():
    import optparse
    parser = optparse.OptionParser('usage: %prog <in.png> <out.png>')
    parser.add_option('-t', '--threshold',
                      type=int, default=30,
                      help='Smaller threshold value (0..255) gives a larger halo [%default]')
    opts, args = parser.parse_args()
    if len(args) != 2:
        parser.error('expected exactly 2 args')

    from geocamUtil.Builder import Builder
    builder = Builder()

    addHalo(builder, args[0], args[1], opts.threshold)

if __name__ == '__main__':
    main()
