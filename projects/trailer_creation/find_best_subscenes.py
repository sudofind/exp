from params_extraction import make_scene_params
from class_PCA import PCA
from class_dyn_params import DynParams
from class_Full import Full

vgg16_param_dir = '/home/dmitriy/Desktop/projects/trailer_creation/feature_extraction/vgg16/res'
dyn_param_dir = '/home/dmitriy/Desktop/projects/trailer_creation/feature_extraction/roman_priz/res'
full_param_dir = '/home/dmitriy/Desktop/projects/trailer_creation/feature_extraction/vgg16/res_full'

def find_best_subscenes_boundaries(trailer_name, movie_name,\
        inds, t_boundaries, m_boundaries, params_proportion):
    best_subscenes = []

    pca = PCA(params_proportion['PCA'], trailer_name, vgg16_param_dir)
    #dyn = DynParams(params_proportion['Dyn'], dyn_param_dir)   
    #full = Full(params_proportion['Full'], full_param_dir)
     
    from tqdm import tqdm
    for i, ind in tqdm(enumerate(inds)):
        t_scene_len = t_boundaries[i][1] - t_boundaries[i][0]
        m_scene_len = m_boundaries[ind][1] - m_boundaries[ind][0]
        print("[{}, {}]".format(t_boundaries[i][0], t_boundaries[i][1]), "[{}, {}]".format(m_boundaries[ind][0], m_boundaries[ind][1]))          
        t_param = pca.get_params(trailer_name, [[0, t_scene_len]], is_movie=False)
        m_param = pca.get_params(movie_name, [m_boundaries[ind][0], m_boundaries[ind][1]] ,is_movie=True)
        #t_param = dyn.get_params(trailer_name, [[0, t_scene_len]], is_movie=False)
        #m_param = dyn.get_params(movie_name, [m_boundaries[ind][0], m_boundaries[ind][1]] ,is_movie=True)
        #t_param = full.get_params(trailer_name, [[0, t_scene_len]], is_movie=False)
        #m_param = full.get_params(movie_name, [m_boundaries[ind][0], m_boundaries[ind][1]] ,is_movie=True)


        #print(len(t_param), len(t_param[0]), len(t_param[0][0]))
        #print(m_param.shape)
        best_mse = ((t_param[0] - m_param[0:t_scene_len + 1]) ** 2).sum()
        best_ind = 0 
        for i in range(m_scene_len - t_scene_len + 1):
            cur_mse = ((t_param[0] - m_param[i: t_scene_len + i + 1]) ** 2).sum() 
            if cur_mse < best_mse:
                best_mse = cur_mse
                best_ind = i
        
        best_subscene_boundaries = [m_boundaries[ind][0] + best_ind, m_boundaries[ind][0] + best_ind + t_scene_len]
        best_subscenes.append(best_subscene_boundaries)

    return best_subscenes        

'''
def find_best_subscenes_boundaries(trailer_name, movie_name,\
        inds, t_boundaries, m_boundaries, params_proportion):
    best_subscenes = []

    from tqdm import tqdm
    for i, ind in tqdm(enumerate(inds)):
        t_scene_len = t_boundaries[i][1] - t_boundaries[i][0]
        m_scene_len = m_boundaries[ind][1] - m_boundaries[ind][0]        
        subscenes = [ [m_boundaries[ind][0] + j, m_boundaries[ind][0] + j + t_scene_len] for j in range(m_scene_len - t_scene_len + 1)]        
        t_scene, subscenes = make_scene_params(trailer_name, movie_name, params_proportion, [[0, t_scene_len]], subscenes, average=False)
        
        best_mse = ((t_scene[0] - subscenes[0]) ** 2).sum()
        best_ind = 0 
        for i, subscene in enumerate(subscenes):
            cur_mse = ((t_scene[0] - subscene) ** 2).sum() 
            if cur_mse < best_mse:
                best_mse = cur_mse
                best_ind = i
        
        best_subscene_boundaries = [m_boundaries[ind][0] + best_ind, m_boundaries[ind][0] + best_ind + t_scene_len]
        best_subscenes.append(best_subscene_boundaries)

    return best_subscenes        
'''
