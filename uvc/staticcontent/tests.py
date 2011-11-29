import os.path
import z3c.testsetup
import uvc.staticcontent
from zope.app.testing.functional import ZCMLLayer

from uvcsite.tests import product_config

ftesting_zcml = os.path.join(
    os.path.dirname(uvc.staticcontent.__file__), 'ftesting.zcml')
FunctionalLayer = ZCMLLayer(ftesting_zcml, __name__, 'FunctionalLayer',
                            allow_teardown=True, product_config = product_config)

test_suite = z3c.testsetup.register_all_tests('uvc.staticcontent', layer=FunctionalLayer)

