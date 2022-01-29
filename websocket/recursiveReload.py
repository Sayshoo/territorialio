from types import ModuleType

try:
    from importlib import reload  # Python 3.4+
except ImportError:
    # Needed for Python 3.0-3.3; harmless in Python 2.7 where imp.reload is just an
    # alias for the builtin reload.
    from imp import reload

def rreload(module):
    """Recursively reload modules."""
    reload(module)
    for attribute_name in dir(module):
        attribute = getattr(module, attribute_name)
        if type(attribute) is ModuleType:
            rreload(attribute)