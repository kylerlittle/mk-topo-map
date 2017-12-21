# Updates
* I actually have _real_ data now. It's not perfect by any stretch of the imagination. The GoPro camera's 'fish' eye view is way too wide, but data is data.
* There is an issue with image writing/resizing. I created a new [issue](https://github.com/kylerlittle/mk-topo-map/issues/1) on github to describe it.
   * I need to completely rid the program of intermediate image writes & probably resizes. I can work around the writes fairly easily, but the resizes are something I need. Each image must be the same size before they're stacked. A simple extra crop won't do the trick because the fields of view are different.
   * For now, I'll keep the resize. But I'll need to use the initial run through the program to determine the correct size to resize to so that image processing can be done in a single loop.
   * The reason why resizing messes up with my data is because of how resizing works. The inherent nature of resizing is image interpolation, or using values of surrounding pixels to make a good approximation of added/removed pixels. Thus, resizing gets rid of large deviations between individual pixels. These deviations are what a variance of laplacian method relies on to pick out clusters of pixels which are in focus. In this way, a lower-quality resize filter might actually be better in my situation. We'll find out.

# To Do Immediately
1. Fix the issue described above. Instead of:
   ```python
   for im in rawImagesDir:
       im.crop()
   for im in croppedImagesDir:
       im.resizeToSmallest()
   for im in resizedImagesDir:
       imageStack.append(im.variance_of_laplacian())
   ```
   It will be more like:
   ```python
   for im in rawImagesDir:
       im.crop()
       im.resize()
       imageStack.append(im.variance_of_laplacian())	
   ```
1. Finish graph function. Accept parameters: tuple: (len, width), so that xy dimensions are actually real and accurate.
1. Run a full test on real data.
1. Set up a long test where parameters are varied. Pick the best one.

# To Do Eventually
1. Create virtualenv so that others in the research group can easily use this software.
1. Make as user-friendly as possible.
1. Update README.txt with explicit instructions.

*Last Updated: 12/20/2017 03:30 PST*