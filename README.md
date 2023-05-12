## Usage
Python command line tool that extracts frames from video file as jpeg. Works with most video formats.
```
$ python main.py -d <output directory> -r <extracted frames per second> -f <path to target video file> 
```
### Command Line Arguments:

* --help | -h: Prints command line argument information
* --rate <arg> | -r <arg>: Number of jpegs extracted per second (OPTIONAL, by default is 10)
* --directory <arg> | -d <arg>: Relative path of output directory where extracted frames will be stored (REQUIRED)
* --file <arg> | -f <arg>: Relative path of video file (REQUIRED)

### Example:
```
$ python main.py -d "shining frames" -r 10 -f shining.mp4 
```
## License

[MIT](https://choosealicense.com/licenses/mit/)
