# Updates
* Fixed issue 1 by working on each image one at a time and resizing using `PIL.Image.NEAREST` filter. Check out this [link](https://github.com/kylerlittle/mk-topo-map/issues/1) for more details.
* Now, the program runs as it should! I obtained my first actual results-- this [crappy little figure](https://github.com/kylerlittle/mk-topo-map/results_2.png). Believe it or not-- it actually gives a decent ballpark estimate of the topographical map of the photomechanical fiber I'm looking at. Unfortunately, there is a lot more noise than I was hoping for... but fortunately, I have many parameters to vary to attempt to get a better picture.

# Next Up
1. Finish graph function. Accept parameters: tuple: (len, width), so that xy dimensions are actually real and accurate.
1. Set up a long test where parameters are varied (namely, `heightDivisor`, `widthDivisor`, and `middlePercentSavings`). Determine the best one.

# Eventually
1. Create virtualenv so that others in the research group can easily use this software.
1. Make as user-friendly as possible.
1. Update README.txt with explicit instructions.

*Last Updated: 12/22/2017 12:30 MST*
