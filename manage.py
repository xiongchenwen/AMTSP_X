from __future__ import print_function
import math
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp
from scipy.spatial import distance_matrix
import pandas

import calculate as cal
import time
import os
import numpy as np

Inf = float("inf")

current_path = os.getcwd()
log_path = current_path + "\\log"
if not os.path.exists(log_path):
    os.mkdir(log_path)


# —— —— —— —— —— 狄克斯特拉算法 —— —— —— —— ——

# 各点间转弯距:d_graph,各点间转弯名称:n_graph
def Graph(x_0, y_0, width, height, offset_width, path_width, turn_r, curve, straight, not_reverse):
    d_graph = {}
    n_graph = {}
    top_list, low_list = cal.Rec_turn_point(x_0, y_0, width, height, offset_width, path_width)
    targ = len(top_list)
    for x in range(0, targ):
        d_graph[x] = {}
        n_graph[x] = {}
    for x in range(0, targ):
        for y in range(0, targ):
            # 选择转弯方式，并且计算出两个转弯点之间的距离。
            # (先做逻辑判断，确定使用何种转弯方式，并计算相应的两点之间距离。)
            # 经过考虑，把逻辑判断并选择转弯方式的工作下放到calculate.py
            if x == y:
                d_graph[x][y] = 0
                n_graph[x][y] = None
            else:
                if top_list[x][0] > top_list[y][0]:
                    A, B = top_list[y], top_list[x]
                else:
                    A, B = top_list[x], top_list[y]
                turn_name, turn_length = cal.Turn_length(A, B, turn_r, curve, straight, not_reverse)
                n_graph[x][y] = turn_name
                d_graph[x][y] = round(turn_length * 100, 0)

    return top_list, d_graph, n_graph,  # d_graph 包含各点之间的距离


# 使用Google
def create_data_model(x_0, y_0, width, height, offset_width, path_width, turn_r, curve, straight, not_reverse):
    top_list, d_graph, n_graph = Graph(x_0, y_0, width, height, offset_width,
                                       path_width, turn_r, curve, straight, not_reverse)

    data = {'distance_matrix': d_graph, 'num_vehicles': 1, 'depot': 0}
    print('distance_matrix', data['distance_matrix'])
    return data


def main(x_0, y_0, width, height, offset_width, path_width, turn_r, curve, straight, not_reverse):
    data = create_data_model(x_0, y_0, width, height, offset_width, path_width, turn_r, curve, straight, not_reverse)

    manager = pywrapcp.RoutingIndexManager(len(data['distance_matrix']),
                                           data['num_vehicles'], data['depot'])

    routing = pywrapcp.RoutingModel(manager)

    # 创建距离回调
    def distance_callback(from_index, to_index):
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        # print('distance_matrix_2', data['distance_matrix'])
        return data['distance_matrix'][from_node][to_node]

    transit_callback_index = routing.RegisterTransitCallback(distance_callback)

    # 定义每个弧的成本。
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)
    # 设置第一个解决方案-启发式
    # search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    # search_parameters.first_solution_strategy = (
    #     routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)

    # 使用引导式本地搜索来逃避本地最小值；这通常是车辆路线选择中最有效的元启发式方法。需要设置搜索时间（我设置为5秒）
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.local_search_metaheuristic = (
        routing_enums_pb2.LocalSearchMetaheuristic.GUIDED_LOCAL_SEARCH)
    search_parameters.time_limit.seconds = 5
    search_parameters.log_search = True

    # 解决这个问题
    assignment = routing.SolveWithParameters(search_parameters)
    # 在控制台上打印解决方案
    if assignment:
        """Prints assignment on console."""
        top_list, d_graph, n_graph = Graph(x_0, y_0, width, height, offset_width,
                                           path_width, turn_r, curve, straight, not_reverse)
        print('n_graph', n_graph)
        print('d_graph', d_graph)
        targ = len(d_graph)
        all_turn_name = []
        index = routing.Start(0)
        print('index', index)
        row_list = []
        plan_output = ''
        all_turn_length = 0
        while not routing.IsEnd(index):
            for x in range(0, targ):
                row = manager.IndexToNode(index)
                print('row', row)
                row_list.append(row)
                print('row_list', row_list)
                turn_name = n_graph[row_list[x - 1]][row]
                print('turn_name', turn_name)
                plan_output += ' {} ->'.format(manager.IndexToNode(index))
                previous_index = index
                index = assignment.Value(routing.NextVar(index))
                all_turn_length += routing.GetArcCostForVehicle(previous_index, index, 0)
                all_turn_name.append(turn_name)

        del all_turn_name[0]
        print('距离：', all_turn_length)
        print('路线：', plan_output)
        print('row_list', row_list)
        print('all_turn_name', all_turn_name)
        return all_turn_length, row_list, all_turn_name


# 经验求解：次序
def Experience(x_0, y_0, width, height, offset_width, path_width, turn_r, curve, straight, not_reverse):
    all_turn_length = 0
    all_turn_name = []
    current_time = time.strftime('%Y-%m-%d-%H-%M-%S')
    top_list, low_list = cal.Rec_turn_point(x_0, y_0, width, height, offset_width, path_width)
    targ = len(top_list)
    row_list = list(range(0, targ))
    with open('{}\\{}_Experience.txt'.format(log_path, current_time), 'w') as f:
        for x in range(0, targ - 1):
            turn_name, turn_length = cal.Turn_length(top_list[x], top_list[x + 1], turn_r, curve, straight, not_reverse)
            all_turn_length = all_turn_length + turn_length
            all_turn_name.append(turn_name)
            front = x
            back = x + 1
            file_output = "Turn_Type: " + turn_name + " Direction: " + "{}-{} ".format(front, back) + "Length:" + str(
                ("%.2f" % turn_length)) + "\n"
            f.write(file_output)
        file_output = "All_length: " + str(("%.2f" % all_turn_length)) + "\n"
        f.write(file_output)
        f.close()
    all_turn_length = round(all_turn_length, 2)
    print(all_turn_length)
    print(all_turn_name)
    return all_turn_length, row_list, all_turn_name


if __name__ == '__main__':
    main()
