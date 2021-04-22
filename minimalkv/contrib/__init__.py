import re
from typing import Optional

from minimalkv import VALID_NON_NUM

VALID_NON_NUM_EXTENDED = VALID_NON_NUM + r"/ "
VALID_KEY_REGEXP_EXTENDED = "^[%s0-9a-zA-Z]+$" % re.escape(VALID_NON_NUM_EXTENDED)
"""This regular expression tests if a key is valid when the extended keyspace mixin is used.
Allowed are all alphanumeric characters, as well as ``!"`#$%&'()+,-.<=>?@[]^_{}~/``. and spaces"""
VALID_KEY_RE_EXTENDED = re.compile(VALID_KEY_REGEXP_EXTENDED)
"""A compiled version of :data:`~minimalkv.VALID_KEY_REGEXP_EXTENDED`."""


class ExtendedKeyspaceMixin:
    """A mixin to extend the keyspace to allow slashes and spaces in keynames.

    Attention: A single / is NOT allowed.
    Use it by extending first from ` :class:`~minimalkv.ExtendedKeyspaceMixin`
    and then by the desired store.
    Note: This Mixin is unsupported and might not work correctly with all backends.
    """

    def _check_valid_key(self, key: Optional[str]):
        """Checks if a key is valid and raises a ValueError if its not.

        When in need of checking a key for validity, always use this
        method if possible.

        :param key: The key to be checked
        """
        if key is not None:
            if not isinstance(key, str):
                raise ValueError("%r is not a valid key type" % key)
            elif not VALID_KEY_RE_EXTENDED.match(key) or key == "/":
                raise ValueError("%r contains illegal characters" % key)
