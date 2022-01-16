import numpy as np
from tqdm import tqdm
from os.path import join
from load_frames import load_frames

RES_DIR = './res_fbf'

def make_best_boundaries_for_one_scene(s_p, m_p): #scene and movie params 
    
    def mse(v1, v2):
        return np.average(((v1 - v2) ** 2))

    best_mse = mse(s_p, m_p[:s_p.shape[0]])
    best_ind = 0    
    for i in tqdm(range(m_p.shape[0] - s_p.shape[0] + 1)):
        cur_mse = mse(s_p, m_p[i: i + s_p.shape[0]])
        if cur_mse < best_mse:
            best_ind = i
            best_mse = cur_mse

    return best_ind, best_ind + s_p.shape[0] - 1

def make_best_boundaries(t_p, m_p, t_b, name):
    ind_to_start = 0
    try:    
        ind_to_start = sum(1 for line in open(join(RES_DIR, name + '.txt'), 'r'))
    except:
        pass
    f = open(join(RES_DIR, name + '.txt'), 'a')
    
    for b in tqdm(t_b):
        best_b = make_best_boundaries_for_one_scene(t_p[b[0]: b[1] + 1], m_p)   
        f.write(str(best_b[0]) + ' ' + str(best_b[1]) + '\n')

def make_best_boundaries_for_one_scene_expanded(s_p, m_p): #scene and movie params 
    
    def mse(v1, v2):
        return np.average(((v1 - v2) ** 2))

    best_mse = mse(s_p, m_p[:s_p.shape[0]])
    best_ind = 0    
    for i in tqdm(range(m_p.shape[0] - s_p.shape[0] + 1)):
        cur_mse = mse(s_p, m_p[i: i + s_p.shape[0]])
        if cur_mse < best_mse:
            best_ind = i
            best_mse = cur_mse

    return best_mse, best_ind,

def do_stuf(cur_pos, next_max, s_p):
    cur_m_p = load_frames('oz_the_great', '/home/dmitriy/Desktop/projects/trailer_creation/feature_extraction/vgg16/res', cur_pos, next_max - 1)
    cur_mse, cur_ind =  make_best_boundaries_for_one_scene_expanded(s_p, cur_m_p)
    return cur_mse, cur_ind    

def make_best_boundaries_for_one_scene_parted(s_p, m_d='kek'):
    #parts = os.listdir(m_d)
    #parts = [parts[i][:-4] for i in range(len(parts))]
    #parts.sort()
    frame_count = 187732 # THIS IS FOR oz_the_great ONLY!!!
    step = 2000 # THIS IS FOR oz_the_great ONLY!!!

    def mse(v1, v2):
        return np.average(((v1 - v2) ** 2))

    best_mse = 1000000000000000. # better to change for mse of the first comaparision
    best_ind = 0
    cur_pos = 0
    part_step = 20000
    next_max = part_step
    
    while True:
        cur_mse, cur_ind = do_stuf(cur_pos, next_max, s_p) 
        if cur_mse < best_mse:
            best_ind = cur_ind + cur_pos
            best_mse = cur_mse

        cur_pos = next_max - 500  
        if next_max >= frame_count:
            break
        next_max += part_step
        if next_max >= frame_count:
            next_max = frame_count        

    return best_ind, best_ind + s_p.shape[0] - 1   


def make_best_boundaries_parted(t_p, t_b, name):
    ind_to_start = 0
    try:    
        ind_to_start = sum(1 for line in open(join(RES_DIR, name + '.txt'), 'r'))
    except:
        pass
    f = open(join(RES_DIR, name + '.txt'), 'a')

    for b in tqdm(t_b):
        best_b = make_best_boundaries_for_one_scene_parted(t_p[b[0]: b[1] + 1])
        f = open(join(RES_DIR, name + '.txt'), 'a')   
        f.write(str(best_b[0]) + ' ' + str(best_b[1]) + '\n')
        f.close()

t_p = np.load('../feature_extraction/vgg16/res/oz_the_great_T0.npz')['arr_0']
t_p = np.resize(t_p, (-1, 25600))
m_p = np.load('./tests/oz_the_great.npz')['arr_0']
t_b = [ \
#[0, 33],
[34, 46],
[47 ,48],
[49, 116],
[117, 177],
[178 ,269],
[270 ,307],
[308 ,390],
[391 ,391],
[392 ,393],
[394 ,394],
[395 ,414],
[415 ,440],
[441 ,462],
[463 ,499],
[500 ,503],
[504 ,549],
[550 ,553],
[554 ,597],
[598 ,672],
[673 ,1028],
[1029, 1252],
[1253, 1273],
[1274, 1344],
[1345, 1385],
[1386, 1411],
[1412, 1449],
[1450, 1450],
[1451, 1544],
[1545, 1594],
[1595, 1696],
[1697, 1740],
[1741, 1827],
[1828, 1880],
[1881, 1894],
[1895, 1916],
[1917, 1968],
[1969, 2016],
[2017, 2042],
[2043, 2064],
[2065, 2078],
[2079, 2093],
[2094, 2180],
[2181, 2210],
[2211, 2270],
[2271, 2329],
[2330, 2354],
[2355, 2370],
[2371, 2382],
[2383, 2386],
[2387, 2401],
[2402, 2452],
[2453, 2489],
[2490, 2512],
[2513, 2556],
[2557, 2583],
[2584, 2619],
[2620, 2638],
[2639, 2677],
[2678, 2714],
[2715, 2735],
[2736, 2754],
[2755, 2758],
[2759, 2768],
[2769, 2783],
[2784, 2804],
[2805, 2832],
[2833, 2873],
[2874, 2893],
[2894, 2913],
[2914, 2933],
[2934, 2953],
[2954, 2954],
[2955, 2967],
[2968, 2986],
[2987, 2988],
[2989, 2992],
[2993, 2993],
[2994, 3038],
[3039, 3060],
[3061, 3074],
[3075, 3084],
[3085, 3096],
[3097, 3108],
[3109, 3112],
[3113, 3114],
[3115, 3124],
[3125, 3125],
[3126, 3128],
[3129, 3129],
[3130, 3132],
[3133, 3134],
[3135, 3161],
[3162, 3185],
[3186, 3211],
[3212, 3327],
[3328, 3387],
[3388, 3934] ]

name = 'ozozoz'
#make_best_boundaries(t_p, m_p, t_b, name)
make_best_boundaries_parted(t_p, t_b, 'parted_test1')
