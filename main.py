import cv2
import sys
import os
from multiprocessing import cpu_count
from multiprocessing.pool import ThreadPool

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

def capture_wrapper(args):
    capture(*args)        

def capture(file_name, home_directory, capture_rate, starting_frame, num_frames):
    vidcap = cv2.VideoCapture(file_name)
    vidcap.set(cv2.CAP_PROP_POS_FRAMES, starting_frame-1)
    success, image = vidcap.read()
    curr_frame = starting_frame
    end_frame = starting_frame + num_frames - 1

    while curr_frame <= end_frame:
        if curr_frame % int(60/capture_rate) == 0:
            cv2.imwrite("{}/frame{}.jpg".format(home_directory, curr_frame), image)  # save frame as JPEG file
            print("wrote {}/frame{}.jpg".format(home_directory, curr_frame))
        success, image = vidcap.read()
        curr_frame += 1
    return 10

def test(x):
    print(x**2)

def capture_parallelize(file_name, home_dir, rate):
    print("STUPID")
    cpus = cpu_count()
    vidcap = cv2.VideoCapture(file_name)
    num_frames = int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT))
    num_processes = cpus - 1

    frames_per_process = int(num_frames/num_processes)
    starting_frames = [i * frames_per_process for i in range(num_processes)]

    # Number of times to caputre frames, includes starting frame
    frame_counts = [frames_per_process] * (num_processes-1) + [(num_frames - frames_per_process * num_processes) + frames_per_process]
    
    # args
    #[(file_name, home_directory, capture_rate, starting_frame, num_frames)]
    args = [(file_name, home_dir, rate, starting_frames[i], frame_counts[i]) for i in range(num_processes)]

    pool = ThreadPool(num_processes)

    with pool as p:
        result = p.map(capture_wrapper, args)
    
    

if(__name__ == "__main__"):
    if file_name and home_dir:
        capture_parallelize(file_name, home_dir, rate)
    
    else:
        print("Missing file name and output directory")




