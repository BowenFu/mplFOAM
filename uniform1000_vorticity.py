import os
import mplFOAM
import style

mf = mplFOAM.mplFOAM(directory='/home/bowen/VIV/Cases/shear1000/uniformRBF')
save_directory = '/home/bowen/VIV/PostProcessing/shear1000/uniform/vorticity'

if not os.path.exists(save_directory):
    os.makedirs(save_directory)

for time in mf.timestep_available[1::4]:
    mf.update_time(time)
    for strip_i in range(0, 20, 4):
        mf.set_slice(
            slice_origin=[0, 0, 0.84 * strip_i + 0.021],
            slice_normal=[0, 0, 1])
        # mf.tricontourf_field('Q', 0)
        mf.tricontour_field(
            field_name='vorticity',
            out_filenames=[
                '{:s}/{:.1f}_{:02d}.png'.
                format(save_directory, time, strip_i)
            ],
            colorbar_range=(-50, 50),
            composition_index=2,
            x_range=(-0.05, 0.8),
            y_range=(-0.15, 0.15),
            contour_num=10,
            figsize=(style.ONE_AND_HALF_COLUMN_WIDTH,
                     style.ONE_AND_HALF_COLUMN_SHORT_HEIGHT / 1.5))
