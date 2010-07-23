import sys
sys.path.remove('/usr/local/Cellar/python/2.6.5/lib/python2.6/site-packages/OWSLib-0.3.1-py2.6.egg')
sys.path.insert(0,'./OWSLib')

from owslib.wfs import WebFeatureService
from owslib.wcs import WebCoverageService
import geojson

def get_features(wfs_url, layer, verbose=False):
    """Get feature from Web Feature Service (WFS) in GeoJSON format
    
    Input:
       wfs_url: URL for web feature service. E.g. http://www.aifdr.org:8080/geoserver/ows?
       layer: Feature layer name as <workspace>:<layer>
       verbose [optional]: Flag controlling the verbosity level. Default is False.
       
    Output:
       GEOJSON dictionary or None.
    """
    
    if verbose:
        print('Retrieving %s from %s' % (layer, wfs_url))
        
    wfs = WebFeatureService(wfs_url, version='1.0.0')
    
    if layer not in wfs.contents.keys():
        return None
    response = wfs.getfeature(typename=[layer], outputFormat='json', maxfeatures=1)
    return geojson.loads(response.read())

def get_coverage(wcs_url, layer, verbose=False):
    """Get coverage from Web Coverage Service (WCS) in GeoTIFF format
    
    Input:
       wcs_url: URL for web ceature service. E.g. http://www.aifdr.org:8080/geoserver/ows?
       layer: Coverage layer name as <workspace>:<layer>
       verbose [optional]: Flag controlling the verbosity level. Default is False.
       
    Output:
       GeoTIFF data or None.    
    """
        
    if verbose:
        print('Retrieving %s from %s' % (layer, wcs_url))
            
    # wcs = WebCoverageService(wcs_url, version='1.1.1')
    wcs = WebCoverageService(wcs_url, version='1.0.0')
    interrogate(wcs)
    if layer not in wcs.contents.keys():
        return None

    response = wcs.getCoverage(typename=[layer], format='GeoTIFF')
    return response

def interrogate(item):
    """Print useful information about item."""
    if hasattr(item, '__name__'):
        print "NAME:    ", item.__name__
    if hasattr(item, '__class__'):
        print "CLASS:   ", item.__class__.__name__
    print "ID:      ", id(item)
    print "TYPE:    ", type(item)
    print "VALUE:   ", repr(item)
    print "CALLABLE:",
    if callable(item):
        print "Yes"
    else:
        print "No"
    if hasattr(item, '__doc__'):
        doc = getattr(item, '__doc__')
    doc = doc.strip()   # Remove leading/trailing whitespace.
    firstline = doc.split('\n')[0]
    print "DOC:     ", firstline
