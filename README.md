# opencv-connect-components
opencv connected components and labeling

Connecting:
  - import packages
  - parse command line arguments
Pre-Processing
  - load image from disk
  - convert to grayscale
  - use Otsu's method to segement foreground from background "threshold"
Connect component analysis
  - input 
      - binary image
      - connectivity type
      - datatype 32-bit short
  - output
      - total unique labels
      - labels
      - stats (startX, startY, h, w, a)
      - center/centroids
Loop over each component
  - filter out background == 0
  - display text to screen
  - extract stats
Visualize
  - clone image
  - draw rectangle
  - draw circle
Construct Mask 
  - use numpy to create matrix
  - get labels matrix for connected component 
  - convert to uint8 
  - bring pixel intensity to 255    
  - provides mask for current component
Display output image
  - examine pixels that are connected to each other

Filtering:
  - import packages
  - parse command line arguments
Pre-Processing
  - load image from disk
  - convert to grayscale
  - use Otsu's method to segement foreground from background "threshold"
Loop over each component
  - start at i == 1 for all connected components
  - display text to screen
  - extract stats
Filter
  - if width is > <
  - if heigth 0 > <
  - if area > <
  - if all 3 are TRUE, than we have a license plate character