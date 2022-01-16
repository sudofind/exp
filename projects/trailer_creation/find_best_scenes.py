import numpy as np

class NotIncludedBefore:
    included_scene_inds = None
    best_top_inds = None
    top_num = None
    t_params = None
    m_params = None
    t_boundaries = None
    m_boundaries = None
    t_lens = None
    m_lens = None
    def __init__(self, t_params, m_params, t_boundaries, m_boundaries, top_num=1000):
        self.best_top_inds = []# np.empty((len(t_boundaries), top_num), dtype='int')
        self.included_scene_inds = []
        self.t_params = t_params
        self.m_params = m_params
        self.t_boundaries = t_boundaries
        self.m_boundaries = m_boundaries
        self.t_lens = [self.t_boundaries[i][1] - self.t_boundaries[i][0] + 1 for i in range(len(t_boundaries))]
        self.m_lens = [self.m_boundaries[i][1] - self.m_boundaries[i][0] + 1 for i in range(len(m_boundaries))]
    
    def fill_best_top_for_one(self, ind):
        scene = self.t_params[ind]
        scenes = self.m_params
        t_len = self.t_lens[ind]
        if not len(scenes):
            print('Error: Список сцен, среди которых выбирается топ лучших, пустой')
            return None
    
        def mse_key(elem):
            return ((scene - elem[:-1]) ** 2).sum()

        scenes = [np.hstack([scenes[i], [i]]) for i in range(len(scenes))]
        new_scenes = []
        for i in range(len(scenes)):
            if t_len <= self.m_lens[i]:
                new_scenes.append(scenes[i])

        new_scenes.sort(key=mse_key)
        new_scenes = np.array(new_scenes)
        
        self.best_top_inds.append(new_scenes[:self.top_num, -1].astype('int'))
        

    def fill_best_top_for_all(self):
        for i in range(len(self.t_boundaries)):
            self.fill_best_top_for_one(i)

    def fill_cur_best(self, scene_ind):
        for ind in self.best_top_inds[scene_ind]:
            if not (ind in self.included_scene_inds):
                    self.included_scene_inds.append(ind)
                    return

    def fill_best_scenes(self):
        for i in range(len(self.t_boundaries)):
            self.fill_cur_best(i)
    
    def get_best_scenes(self):
        self.fill_best_top_for_all()
        self.fill_best_scenes()
        return self.included_scene_inds

class Simple:
    included_scene_inds = None
    best_top_inds = None
    top_num = None
    t_params = None
    m_params = None
    t_boundaries = None
    m_boundaries = None
    t_lens = None
    m_lens = None
    def __init__(self, t_params, m_params, t_boundaries, m_boundaries, top_num=1000):
        self.best_top_inds = []# np.empty((len(t_boundaries), top_num), dtype='int')
        self.included_scene_inds = []
        self.t_params = t_params
        self.m_params = m_params
        self.t_boundaries = t_boundaries
        self.m_boundaries = m_boundaries
        self.t_lens = [self.t_boundaries[i][1] - self.t_boundaries[i][0] + 1 for i in range(len(t_boundaries))]
        self.m_lens = [self.m_boundaries[i][1] - self.m_boundaries[i][0] + 1 for i in range(len(m_boundaries))]
    
    def fill_best_top_for_one(self, ind):
        scene = self.t_params[ind]
        scenes = self.m_params
        t_len = self.t_lens[ind]
        if not len(scenes):
            print('Error: Список сцен, среди которых выбирается топ лучших, пустой')
            return None
    
        def mse_key(elem):
            return ((scene - elem[:-1]) ** 2).sum()
        
        scenes = [np.hstack([scenes[i], [i]]) for i in range(len(scenes))]
        #print(scenes[0])
        #print(scenes[15])
        #exit(0)
        new_scenes = []
        for i in range(len(scenes)):
            if t_len <= self.m_lens[i]:
                new_scenes.append(scenes[i])
        
        new_scenes.sort(key=mse_key)
        new_scenes = np.array(new_scenes)
        self.best_top_inds.append(new_scenes[:self.top_num, -1].astype('int'))
        

    def fill_best_top_for_all(self):
        #print(self.t_boundaries)
        for i in range(len(self.t_boundaries)):
            self.fill_best_top_for_one(i)

    def fill_cur_best(self, scene_ind):
        i = 0
        for ind in self.best_top_inds[scene_ind]:
            if i == 0: #THIS INDEX DEFINES, what scene will be choosen from top (if 0, then the best scene is chosen)
                self.included_scene_inds.append(ind)
                return
            i += 1
    def fill_best_scenes(self):
        for i in range(len(self.t_boundaries)):
            self.fill_cur_best(i)
    
    def get_best_scenes(self):
        self.fill_best_top_for_all()
        #print(self.best_top_inds[108])
        #print(self.m_lens[108])
        #exit(0)
        self.fill_best_scenes()
        return self.included_scene_inds
    
    def get_best_top(num=3):
        boundaries = self.besttop_inds[:,:num]
        #for i in range(len(boundaries)):
        #    for j in range(len(boundaries[0]):
        #        boundaries[i][j] = self.m_boundaries[boundaries[i][j]]

        return boundaries
    
def find_best_scenes(t_params, m_params, t_boundaries, m_boundaries):
    #best_scenes_getter = NotIncludedBefore(t_params, m_params, t_boundaries, m_boundaries)
    print('\n\n\n__________________________\n')
    best_scenes_getter = Simple(t_params, m_params, t_boundaries, m_boundaries)
    best_scenes = best_scenes_getter.get_best_scenes()
    print('\n__________________________\n\n\n')
    return best_scenes
