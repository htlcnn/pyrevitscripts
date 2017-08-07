# pyrevitscripts
My scripts to use with pyRevit


### [MassJoin](HTL.tab/MassJoin.panel/MassJoin.pushbutton)
Mass join walls, floors, columns and beams


### [AutoFoundation](HTL.tab/Foundation.panel/AutoFoundation.pushbutton)
Automate creating pile foundation.

Pile Cap and Pile family must have parameters: 'Number of pile segments', 'D', 'L1', 'L2', 'L3', 'L4', 'L5', 'L6', 'L7'

Pile Cap must have parameters: 'Length' (horizontal), 'Width' (vertical), 'Foundation Thickness'

All pile instances in Pile Cap family must be deleted manually before running this script.

Demo video: https://youtu.be/7uYuNca2Umg

### [Update Stirrup Dimensions](HTL.tab/Dimension.panel/UpdateStirrupDim.pushbutton)
Update all stirrup dimensions to Vietnamese style. Dimension type name pattern: 'UDIC Stirrup - 10a200' (contains `UDIC Stirrup` in prefix, has ` - ` as separator between prefix and suffix is diameter with spacing (`x`a`y`)

Demo video: https://youtu.be/sqe5WYU2l6A
