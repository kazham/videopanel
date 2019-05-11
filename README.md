# VideoPanel

VideoPanel is a Python script that creates one video window composed from several video sources.

## Installation

Install [Python](https://www.python.org/).
Install OpenCV and NumPy using [pip](https://pip.pypa.io), which usually comes with [Python](https://www.python.org/).

## Usage

Open VideoPanel.py file in any editor.
Find pathList array declaration at the top of the file.
Change elements of this array to whatever you want.

This program was created for RTSP streams joining, so it shows final frames as fast as possible (i.e. with delay of 1ms).
Now it is obvious that joined video frame shoud be played with concerns of FPSs of the original videos.

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License
[MIT](https://choosealicense.com/licenses/mit/)
