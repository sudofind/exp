from sklearn.decomposition import PCA
import numpy as np
import os
from os.path import join
from tqdm import tqdm
import cv2
from pathlib import Path

PROGA_DIR = '/home/dmitriy/Desktop/projects/trailer_creation/main'
FORMATED_BOUNDARIES_DIR = join(PROGA_DIR, 'cashe', 'formated_boundaries')
UNFORMATED_BOUNDARIES_DIR = join(PROGA_DIR, 'cashe', 'unformated_boundaries')
AVERAGE_SCENE_PARAMS_DIR = join(PROGA_DIR, 'cashe', 'average_scene_params')
#print(AVERAGE_SCENE_PARAMS_DIR)
VIDEOS_DIR = join(PROGA_DIR, 'videos')
VQMT3D_PATH = "/home/dmitriy/Desktop/projects/trailer_creation/VQMT3D/source/vg_main-master/build/VQMT3D/bin/VQMT3D"
PARAMS_DIR = "/home/dmitriy/Desktop/projects/trailer_creation/feature_extraction/vgg16/res"
FULL_PARAMS_DIR = "/home/dmitriy/Desktop/projects/trailer_creation/feature_extraction/vgg16/res_full"
TMP_DIR = join(PROGA_DIR, 'tmp')

global g_pca
global g_top_inds
global included_scenes
global g_init_inds

g_init_inds = None
g_pca = None
g_top_inds = None
included_scenes = []

def calc_average_scene_params(video, boundaries, is_dir=False):

    scene_params = None
    if is_dir:
        cash_path = join(AVERAGE_SCENE_PARAMS_DIR, video.split('/')[-1])
        if Path(cash_path + '.npz').is_file():
            scene_params = np.load(cash_path + '.npz')['arr_0']
            return scene_params

        file_names = os.listdir(video)
        nums = []
        for file_name in file_names:
            nums.append(int(file_name[:-4]))
        nums.sort()

        temp_arr = np.load(join(video, str(nums[0]) + '.npz'))['arr_0']
        temp_shape = temp_arr.shape
        tsn = len(temp_shape)
        tsn_sz = temp_shape[tsn-3] * temp_shape[tsn-2] * temp_shape[tsn-1]
        scene_params = np.empty((len(boundaries), tsn_sz))

        print('Calculating average scene params of cashed video:')
        cur_sum = np.zeros((1, tsn_sz))
        i = 0
        a, b = boundaries[i][0], boundaries[i][1]
        scene_len = b - a + 1
        filled = 0
        for num in tqdm(nums):
            part = np.resize(np.load(join(video, str(num) + '.npz'))['arr_0'], (-1, tsn_sz))
            j = 0
            while 1:
                copy_num = min(scene_len - filled, len(part) - j)
                cur_sum += np.sum(part[j: copy_num], axis=0)
                if copy_num == scene_len - filled:
                    scene_params[i] = cur_sum / scene_len
                    j += copy_num
                    i += 1
                    if i >= len(boundaries):
                        break
                    a, b = boundaries[i][0], boundaries[i][1]
                    scene_len = b - a + 1
                    filled = 0
                    cur_sum = np.zeros((1, tsn_sz))
                else:
                    filled += len(part) - j
                    break
        #print(cash_path)
        np.savez_compressed(cash_path, scene_params)
    else:
        scene_params = np.empty((len(boundaries), video.shape[1]))    
        print('Calculating average scene params of numpy array: ', end='')
        i = 0
        for boundary in boundaries:
            scene_params[i] = np.average(video[boundary[0]: boundary[1] + 1], axis=0)
            i += 1
        print('done')
    return scene_params   

def make_PCAchka(video, n_components=None, to_fit=False):
    global g_pca
    if to_fit:
        g_pca = PCA(n_components=n_components)
        g_pca.fit(video)
    else:
        return g_pca.transform(video)

def make_top_variance_indicies(video, n_top_inds):
    variance = np.var(video, axis=0)
    inds = np.arange(variance.shape[0])
    video_for_sort = np.transpose(np.vstack([video, variance, inds]))

    def key_fun(elem):
        return elem[-2]

    video_for_sort = list(video_for_sort)
    video_for_sort.sort(key=key_fun)
    video_for_sort = np.array(video_for_sort)
    top_var_inds = video_for_sort[0:n_top_inds, -1]

    top_var_inds = top_var_inds.astype('int')
    #print('ssss', top_var_inds.shape)
    return top_var_inds

def make_top_variance_params(video, n_top_inds=None, to_fit=False):
    global g_top_inds
    if to_fit:
        g_top_inds = make_top_variance_indicies(video, n_top_inds)
    else:
        print(video.shape)
        video = video[:,g_top_inds]
        print(video.shape)
        return np.resize(video, (video.shape[0], video.shape[-1])) 

def make_initial_PCAchka(video, n_components=None, to_fit = False):
    global g_pca
    global g_init_inds

    if to_fit and g_pca is None:
        g_pca = PCA(n_components=n_components)
        g_pca.fit(video)
    else:
        if g_init_inds is None:
            vals = np.absolute(g_pca.components_).sum(axis=0)
    
            def key_fun(elem):
                return -elem[0]

            vals = np.vstack([vals, np.arange(vals.size)])
            vals = list(np.transpose(vals))
            vals.sort(key=key_fun)
            vals = np.array(vals)
            g_init_inds = vals[:len(g_pca.components_), 1]
            g_init_inds = g_init_inds.astype('int')
        print(video[:,g_init_inds].shape)
        return video[:,g_init_inds]
        


def calc_params(template_trailer_name, movie, params_propotion, trailer_boundaries, movie_boundaries, to_fit=False):

    template_trailer = np.load(join(PARAMS_DIR, template_trailer_name + '.npz'))['arr_0']
    templ_shape = template_trailer.shape
    tsn = len(templ_shape)
    tsn_sz = templ_shape[tsn-3] * templ_shape[tsn-2] * templ_shape[tsn-1]
    template_trailer = np.resize(template_trailer,\
                 (templ_shape[0], templ_shape[-1]*templ_shape[-2]*templ_shape[-3]))

    movie_path = join(PARAMS_DIR, movie)

    average_trailer_scene_params = None
    average_movie_scene_params = None

    if params_propotion[0] > 0 or params_propotion[1] > 0 \
                               or params_propotion[2] > 0: 
        average_trailer_scene_params = calc_average_scene_params(trailer, trailer_boundaries)
        if not (movie is None):
            average_movie_scene_params = calc_average_scene_params(movie_path, movie_boundaries, is_dir=True)

    trailer_params = np.array([[] for i in range(len(trailer_boundaries))])
    movie_params = np.array([[] for i in range(len(movie_boundaries))])

    print('Calculating params: ')
    if params_propotion[0] > 0:
        print('    Calculating trailer PCA params: ', end='')
        if to_fit:    
            make_PCAchka(trailer, to_fit=True, n_components=params_propotion[0])
        pca_trailer_params = make_PCAchka(average_trailer_scene_params)
        trailer_params = np.hstack([trailer_params, pca_trailer_params])
        print('done')
        if not (movie is None):
            print('    Calculating movie PCA params: ', end='')
            pca_movie_params = make_PCAchka(average_movie_scene_params)
            movie_params = np.hstack([movie_params, pca_movie_params])
            print('done')

    if params_propotion[1] > 0:
        if to_fit:
            make_initial_PCAchka(trailer, to_fit=True, n_components=params_propotion[1])
        init_pca_trailer_params = make_initial_PCAchka(average_trailer_scene_params)
        trailer_params = np.hstack([trailer_params, init_pca_trailer_params])
        if not (movie is None):
            init_pca_movie_params = make_initial_PCAchka(average_movie_scene_params)
            movie_params = np.hstack([movie_params, init_pca_movie_params])
            
    if params_propotion[2] > 0:
        #print(trailer.shape)
        #print('    Calculating trailer top variance params: ', end='')
        if to_fit:
            #print('____________________________________')
            make_top_variance_params(trailer, params_propotion[2], to_fit=True)
            #print(type(g_top_inds))
        #print(average_trailer_scene_params.shape)
        trailer_top_var_pars = make_top_variance_params(average_trailer_scene_params)
        #print(trailer_params.shape, trailer_top_var_pars.shape)
        #print(trailer_params.shape, trailer_top_var_pars.shape)
        trailer_params = np.hstack([trailer_params, trailer_top_var_pars])
        #print('done')
        if not (movie is None):        
            print('    Calculating movie top variance params: ', end='')
            movie_top_var_pars = make_top_variance_params(average_movie_scene_params)
            movie_params = np.hstack([movie_params, movie_top_var_pars])
            print('done')

    if params_propotion[3] > 0:
        template_trailer = np.load(join(FULL_PARAMS_DIR, template_trailer_name + '.npz'))['arr_0']
        templ_shape = template_trailer.shape
        tsn = len(templ_shape)
        tsn_sz = 1
        for i in range(1, tsn):
            tsn_sz *= templ_shape[i]
        template_trailer = np.resize(template_trailer, (templ_shape[0], tsn_sz))
    
        if not (movie is None):
            movie_path = join(FULL_PARAMS_DIR, movie)
    
        average_trailer_scene_params = calc_average_scene_params(trailer, trailer_boundaries)
        if not (movie is None):
            average_movie_scene_params = calc_average_scene_params(movie_path, movie_boundaries, is_dir=True) 

        trailer_params = np.hstack([trailer_params, average_traielr_scene_params])
        movie_params = np.hstack([movie_params, average_movie_scene_params])


    #print('done')
    if not (movie is None):
        return trailer_params, movie_params
    else:
        return trailer_params

def calc_params_of_single_scene(scene, param_propotion):
    #print(scene.shape)
    scene_params = [] 
    if params_propotion[0] > 0:
        pass

def make_scene_params(template_trailer_name, movie, params_propotion, trailer_boundaries, movie_boundaries):
    '''
    0. PCA - требует набор кадров (один трейлер или конкатенация нескольких),
          на котором нужно тренироваться. Также нужно количество признаков. Ну и тестовый трейлер. 
    1. Исходные признаки, редьюснутые с помощью PCA - то же самое, что PCA.
    2. Топ признаков по дисперсии - только количество признаков.
    3. Топ признаков по корреляции - только количество признаков
    4.Признаки Романа - нужен только трейлер. А вообще... Кажется, нужно считать характеристики 
                      каждой сцены, а не каждого кадра. Так что нужно что-то менять...
    5. Аудиохарактеристики
    '''

    return calc_params(template_trailer_name, movie,\
                        params_propotion, trailer_boundaries, movie_boundaries, to_fit=True)
        
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
            call([VQMT3D_PATH, \
                "--o={kek}".format(kek=join(FORMATED_BOUNDARIES_DIR, name + '.txt')),\
                join(VIDEOS_DIR, name + '.mp4'), join(VIDEOS_DIR, name + '.mp4')])
        except KeyboardInterrupt:
            call(['rm', "{kek}".format(kek=join(FORMATED_BOUNDARIES_DIR, name + '.txt'))])
        boundaries = load_boundaries(name)

    return boundaries

def find_best_top(scene, scenes, trailer_len, movie_lens, top_num=1000):
    if not len(scenes):
        print('Error: Список сцен, среди которых выбирается топ лучших, пустой')
        return None
    
    def mse_key(elem):
        return ((scene - elem[:-1]) ** 2).sum()
    #print(len(scenes),end=' ')
    scenes = [np.hstack([scenes[i], [i]]) for i in range(len(scenes))]
    new_scenes = []
    for i in range(len(scenes)):
        if trailer_len <= movie_lens[i]:
            new_scenes.append(scenes[i])
            #print(trailer_len, movie_lens[i]) 
    #print(len(new_scenes))  
    #scenes = list(np.hstack(scenes, np.resize(np.arange(len(scenes)), (len(scenes), 1)))
    #print(new_scenes[0])
    #print("_________")    
    new_scenes.sort(key=mse_key)
    #print(new_scenes[0])
    new_scenes = np.array(new_scenes)
    #print(new_scenes)
    #print('__________________')
    #print(new_scenes[:top_num])
    return new_scenes[:top_num, -1].astype('int')


def find_best_match(scene, scenes, trailer_len=None, movie_lens=None):
    if trailer_len == None and movie_lens == None:
        trailer_len = scene.shape[0]
        movie_lens = [scene.shape[0] for i in range(len(scenes))]
    if not len(scenes):
        print('Второй параметр - список сцен, с которыми нужно сравнивать. Какого хера он пустой?')
        return None
    
    best_scene_ind = 0
    best_mse = ((scene - scenes[best_scene_ind]) ** 2).sum()
    long_ind = -1
    for i in range(len(scenes)):
        if movie_lens[i] >= trailer_len:
            long_ind = i
            break
    if long_ind == -1:
        print('''В фильме нет сцен, длиннее проверяемой сцены трейлера.
                Подсчёт лучшей сцены из тех, длина которых >= длине проверямой сцены, 
                осуществляется, но некорректен''')
        long_ind = 0
    best_long_scene_ind = long_ind
    best_long_mse = ((scene - scenes[best_scene_ind]) ** 2).sum()
    for i in range(1, len(scenes)):
        mse = ((scene - scenes[i]) ** 2).sum()
        if mse < best_mse:
            best_scene_ind = i
            best_mse = mse
            #print()
            if movie_lens[i] >= trailer_len:
                best_long_scene_ind = i
                best_long_mse = mse
    #print(trailer_len, movie_lens[best_long_scene_ind])
    return best_scene_ind, best_long_scene_ind

def give_best_ind_not_given_b4(best_top, scene_len, scenes_lens):
    global included_scenes
    for ind in best_top:
        try:
            if not (ind in included_scenes):
                included_scenes.append(ind)
                return ind
        except:
            included_scenes = [ind]

def find_best_trailer(trailer_scenes, movie_scenes, trailer_boundaries, movie_boundaries, step=1):
    trailer_lens = np.array([int(trailer_boundaries[i][1] - trailer_boundaries[i][0] + 1) for i in range(len(trailer_boundaries))])
    movie_lens = np.array([int(movie_boundaries[i][1] - movie_boundaries[i][0] + 1) for i in range(len(movie_boundaries))])
    
    new_trailer_scenes_inds = []
    new_long_trailer_scenes_inds = []
    new_trailer_scenes_from_top = []
    i = 0
    print('Calculating best scenes inds: ')
    movie_scenes_lens = [len(movie_scenes[i]) for i in range(len(movie_scenes))]
    for j in tqdm(range(len(trailer_scenes))):
        i += 1
        if i % step:
            new_trailer_scenes_inds.append(0)
            new_long_trailer_scenes_inds.append(0)
            continue
        
        #print(t_scene.shape, trailer_scenes.shape)
        best_scene_ind, best_long_scene_ind = find_best_match(trailer_scenes[j], movie_scenes, trailer_lens[j], movie_lens)
        best_top = find_best_top(trailer_scenes[j], movie_scenes, trailer_lens[j], movie_lens)
        #print(best_top)
        for i in range(len(best_top)):
            best_top[i] = int(best_top[i])
        best_long_scene_ind = best_top[0]
        #print(best_top)
        best_top_ind = int(give_best_ind_not_given_b4(best_top, trailer_lens[j], movie_lens[best_top]))
        #print(type(best_top_ind))
        #print(best_top_ind)
        #if best_top_ind is None:
        #    print('suka')
        #print(best_top)
        #print("___________________________________")
        new_trailer_scenes_inds.append(best_scene_ind)
        new_long_trailer_scenes_inds.append(best_long_scene_ind)
        new_trailer_scenes_from_top.append(best_top_ind)

    #print(new_trailer_scenes_from_top)

    return new_trailer_scenes_inds, new_long_trailer_scenes_inds, new_trailer_scenes_from_top

def load_frames(video, start_frame, end_frame):
    video = join(PARAMS_DIR, video)
    
    nums = []
    file_names = os.listdir(video)
    for file_name in file_names:
        nums.append(int(file_name[:-4]))
    nums.sort()

    temp_arr = np.load(join(video, str(nums[0]) + '.npz'))['arr_0']
    temp_shape = temp_arr.shape
    tsn = len(temp_shape)
    tsn_sz = temp_shape[tsn-3] * temp_shape[tsn-2] * temp_shape[tsn-1]
    tsn_first = temp_shape[0]
    frames_num = end_frame - start_frame + 1
    frames = np.empty((frames_num, tsn_sz))
    
    step = nums[1]
    cur_frame = start_frame
    filled = 0
    while filled < frames_num:
        #print(filled, cur_frame, frames_num)
        #input()
        load_num = cur_frame - cur_frame % step 
        begin_part_num = load_num
        if load_num > nums[-1]:
            load_num = nums[-1]
            begin_part_num = nums[-2] + step
        part = np.resize(np.load(join(video, str(load_num) + '.npz'))['arr_0'], (tsn_first, tsn_sz))

        copy_num = min(frames_num - filled, begin_part_num + step - cur_frame)
        #print(frames_num - filled, len(part) - cur_frame + 1, copy_num)
        #print(filled, cur_frame - begin_part_num)
        frames[filled: filled + copy_num] = part[cur_frame - begin_part_num: cur_frame - begin_part_num + copy_num]
        filled += copy_num
        cur_frame += copy_num
        
    return frames
        
def find_best_subscene_left_boundary_offset(subscene, scene):
    a = np.array(scene[0: 0 + subscene.shape[0]])
    print(subscene.shape, scene.shape)
    scenes = [scene[i: i + subscene.shape[0]] for i in range(scene.shape[0] - subscene.shape[0] + 1)]
    #print(subscene.shape, scene[0].shape)
    if len(scenes):
        _, best_ind = find_best_match(subscene, scenes)
    
    return best_ind

def find_best_subscenes_boundaries(trailer_name, movie_name, scenes_matches, trailer_boundaries, movie_boundaries, params_propotion):
    trailer = np.load(join(PARAMS_DIR, trailer_name + '.npz'))['arr_0']
    temp_shape = trailer.shape
    tsn = len(temp_shape)
    tsn_sz = temp_shape[tsn-3] * temp_shape[tsn-2] * temp_shape[tsn-1]
    tsn_first = temp_shape[0]
    trailer = np.resize(trailer, (tsn_first, tsn_sz))
    trailer = calc_params(trailer, None, params_propotion, [[i, i] for i in range(len(trailer))], movie_boundaries)
    movie = join(PARAMS_DIR, movie_name)
    
    best_subscenes_boundaries = []
    print('Calculating best subscenes:')
    for i in tqdm(range(len(scenes_matches))):
        subscene = trailer[trailer_boundaries[i][0] : trailer_boundaries[i][1] + 1]
        print('trailer bounds:', trailer_boundaries[i][0], trailer_boundaries[i][1])
        scene_boundary = movie_boundaries[scenes_matches[i]]
        scene = load_frames(movie, scene_boundary[0], scene_boundary[1], full)
        scene = calc_params(scene, None, params_propotion, [[i, i] for i in range(len(scene))], movie_boundaries)
        #print('Границы большой сцены:', scene_boundary[0], scene_boundary[1])
        print('LENS:',len(subscene), len(scene))
        bslbo = find_best_subscene_left_boundary_offset(subscene, scene)
        best_subscene_boundary = [scene_boundary[0] + bslbo, scene_boundary[0] + bslbo + subscene.shape[0]]
        best_subscenes_boundaries.append(best_subscene_boundary)
    
    return best_subscenes_boundaries
'''
def do_trailer(movie_name, best_subscenes_boundaries, trailer_name):
    from subprocess import call
    movie = cv2.VideoCapture(join(VIDEOS_DIR, movie_name))
    fps = movie.get(cv2.CAP_PROP_FPS)
    print(fps)
    frameWidth = int(movie.get(cv2.CAP_PROP_FRAME_WIDTH))
    frameHeight = int(movie.get(cv2.CAP_PROP_FRAME_HEIGHT))
    frameSZ = (frameWidth, frameHeight)
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    trailer = cv2.VideoWriter(join(PROGA_DIR, 'res/trailers/' + trailer_name + '.avi'), fourcc, fps, frameSZ)
    print('Making trailer:') 
    fps = movie.get(cv2.CAP_PROP_FPS)
    for boundary in tqdm(best_subscenes_boundaries):
        movie.set(cv2.CAP_PROP_POS_FRAMES, boundary[0])
        for i in range(boundary[1] - boundary[0] + 1):
            ret, frame = movie.read()
            trailer.write(frame)
            start_time = boundary[0] / fps
            end_time = boundary[1] / fps

        print(join(TMP_DIR, movie_name[:-4] + '.acc'), os.path.isfile(join(TMP_DIR, movie_name[:-4] + '.aac')))
        if os.path.isfile(join(TMP_DIR, movie_name[:-4] + '.aac')):
            print(join(VIDEOS_DIR, movie_name), '\n', join(TMP_DIR, 'tmp.aac'))
            call(['ffmpeg', '-i', join(VIDEOS_DIR, movie_name), '-vn', '-acodec', 'copy', \
                        '-ss', str(30), '-to', str(40), join(TMP_DIR, 'tmp.aac')])
            print(2)
            print(TMP_DIR)
            call(['cd'])
            concat_string = '"concat:' + movie_name[:-4] + '.aac' + '|' + 'tmp.aac' + '"' 
            call(['ffmpeg', '-i', concat_string, '-acodec', 'copy', movie_name])
            call('rm', join(TMP_DIR, 'tmp.aac'))
        
    trailer.release()
    movie.release()
'''
'''
def do_trailer2(movie_name, boundaries, trailer_name):
    movie_path = join(VIDEOS_DIR, movie_name)
    from subprocess import call
    call(['mkdir', join(TMP_DIR, 'scenes')])
    #Create list of scenes
    f_scenes = open(join(TMP_DIR, 'scenes', 'list.txt'), 'w')
    fps = cv2.VideoCapture(movie_path).get(cv2.CAP_PROP_FPS)
    
    for i, b in enumerate(boundaries):
        s_time = b[0] / fps
        e_time = b[1] / fps
        call(['ffmpeg', '-i', movie_path, '-ss', str(s_time), '-to', str(e_time),\
                     join(TMP_DIR, 'scenes', str(i) + '.avi')])
        f_scenes.write( "file " + "'" + join(TMP_DIR, 'scenes', str(i) +  '.avi') + "'\n")
    f_scenes.close()

    #Create full trailer
    call(['ffmpeg', '-f', 'concat', '-safe', '0', '-i', join(TMP_DIR, 'scenes', 'list.txt'), '-c', 'copy',\
            join(PROGA_DIR, 'res', 'trailers', trailer_name + '.avi')])

    #call(['rm', '-r', join(TMP_DIR, 'scenes')])
'''

def do_trailer3(movie_name, boundaries, trailer_name):
    movie_path = join(VIDEOS_DIR, movie_name)
    from subprocess import call
    call(['mkdir', join(TMP_DIR, 'scenes')])
    fps = cv2.VideoCapture(movie_path).get(cv2.CAP_PROP_FPS)
    
    for i, b in enumerate(boundaries):
        s_time = b[0] / fps
        e_time = b[1] / fps
        call(['ffmpeg', '-i', movie_path, '-ss', str(s_time), '-to', str(e_time),\
                     join(TMP_DIR, 'scenes', str(i) + '.avi')])

    #Create full trailer
    if len(boundaries):
        call(['ffmpeg', '-i', join(TMP_DIR, 'scenes', '0.avi'), join(TMP_DIR, 'scenes','trailer.avi')])

    for i in range(1, len(boundaries)):
        call(['ffmpeg', '-i', 'concat:' + join(TMP_DIR, 'scenes','trailer.avi') \
                + '|' + join(TMP_DIR, 'scenes', str(i) + '.avi'), '-codec', 'copy',\
                 join(TMP_DIR, 'scenes', 'kek.avi')])
        call(['rm', join(TMP_DIR, 'scenes','trailer.avi')])
        call(['mv', join(TMP_DIR, 'scenes','kek.avi'), join(TMP_DIR, 'scenes','trailer.avi')])    

    call(['mv', join(TMP_DIR, 'scenes','trailer.avi'), join(TMP_DIR, 'scenes', trailer_name + '.avi')])
    call(['cp', join(TMP_DIR, 'scenes', trailer_name + '.avi'), join(PROGA_DIR, 'res', 'trailers')])    

    #call(['rm', '-r', join(TMP_DIR, 'scenes')])

def create_trailer(template_trailer_name, movie_name, params_propotion):
    
    trailer_boundaries = detect_scene_boundaries(template_trailer_name)
    movie_boundaries = detect_scene_boundaries(movie_name)
    trailer_scene_params, movie_scene_params = make_scene_params(template_trailer_name, \
                              movie_name, params_propotion, trailer_boundaries, movie_boundaries)
    
    inds, long_inds, top_inds = find_best_trailer(trailer_scene_params, movie_scene_params, trailer_boundaries, movie_boundaries)
    
    best_subscenes_boundaries = find_best_subscenes_boundaries(template_trailer_name, movie_name,\
                                              top_inds, trailer_boundaries, movie_boundaries, params_propotion)

    fname = movie_name + '_from_' + template_trailer_name + '_' + str(params_propotion[0])
    for i in range(1, len(params_propotion)):
        fname += '_' + str(params_propotion[i])
    f = open('./res/boundaries/' + fname + '.txt', 'w')
    for scene in best_subscenes_boundaries:
        f.write(str(scene[0]) + ' ' + str(scene[1]) + '\n')

    do_trailer3(movie_name + '.mp4', best_subscenes_boundaries, trailer_name=fname)

g_init_inds = None
g_pca = None
g_top_inds = None
included_scenes = []
create_trailer('prometheus_T0', 'lalaland', [1000, 0, 0, 0, 0])

'''
g_init_inds = None
g_pca = None
g_top_inds = None
included_scenes = []
create_trailer('prometheus_T0', 'lalaland', [0, 1000, 0, 0, 0])
g_init_inds = None
g_pca = None
g_top_inds = None
included_scenes = []
create_trailer('prometheus_T0', 'lalaland', [0, 0, 1000, 0, 0])
g_init_inds = None
g_pca = None
g_top_inds = None
included_scenes = []
'''
