# Updates
* Fixed issue 1 by working on each image one at a time and resizing using `PIL.Image.NEAREST` filter. Check out this [link](https://github.com/kylerlittle/mk-topo-map/issues/1) for more details.
* Now, the program runs as it should! I obtained my first actual results-- this [crappy little figure](https://github.com/kylerlittle/mk-topo-map/blob/master/topo-maps/test-1.png). Believe it or not-- it actually gives a decent ballpark estimate of the topographical map of the photomechanical fiber I'm looking at. Unfortunately, there is a lot more noise than I was hoping for... but fortunately, I have many parameters to vary to attempt to get a better picture. If that doesn't work, then I'll just need to use a different camera. The GO-PRO is nice because it has a fixed focal length, but the fish eye field of view is quite annoying and difficult to work with.

# Next Up
1. Finish graph function. Accept parameters: tuple: (len, width), so that xy dimensions are actually real and accurate. Also, instead of displaying the graph, save it as a figure in the appropriate directory.
1. Set up a long test where parameters are varied (namely, `heightDivisor`, `widthDivisor`, and `middlePercentSavings`). Determine the best one.
1. Clean up error handling in `cropPhotos`, `resizePhotos`, `createLaplacianStack`, and `crop_resize_lpc`.
1. Modularize code in `crop_resize_lpc`. This function is way too damn messy.

# Eventually
1. Create virtualenv so that others in the research group can easily use this software, or make shell scripts so necessary software is installed on the user's computer.
1. Make as user-friendly as possible.
1. Update README.txt with explicit instructions.

*Last Updated: 12/22/2017 16:04 PST*
