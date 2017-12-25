# Updates
* Fixed issue 1 by working on each image one at a time and resizing using `PIL.Image.NEAREST` filter. Check out this [link](https://github.com/kylerlittle/mk-topo-map/issues/1) for more details.
* The program officially runs as it should! Unfortunately, there is a lot more noise than I was hoping for... but fortunately, I have many parameters to vary to attempt to get a better picture. If that doesn't work, then I'll just need to use a different camera. The GO-PRO is nice because it has a fixed focal length, but the fish eye field of view is quite annoying and difficult to work with.
* Ran a long test yesterday. The [figures](https://github.com/kylerlittle/mk-topo-map/tree/master/topo-maps) are quite noisy. The good news is that it seems that at some point, the model will converge to the object's shape. With each increment in the width and height divisors, the figure becomes less messy and has a shape more like what I'm imaging. Next, I will run `vary_whd` with `whd_range = (26, 100)`. I'd like to quantitatively determine the precision we can maintain with a method like this,
* I will also vary PIL's resizing filters since these clearly have a large impact on the outcome of this program.
* Lastly, it appears that my *pre_crop* method is faulty in `crop_resize_lpc`. I had forgotten that I'm using the VIPS crop rather than PIL's. This needs to be fixed.

# Next Up
1. Run more long tests where parameters are varied (namely, `heightDivisor`, `widthDivisor`, `middlePercentSavings`, and PIL's resizing filters).
1. Finish graph function. Accept parameters: tuple: (len, width), so that xy dimensions are actually real and accurate. Also, instead of displaying the graph, save it as a figure in the appropriate directory.
1. Clean up error handling in `cropPhotos`, `resizePhotos`, `createLaplacianStack`, and `crop_resize_lpc`.
1. Modularize code in `crop_resize_lpc`. This function is way too damn messy.

# Eventually
1. Create virtualenv so that others in the research group can easily use this software, or make shell scripts so necessary software is installed on the user's computer.
1. Make as user-friendly as possible.
1. Update README.txt with explicit instructions.

*Last Updated: 12/25/2017 08:44 PST*