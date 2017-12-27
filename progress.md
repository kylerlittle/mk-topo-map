# Updates
* Fixed issue 1 by working on each image one at a time and resizing using `PIL.Image.NEAREST` filter. Check out this [link](https://github.com/kylerlittle/mk-topo-map/issues/1) for more details.
* At this point, I'm just trying to vary parameters to create the best model. I have an idea of how I'm going to 'smooth' the figures.
* I hope that the models will converge to the object's shape at some point in the variation of parameters (as it theoretically should). If so, my research will be complete.

# Next Up
1. Vary PIL's resizing filters since these clearly have a large impact on the outcome of this program.
1. Run more `vary` tests.
1. Finish graph function. Accept parameters: tuple: (len, width), so that xy dimensions are actually real and accurate. Also, instead of displaying the graph, save it as a figure in the appropriate directory.
1. Clean up error handling in `cropPhotos`, `resizePhotos`, `createLaplacianStack`, and `crop_resize_lpc`.
1. Clean up easy if/else statements (specifically with testMode) with ternary operator. Looks like:
   ``` python
   a if b else c
   ```
1. Modularize code in `crop_resize_lpc`. This function is way too damn messy.

# Eventually
1. Create virtualenv so that others in the research group can easily use this software, or make shell scripts so necessary software is installed on the user's computer.
1. Get better images for the `raw-images-test/` directory to make it easier for the user to understand the program's behavior.
1. Make as user-friendly as possible.
1. Update README.txt with explicit instructions.

*Last Updated: 12/26/2017 17:15 PST*
