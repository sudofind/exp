import cv2
from os.path import join



def do_trailer(movie_name, boundaries, trailer_name, videos_dir, tmp_dir, proga_dir):
    print(movie_name)
    print(boundaries)
    print(trailer_name)
    print(videos_dir)
    print(tmp_dir)
    print(proga_dir)

    movie_path = join(videos_dir, movie_name)
    from subprocess import call
    call(['mkdir', join(tmp_dir, 'scenes')])
    fps = cv2.VideoCapture(movie_path).get(cv2.CAP_PROP_FPS)
    
    for i, b in enumerate(boundaries):
        s_time = b[0] / fps
        e_time = b[1] / fps
        call(['ffmpeg', '-i', movie_path, '-ss', str(s_time), '-to', str(e_time), '-vcodec', 'copy', '-acodec', 'copy',\
                     join(tmp_dir, 'scenes', str(i) + '.mp4')])

    #Create full trailer
    if len(boundaries):
        call(['ffmpeg', '-i', join(tmp_dir, 'scenes', '0.mp4'), '-vcodec', 'copy', '-acodec', 'copy', join(tmp_dir, 'scenes','trailer.mp4')])

    for i in range(1, len(boundaries)):
        call(['ffmpeg', '-i', 'concat:' + join(tmp_dir, 'scenes','trailer.mp4') \
                + '|' + join(tmp_dir, 'scenes', str(i) + '.mp4'), '-vcodec', 'copy', '-acodec', 'copy',\
                 join(tmp_dir, 'scenes', 'kek.mp4')])
        call(['rm', join(tmp_dir, 'scenes','trailer.mp4')])
        call(['mv', join(tmp_dir, 'scenes','kek.mp4'), join(tmp_dir, 'scenes','trailer.mp4')])    

    call(['mv', join(tmp_dir, 'scenes','trailer.mp4'), join(tmp_dir, 'scenes', trailer_name + '.mp4')])
    call(['cp', join(tmp_dir, 'scenes', trailer_name + '.mp4'), join(proga_dir, 'res', 'trailers')])    
'''
p_dir = '/home/dmitriy/Desktop/projects/trailer_creation/main'
t_dir = join(p_dir, 'tmp')
v_dir = join(p_dir, 'videos')

do_trailer('lalaland.mp4', [[500, 600], [700, 800]], 'NY_DAVAY', v_dir, t_dir, p_dir)
'''
