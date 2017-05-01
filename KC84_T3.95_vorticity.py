import mplFOAM
import style
from matplotlib import rcParams
rcParams['savefig.dpi'] = 100


mf = mplFOAM.mplFOAM(directory='/home/bowen/VIV/Cases/fushixiao/KC84_T3.95')
for time in mf.timestep_available[1:]:
    if time < 30:
        continue
    print(time)
    mf.update_time(time)
    #for strip_i in range(2, 20, 4):
    for strip_i in [10]:
        mf.set_slice(
            slice_origin=[0, 0, 1 * strip_i + 0.005],
            slice_normal=[0, 0, 1])
        # mf.tricontourf_field('Q', 0)
        mf.tricontourf_field(
            field_name='vorticity',
            out_filenames=[
                '/home/bowen/VIV/PostProcessing/fushixiao/KC84_T3.95/vorticity/{:02d}_{:.2f}.png'.
                format(strip_i, time)
            ],
            colorbar_range=(-40, 40),
            composition_index=2,
            x_range=(-0.15, 0.15),
            y_range=(-0.6, 0.6),
            contour_num=10,
            figsize=(style.ONE_AND_HALF_COLUMN_WIDTH,
                     style.ONE_AND_HALF_COLUMN_LONG_HEIGHT * 1.5))
