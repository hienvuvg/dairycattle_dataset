import numpy as np
from sympy.solvers import solve
from sympy import *

# New number 2024.01.23
n_y = 5.33 - 0.2
s_y = 6.46 - 0.2

# # Previously used numbers
# n_y = 5.7
# s_y = 5.67

anchors_3D_position = np.asarray([
                    [0,0,0],            #
                    [-6.1,n_y , 3.88],  # 1
                    [0, n_y, 4.04],     # 2
                    [6.1, n_y, 3.95],   # 3
                    [-0.36, 0, 5.17],   # 4
                    [0.36, 0, 5.17],    # 5
                    [-6.1, -s_y, 5.47],# 6
                    [0, -s_y, 5.36],   # 7
                    [6.1, -s_y, 5.49]])# 8

class triagulation():
    def __init__(self):
        self.dummy = 0

    def check_numbers_exist(self, arr1, arr2):
        return np.all(np.isin(arr1, arr2))

    def get_smallest_samples(self, array, index, n_data):
        feature_to_sort = array[:,index]
        shortest_indices = np.argsort(feature_to_sort)[:n_data]
        smallest_data_points = array[shortest_indices]
        return smallest_data_points

    def get_largest_samples(self, array, index, n_data):
        feature_to_sort = array[:,index]
        lastest_indices = np.argsort(feature_to_sort)[-n_data:]
        largest_data_points = array[lastest_indices]
        return largest_data_points

    # def mannual_data_points(self, data_points):
    #     anchor_1 = data_points[0,:]
    #     anchor_2 = data_points[1,:]
    #     anchor_3 = data_points[2,:]
    #     anchor_4 = data_points[3,:]
    #     anchor_5 = data_points[4,:]
    #     anchor_6 = data_points[5,:]
    #     anchor_7 = data_points[6,:]
    #     anchor_8 = data_points[7,:]

    #     selected_samples = np.vstack((anchor_3, anchor_5, anchor_8))
    #     # selected_samples = np.vstack((anchor_1, anchor_4, anchor_6))
    #     # selected_samples = np.vstack((anchor_4, anchor_6, anchor_7))

    #     return selected_samples

    def cal_group_score(self, data_dict):
        data_array = data_dict["group_data"]
        # invalid_anchor_id = 0

        anchor_ids = data_array[:,1]
        proba_LOS = data_array[:,4]
        if np.any(anchor_ids == -1) or np.any(proba_LOS < 30): # invalid ID 
            data_dict["score"] = -1.0
        else:
            distance = -1/10 * np.mean(data_array[:,2]) + 13/10
            n_samples = np.abs(np.mean(data_array[:,3])/5)  # Normalization
            LOS_proba = np.abs(np.mean(data_array[:,4])/100) # Normalization

            # data_dict["score"] = distance * 8 + n_samples * 3 + LOS_proba * 5 # Combining different factos
            data_dict["score"] = (-1)*np.sum(data_array[:,2]) + 50 # Based only on the shortest distance

        min_LOS = 0 # Filtering out based on LOS
        for data_point in data_array:
            if data_point[4] < min_LOS: 
                data_dict["score"] = -1.0
        
    def find_best_group(self, data_points):

        anchor_1 = data_points[0,:] # Takes in a row corresponding to data from one anchor
        anchor_2 = data_points[1,:]
        anchor_3 = data_points[2,:]
        anchor_4 = data_points[3,:]
        anchor_5 = data_points[4,:]
        anchor_6 = data_points[5,:]
        anchor_7 = data_points[6,:]
        anchor_8 = data_points[7,:]

        # Small triangles
        anchor_group_1 = np.vstack((anchor_1, anchor_2, anchor_4)) # Group containing data of three anchors
        anchor_group_2 = np.vstack((anchor_2, anchor_3, anchor_5))
        anchor_group_3 = np.vstack((anchor_1, anchor_4, anchor_6))
        anchor_group_4 = np.vstack((anchor_3, anchor_5, anchor_8))
        anchor_group_5 = np.vstack((anchor_4, anchor_6, anchor_7))
        anchor_group_6 = np.vstack((anchor_5, anchor_7, anchor_8))

        # Medium triangles 1
        anchor_group_7 = np.vstack((anchor_1, anchor_6, anchor_7))
        anchor_group_8 = np.vstack((anchor_2, anchor_6, anchor_7))
        anchor_group_9 = np.vstack((anchor_1, anchor_2, anchor_6))
        anchor_group_10 = np.vstack((anchor_1, anchor_2, anchor_7))

        # Medium triangles 2
        anchor_group_11 = np.vstack((anchor_2, anchor_7, anchor_8))
        anchor_group_12 = np.vstack((anchor_3, anchor_7, anchor_8))
        anchor_group_13 = np.vstack((anchor_2, anchor_3, anchor_7))
        anchor_group_14 = np.vstack((anchor_2, anchor_3, anchor_8))

        # Big triangles
        anchor_group_15 = np.vstack((anchor_1, anchor_7, anchor_3))
        anchor_group_16 = np.vstack((anchor_6, anchor_2, anchor_8))

        anchor_group_17 = np.vstack((anchor_1, anchor_6, anchor_3))
        anchor_group_18 = np.vstack((anchor_1, anchor_6, anchor_8))
        anchor_group_19 = np.vstack((anchor_3, anchor_8, anchor_1))
        anchor_group_20 = np.vstack((anchor_3, anchor_8, anchor_6))

        anchor_group_list = [ anchor_group_1,
                            anchor_group_2,
                            anchor_group_3,
                            anchor_group_4,
                            anchor_group_5,
                            anchor_group_6,
                            anchor_group_7,
                            anchor_group_8,
                            anchor_group_9,
                            anchor_group_10,
                            anchor_group_11,
                            anchor_group_12,
                            anchor_group_13,
                            anchor_group_14,
                            anchor_group_15,
                            anchor_group_16,
                            anchor_group_17,
                            anchor_group_18,
                            anchor_group_19,
                            anchor_group_20]
        
        anchor_group_dict_list = []
        for anchor_group in anchor_group_list:
            anchor_group_dict = {"group_data": anchor_group, "score": 0}
            anchor_group_dict_list.append(anchor_group_dict)

        combined_list = []
        for anchor_group_dict in anchor_group_dict_list:
            self.cal_group_score(anchor_group_dict)
            combined_list.append(anchor_group_dict)

        sorted_list = sorted(combined_list, key=lambda x: x["score"], reverse=True) # sort in decreasing order by score
        first_dict = sorted_list[0]
        data_point = first_dict['group_data']
        # print(data_point[:,1].astype('int'))

        if first_dict['score'] == -1:
            return (-1) * np.ones((3, 6))
        else:
            for element in sorted_list:
                print(int(element['score']), end=' ')
            print('\t', end=' ')
            return data_point

    def location_cal(self, anchors_3D_position, an_id, d): # an_id starts from 1
        x, y, z = symbols('x, y, z')
        A1 = anchors_3D_position[an_id[0]][0]
        A2 = anchors_3D_position[an_id[0]][1]
        A3 = anchors_3D_position[an_id[0]][2]
        B1 = anchors_3D_position[an_id[1]][0]
        B2 = anchors_3D_position[an_id[1]][1]
        B3 = anchors_3D_position[an_id[1]][2]
        C1 = anchors_3D_position[an_id[2]][0]
        C2 = anchors_3D_position[an_id[2]][1]
        C3 = anchors_3D_position[an_id[2]][2]

        Eq1 = Eq(x**2 + y**2 + z**2 - 2*(A1*x + A2*y + A3*z), d[0]**2 - (A1**2 + A2**2 + A3**2))
        Eq2 = Eq(x**2 + y**2 + z**2 - 2*(B1*x + B2*y + B3*z), d[1]**2 - (B1**2 + B2**2 + B3**2))
        Eq3 = Eq(x**2 + y**2 + z**2 - 2*(C1*x + C2*y + C3*z), d[2]**2 - (C1**2 + C2**2 + C3**2))
        # try:
        x1, x2 = solve([Eq1, Eq2, Eq3], [x, y, z])
        # except:
        #     x1 = solve([Eq1, Eq2, Eq3], [x, y, z])
        #     x2 = np.array([0, 0, 10])

        x1 = [complex(item) for item in x1]
        x2 = [complex(item) for item in x2]
        # print(x1, end=" ")
        if np.iscomplex(x1[0]) or np.iscomplex(x1[1]) or np.iscomplex(x1[2]):

            # print(' ')
            return np.round(x1,3)
        else:

            if float(np.real(x2[2])) < float(np.real(x1[2])):
                x1[2] = x2[2]
            # loc = np.round(np.array([float(np.real(x1[0])), float(np.real(x1[1])), float(np.real(x1[2])), float(np.real(x2[2]))]),3)
            loc = np.round(np.array([float(np.real(x1[0])), float(np.real(x1[1])), float(np.real(x1[2]))]),3)
            # print(str('[%.2f\t%.2f\t%.2f]' %(loc[0], loc[1], loc[2])))
            return loc
        # return 1



# Example usage:
# ===============================================
if __name__ == '__main__':

    localizer = triagulation()

    data_point = np.array(
        [[1690174841,	1,	11.6,	5,	0,	-99.7],
        [1690174841,	2,	7.01,	5,	76,	-93.7],
        [1690174841,	3,	6.28,	5,	6,	-93.7],
        [1690174841,	4,	5.97,	5,	97,	-97.4],
        [1690174841,	5,	5.48,	5,	0,	-93.4],
        [1690174841,	6,	12.6,	5,	0,	-95.9],
        [1690174841,	7,	8.95,	5,	80,	-92.7],
        [1690174841,	8,	8.26,	5,	0,	-94.1]]
    )

    for i in range(8):
        print(f'{int(data_point[i,0])}\t{int(data_point[i,1])}\t{data_point[i,2]:.2f}\t{int(data_point[i,3])}\t{int(data_point[i,4])}\t{int(data_point[i,5])}')

    ## Localization
    prev_location = np.array([0, 0, 0]).astype(float) # first initial location
    curr_location, loss_value, n_iterations, selected_anchor_ids = localizer.location_cal(prev_location, data_point)

    print(f"curr_location {curr_location}")
    print(f"loss_value {loss_value}")
    print(f"n_iterations {n_iterations}")
    print(f"selected_anchor_ids {selected_anchor_ids}")

    print("\nDone\n")
            

