for i in range(1, 44):
    if i < 10:
        filename = "field_0" + str(i) + "_cont_selfcal2.image"
        fitsname = "field_0" + str(i) + "_cont_selfcal2.fits"
    else:
        filename = "field_" + str(i) + "_cont_selfcal2.image"
        fitsname = "field_" + str(i) + "_cont_selfcal2.fits"

    exportfits(imagename = filename, fitsimage = fitsname)
