# points-graph

Just a simple proof of concept point grapher written in Python and PyQt in ~2 hours. I'll keep developing it if time permits. 

So far you can zoom in and out with mouse wheel and hardcode the points into the `GPointsList` list. To add your own point to plot simply add it to the array using following pattern (found in `Grid` class):

```python
self.GPointsList.append(self.GPoint(x, y))
```

TODO:
* plot points via GUI
* move around the graph by holding down the middle mouse button and moving the mouse
* plot linear and polynomial functions using straight lines and bezier curves
* tooltips for points plots and function graphs
