from os.path import join
import numpy as np
import os

def load_frames(video, params_dir, start_frame, end_frame):
    video = join(params_dir, video)
    
    nums = []
    file_names = os.listdir(video)
    for file_name in file_names:
        nums.append(int(file_name[:-4]))
    nums.sort()
    
    temp_arr = np.load(join(video, str(nums[0]) + '.npz'))['arr_0']
    temp_shape = temp_arr.shape
    #print(temp_shape)
    tsn_first = temp_shape[0]
    tsn_sz = 1
    for i in range(1, len(temp_shape)):
        tsn_sz *= temp_shape[i]

    frames_num = end_frame - start_frame + 1
    #print(frames_num, tsn_sz)
    frames = np.empty((frames_num, tsn_sz))
    
    #print(nums[0].shape)
    step = None
    #try:
    step = nums[1]
    #except:
    #    step = nums[0].shape[0]    

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
