import mplFOAM
import style
from matplotlib import rcParams
rcParams['savefig.dpi'] = 100


mf = mplFOAM.mplFOAM(directory='/home/bowen/VIV/Cases/fushixiaoSway/KC168_T7.5_long_2dof')
for time in mf.timestep_available[1:]:
    if time < 14.0625 or time < 12.1875:
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
            # field_name='vorticity',
            field_name='vorticity',
            out_filenames=[
                '/home/bowen/VIV/PostProcessing/fushixiaoSway/KC168_T7.5_long_2dof/vorticity/{:02d}_{:.2f}.png'.
                format(strip_i, time)
            ],
            colorbar_range=(-50, 50),
            composition_index=2,
            x_range=(-0.09, 0.09),
            y_range=(-0.36, 0.36),
            contourf_num=20,
            figsize=(style.ONE_AND_HALF_COLUMN_WIDTH,
                     style.ONE_AND_HALF_COLUMN_LONG_HEIGHT * 1.5))
        mf.tricontour_field(
            # field_name='vorticity',
            field_name='vorticity',
            out_filenames=[
                '/home/bowen/VIV/PostProcessing/fushixiaoSway/KC168_T7.5_fine/vorticity_gray/{:02d}_{:.2f}.png'.
                format(strip_i, time)
            ],
            colorbar_range=(-50, 50),
            composition_index=2,
            x_range=(-0.09, 0.09),
            y_range=(-0.35, 0.35),
            contour_num=16,
            figsize=(style.SINGLE_COLUMN_WIDTH,
                     style.SINGLE_COLUMN_WIDTH * 4))
