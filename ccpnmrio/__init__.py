__doc__ = """
ccpnmrio
========

*Reading and writing information from ccpnmr analysis.*

I wanted a package that automated the hacking I found myself doing every time
I needed to look at peak list data exported from ccpnmr's analysis software in
something like a Jupyter notebook. This is that package. It probably stinks but
hopefully it will get better.
"""

# Register PhyloPandas Methods
from .peakio import read_ccp
