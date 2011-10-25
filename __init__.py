import sys
import os

DECKARD_ROOT = os.path.dirname(__file__)

# we need to include wire_swig which lies under our directory
sys.path.insert(0, DECKARD_ROOT)
sys.path.insert(0, DECKARD_ROOT + '/wire_swig')

print sys.path

__all__ = ["manager", "search", "index"]