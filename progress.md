# Updates
* Fixed issue 1 by working on each image one at a time and resizing using `PIL.Image.NEAREST` filter. Check out this [link](https://github.com/kylerlittle/mk-topo-map/issues/1) for more details.
* Fixed issue 2 by making it so maximum number of iterations may elapse before a pixel cluster is "off limits." Check out this [link](https://github.com/kylerlittle/mk-topo-map/issues/2) for more details.
* Also, GREAT NEWS finally! Achieved my [first promising result](https://github.com/kylerlittle/mk-topo-map/tree/master/topo-maps). Compare *best_fig_1.png* to *best_fig_1_actual.jpg* and compare *best_fig_2.png* to *best_fig_2_actual.jpg* and you should find a lot of similarities. My program remarkably catchs some subtleties in the conformational changes of the fiber I didn't notice upon first glance. The figures are still quity noisy, but I think I'll be able to smooth them.
* Secondly, it appears that the models are converging to the object's shape in the variation of parameters (as it theoretically should). I still need to alter more parameters and attempt to smooth the figures, but I'm making excellent progress.
* One really awesome thing I just noticed is that the xy dimensions in *best_fig_3.png* are legitimately accurate. When the model converges to the object in the z direction, it also converges in the xy direction. This is so cool.
* Here's an interesting thing to remember for matplotlib
  * So I tried this thing where I edited matplotlib's graph files so that it autoscales my graph to a rectangular plot if the matrix is rectangular. Check out this [link](https://stackoverflow.com/questions/10326371/setting-aspect-ratio-of-3d-plot) for more information. FYI, on my computer, `get_proj` function is inside `/usr/lib/python2.7/dist-packages/mpl_toolkits/mplot3d/axes3d.py`. This actually worked like a charm; however, I changed it back for my latest run.
* I finally varied PIL's resizing filters since these seem to have a large impact on the outcome of this program...
   * The amazing thing is that the results were almost identical between resizing filters, when the other parameters were kept constant. This is a great thing. I was actually hoping that the resizing filters DIDN'T have a large impact on the outcome of the program. If they did, then that would mean my data was being somewhat arbitrarily manipulated by unrelated human-imposed edits, and that would mean the output of the program wouldn't entirely be caused by the true physics of the situation. Now that I know this is NOT the case, that's actually incredible news. That means this idea was worth it after all. Even though this is another failed attempt at smoothing the figures, it just means I need better data. That can be accomplished by getting a camera that (1) isn't a piece of shit with a wide ass fish-eye lens and (2) pauses for long enough during its translation to remove unnecessary blurring.

# Next Up
1. Finish graph function. Accept parameters: tuple: (len, width), so that xy dimensions are actually real and accurate. Also, instead of displaying the graph, save it as a figure in the appropriate directory.
1. Clean up error handling in `cropPhotos`, `resizePhotos`, `createLaplacianStack`, and `crop_resize_lpc`.
1. Clean up easy if/else statements (specifically with testMode) with ternary operator. Looks like:
   ``` python
   a if condition else b
   ```
1. Modularize code in `crop_resize_lpc`. This function is way too damn messy.

# Eventually
1. Create virtualenv so that others in the research group can easily use this software, or make shell scripts so necessary software is installed on the user's computer.
1. Get better images for the `raw-images-test/` directory to make it easier for the user to understand the program's behavior.
1. Make `VoL` (variance of laplacian method) in C/C++. This phase in the program is the bottleneck; it needs to be sped up. The method is composed of basic matrix convulation and variance calculations. There are plenty of C++ libraries that can do this. For instance, consider CUTLASS.
1. Make as user-friendly as possible.
1. Update README.txt with explicit instructions.

*Last Updated: 2/06/2018 20:19 PST*
