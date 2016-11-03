#!/usr/bin/env python
# encoding: utf-8
# mplFOAM module
# plot OpenFoam data with matplotlib

import os
import numpy
import matplotlib.pyplot
import vtk

try:
    paraview.simple
except:
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
        volume_fields = openfoam_case.VolumeFields.Available
        openfoam_case.VolumeFields = volume_fields

        # Read the specified time steps
        # if times is None:
        # Get the latest timestep if none is specified
        self._timestep_available = openfoam_case.TimestepValues[:]
        #openfoam_case.TimestepValues = openfoam_case.TimestepValues[-1]

        # Print some basic informations on the loaded self.openfoam_case_merged
        if True:
            print "Case directory: ", directory
        #     print "Mesh parts: ", mesh_parts
        #     print "Volume fields: ", volume_fields
        #     print "Timestep values: ", openfoam_case.TimestepValues

        self.openfoam_case_merged = paraview.simple.MergeBlocks(openfoam_case)
        # openfoam_data = servermanager.Fetch(openfoam_case)

    def extractDataInPatch(self):
        "Extract the data from a patch and"

        # Select the active source
        # SetActiveSource(self.openfoam_case_merged)

        # Define the data
        Tetrahedralize1 = Tetrahedralize()
        data = paraview.simple.servermanager.Fetch(Tetrahedralize1)

        # Define the number of points, cells and arrays
        nb_points = self.openfoam_case_merged.GetNumberOfPoints()
        nb_cells = self.openfoam_case_merged.GetNumberOfCells()
        nb_arrays = self.openfoam_case_merged.GetPointData().GetNumberOfArrays()

        # Get Paraview's own triangulation
        #cells = data.GetPolys()
        #triangles = cells.GetData()
        #nb_triangles = triangles.GetNumberOfTuples()/4

        nb_triangles = nb_cells
        tri = numpy.zeros((nb_triangles, 3))

        for i in xrange(0, nb_triangles):
            tri[i, 0] = triangles.GetTuple(4 * i + 1)[0]
            tri[i, 1] = triangles.GetTuple(4 * i + 2)[0]
            tri[i, 2] = triangles.GetTuple(4 * i + 3)[0]

        # Display some informations on the slice
        if True:

            # print 'Patch name :', patchName
            print "Number of cells:", nb_cells
            print "Number of triangles:", nb_triangles
            print "Number of points:", nb_points
            print "Number of arrays:", nb_arrays

            for i in range(nb_arrays):
                print 'Array [', i, '] name:', self.openfoam_case_merged.GetPointData().GetArrayName(i)

        # Put the points coordinates in x, y and z arrays
        x = []
        y = []
        z = []
        # points=zeros((nb_points,3))

        for i in range(nb_points):
            coord = self.openfoam_case_merged.GetPoint(i)
            xx, yy, zz = coord[:3]
            x.append(xx)
            y.append(yy)
            z.append(zz)

            #points[i,0] = xx
            #points[i,1] = yy
            #points[i,2] = zz

        x = numpy.array(x)
        y = numpy.array(y)
        z = numpy.array(z)

        # print 'Points',points

        # Define the velocity components U=(u,v,w)
        U = vtk.util.numpy_support.vtk_to_numpy(
            self.openfoam_case_merged.GetPointData().GetArray('U'))
        u = U[:, 0]
        v = U[:, 1]
        w = U[:, 2]

        # Define the cinematique pressure p => p/\rho
        p = vtk.util.numpy_support.vtk_to_numpy(
            self.openfoam_case_merged.GetPointData().GetArray('p'))

        # Return the values extracted from the slice
        # return x,y,z,u,v,w,p,tri

    def extract_plane(self, slice_origin=[0, 0, 0], slice_normal=[0, 0, 1]):
        """
        Extract Paraview slice object from OpenFOAM self.openfoam_case_merged `self.openfoam_case_merged`

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
        nb_points = self.plane_data.GetNumberOfPoints()
        nb_cells = self.plane_data.GetNumberOfCells()
        nb_arrays = self.plane_data.GetPointData().GetNumberOfArrays()

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

    def extract_plane_triangulation(self, verbose=True):
        """Extract the triangulation of the plane"""

        # Get Paraview's own triangulation
        cells = self.plane_data.GetPolys()
        triangles = cells.GetData()
        nb_triangles = triangles.GetNumberOfTuples() / 4

        tri = numpy.zeros((nb_triangles, 3))

        for i in xrange(0, nb_triangles):
            tri[i, 0] = triangles.GetTuple(4 * i + 1)[0]
            tri[i, 1] = triangles.GetTuple(4 * i + 2)[0]
            tri[i, 2] = triangles.GetTuple(4 * i + 3)[0]

        # Display some informations on the triangulation
        if verbose:
            print "Number of triangles:", nb_triangles

        # Return the triangulation of the plane
        # return tri, triangles

    def extract_plane_points(self, verbose=True):
        """Extract the points of the plane"""

        # Get the number of points
        nb_points = self.plane_data.GetNumberOfPoints()

        # Put the points coordinates in x, y and z arrays
        x = []
        y = []
        z = []

        for i in range(nb_points):
            coord = self.plane_data.GetPoint(i)
            xx, yy, zz = coord[:3]
            x.append(xx)
            y.append(yy)
            z.append(zz)

        x = numpy.array(x)
        y = numpy.array(y)
        z = numpy.array(z)

        # Display some informations on the triangulation points
        if verbose:
            print "Number of points:", nb_points
            print "xrange: [%5.3f, %5.3f]" % (x.min(), x.max())
            print "yrange: [%5.3f, %5.3f]" % (y.min(), y.max())
            print "zrange: [%5.3f, %5.3f]" % (z.min(), z.max())

        # Return the cartesian coordinates of the triangulation points
        # return x,y,z

    def extract_plane_vector_field(self, field_name, verbose=True):
        """Extract the vector field components in the plane"""

        # Define the velocity components U=(u,v,w)
        U = vtk.util.numpy_support.vtk_to_numpy(
            self.plane_data.GetPointData().GetArray(field_name))
        u = U[:, 0]
        v = U[:, 1]
        w = U[:, 2]

        # Return the vector field components
        # return u,v,w

    def extract_plane_scalar_field(self, field_name, verbose=True):
        """Extract the scalar field `field_name` in the plane `self.plane_data`"""

        # Put the scalar field field_name in array scalar
        scalar = self.plane_data.GetPointData().GetArray(field_name)

        # Return the scalar field values extracted from the plane
        # return  scalar

    def tricontourf_field(self, field_name, composition_index=None):
        triangles = self.plane_data.GetPolys().GetData()
        points = self.plane_data.GetPoints()

        # Mapping data: cell -> point
        mapper = vtk.vtkCellDataToPointData()
        mapper.AddInputData(self.plane_data)
        mapper.Update()
        mapped_data = mapper.GetOutput()

        # Extracting interpolate point data
        data_value = mapped_data.GetPointData().GetArray(field_name)
        print(field_name)

        ntri = triangles.GetNumberOfTuples() / 4
        npts = points.GetNumberOfPoints()
        nvls = data_value.GetNumberOfTuples()

        tri = numpy.zeros((ntri, 3))
        x = numpy.zeros(npts)
        y = numpy.zeros(npts)
        return_data = numpy.zeros(nvls)

        for i in xrange(0, ntri):
            tri[i, 0] = triangles.GetTuple(4 * i + 1)[0]
            tri[i, 1] = triangles.GetTuple(4 * i + 2)[0]
            tri[i, 2] = triangles.GetTuple(4 * i + 3)[0]

        for i in xrange(npts):
            pt = points.GetPoint(i)
            x[i] = pt[0]
            y[i] = pt[1]

        for i in xrange(0, nvls):
            result = data_value.GetTuple(i)
            if composition_index is not None:
                result = result[composition_index]
            return_data[i] = result
        print(max(return_data))

        matplotlib.pyplot.tricontour(x, y, tri, return_data, 6)
    #    matplotlib.pyplot.tricontourf(x, y, tri, return_data, 16)
        matplotlib.pyplot.grid()
        matplotlib.pyplot.show()

    @property
    def timestep_available(self):
        return self._timestep_available

    def update_time(self, time):
        assert time in self.timestep_available
        paraview.simple.UpdatePipeline(time=time)
