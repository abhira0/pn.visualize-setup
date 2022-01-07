# visualize-setup
Visualize any testbed (supports both .xml and .yaml) (undisclosed format)

## [Check out this webpage (it's interactive)](https://abhira0.github.io/visualize-setup/)

## Features
* Interactive network graph: Able to move nodes
* Hover on nodes to get node info
* Hover on edges to get edge info
* Edge width is determined by number of ports between nodes.
## Snapshot
![Snapshot](https://github.com/abhira0/visualize-setup/blob/main/pics/snapshot.PNG)
<br>
![Snapshot](https://github.com/abhira0/visualize-setup/blob/main/pics/Capture2.PNG)
<br>
![Snapshot](https://github.com/abhira0/visualize-setup/blob/main/pics/Capture3.PNG)
<br>

## Requirements
* Python 3.9.6+
* All other package requirements are written inside requirements.txt and can be installed using the following command:
`pip install -r requirements.txt`

## Use
1. Clone the repository or just downloading the testbed_visualizer.py would suffice.
2. Run: `python testbed_visualizer.py <testbed_path>`
3. New html file with the same name as input file will be generated. Also, python script will automatically open the html file in your default browser after saving it locally.
## Bugs & Errors
* Please raise issues on github.
