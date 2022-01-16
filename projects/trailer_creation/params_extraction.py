from class_PCA import PCA
from class_Full import Full
from class_dyn_params import DynParams
import numpy as np

vgg16_param_dir = '/home/dmitriy/Desktop/projects/trailer_creation/feature_extraction/vgg16/res'
full_param_dir = '/home/dmitriy/Desktop/projects/trailer_creation/feature_extraction/vgg16/res_full'
dyn_param_dir = '/home/dmitriy/Desktop/projects/trailer_creation/feature_extraction/roman_priz/res'

def make_scene_params(trailer_name, movie_name, params_proportion, t_boundaries, m_boundaries, average=True):

    if average:
        trailer_params = np.empty((len(t_boundaries), 0))
        movie_params = np.empty((len(m_boundaries), 0))
        
        pca_method = PCA(params_proportion['PCA'], trailer_name, vgg16_param_dir)
        print('Initialization pca: ok')
        pca_t_params = pca_method.get_aver_params(trailer_name, t_boundaries)
        print('Getting average params of trailer: ok')
        trailer_params = np.hstack([trailer_params, pca_t_params])
        pca_m_params = pca_method.get_aver_params(movie_name, m_boundaries, is_movie=True)
        print('Getting average params of movie: ok')
        print(movie_params.shape, pca_m_params.shape)
        movie_params = np.hstack([movie_params, pca_m_params])
        '''
        full_method = Full(params_proportion['Full'], full_param_dir)
        full_t_params = full_method.get_aver_params(trailer_name, t_boundaries)
        trailer_params = np.hstack([trailer_params, full_t_params])
        full_m_params = full_method.get_aver_params(movie_name, m_boundaries, is_movie=True)
        print(movie_params.shape, full_m_params.shape)
        movie_params = np.hstack([movie_params, full_m_params])
        
        dyn_method = DynParams(params_proportion['Dyn'], dyn_param_dir)
        dyn_t_params = dyn_method.get_aver_params(trailer_name, t_boundaries)
        trailer_params = np.hstack([trailer_params, dyn_t_params])
        dyn_m_params = dyn_method.get_aver_params(movie_name, m_boundaries, is_movie=True)
        movie_params = np.hstack([movie_params, dyn_m_params])
        '''
        return trailer_params, movie_params
    else:
        print("YOBANA VROT, PALYNDRA!!!")
        trailer_params = [ np.empty((t_boundaries[i][1] - t_boundaries[i][0] + 1, 0)) for i in range(len(t_boundaries))]
        movie_params = [ np.empty((m_boundaries[i][1] - m_boundaries[i][0] + 1, 0)) for i in range(len(m_boundaries))]
        
        pca_method = PCA(params_proportion['PCA'], trailer_name, vgg16_param_dir)
        pca_t_params = pca_method.get_params(trailer_name, t_boundaries)
        for i in range(len(pca_t_params)):        
            trailer_params[i] = np.hstack([trailer_params[i], pca_t_params[i]])
        pca_m_params = pca_method.get_params(movie_name, m_boundaries, is_movie=True)
        for i in range(len(pca_m_params)):        
            movie_params[i] = np.hstack([movie_params[i], pca_m_params[i]])
        '''
        full_method = Full(params_proportion['Full'], full_param_dir)
        full_t_params = full_method.get_aver_params(trailer_name, t_boundaries)
        for i in range(len(full_t_params)):        
            trailer_params[i] = np.hstack([trailer_params[i], full_t_params[i]])        
        full_m_params = full_method.get_aver_params(movie_name, m_boundaries)
        for i in range(len(full_m_params)):        
            movie_params[i] = np.hstack([movie_params[i], full_m_params[i]])
            
        dyn_method = DynParams(params_proportion['Dyn'], dyn_param_dir)
        dyn_t_params = dyn_method.get_aver_params(trailer_name, t_boundaries)
        for i in range(len(dyn_t_params)):        
            trailer_params[i] = np.hstack([trailer_params[i], dyn_t_params[i]])
        dyn_m_params = dyn_method.get_aver_params(movie_name, m_boundaries)
        for i in range(len(dyn_m_params)):        
            movie_params[i] = np.hstack([movie_params[i], dyn_m_params[i]])
        '''        
        return trailer_params, movie_params

