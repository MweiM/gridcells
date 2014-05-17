from __future__ import absolute_import, division, print_function

import pytest
import numpy as np
from gridcells.core import Position2D
from gridcells.core import CircularArena, Pair2D
from gridcells.analysis import spatialRateMap
import fields_ref_impl as refimp


@pytest.fixture(scope='module')
def reference_data():
    class InputData(object):
        def __init__(self, spikeTimes, pos_x, pos_y, pos_dt, arena_diam, h):
            self.spikeTimes = spikeTimes
            self.pos_x = pos_x
            self.pos_y = pos_y
            self.pos_dt = pos_dt
            self.arena_diam = arena_diam
            self.h = h
    data_dir = "tests/data"
    arena_diam = 180.0
    ref_data = InputData(
        spikeTimes = np.loadtxt("%s/spikeTimes.txt" % data_dir),
        pos_x      = np.loadtxt("%s/pos_x.txt" % data_dir) + arena_diam/2.,
        pos_y      = np.loadtxt("%s/pos_y.txt" % data_dir) + arena_diam/2.,
        pos_dt     = 20,
        arena_diam = arena_diam,
        h          = 3)
    return ref_data


@pytest.fixture(scope='module')
def reference_spatial_map(reference_data):
    d = reference_data
    ref_rate_map, ref_xedges, ref_yedges = refimp.SNSpatialRate2D(
            d.spikeTimes,
            d.pos_x, d.pos_y, d.pos_dt,
            d.arena_diam,
            d.h)
    return d, ref_rate_map, ref_xedges, ref_yedges


class TestSpatialRateMap(object):
    '''Test the correctness of firing field analysis.'''
    rtol = 1e-3
    arenaR = 90. # cm
    sigma  = 3.  # cm

    def test_NaiveVersion(self, reference_spatial_map):
        d, ref_rate_map, ref_xedges, ref_yedges = reference_spatial_map

        # Tested code
        ar = CircularArena(self.arenaR, Pair2D(self.sigma, self.sigma))
        pos = Position2D(d.pos_x, d.pos_y, d.pos_dt)
        theirRateMap = spatialRateMap(d.spikeTimes, pos, ar, self.sigma)
        theirEdges = ar.getDiscretisation()
        #print(np.max(np.abs(theirRateMap - ref_rate_map)))
        np.testing.assert_allclose(theirRateMap, ref_rate_map, self.rtol)
        np.testing.assert_allclose(theirEdges.x, ref_xedges, self.rtol)
        np.testing.assert_allclose(theirEdges.y, ref_yedges, self.rtol)

