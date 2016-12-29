#!/usr/bin/env python
# encoding: utf-8
# mplFOAM module
# plot OpenFoam data with matplotlib

import style

import os
import numpy
import matplotlib.pyplot
import vtk

import paraview.simple
paraview.simple._DisableFirstRenderCameraReset()

import vtk.util.numpy_support


class mplFOAM:
    def __init__(self, directory=None):
        """
        Read the OpenFOAM self.openfoam_case_merged

        Parameters
        ----------
        directory : str, optional
        Directory path of the OpenFOAM self.openfoam_case_merged

        openfoam_case_merged : paraview object
        """

        # Create the OpenFOAM file self.openfoam_case_merged
        if directory is None:
            directory = os.getcwd().split('/')[-1]
        if directory[-1] != '/':
            directory += '/'
        filename = directory.split('/')[-1]

        filename = directory + '.OpenFOAM'
        case_file = open(filename, 'w')
        case_file.close()

        # Define the OpenFOAM data source
        openfoam_case = paraview.simple.OpenDataFile(filename)

        # Import all the mesh parts if none are specified
        mesh_parts = openfoam_case.MeshParts.Available
        openfoam_case.MeshParts = mesh_parts

        # Import all the volume fields if none are specified
        self._field_available = openfoam_case.VolumeFields.Available
        openfoam_case.VolumeFields = self._field_available

        # Get the latest timestep if none is specified
        self._timestep_available = openfoam_case.TimestepValues[:]

        self.openfoam_case_merged = paraview.simple.MergeBlocks(openfoam_case)

    def set_slice(self, slice_origin=[0, 0, 0], slice_normal=[0, 0, 1]):
        """
        Extract Paraview slice object from OpenFOAM
        self.openfoam_case_merged `self.openfoam_case_merged`

        Parameters
        ----------
        self.openfoam_case_merged : Paraview object
        OpenFOAM self.openfoam_case_merged

        slice_origin : list of float
        Slice point origin [x, y, z] in cartesian coordinates

        slice_normal : list of float
        Slice point normal [nx, ny, nz] in cartesian coordinates

        Return
        ------
        self.plane_data: paraview slice object

        """
        # Select the active source
        paraview.simple.SetActiveSource(self.openfoam_case_merged)

        # Define the plane
        Slice1 = paraview.simple.Slice(SliceType="Plane")
        Slice1.SliceType = 'Plane'
        Slice1.SliceType.Origin = slice_origin
        Slice1.SliceType.Normal = slice_normal
        # Slice1.UpdatePipeline()

        self.plane_data = paraview.simple.servermanager.Fetch(Slice1)

        # Define the number of points, cells and arrays
        # nb_points = self.plane_data.GetNumberOfPoints()
        # nb_cells = self.plane_data.GetNumberOfCells()
        # nb_arrays = self.plane_data.GetPointData().GetNumberOfArrays()

        # Display some informations on the slice
        # if verbose:
        #    print 'Slice origin:', slice_origin
        #    print 'Slice normal:', slice_normal
        #    print "Number of cells:", nb_cells
        #    print "Number of points:", nb_points
        #    print "Number of arrays:", nb_arrays

        #    for i in range(nb_arrays):
        # print 'Array [',i,'] name:',
        # self.plane_data.GetPointData().GetArrayName(i)

    def tricontourf_field(self,
                          field_name,
                          out_filenames,
                          composition_index=None,
                          x_range=None,
                          y_range=None,
                          colorbar=False,
                          colorbar_range=None,
                          contour_num=10,
                          contourf_num=20,
                          figsize=(style.ONE_AND_HALF_COLUMN_WIDTH,
                                   style.ONE_AND_HALF_COLUMN_SHORT_HEIGHT)):
        assert field_name in self.field_available
        triangles = self.plane_data.GetPolys().GetData()
        points = self.plane_data.GetPoints()

        # Mapping data: cell -> point
        mapper = vtk.vtkCellDataToPointData()
        mapper.AddInputData(self.plane_data)
        mapper.Update()
        mapped_data = mapper.GetOutput()

        # Extracting interpolate point data
        data_value = mapped_data.GetPointData().GetArray(field_name)

        ntri = triangles.GetNumberOfTuples() / 4
        npts = points.GetNumberOfPoints()
        nvls = data_value.GetNumberOfTuples()

        tri = numpy.zeros((ntri, 3))
        x = numpy.zeros(npts)
        y = numpy.zeros(npts)
        results = numpy.zeros(nvls)

        for i in range(0, ntri):
            tri[i, 0] = triangles.GetTuple(4 * i + 1)[0]
            tri[i, 1] = triangles.GetTuple(4 * i + 2)[0]
            tri[i, 2] = triangles.GetTuple(4 * i + 3)[0]

        for i in range(npts):
            pt = points.GetPoint(i)
            x[i] = pt[0]
            y[i] = pt[1]

        for i in range(0, nvls):
            result = data_value.GetTuple(i)
            if composition_index is not None:
                result = result[composition_index]
            results[i] = result

        matplotlib.pyplot.clf()
        matplotlib.pyplot.gcf().set_size_inches(figsize)
        matplotlib.pyplot.axis('off')
        matplotlib.pyplot.axes().set_aspect('equal', 'datalim')
        if x_range:
            matplotlib.pyplot.xlim(x_range)
        if y_range:
            matplotlib.pyplot.ylim(y_range)

        #matplotlib.pyplot.triplot(x,y)
        #matplotlib.pyplot.show()


        if colorbar_range:
            contour_range = numpy.linspace(colorbar_range[0],
                                           colorbar_range[1], contour_num)
            contourf_range = numpy.linspace(colorbar_range[0],
                                            colorbar_range[1], contour_num)
            results[results > colorbar_range[1]] = colorbar_range[1]
            results[results < colorbar_range[0]] = colorbar_range[0]

            matplotlib.pyplot.tricontour(
                x, y, tri, results, contour_range, colors='0.2')
        else:
            matplotlib.pyplot.tricontour(x, y, tri, results, colors='0.2')

        if colorbar:
            matplotlib.pyplot.colorbar().ax.set_title(colorbar_zlabel)

        # matplotlib.pyplot.tricontourf(x, y, tri, results, contourf_range)
        matplotlib.pyplot.tight_layout()
        for out_filename in out_filenames:
            matplotlib.pyplot.savefig(out_filename)
    @property
    def field_available(self):
        return self._field_available

    @property
    def timestep_available(self):
        return self._timestep_available

    def update_time(self, time):
        assert time in self.timestep_available
        paraview.simple.UpdatePipeline(time=time)
