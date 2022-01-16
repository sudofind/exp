from os.path import join
from subprocess import call

p_dir = '/home/dmitriy/Desktop/projects/trailer_creation/main'
t_dir = join(p_dir, 'tmp_make_trailer')


def do(boundaries, trailer_name, videos_dir, tmp_dir=t_dir, proga_dir=p_dir):
    if True:
        call(['ffmpeg', '-i', join(tmp_dir, 'scenes', '0.mp4'), join(tmp_dir, 'scenes','trailer.mp4')])

    for i in range(1, 191):
        call(['ffmpeg', '-i', 'concat:' + join(tmp_dir, 'scenes','trailer.mp4') \
                + '|' + join(tmp_dir, 'scenes', str(i) + '.mp4'), '-codec', 'copy',\
                 join(tmp_dir, 'scenes', 'kek.mp4')])
        input()
        call(['rm', join(tmp_dir, 'scenes','trailer.mp4')])
        call(['mv', join(tmp_dir, 'scenes','kek.mp4'), join(tmp_dir, 'scenes','trailer.mp4')])  

do(190, 2,3)
