from sbd import detect_scene_boundaries
from params_extraction import make_scene_params
from find_best_scenes import find_best_scenes
from find_best_subscenes import find_best_subscenes_boundaries
from make_video import do_trailer
from os.path import join
import numpy as np

p_dir = '/home/dmitriy/Desktop/projects/trailer_creation/main'
t_dir = join(p_dir, 'tmp_make_trailer')
v_dir = join(p_dir, 'videos')

def create_trailer(template_trailer_name, movie_name, params_propotion):
    
    trailer_boundaries = detect_scene_boundaries(template_trailer_name)
    movie_boundaries = detect_scene_boundaries(movie_name)
    #template_trailer_path = join(trailer_vid_dir, template_trailer_name)
    #movie_path = join(movie_vid_dir, movie_name)
    print('Detect scenes: ok')
    trailer_scene_params, movie_scene_params = make_scene_params(template_trailer_name, \
                              movie_name, params_propotion, trailer_boundaries, movie_boundaries)
    #np.savez_compressed('./tests/oz_trailer_pca_params', trailer_scene_params)
    #np.savez_compressed('./tests/oz_movie_pca_params', movie_scene_params)

    #print(trailer_scene_params[11] == movie_scene_params[11])    
    #exit(0)
    print('Calculating scenes params: ok')
    print(trailer_scene_params.shape, movie_scene_params.shape)
    #print('EEERRE', trailer_scene_params[0], movie_scene_params[0])
    inds = find_best_scenes(trailer_scene_params, movie_scene_params, trailer_boundaries, movie_boundaries)
    print(inds)
    #exit(0)
    print('Calculating best scenes: ok')
    print(inds)
    best_subscenes_boundaries = find_best_subscenes_boundaries(template_trailer_name, movie_name,\
                                              inds, trailer_boundaries, movie_boundaries, params_propotion)
    print('Calculating best subscenes: ok')
    print(best_subscenes_boundaries)
    fname = movie_name + '_from_' + template_trailer_name
#    for i in range(1, len(params_propotion)):
#        fname += '_' + str(params_propotion[i])
    f = open('./res/boundaries_make_trailer/' + fname + '.txt', 'w')
    for scene in best_subscenes_boundaries:
        f.write(str(scene[0]) + ' ' + str(scene[1]) + '\n')
    f.close()
    for i in range(len(best_subscenes_boundaries)):
        best_subscenes_boundaries[i][1] += 1

    do_trailer(movie_name + '.mp4', best_subscenes_boundaries, trailer_name=fname, videos_dir=v_dir, tmp_dir=t_dir, proga_dir=p_dir)
  
create_trailer('oz_the_great_T0', 'oz_the_great', {'PCA': 1000}) #{'Dyn': ['3d_color_hist', 'motion_hist']})
