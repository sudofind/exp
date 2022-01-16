from os.path import join
from load_frames import load_frames
import numpy as np

class DynParams:
    param_dir = None
    param_names = None
    def __init__(self, param_names, param_dir):
        self.param_dir = param_dir
        self.param_names = param_names

    def get_params(self, video_name, boundaries, is_movie=False):
        params = [np.load(join(self.param_dir, self.param_names[i], video_name + '.npz'))['arr_0'] for i in range(len(self.param_names))]
        pars = np.empty((params[0].shape[0], 0))
        for param in params:
            pars = np.hstack([pars, param / param.shape[1]])

        if not is_movie:
            params = []
            for boundary in boundaries:
                scene_params = pars[boundary[0]: boundary[1] + 1]
                params.append(scene_params)
            return params

        else:
            return pars[boundaries[0]: boundaries[1] + 1]

    def get_aver_params(self, video_name, boundaries, is_movie=False):
        params = [np.load(join(self.param_dir, self.param_names[i], video_name + '.npz'))['arr_0'] for i in range(len(self.param_names))]
        pars = np.empty((params[0].shape[0], 0))
        for param in params:
            pars = np.hstack([pars, param])

        aver_pars = np.empty((len(boundaries), pars.shape[1]))

        for i, boundary in enumerate(boundaries):
            #print(boundary[0], boundary[1])
            #input()
            aver_pars[i] = np.average(pars[boundary[0] : boundary[1] + 1], axis=0)
            #print(aver_pars[i])
        print(aver_pars)
        return aver_pars
