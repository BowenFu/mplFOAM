'''
Designed to control all figure styles.
Author: Bowen Fu
Date: 2016/10/20
'''

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot
import matplotlib.ticker
from matplotlib.pyplot import rcParams
from cycler import cycler

NO_POWER_FORM = matplotlib.ticker.ScalarFormatter(
    useMathText=False, useOffset=False)
NO_POWER_FORM.set_scientific(False)

SHORT_XTICK_MAX_LENGTH = 3
SHORT_YTICK_MAX_LENGTH = 3

LONG_XTICK_MAX_LENGTH = 6
LONG_YTICK_MAX_LENGTH = 6

LEFT_CORNER = 0.03
TOP_CORNER = 0.91

GOLDEN_RATIO = 1.618

MINIMAL_WIDTH = 1.18
MINIMAL_SHORT_HEIGHT = MINIMAL_WIDTH / GOLDEN_RATIO
MINIMAL_LONG_HEIGHT = MINIMAL_WIDTH * GOLDEN_RATIO

SINGLE_COLUMN_WIDTH = 3.54
SINGLE_COLUMN_SHORT_HEIGHT = SINGLE_COLUMN_WIDTH / GOLDEN_RATIO
SINGLE_COLUMN_LONG_HEIGHT = SINGLE_COLUMN_WIDTH * GOLDEN_RATIO

ONE_AND_HALF_COLUMN_WIDTH = 5.51
ONE_AND_HALF_COLUMN_SHORT_HEIGHT = ONE_AND_HALF_COLUMN_WIDTH / GOLDEN_RATIO
ONE_AND_HALF_COLUMN_LONG_HEIGHT = ONE_AND_HALF_COLUMN_WIDTH * GOLDEN_RATIO

FULL_WIDTH = 7.48
FULL_SHORT_HEIGHT = FULL_WIDTH / GOLDEN_RATIO
FULL_LONG_HEIGHT = FULL_WIDTH * GOLDEN_RATIO

DARKEST_COLOR = '0.1'
DARK_COLOR = '0.2'
REFERENCE_LIGHT_COLOR = '0.4'
# for contour
LIGHT_COLOR = '0.8'

CMAP_SINGLE = matplotlib.pyplot.get_cmap('Blues')
CMAP_DOUBLE = CMAP2 = matplotlib.pyplot.get_cmap('RdBu')
# CMAP_DOUBLE = CMAP2 = matplotlib.pyplot.get_cmap('RdBu_r')

SINGLE_LINE_STYLE = dict(color=DARK_COLOR, linewidth=1,
                         marker='', linestyle='solid')
REFERENCE_LINE_STYLE = dict(
    color=REFERENCE_LIGHT_COLOR,
    alpha=0.3,
    linewidth=1,
    marker='',
    linestyle='solid')
LIGHT_LINE_STYLE = dict(color=LIGHT_COLOR, linewidth=1,
                        alpha=0.3, marker='', linestyle='solid')

MARKER_STYLES = [
    dict(markeredgecolor='0.1', linestyle='-', color='0.5',
         markersize=4, markevery=1, marker=r'$\boxdot$'),
    dict(markeredgecolor='0.1', linestyle='-', color='0.5',
         markersize=4, markevery=1, marker=r'$\odot$'),
    dict(markeredgecolor='0.1', linestyle='-', color='0.5',
         markersize=4, markevery=1, marker=r'$\bigtriangleup$'),
    dict(markeredgecolor='0.1', linestyle='-', color='0.5',
         markersize=4, markevery=1, marker=r'$\bigtriangledown$'),
    dict(markeredgecolor='0.1', linestyle='-', color='0.5',
         markersize=4, markevery=1, marker=r'$\diamondsuit$'),
    dict(markeredgecolor='0.1', linestyle='-', color='0.5',
         markersize=4, markevery=1, marker=r'$\heartsuit$'),
    dict(markeredgecolor='0.1', linestyle='-', color='0.5',
         markersize=4, markevery=1, marker=r'$\boxtimes$')
]

rcParams['axes.prop_cycle'] =\
    cycler(marker=['', r'$\odot$', r'$\boxdot$']) *\
    cycler(color=[DARKEST_COLOR, REFERENCE_LIGHT_COLOR]) *\
    cycler(linestyle=['-', '--']) *\
    cycler(markevery=[8]) *\
    cycler(markersize=[2.0])  # *cycler(markeredgecolor='k')

rcParams['lines.color'] = DARK_COLOR

rcParams['figure.figsize'] = SINGLE_COLUMN_WIDTH, SINGLE_COLUMN_SHORT_HEIGHT
rcParams['savefig.dpi'] = 600
rcParams['savefig.bbox'] = 'tight'
rcParams['legend.numpoints'] = 1

rcParams['legend.loc'] = 'best'
rcParams['legend.fontsize'] = 'medium'
rcParams['legend.handletextpad'] = 0.4

rcParams['markers.fillstyle'] = 'none'

rcParams['axes.formatter.limits'] = [-2, 3]
rcParams['axes.formatter.use_mathtext'] = True
rcParams['axes.formatter.useoffset'] = False
rcParams['axes.labelsize'] = 'medium'
rcParams['axes.titlesize'] = 'medium'
rcParams['grid.alpha'] = 0.8

rcParams.update({'font.size': 8})
rcParams.update({'font.family': 'serif'})
