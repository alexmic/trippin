"""
Various utility and helper methods.
"""
import imp

def load_object(dotted_name, parent=None):
    """ Loads an object or module from a dotted path. """
    parts = dotted_name.split(".")
    path = parent.__path__ if parent and hasattr(parent, "__path__") else None
    try:
        c = imp.load_module(parts[0], *imp.find_module(parts[0], path))
        return c if len(parts) == 1 else load_object(".".join(parts[1:]), c) 
    except ImportError as e:
        return getattr(parent, parts[0])