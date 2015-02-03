from glue.core import Data
from glue.core.coordinates import coordinates_from_wcs
from glue.config import data_factory
from glue.core.data_factories import has_extension

import astropy.io.fits as fits
from astropy.wcs import WCS


@data_factory('Hubble Image', has_extension('fits fit fits.gz'), default='fits fit fits.gz')
def herschel_data(filename):
    """
    Data loader customized for 'typical' hubble fits files

    This function extracts extensions named 'image'
    from a file. Each is retuned as a glue Data object

    astropy.wcs.WCS objects are used to parse wcs.

    Any other extensions are ignored
    """

    result = []

    hdulist = fits.open(filename, memmap=True)

    index = 1

    def _get_image_ext(i, index):
        d = Data("image_%i" % (index))
        d.coords = coordinates_from_wcs(WCS(hdulist[i].header))

        index = index + 1
        d.add_component(hdulist[i].data, hdulist[i].name)
        return d

    for i, h in enumerate(hdulist):
        if h.name != 'image':
            continue
        result.append(_get_image_ext(i, index))
        index += 1

    return result
