import os
from os.path import join

p_dir = '/home/dmitriy/Desktop/projects/trailer_creation/main'
FORMATED_BOUNDARIES_DIR = join(p_dir, 'cashe', 'formated_boundaries')
UNFORMATED_BOUNDARIES_DIR = join(p_dir, 'cashe', 'unformated_boundaries')
VIDEOS_DIR = join(p_dir, 'videos')
VQMT3D_PATH = '/home/dmitriy/Desktop/projects/trailer_creation/VQMT3D/source/vg_main-master/build/VQMT3D/bin/VQMT3D'

def load_boundaries(name):
    boundaries = []
    in_file = open(join(FORMATED_BOUNDARIES_DIR, name + '.txt'))
    for line in in_file:
        bound = line.split()
        bound = [int(bound[0]), int(bound[1])]
        boundaries.append(bound)
    return boundaries

def format_boundaries(name):
    boundaries = []
    in_file = open(join(UNFORMATED_BOUNDARIES_DIR, name + '.txt'))
    out_file = open(join(FORMATED_BOUNDARIES_DIR, name + '.txt'), 'w+')
    for line in in_file:
        bound = line.split()
        bound = [int(bound[0]), int(bound[1])]
        bound = [bound[0] - bound[1], bound[0] - 1]
        out_file.write(str(bound[0]) + ' ' + str(bound[1]) + '\n')
        boundaries.append(bound)
    return boundaries

def detect_scene_boundaries(name):
    boundaries = None
    if os.path.isfile(join(FORMATED_BOUNDARIES_DIR, name + '.txt')):
        boundaries = load_boundaries(name)
    elif os.path.isfile(join(UNFORMATED_BOUNDARIES_DIR, name + '.txt')):
        boundaries = format_boundaries(name)
    else:
        print("Can't found boundaries in cashe. Calculating boundaries: ", end='')
        from subprocess import call
        try:
            print(name)
            call([VQMT3D_PATH, \
                "--o={kek}".format(kek=join(FORMATED_BOUNDARIES_DIR, name + '.txt')),\
                join(VIDEOS_DIR, name + '.mp4'), join(VIDEOS_DIR, name + '.mp4')])
        except KeyboardInterrupt:
            call(['rm', "{kek}".format(kek=join(FORMATED_BOUNDARIES_DIR, name + '.txt'))])
        except:
            exit(0)
        boundaries = load_boundaries(name)

    return boundaries
