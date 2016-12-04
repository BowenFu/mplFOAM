import mplFOAM
import style


mf = mplFOAM.mplFOAM(
        directory='/home/bowen/VIV/Cases/shear1000/uniformRBF')
for time in mf.timestep_available[1::2]:
    mf.update_time(time)
    for strip_i in range(0, 20, 2):
        mf.set_slice(
                slice_origin=[0, 0, 0.84*strip_i+0.021], slice_normal=[0, 0, 1])
        # mf.tricontourf_field('Q', 0)
        mf.tricontourf_field(
                field_name='vorticity', 
                out_filenames=['/home/bowen/VIV/PostProcessing/shear1000/uniform/vorticity/{:.1f}_{:02d}.png'.format(time, strip_i)],
                colorbar_range=(-50, 50),
                composition_index=2,
                x_range=(-0.05, 0.8),
                y_range=(-0.15,0.15),
                contour_num=10,
                figsize=(style.SINGLE_COLUMN_WIDTH,
                    style.SINGLE_COLUMN_SHORT_HEIGHT/1.5)
                )
