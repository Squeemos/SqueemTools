## Graphing
### Graphing.py:
#### GetRadius(area)
 Returns the radius of a circle in longitude/latitude (rough estimate)
- Area is the area of the circle 

#### MakeBigGraph(dataset,buffer,areaofInterest)
Graphs GLM data from an xarray container
- Dataset is an xarray container with GLM data
- Buffer is how much extra area around the data (in longitude/latitude) to show
  - Default: 0
- Area of interest will draw a rectangle surrounding this area. Will also draw a second, smaller map zoomed in
  - Default: None
