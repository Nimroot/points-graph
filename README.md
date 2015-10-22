# points-graph

Just a simple proof of concept point grapher written in Python and PyQt in ~2 hours. I'll keep developing it if time permits.

So far you are able to move the graph around with MMB/RMB and plot the points on the graph with LMB. You can also add your own point to plot by simply adding it to the array using following pattern (found in `Grid` class):

```python
self.PointsList.append(QPoint(x, y))
```
Requirements:
* Python 3.x
* PyQt5

TODO:
* ~~plot points via GUI~~
* Add a visual tick marks which indicate value on the axis
* Implement new way of handling zooming (the old one leads to ugly results)
* ~~move around the graph by holding down the middle mouse button and moving the mouse~~
* plot linear and polynomial functions using straight lines and bezier curves
* tooltips for point plots and function graphs
