mplFOAM
=======

Some Python functions to plot OpenFOAM data with Matplotlib using paraview.simple and numpy_support from vtk.util.

At present time it only support:
* surface plot in slice
* plot along line

Usage:

.. code-block:: python

    import mplFOAM
    import matplotlib.pyplot

    m = mplFOAM.mplFOAM(directory='path/to/case/')
    print(m.timestep_available)
    for time in m.timestep_available[::5]:
        m.update_time(time)
        m.extract_plane(slice_origin=[0, 0, 6], slice_normal=[0, 0, 1])
        m.tricontourf_field("U", 0)

