from sklearn.decomposition import PCA as _PCA
from load_frames import load_frames
import numpy as np
from os.path import join
from pathlib import Path

p_dir = '/home/dmitriy/Desktop/projects/trailer_creation/main'
AVERAGE_SCENE_PARAMS_DIR = join(p_dir, 'cashe', 'average_scene_params')

class PCA:
    param_dir = None
    pca_obj = None
    param_num = None
    def __init__(self, param_num, train_video_name, param_dir):
        self.param_dir = param_dir
        self.param_num = param_num
        self.pca_obj = _PCA(n_components=param_num)

        train_params = np.load(join(self.param_dir, train_video_name + '.npz'))['arr_0']
        print('Load train video: ok')
        j = 1
        sz1 = train_params.shape[0]
        if sz1 == 1:
            sz1 = train_params.shape[1]
            j = 2
        sz2 = 1
        for i in range(j, len(train_params.shape)):
            sz2 *= train_params.shape[i]
        train_params = np.resize(train_params, (sz1, sz2))
        print('Before fitting')
        print(train_params.shape)
        self.pca_obj.fit(train_params)
        print('After fitting')

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
                params.append(np.average(scene_params, axis=0))
            return np.array(self.pca_obj.transform(params))

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

            return self.pca_obj.transform(all_scene)


    '''
    def get_params(self, video_name, boundaries, is_movie=False):
        
        params = []
        print(boundaries[0], boundaries[-1])
        from tqdm import tqdm
        for boundary in tqdm(boundaries):
            scene_params = None
            if is_movie:
                scene_params = load_frames(video_name, self.param_dir, boundary[0], boundary[1])
            else:
                scene_params = np.load(join(self.param_dir, video_name + '.npz'))['arr_0']
                
            j = 1
            sz1 = scene_params.shape[0]
            if sz1 == 1:
                sz1 = scene_params.shape[1]
                j = 2
            sz2 = 1
            for i in range(j, len(scene_params.shape)):
                sz2 *= scene_params.shape[i]
            scene_params = np.resize(scene_params, (sz1, sz2))

            if not is_movie:
                scene_params = scene_params[boundary[0] : boundary[1] + 1]

            scene_params = self.pca_obj.transform(scene_params)
            params.append(scene_params)
                        
        return params
    '''
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
            return np.array(self.pca_obj.transform(params))

        else:

            cash_path = join(AVERAGE_SCENE_PARAMS_DIR, video_name)
            if Path(cash_path + '.npz').is_file():
                print('OK')                
                scene_params = np.load(cash_path + '.npz')['arr_0']
                return np.array(self.pca_obj.transform(scene_params))
            else:
                print('NOT OK')
                from tqdm import tqdm
                for boundary in tqdm(boundaries):
                    scene_params = load_frames(video_name, self.param_dir, boundary[0], boundary[1])                
                    j = 1
                    sz1 = scene_params.shape[0]
                    if sz1 == 1:
                        sz1 = scene_params.shape[1]
                        j = 2
                    sz2 = 1
                    for i in range(j, len(scene_params.shape)):
                        sz2 *= scene_params.shape[i]

                    scene_params = np.resize(scene_params, (sz1, sz2))


                    scene_params = self.pca_obj.transform(scene_params)
                    params.append(scene_params)
                        
                return params
