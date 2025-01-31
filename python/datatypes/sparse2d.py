from .database import recoBase
from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph, numpy
from .connectedObjects import connectedBox, boxCollection
from matplotlib  import cm, colors

from larcv import larcv

class sparse2d(recoBase):

    """docstring for sparse2d"""

    def __init__(self):
        super(sparse2d, self).__init__()
        self._product_name = 'sparse2d'

        self._listOfClusters = []

        # Defining the sparse2d colors:
        self._clusterColors = [
            (0, 147, 147, 125),  # dark teal
            (0, 0, 252, 125),   # bright blue
            (156, 0, 156, 125),  # purple
            (255, 0, 255, 125),  # pink
            (255, 0, 0, 125),  # red
            (175, 0, 0, 125),  # red/brown
            (252, 127, 0, 125),  # orange
            (102, 51, 0, 125),  # brown
            (127, 127, 127, 125),  # dark gray
            (210, 210, 210, 125),  # gray
            (100, 253, 0, 125)  # bright green
        ]

    # this is the function that actually draws the cluster.
    def drawObjects(self, view_manager, io_manager, meta):

        #Get the list of sparse2d sets:
        sparse_2d_set = io_manager.get_data(self._product_name, str(self._producerName))
        sparse_2d_set = larcv.EventSparseTensor2D.to_sparse_tensor(sparse_2d_set)
        # if self._producerName in io_manager.producer_list(self._product_name):
        #     hasROI = True
        # else:
        #     hasROI = False

        # if hasROI:
        #     event_roi = io_manager.get_data(self._product_name, str(self._producerName))

        for plane, view in view_manager.getViewPorts().items():
            self._drawnObjects.append([])

            colorIndex = 0

            active_map = view._activeMap
            cols = []
            vals = []
            for val, rgba in active_map['ticks']:
                cols.append(numpy.asarray(rgba) / 255.)
                vals.append(val)

            cmap = pyqtgraph.ColorMap(vals, cols)

            # n = len(uids); 
            # colors = cmap(range(n), bytes = True);


            # Get the sparse2d clusters for this plane:
            # try:
            voxelset = sparse_2d_set.sparse_tensor(plane)
            meta = voxelset.meta()

            indexes = numpy.copy(larcv.as_ndarray_sizet(voxelset.indexes()))
            values  = numpy.copy(larcv.as_ndarray_float(voxelset.values()))

            # Reject all out-of-bounds indexes:
            in_bounds = indexes < meta.total_voxels()
            oob = indexes >= meta.total_voxels()
            indexes = indexes[in_bounds]
            values  = values[in_bounds]

            dims = [meta.number_of_voxels(0), meta.number_of_voxels(1) ]

            y, x = numpy.unravel_index(indexes, dims)

            y = y.astype(float) + 0.5
            x = x.astype(float) + 0.5

            # colors = cmap.map(values, mode='float')



            this_item = pyqtgraph.ScatterPlotItem()

            this_item.setData(x, y, size=1, pxMode=False, symbol='s', pen=None)

            view._plot.addItem(this_item)
            self._drawnObjects[plane].append(this_item)

