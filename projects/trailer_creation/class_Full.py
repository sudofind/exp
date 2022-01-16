from load_frames import load_frames
import numpy as np
from os.path import join
from pathlib import Path
from tqdm import tqdm

p_dir = '/home/dmitriy/Desktop/projects/trailer_creation/main'
AVERAGE_SCENE_PARAMS_MAKE_DIR = join(p_dir, 'cashe', 'average_scene_params_make_trailer')

class Full:
    param_dir = None
    param_names = None
    def __init__(self, param_names, param_dir):
        self.param_dir = param_dir
        self.param_names = param_names

    def get_params(self, video_name, boundaries, is_movie=False):
        params = []
        v_params = None
        if not is_movie:
            v_params = np.load(join(self.param_dir, video_name + '.npz'))['arr_0']
            j = 1
            sz1 = v_params.shape[0]
            if sz1 == 1:
                sz1 = v_params.shape[1]
                j = 2
            sz2 = 1
            for i in range(j, len(v_params.shape)):
                sz2 *= v_params.shape[i]
            v_params = np.resize(v_params, (sz1, sz2))
            for boundary in boundaries:
                scene_params = v_params[boundary[0]: boundary[1] + 1]
                params.append(scene_params)
            return params

        else:
            all_scene = load_frames(video_name, self.param_dir, boundaries[0], boundaries[1])
            j = 1
            sz1 = all_scene.shape[0]
            if sz1 == 1:
                sz1 = all_scene.shape[1]
                j = 2
            sz2 = 1
            for i in range(j, len(all_scene.shape)):
                sz2 *= all_scene.shape[i]

            all_scene = np.resize(all_scene, (sz1, sz2))

            return all_scene

    def get_aver_params(self, video_name, boundaries, is_movie=False):
        params = []
        v_params = None
        if not is_movie:
            v_params = np.load(join(self.param_dir, video_name + '.npz'))['arr_0']
            j = 1
            sz1 = v_params.shape[0]
            if sz1 == 1:
                sz1 = v_params.shape[1]
                j = 2
            sz2 = 1
            for i in range(j, len(v_params.shape)):
                sz2 *= v_params.shape[i]
            v_params = np.resize(v_params, (sz1, sz2))
            for boundary in boundaries:
                scene_params = v_params[boundary[0]: boundary[1] + 1]
                params.append(np.average(scene_params, axis=0))
            return np.array(params)

        else:

            cashe_path = join(AVERAGE_SCENE_PARAMS_MAKE_DIR, video_name)
            if Path(cashe_path + '.npz').is_file():
                print('OK')                
                scene_params = np.load(cashe_path + '.npz')['arr_0']
                return np.array(scene_params)
            else:
                print('NOT OK')
                aver_params = []
                for boundary in tqdm(boundaries):
                    scene_params = load_frames(video_name, self.param_dir, boundary[0], boundary[1])                
                    sz1 = scene_params.shape[0]
                    sz2 = 1
                    for i in range(1, len(scene_params.shape)):
                        sz2 *= scene_params.shape[i]

                    #print(boundary[0], boundary[1]) 
                    scene_params = np.resize(scene_params, (sz1, sz2))
                    #print(scene_params.shape)
                    cur_aver_params = np.average(scene_params, axis=0)
                    #print(cur_aver_params.shape)
                    aver_params.append(cur_aver_params)
                    #print(np.array(aver_params).shape)

                np.savez_compressed(cashe_path, np.array(aver_params))
                return np.array(aver_params)
