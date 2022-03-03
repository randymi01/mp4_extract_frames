import cv2
import sys
import os

# opt arg

opt_long = {}
long_opts_required_args = ["--dir", "--rate", "--file"]

opt_short = {}
short_opts_required_args = ["-d", '-r', "-f"]

opt_arg = []

arg_list = sys.argv[1::]

skip = False
for i in range(len(arg_list)):
    if skip:
        skip = False
        continue
    if arg_list[i][:2] == "--" and arg_list[i] in long_opts_required_args:
        opt_long[arg_list[i]] = arg_list[i+1]
        skip = True
    elif arg_list[i][:2] == "--":
        opt_long[arg_list[i]] = ""
    elif arg_list[i][0] == "-" and arg_list[i] in short_opts_required_args:
        opt_short[arg_list[i]] = arg_list[i+1]
        skip = True
    elif arg_list[i][0] == "-":
        opt_short[arg_list[i]] = ""
    else:
        opt_arg.append(arg_list[i])

home_dir = ""
file_name = ""
rate = 10

def make_folder(folder_name):
    try:
        os.mkdir(folder_name)
    except FileExistsError:
        pass
    # empty the target folder
    for file in os.scandir(folder_name):
        os.remove(file.path)


for long_opt, long_arg in opt_long.items():
    # --dir <arg> specifies folder name
    if long_opt == "--dir":
        make_folder(long_arg)
        home_dir = long_arg
    # --rate <arg> captures per sec
    elif long_opt == "--rate":
        rate = int(long_arg)
    # --file <arg> filename
    elif long_opt == "--file":
        file_name = long_arg
    # --help
    elif long_opt == "--help":
        print("""
        use -f or --f to specify filename supports mp4
        use -r or --rate to specify number of frames captured per second
        use -d or --dir to specify directory to output into
        """)
    else:
        print("long argument {} not found".format(long_opt))

for short_opt, short_arg in opt_short.items():
    # -d <arg> specifies folder name
    if short_opt == "-d":
        make_folder(short_arg)
        home_dir = short_arg
    # -r <arg> captures per sec
    elif short_opt == "-r":
        rate = int(short_arg)
    # -f <arg> filename
    elif short_opt == "-f":
        file_name = short_arg
    # -h
    elif short_opt == "-h":
        print("""use -f or --f to specify filename supports mp4
                use -r or --rate to specify number of frames captured per second
                use -d or --dir to specify directory to output into""")
    else:
        print("short argument {} not found".format(short_opt))

def capture(filename, home_directory, capture_rate):
    vidcap = cv2.VideoCapture(filename)
    success, image = vidcap.read()
    frame_count = 1
    image_count = 1
    while success:
        if frame_count % int(60/capture_rate) == 0:
            cv2.imwrite("{}/frame{}.jpg".format(home_directory, image_count), image)  # save frame as JPEG file
            print("wrote {}/frame{}.jpg".format(home_directory, image_count))
            image_count += 1
        success, image = vidcap.read()
        frame_count += 1


if(__name__ == "__main__"):
    if file_name and home_dir:
        capture(file_name, home_dir, rate)
    else:
        print("Missing file name and output directory")




