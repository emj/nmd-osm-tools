#!/usr/bin/python3

# Remap pixel values in a paletted GeoTiff from NMD
# Compared to stock GDAL tools, this script tries to transfer all metadata
# and color table from the first band of the input file into the output file.
# Input data is a TIFF file available at:
# - http://www.naturvardsverket.se/Sa-mar-miljon/Kartor/Nationella-Marktackedata-NMD/

import sys
import gdal
import numpy

def usage():
    print("Usage: %s <input.tiff> <output.tiff>" % sys.argv[0], file = sys.stderr)
    sys.exit(1)

def main(argv):
    if len(argv) != 3:
        usage()
    input_name = argv[1]
    output_name = argv[2]

    # Read pixel array and all relevant metadata
    input_tiff = gdal.Open(input_name)
    geotransform = input_tiff.GetGeoTransform()
    projection = input_tiff.GetProjection()
    metadata = input_tiff.GetMetadata()
    band = input_tiff.GetRasterBand(1)
    band_meta = band.GetMetadata()
    band_descr = band.GetDescription()
    band_ct = band.GetColorTable()

    xsize = band.XSize
    ysize = band.YSize

    input_array = band.ReadAsArray()

    # NOTE Cannot clean up resources for input data because apparently there are
    # alive references to them from output data (according to where GDB
    # shows it crashes if you uncomment two following lines)
#    input_tiff = None
#    band = None


    # Remap specific pixel values that will have identical tags
    remap_table = dict()
    remap_table[111] = 113
    remap_table[112] = 113

    remap_table[115] = 117
    remap_table[116] = 117

    remap_table[121] = 123
    remap_table[122] = 123

    remap_table[125] = 127
    remap_table[126] = 127

    # TODO: I feel like making a copy of the array here would lead to twice
    # the memory consumption. But I failed to perform an in-place data update.
    # Someone who knows NumPy better than me, please fix this.

    output_array = numpy.copy(input_array)
    for k, v in remap_table.items(): output_array[input_array == k] = v

    # Open an output file and start forming its contents
    driver = gdal.GetDriverByName('GTiff')

    output_tiff = driver.Create(output_name, xsize, ysize, 1, gdal.GDT_Byte,
                                options=['COMPRESS=LZW'])
    output_tiff.SetGeoTransform(geotransform)
    output_tiff.SetProjection(projection)
    output_tiff.SetMetadata(metadata)

    output_band = output_tiff.GetRasterBand(1)
    output_band.WriteArray(output_array)
    output_band.SetMetadata(band_meta)
    output_band.SetDescription(band_descr)
    output_band.SetColorTable(band_ct)

    # Save and close the output file
    output_tiff.FlushCache()
    output_tiff = None

if __name__ == "__main__":
    sys.exit(main(sys.argv))
