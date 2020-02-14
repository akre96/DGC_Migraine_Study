""" Group of functions that make plots prettier

"""
import matplotlib.pyplot as plt
import seaborn as sns

def despine_thicken_axes(
    ax,
    lw: float = 4,
    fontsize: float = 30,
    rotate_x: float = 0,
    rotate_y: float = 0,
  ):
  """ Despine axes, rotate x or y, thicken axes

  Arguments:
      ax -- matplotlib axis to modify

  Keyword Arguments:
      lw {float} -- line width for axes (default: {4})
      fontsize {float} --  fontsize for axes labels/ticks (default: {30})
      rotate_x {float} -- rotation in degrees for x-axis ticks (default: {0})
      rotate_y {float} -- rotation in degrees for y-axis ticks (default: {0})

  Returns:
      ax -- modified input axis
  """
  ax.xaxis.set_tick_params(width=lw, length=lw*2)
  ax.yaxis.set_tick_params(width=lw, length=lw*2)
  for axis in ['top','bottom','left','right']:
    ax.spines[axis].set_linewidth(4)
  ax.tick_params(axis='both', which='major', labelsize=fontsize)
  ax.tick_params(axis='both', which='minor', labelsize=fontsize*.8)
  ax.set_ylabel(ax.get_ylabel(), fontsize=fontsize)
  ax.set_xlabel(ax.get_xlabel(), fontsize=fontsize)
  sns.despine()
  ax.tick_params(axis='x', rotation=rotate_x)
  ax.tick_params(axis='y', rotation=rotate_y)
  return ax
