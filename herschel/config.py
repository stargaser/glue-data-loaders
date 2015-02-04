from glue.core import Data
from glue.core.coordinates import coordinates_from_wcs
from glue.config import data_factory
from glue.core.data_factories import has_extension

import astropy.io.fits as fits
from astropy.wcs import WCS
import numpy as np


@data_factory('Herschel Image', has_extension('fits fit fits.gz'), default='fits fit fits.gz')
def herschel_data(filename):
    """
    Data loader customized for Herschel fits files

    This function extracts extension named 'image',
    'error', 'coverage', etc
    from a file. Each is retuned as a glue Data object.
    To handle PACS cubes, if ImageIndex extension is present
    it is used to provide wavelengths

    astropy.wcs.WCS objects are used to parse wcs.

    Any other extensions are ignored
    """


    hdulist = fits.open(filename, memmap=True)

    d = Data("data")
    # Fix for invalid CUNIT values in 12.1 PACS data
    for c in ['CUNIT1', 'CUNIT2']:
        if hdulist['image'].header[c]:
            del hdulist['image'].header[c]
    d.coords = coordinates_from_wcs(WCS(hdulist['image'].header))
    wavelengths = None
    for h in hdulist:
        if (h.name in ['image', 'error', 'cov']):
            d.add_component(hdulist[h.name].data, h.name)
        if (h.name == 'ImageIndex'):
            wavelengths = hdulist[h.name].data.field(0)
            
    # Fix up wavelengths if needed
    if ((wavelengths != None) and (d['Wavelength'].shape[0] == len(wavelengths))):
        warray = np.zeros(d['Wavelength'].shape, dtype=d['Wavelength'].dtype)
        warray += wavelengths[:, np.newaxis, np.newaxis]
        d.remove_component('Wavelength')
        d.add_component(warray, label='Wavelength')

    return d
