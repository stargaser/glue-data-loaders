# Herschel FITS files

`herschel_data` is a custom data loader for PACS spectroscopy FITS cubes
from the Herschel Space Observatory. It scans FITS files for
extensions named 'image', and constructs a Glue data object from each.

The loader uses the astropy.io.fits library for
parsing the WCS metadata.


