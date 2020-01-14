import math
import numpy as np


# —— —— —— 显示相关 —— —— ——

# 即将调整默认参数，所有依赖此函数的函数功能都会受到影响。
def Rectangle(x_0, y_0, chang, kuan, angle):
    angle_0 = math.radians(angle)
    angle_1 = math.radians(90 + angle)
    angle_2 = math.radians(180 + angle)
    x_1 = x_0 + chang * math.cos(angle_0)
    y_1 = y_0 + chang * math.sin(angle_0)
    x_2 = x_1 + kuan * math.cos(angle_1)
    y_2 = y_1 + kuan * math.sin(angle_1)
    x_3 = x_2 + chang * math.cos(angle_2)
    y_3 = y_2 + chang * math.sin(angle_2)
    x_list = [x_0, x_1, x_2, x_3, x_0]
    y_list = [y_0, y_1, y_2, y_3, y_0]
    return x_list, y_list


# 圆弧函数
def arc(r, angle_0, angle_1, xin_x, xin_y):
    angle_list = [math.radians(x) for x in np.arange(angle_0, angle_1)]
    angle_list.append(math.radians(angle_1))
    x_list = [xin_x + r * math.cos(x) for x in angle_list]
    y_list = [xin_y + r * math.sin(x) for x in angle_list]
    return x_list, y_list


# 矩形平行线填充。注意：在矩形有偏置线的情况下，要传入偏置后的数据。n
def Parallel(x_0, y_0, width, height, path_width):
    y_1 = y_0 + height
    a = list(np.arange(x_0, x_0 + width, path_width))
    #	print(a)
    parallel = []
    for x in a:
        parallel.append([[x, x], [y_0, y_1]])
    parallel = parallel[1:]
    #	print(parallel)
    return parallel


# 矩形边界田块偏置线生成。待改进：此项只针对矩形，而非通用的多边形偏置算法。
# 调用这个文件里的矩形绘制函数:
# def rectangle(x_0,y_0,chang,kuan,angle):

# 偏置宽度(有根据工作幅宽进行圆整)
# —— —— —— 根据***要求，添加一个偏置逻辑 —— —— ——
# 具体为，人为设置偏置次数，若次数为-1，自动计算偏置次数。
# 若偏置次数为其他值时，按设定直接偏置，不管是否越过边界。
# 参数名命名为offset_para
def Offset_width(turn_r, path_width, not_reverse, offset_para):
    if offset_para == -1:
        if not_reverse:
            offset_width = 3 * turn_r + (path_width / 2)
            if offset_width % path_width == 0:
                offset_width = offset_width
            else:
                offset_width = offset_width + (path_width - offset_width % path_width)
        else:
            offset_width = turn_r + (path_width / 2)
            if offset_width % path_width == 0:
                offset_width = offset_width
            else:
                offset_width = offset_width + (path_width - offset_width % path_width)
    else:
        offset_width = offset_para * path_width
    return offset_width


# 内部行作业矩形
def Rec_Offset(x_0, y_0, width, height, offset_width):
    angle = 0
    x_0 = x_0 + offset_width
    y_0 = y_0 + offset_width
    width = width - 2 * offset_width
    height = height - 2 * offset_width
    x_list, y_list = Rectangle(x_0, y_0, width, height, angle)
    return x_list, y_list


# 即环形工作幅
def Rec_Mutil_offsets(x_0, y_0, width, height, offset_width, path_width):
    angle = 0
    rec_mutil_offsets = []
    offset_list = list(np.arange(offset_width, 0, -path_width))
    offset_list = offset_list[1:]
    for x in offset_list:
        x_ = x_0 + x
        y_ = y_0 + x
        width_ = width - 2 * x
        height_ = height - 2 * x
        x_list, y_list = Rectangle(x_, y_, width_, height_, angle)
        rec_mutil_offsets.append([x_list, y_list])
    return rec_mutil_offsets


# 求取转弯关键点(单环)
def Circle_point(x_0, y_0, width, height, offset_width):
    width = width - 2 * offset_width
    height = height - 2 * offset_width
    LL = [x_0 + offset_width, y_0 + offset_width]
    TL = [LL[0], LL[1] + height]
    TR = [LL[0] + width, LL[1] + height]
    LR = [LL[0] + width, LL[1]]
    return TL, TR, LL, LR


# 求取环形转弯关键点(多环)
def Circle_points(x_0, y_0, width, height, offset_width, path_width):
    LLs = []
    TLs = []
    TRs = []
    LRs = []
    offset_list = list(np.arange(offset_width - (path_width / 2), 0, -path_width))
    for x in offset_list:
        TL, TR, LL, LR = Circle_point(x_0, y_0, width, height, x)
        LLs.append(LL)
        TLs.append(TL)
        TRs.append(TR)
        LRs.append(LR)
    return LLs, TLs, TRs, LRs


# 环状转弯方式
def Circle_turn(x_0, y_0, width, height, offset_width, path_width, turn_r):
    all_turn = []
    LLs, TLs, TRs, LRs = Circle_points(x_0, y_0, width, height, offset_width, path_width)
    for x in range(0, len(LLs)):
        TL_turn = arc(turn_r, 90, 180, TLs[x][0] + turn_r, TLs[x][1] - turn_r)
        TR_turn = arc(turn_r, 0, 90, TRs[x][0] - turn_r, TRs[x][1] - turn_r)
        LL_turn = arc(turn_r, 180, 270, LLs[x][0] + turn_r, LLs[x][1] + turn_r)
        LR_turn = arc(turn_r, 270, 360, LRs[x][0] - turn_r, LRs[x][1] + turn_r)
        all_turn.append(TL_turn)
        all_turn.append(TR_turn)
        all_turn.append(LL_turn)
        all_turn.append(LR_turn)
    return all_turn


# 计算环状转弯方式总长度
def Circle_turn_length(offset_width, path_width, turn_r):
    mark = offset_width / path_width
    circle_turn_length = mark * 2 * math.pi * turn_r
    return circle_turn_length


# 求取跨行关键点
def C2C_points(top_point, low_point, row_list, offset_width, path_width):
    mark = row_list[-1]
    c2c_points = []
    # 如果是偶数条作业行，则从下边界出。
    if len(row_list) % 2 == 0:
        point_ = low_point[mark]
        c2c_0 = point_[1] - (path_width) / 2
        c2c_point_y = list(np.arange(c2c_0, point_[1] - offset_width, -path_width))
        edge_top = False
    # 如果是奇数条作业行，则从上边界出。
    else:
        point_ = top_point[mark]
        c2c_0 = point_[1] + (path_width) / 2
        c2c_point_y = list(np.arange(c2c_0, point_[1] + offset_width, path_width))
        edge_top = True
    for y in c2c_point_y:
        c2c_points.append([point_[0], y])
    return c2c_points, edge_top


# 求取行跨行关键点（给turn_r>path_width/2)使用）
def C2C_2_points(top_point, low_point, row_list, offset_width, path_width):
    c2c_2_points = []
    diff_length = path_width / 2
    c2c_points, edge_top = C2C_points(top_point, low_point, row_list, offset_width, path_width)
    mark = len(c2c_points)
    if edge_top:
        for x in range(0, mark):
            c2c_2_point = [c2c_points[x][0], c2c_points[x][1] - diff_length]
            c2c_2_points.append(c2c_2_point)
    else:
        for x in range(0, mark):
            c2c_2_point = [c2c_points[x][0], c2c_points[x][1] + diff_length]
            c2c_2_points.append(c2c_2_point)
    return c2c_2_points, edge_top


# 环形路径线，直线。上、下、左、右
def Cir_routes(x_0, y_0, width, height, top_point, low_point, row_list, offset_width, path_width, \
               turn_r):
    topline = []
    lowline = []
    leftline = []
    rightline = []
    l_length = turn_r - (path_width) / 2
    radian_ = math.acos(l_length / turn_r)
    v_length = turn_r * math.sin(radian_)
    LLs, TLs, TRs, LRs = Circle_points(x_0, y_0, width, height, offset_width, path_width)
    c2c_points, edge_top = C2C_points(top_point, low_point, row_list, offset_width, path_width)
    for x in range(0, len(LLs)):
        if edge_top:
            if turn_r <= (path_width) / 2:
                topline1 = [[TLs[x][0] + turn_r, c2c_points[x][0] - turn_r], [TLs[x][1], TLs[x][1]]]
                topline2 = [[c2c_points[x][0] + turn_r, TRs[x][0] - turn_r], [TLs[x][1], TLs[x][1]]]
                topline = topline + [topline1, topline2]
            else:
                topline1 = [[TLs[x][0] + v_length, c2c_points[x][0] - v_length], [TLs[x][1], TLs[x][1]]]
                topline2 = [[c2c_points[x][0] + v_length, TRs[x][0] - v_length], [TLs[x][1], TLs[x][1]]]
                topline = topline + [topline1, topline2]
            lowline = lowline + [[[LLs[x][0] + turn_r, LRs[x][0] - turn_r], [LLs[x][1], LLs[x][1]]]]
        else:
            if turn_r <= (path_width) / 2:
                lowline1 = [[LLs[x][0] + turn_r, c2c_points[x][0] - turn_r], [LLs[x][1], LLs[x][1]]]
                lowline2 = [[c2c_points[x][0] + turn_r, LRs[x][0] - turn_r], [LLs[x][1], LLs[x][1]]]
                lowline = lowline + [lowline1, lowline2]
            else:
                lowline1 = [[LLs[x][0] + v_length, c2c_points[x][0] - v_length], [LLs[x][1], LLs[x][1]]]
                lowline2 = [[c2c_points[x][0] + v_length, LRs[x][0] - v_length], [LLs[x][1], LLs[x][1]]]
                lowline = lowline + [lowline1, lowline2]
            topline = topline + [[[TLs[x][0] + turn_r, TRs[x][0] - turn_r], [TLs[x][1], TLs[x][1]]]]

        leftline = leftline + [[[TLs[x][0], TLs[x][0]], [TLs[x][1] - turn_r, LLs[x][1] + turn_r]]]
        rightline = rightline + [[[TRs[x][0], TRs[x][0]], [TRs[x][1] - turn_r, LRs[x][1] + turn_r]]]

    return topline, lowline, leftline, rightline


def Circle_routes(x_0, y_0, width, height, top_point, low_point, row_list, offset_width, path_width, \
                  turn_r):
    topline, lowline, leftline, rightline = Cir_routes(x_0, y_0, width, height, top_point, low_point, \
                                                       row_list, offset_width, path_width, turn_r)
    all_line = topline + lowline + leftline + rightline
    return all_line


# 求环形路径线的总长度
def Circle_route_length(x_0, y_0, width, height, top_point, low_point, row_list, offset_width, path_width, \
                        turn_r):
    circle_route_length = 0
    topline, lowline, leftline, rightline = Cir_routes(x_0, y_0, width, height, top_point, low_point, \
                                                       row_list, offset_width, path_width, turn_r)
    for x in topline:
        circle_route_length = circle_route_length + (abs(x[0][1] - x[0][0]))
    for x in lowline:
        circle_route_length = circle_route_length + (abs(x[0][1] - x[0][0]))
    for x in leftline:
        circle_route_length = circle_route_length + (abs(x[1][0] - x[1][1]))
    for x in rightline:
        circle_route_length = circle_route_length + (abs(x[1][0] - x[1][1]))
    print('circle_route_length', circle_route_length)
    return circle_route_length


# 环形行间转弯函数，turn_r<=(path_width)/2情况下。
def C2C_1_turn(top_point, low_point, row_list, turn_r, offset_width, path_width):
    c2c_turn1 = []
    c2c_turn2 = []
    c2c_line = []
    length = 2 * ((path_width / 2) - turn_r)
    c2c_points, edge_top = C2C_points(top_point, low_point, row_list, \
                                      offset_width, path_width)
    mark = row_list[-1]
    if edge_top:
        if mark < (len(top_point)) / 2:
            for x in c2c_points:
                turn1 = arc(turn_r, 90, 180, x[0] + turn_r, x[1] - turn_r)
                turn2 = arc(turn_r, 270, 360, x[0] - turn_r, x[1] + turn_r)
                line = [[x[0], x[0]], [x[1] - turn_r - length, x[1] - turn_r]]
                c2c_turn1.append(turn1)
                c2c_turn2.append(turn2)
                c2c_line.append(line)
        else:
            for x in c2c_points:
                turn1 = arc(turn_r, 0, 90, x[0] - turn_r, x[1] - turn_r)
                turn2 = arc(turn_r, 180, 270, x[0] + turn_r, x[1] + turn_r)
                line = [[x[0], x[0]], [x[1] - turn_r - length, x[1] - turn_r]]
                c2c_turn1.append(turn1)
                c2c_turn2.append(turn2)
                c2c_line.append(line)
    else:
        if mark < (len(low_point)) / 2:
            for x in c2c_points:
                turn1 = arc(turn_r, 180, 270, x[0] + turn_r, x[1] + turn_r)
                turn2 = arc(turn_r, 0, 90, x[0] - turn_r, x[1] - turn_r)
                line = [[x[0], x[0]], [x[1] + turn_r + length, x[1] + turn_r]]
                c2c_turn1.append(turn1)
                c2c_turn2.append(turn2)
                c2c_line.append(line)
        else:
            for x in c2c_points:
                turn1 = arc(turn_r, 270, 360, x[0] - turn_r, x[1] + turn_r)
                turn2 = arc(turn_r, 90, 180, x[0] + turn_r, x[1] - turn_r)
                line = [[x[0], x[0]], [x[1] + turn_r + length, x[1] + turn_r]]
                c2c_turn1.append(turn1)
                c2c_turn2.append(turn2)
                c2c_line.append(line)
    c2c_line = c2c_line[1:]
    c2c_1_turn = c2c_line + c2c_turn1 + c2c_turn2
    # 能不能把返回值合并起来？串成一个数组。
    return c2c_1_turn


# 计算第一类行间跨度长度。
def C2C_1_turn_length(turn_r, offset_width, path_width):
    mark = offset_width / path_width
    turn_length = mark * math.pi * turn_r
    line_length = (mark - 0.5) * (turn_r - path_width / 2)
    c2c_1_turn_length = turn_length + line_length
    return c2c_1_turn_length


# 环形行间转弯函数，turn_r>path_width/2
# 传入跨行时的关键点
def C2C_2_turn(top_point, low_point, row_list, turn_r, offset_width, path_width):
    if offset_width:
        c2c_turn1 = []
        c2c_turn2 = []
        rec_out_turn = []
        field_out_turn = []
        mark = row_list[-1]
        l_length = turn_r - (path_width) / 2
        radian_ = math.acos(l_length / turn_r)
        v_length = turn_r * math.sin(radian_)
        c2c_2_points, edge_top = C2C_2_points(top_point, low_point, row_list, offset_width, path_width)
        if edge_top:
            if mark < (len(top_point) / 2):
                radian1 = math.degrees(1.5 * math.pi + radian_)
                radian2 = math.degrees(0.5 * math.pi + radian_)
                for x in c2c_2_points[1:]:
                    O1 = [x[0] - v_length, x[1] + l_length]
                    O2 = [x[0] + v_length, x[1] - l_length]
                    turn1 = arc(turn_r, 270, radian1, O1[0], O1[1])
                    turn2 = arc(turn_r, 90, radian2, O2[0], O2[1])
                    c2c_turn1.append(turn1)
                    c2c_turn2.append(turn2)
                # 出矩形
                O1_ = [c2c_2_points[0][0] + turn_r, c2c_2_points[0][1] + (path_width) / 2 - turn_r]
                r_out_turn = arc(turn_r, 90, 180, O1_[0], O1_[1])
                # 出地块
                O2_ = [c2c_2_points[-1][0] - v_length, c2c_2_points[-1][1] + path_width + l_length]
                f_out_turn = arc(turn_r, 270, radian1, O2_[0], O2_[1])
                rec_out_turn.append(r_out_turn)
                field_out_turn.append(f_out_turn)

            else:
                radian1 = math.degrees(1.5 * math.pi - radian_)
                radian2 = math.degrees(0.5 * math.pi - radian_)
                for x in c2c_2_points[1:]:
                    O1 = [x[0] + v_length, x[1] + l_length]
                    O2 = [x[0] - v_length, x[1] - l_length]
                    turn1 = arc(turn_r, radian1, 270, O1[0], O1[1])
                    turn2 = arc(turn_r, radian2, 90, O2[0], O2[1])
                    c2c_turn1.append(turn1)
                    c2c_turn2.append(turn2)
                # 出矩形
                O1_ = [c2c_2_points[0][0] - turn_r, c2c_2_points[0][1] + (path_width) / 2 - turn_r]
                print(c2c_2_points[0])
                r_out_turn = arc(turn_r, 0, 90, O1_[0], O1_[1])
                # 出地块
                O2_ = [c2c_2_points[-1][0] + v_length, c2c_2_points[-1][1] + path_width + l_length]
                f_out_turn = arc(turn_r, radian1, 270, O2_[0], O2_[1])
                rec_out_turn.append(r_out_turn)
                field_out_turn.append(f_out_turn)

        else:
            if mark < (len(low_point) / 2):
                radian1 = math.degrees(0.5 * math.pi - radian_)
                radian2 = math.degrees(1.5 * math.pi - radian_)
                for x in c2c_2_points[1:]:
                    O1 = [x[0] - v_length, x[1] - l_length]
                    O2 = [x[0] + v_length, x[1] + l_length]
                    turn1 = arc(turn_r, radian1, 90, O1[0], O1[1])
                    turn2 = arc(turn_r, radian2, 270, O2[0], O2[1])
                    c2c_turn1.append(turn1)
                    c2c_turn2.append(turn2)
                # 出矩形
                O1_ = [c2c_2_points[0][0] + turn_r, c2c_2_points[0][1] - (path_width) / 2 + turn_r]
                r_out_turn = arc(turn_r, 90, 180, O1_[0], O1_[1])
                # 出地块
                O2_ = [c2c_2_points[-1][0] - v_length, c2c_2_points[-1][1] - path_width - l_length]
                f_out_turn = arc(turn_r, radian1, 90, O2_[0], O2_[1])
                rec_out_turn.append(r_out_turn)
                field_out_turn.append(f_out_turn)
            else:
                radian1 = math.degrees(0.5 * math.pi + radian_)
                radian2 = math.degrees(1.5 * math.pi + radian_)
                for x in c2c_2_points[1:]:
                    O1 = [x[0] + v_length, x[1] - l_length]
                    O2 = [x[0] - v_length, x[1] + l_length]
                    turn1 = arc(turn_r, 90, radian1, O1[0], O1[1])
                    turn2 = arc(turn_r, 270, radian2, O2[0], O2[1])
                    c2c_turn1.append(turn1)
                    c2c_turn2.append(turn2)
                # 出矩形
                O1_ = [c2c_2_points[0][0] - turn_r, c2c_2_points[0][1] - (path_width) / 2 + turn_r]
                r_out_turn = arc(turn_r, 270, 360, O1_[0], O1_[1])
                # 出地块
                O2_ = [c2c_2_points[-1][0] + v_length, c2c_2_points[-1][1] - path_width - l_length]
                f_out_turn = arc(turn_r, 90, radian1, O2_[0], O2_[1])
                rec_out_turn.append(r_out_turn)
                field_out_turn.append(f_out_turn)

        c2c_2_turn = c2c_turn1 + c2c_turn2 + rec_out_turn + field_out_turn
    else:
        c2c_2_turn = []
    return c2c_2_turn


# 计算第二类行间跨度长度
def C2C_2_turn_length(turn_r, offset_width, path_width):
    l_length = turn_r - (path_width) / 2
    radian_ = math.acos(l_length / turn_r)
    turn_1_length = radian_ * turn_r
    turn_2_length = math.pi * turn_r / 2
    mark = offset_width / path_width
    c2c_2_turn_length = (mark - 0.5) * 2 * turn_1_length + turn_2_length
    return c2c_2_turn_length


def C2C_turn(top_point, low_point, row_list, turn_r, offset_width, path_width):
    if turn_r <= (path_width) / 2:  # U型
        c2c_turn = C2C_1_turn(top_point, low_point, row_list, turn_r, offset_width, path_width)
    else:
        c2c_turn = C2C_2_turn(top_point, low_point, row_list, turn_r, offset_width, path_width)
    return c2c_turn


# 环形行间跨度总长度计算
def C2C_turn_length(offset_width, turn_r, path_width):
    if turn_r <= (path_width) / 2:
        c2c_turn_lentgh = C2C_1_turn_length(turn_r, offset_width, path_width)
    else:
        c2c_turn_lentgh = C2C_2_turn_length(turn_r, offset_width, path_width)
    return c2c_turn_lentgh


# 调用一般矩形平行线填充函数
# def Parallel(x_0,y_0,width,height,path_width):
def Offset_Parallel(x_0, y_0, width, height, offset_width, path_width):
    angle = 0
    x_0 = x_0 + offset_width
    y_0 = y_0 + offset_width
    width = width - 2 * offset_width
    height = height - 2 * offset_width
    offset_parallel = Parallel(x_0, y_0, width, height, path_width)
    return offset_parallel


# 矩形车辆路径线
# 先使用list生成列表，但是对于path_width/2,结果为小数的不适用
# 后续需要重新调整生成route_list的方法。
# 一般行作业路径线

# 行作业路径线，（传入row_list，注意出矩形作业区那行的长度)
# 不是一个理想的处理方式，最好是后续某个函数补长、截短最后行的最后一行?
def Rec_Route(x_0, y_0, width, height, turn_r, path_width, row_list, offset_para):
    mark = row_list[-1]
    length = turn_r - path_width / 2
    route_x0 = x_0 + (path_width / 2)
    y_height = y_0 + height
    route_list_x = list(np.arange(route_x0, x_0 + width, path_width))
    route_list = []
    for x in route_list_x:
        route_list.append([[x, x], [y_0, y_height]])
    # 作业行下方补长、截短。
    if offset_para == 0:
        pass
    else:
        if len(row_list) % 2 == 0:
            route_list[mark][1] = [y_0 + length, y_height]
        else:
            route_list[mark][1] = [y_0, y_height - length]
    return route_list


# 计算作业路径线长度。(注意传入的是route_list时是矩形路径线
# 或offset_route时是偏矩形路径线)
def Rec_Route_length(x_0, y_0, width, height, turn_r, path_width, row_list, offset_para):
    route_list = Rec_Route(x_0, y_0, width, height, turn_r, path_width, row_list, offset_para)
    rec_route_length = 0
    for x in route_list:
        rec_route_length = rec_route_length + abs(x[1][1] - x[1][0])
    return rec_route_length


# 偏置后矩形路径线
def Rectangle_routes(x_0, y_0, width, height, offset_width, turn_r, path_width, row_list, offset_para):
    angle = 0
    x_0 = x_0 + offset_width
    y_0 = y_0 + offset_width
    width = width - 2 * offset_width
    height = height - 2 * offset_width
    rectangle_routes = Rec_Route(x_0, y_0, width, height, turn_r, path_width, row_list, offset_para)
    return rectangle_routes


# 进入工作时路径线，红线显示，不播种。
def Rec_Route_In(x_0, y_0, width, heigth, offset_width, path_width):
    x_0 = x_0 + offset_width + (path_width / 2)
    y_1 = y_0 + offset_width
    route_in = ((x_0, x_0), (y_0, y_1))
    return route_in


def Rec_Route_In_length(offset_width):
    return offset_width


# 默认turn_list列表的数据结构是:[[x_0,y_0],[x_1,y_1]] 待确定？
# 接收来之rec_vehicle_route_line的数据。

# 行作业转弯点
def Rec_turn_point(x_0, y_0, width, height, offset_width, path_width):
    angle = 0
    x_0 = x_0 + offset_width
    y_0 = y_0 + offset_width
    width = width - 2 * offset_width
    height = height - 2 * offset_width
    y_top = y_0 + height
    route_x0 = x_0 + (path_width / 2)
    x_list = (list(np.arange(route_x0, x_0 + width, path_width)))
    top_list = []
    low_list = []
    for x in x_list:
        top_list.append([x, y_top])
    for x in x_list:
        low_list.append([x, y_0])
    #	print(top_list)
    #	print(low_list)
    return top_list, low_list


# 引用圆弧绘制函数绘制
# def arc(r,angle_0,angle_1,xin_x,xin_y):
# 	return x_list,y_list
# "n"型转弯
# 处理转弯数据，为了格式统一，数据简洁明了。
# 对某一些算出的弧线坐标点组使用reverse()方法，使坐标点的顺序通顺。

# 两种方向标识的统一函数。
# 接受矩形内方向标识调用、环形方向标识调用。
def Direction_mark(x, y, path_width, top_mark):
    width = path_width / 8
    height = 2 * width
    if top_mark:
        left_point = [x - width, y - height]
        right_point = [x + width, y - height]
        all_x = [left_point[0], x, right_point[0]]
        all_y = [left_point[1], y, right_point[1]]
    else:
        left_point = [x - width, y + height]
        right_point = [x + width, y + height]
        all_x = [left_point[0], x, right_point[0]]
        all_y = [left_point[1], y, right_point[1]]
    return all_x, all_y


# 绘制矩形内方向标识。
def Line_direction(row_list, list1, list2, path_width):
    direction_up = []
    direction_down = []
    for x in range(0, len(row_list)):
        if x % 2 == 0:
            targ = row_list[x]
            top_mark = True
            x = list1[targ][0]
            y = (list1[targ][1] + list2[targ][1]) / 2
            all_x, all_y = Direction_mark(x, y, path_width, top_mark)
            direction_up.append([all_x, all_y])
        else:
            targ = row_list[x]
            top_mark = False
            x = list1[targ][0]
            y = (list1[targ][1] + list2[targ][1]) / 2
            all_x, all_y = Direction_mark(x, y, path_width, top_mark)
            direction_down.append([all_x, all_y])
    return direction_up, direction_down


# 绘制环形行的方向标识。
# 注意LLs,TLs,TRs,LRs是以(x,y)此类形式存储，与其他的数据形式不同。
def Circle_direction(x_0, y_0, width, height, offset_width, path_width, top_point, low_point, \
                     row_list):
    circle_direction = []
    LLs, TLs, TRs, LRs = Circle_points(x_0, y_0, width, height, offset_width, path_width)
    c2c_points, edge_top = C2C_points(top_point, low_point, row_list, \
                                      offset_width, path_width)
    mark = row_list[-1]
    if edge_top:
        if mark < (len(top_point)) / 2:
            top_mark = False
        else:
            top_mark = True
    else:
        if mark < (len(low_point)) / 2:
            top_mark = True
        else:
            top_mark = False
    for x in range(0, len(TRs)):
        x_c = TRs[x][0]
        y_c = (TRs[x][1] + LRs[x][1]) / 2
        direction = Direction_mark(x_c, y_c, path_width, top_mark)
        circle_direction.append(direction)
    return circle_direction


# 行号标记
def Row_mark(row_list, list1, list2, path_width):
    x_ = []
    y_ = []
    for i in range(0, len(row_list)):
        y = (list1[i][1] + list2[i][1]) / 2.2
        x = list1[i][0]
        x_.append(x)
        y_.append(y)
    return x_, y_


# 各类转弯方式计算。
def U_turn(A, B, turn_r, TOP_EDGE):
    if TOP_EDGE:
        O1 = [A[0] + turn_r, A[1]]
        O2 = [B[0] - turn_r, B[1]]
        degree1 = math.degrees(math.atan((O2[1] - O1[1]) / (O2[0] - O1[0])))
        degree2 = degree1 + 90
        radian2 = math.radians(degree2)
        H1 = [O1[0] + turn_r * math.cos(radian2), O1[1] + turn_r * math.sin(radian2)]
        H2 = [O2[0] + turn_r * math.cos(radian2), O2[1] + turn_r * math.sin(radian2)]
        arc1 = arc(turn_r, degree2, 180, O1[0], O1[1])
        arc1[0].reverse()
        arc1[1].reverse()
        arc2 = arc(turn_r, 0, degree2, O2[0], O2[1])
        arc2[0].reverse()
        arc2[1].reverse()
        line_x = [H1[0], H2[0]]
        line_y = [H1[1], H2[1]]
        x = arc1[0] + line_x + arc2[0]
        y = arc1[1] + line_y + arc2[1]
    else:
        O1 = [A[0] + turn_r, A[1]]
        O2 = [B[0] - turn_r, B[1]]
        degree1 = math.degrees(math.atan((O2[1] - O1[1]) / (O2[0] - O1[0])))
        degree2 = 360 - (90 - degree1)
        radian2 = math.radians(degree2)
        H1 = [O1[0] + turn_r * math.cos(radian2), O1[1] + turn_r * math.sin(radian2)]
        H2 = [O2[0] + turn_r * math.cos(radian2), O2[1] + turn_r * math.sin(radian2)]
        arc1 = arc(turn_r, 180, degree2, O1[0], O1[1])
        arc2 = arc(turn_r, degree2, 360, O2[0], O2[1])
        line_x = [H1[0], H2[0]]
        line_y = [H1[1], H2[1]]
        x = arc1[0] + line_x + arc2[0]
        y = arc1[1] + line_y + arc2[1]
    return [x, y]


def U2_turn(A, B, turn_r, TOP_EDGE):
    if TOP_EDGE:
        O1 = [A[0] + turn_r, A[1]]
        O2 = [B[0] - turn_r, B[1]]
        O3 = []
        h = O2[1] - O1[1]
        if A[1] >= B[1]:
            B2 = [B[0], A[1]]
            O3 = O1
            line1 = [[B[0], B[0]], [B[1], B2[1]]]
            arc1 = arc(turn_r, 0, 180, O3[0], O3[1])
            arc1[0].reverse()
            arc1[1].reverse()
            x = arc1[0] + line1[0]
            y = arc1[1] + line1[1]
        else:
            A2 = [A[0], B[1]]
            O3 = O2
            line1 = [[A[0], A[0]], [A[1], A2[1]]]
            arc1 = arc(turn_r, 0, 180, O3[0], O3[1])
            x = line1[0] + arc1[0]
            y = line1[1] + arc1[1]
    else:
        O1 = [A[0] + turn_r, A[1]]
        O2 = [B[0] - turn_r, B[1]]
        O3 = []
        h = O2[1] - O1[1]
        if A[1] >= B[1]:
            A2 = [A[0], B[1]]
            O3 = O2
            line1 = [[A[0], A[0]], [A[1], A2[1]]]
            arc1 = arc(turn_r, 180, 360, O3[0], O3[1])
            x = line1[0] + arc1[0]
            y = line1[1] + arc1[1]
        else:
            B2 = [B[0], A[1]]
            O3 = O1
            line1 = [[B[0], B[0]], [B[1], B2[1]]]
            arc1 = arc(turn_r, 180, 360, O3[0], O3[1])
            x = arc1[0] + line1[0]
            y = arc1[1] + line1[1]
    return [x, y]


# "Ω"型转弯
def O_turn(A, B, turn_r, TOP_EDGE):
    if TOP_EDGE:
        O1 = [A[0] - turn_r, A[1]]
        O2 = [B[0] + turn_r, B[1]]
        C = [(O1[0] + O2[0]) / 2, (O1[1] + O2[1]) / 2]
        O1O2 = ((O2[1] - O1[1]) ** 2 + (O2[0] - O1[0]) ** 2) ** .5
        O1O2 = round(O1O2, 6)
        O3C = ((2 * turn_r) ** 2 - (O1O2 / 2) ** 2) ** .5
        degree1 = math.degrees(math.atan((O2[1] - O1[1]) / (O2[0] - O1[0])))
        degree2 = degree1 + 90
        radian2 = math.radians(degree2)
        O3 = [C[0] + O3C * math.cos(radian2), C[1] + O3C * math.sin(radian2)]
        # 我也不知道我算H1、H2两个点有什么用，就先放这里吧。
        H1 = [(O3[0] + O1[0]) / 2, (O3[1] + O1[1]) / 2]
        H2 = [(O3[0] + O2[0]) / 2, (O3[1] + O2[1]) / 2]
        # degreeO1O2O3 = math.degrees(math.atan((O1O2/2)/O3_C))
        degreeO312 = math.degrees(math.atan(O3C / (O1O2 / 2)))
        degree3 = degree1 + degreeO312
        degree4 = 180 - (degreeO312 - degree1)
        degree5 = 180 + degree3
        degree6 = 180 + degree4
        arc1_x, arc1_y = arc(turn_r, 0, degree3, O1[0], O1[1])
        arc2_x, arc2_y = arc(turn_r, degree4, 180, O2[0], O2[1])
        arc3_x, arc3_y = arc(turn_r, 0, degree5, O3[0], O3[1])
        arc3_x.reverse()
        arc3_y.reverse()
        arc4_x, arc4_y = arc(turn_r, degree6, 360, O3[0], O3[1])
        arc4_x.reverse()
        arc4_y.reverse()
        x = arc1_x + arc3_x + arc4_x + arc2_x
        y = arc1_y + arc3_y + arc4_y + arc2_y
    else:
        O1 = [A[0] - turn_r, A[1]]
        O2 = [B[0] + turn_r, B[1]]
        C = [(O1[0] + O2[0]) / 2, (O1[1] + O2[1]) / 2]
        O1O2 = ((O2[1] - O1[1]) ** 2 + (O2[0] - O1[0]) ** 2) ** .5
        O3C = ((2 * turn_r) ** 2 - (O1O2 / 2) ** 2) ** .5
        degree1 = math.degrees(math.atan((O2[1] - O1[1]) / (O2[0] - O1[0])))
        degree2 = degree1 + 270
        radian2 = math.radians(degree2)
        O3 = [C[0] + O3C * math.cos(radian2), C[1] + O3C * math.sin(radian2)]
        # 我也不知道我算H1、H2两个点有什么用，就先放这里吧。
        H1 = [(O3[0] + O1[0]) / 2, (O3[1] + O1[1]) / 2]
        H2 = [(O3[0] + O2[0]) / 2, (O3[1] + O2[1]) / 2]
        # degreeO1O2O3 = math.degrees(math.atan((O1O2/2)/O3_C))
        degreeO312 = math.degrees(math.atan(O3C / (O1O2 / 2)))
        degree3 = 360 - (degreeO312 - degree1)
        degree4 = 180 + degreeO312 + degree1
        degree5 = 180 - (degreeO312 - degree1)
        degree6 = degreeO312 + degree1
        arc1_x, arc1_y = arc(turn_r, degree3, 360, O1[0], O1[1])
        arc1_x.reverse()
        arc1_y.reverse()
        arc2_x, arc2_y = arc(turn_r, 180, degree4, O2[0], O2[1])
        arc2_x.reverse()
        arc2_y.reverse()
        arc3_x, arc3_y = arc(turn_r, degree5, 360, O3[0], O3[1])
        arc4_x, arc4_y = arc(turn_r, 0, degree6, O3[0], O3[1])
        x = arc1_x + arc3_x + arc4_x + arc2_x
        y = arc1_y + arc3_y + arc4_y + arc2_y
    return [x, y]


# "T"型转弯
def T_turn(A, B, turn_r, TOP_EDGE):
    if TOP_EDGE:
        O1 = [A[0] + turn_r, A[1]]
        O2 = [B[0] - turn_r, B[1]]
        C = [(O1[0] + O2[0]) / 2, (O1[1] + O2[1]) / 2]
        O1O2 = ((O1[0] - O2[0]) ** 2 + (O1[1] - O2[1]) ** 2) ** .5
        O3C = ((2 * turn_r) ** 2 - (O1O2 / 2) ** 2) ** .5
        degree1 = math.degrees(math.atan(abs(O1[1] - O2[1]) / (O1[0] - O2[0])))
        degree2 = 90 - degree1
        radian2 = math.radians(degree2)
        O3 = [C[0] + O3C * math.cos(radian2), C[1] + O3C * math.sin(radian2)]
        degreeO321 = math.degrees(math.atan(O3C / (O1O2 / 2)))
        degree3 = degreeO321 - degree1
        degree4 = 180 - (degree1 + degreeO321)
        degree5 = 180 + degree3
        degree6 = 180 + degree4
        H1 = [(O1[0] + O3[0]) / 2, (O1[1] + O3[1]) / 2]
        H2 = [(O2[0] + O3[0]) / 2, (O2[1] + O3[1]) / 2]
        arc1_x, arc1_y = arc(turn_r, degree4, 180, O1[0], O1[1])
        arc2_x, arc2_y = arc(turn_r, 0, degree3, O2[0], O2[1])
        arc3_x, arc3_y = arc(turn_r, degree5, degree6, O3[0], O3[1])
        x = arc1_x + arc3_x + arc2_x
        y = arc1_y + arc3_y + arc2_y
    else:
        O1 = [A[0] + turn_r, A[1]]
        O2 = [B[0] - turn_r, B[1]]
        C = [(O1[0] + O2[0]) / 2, (O1[1] + O2[1]) / 2]
        O1O2 = ((O1[0] - O2[0]) ** 2 + (O1[1] - O2[1]) ** 2) ** .5
        O3C = ((2 * turn_r) ** 2 - (O1O2 / 2) ** 2) ** .5
        degree1 = math.degrees(math.atan(abs(O1[1] - O2[1]) / (O1[0] - O2[0])))
        degree2 = 180 + 90 - degree1
        radian2 = math.radians(degree2)
        O3 = [C[0] + O3C * math.cos(radian2), C[1] + O3C * math.sin(radian2)]
        degreeO321 = math.degrees(math.atan(O3C / (O1O2 / 2)))
        degree3 = 180 + degreeO321 - degree1
        degree4 = 360 - degreeO321 - degree1
        degree5 = degreeO321 - degree1
        degree6 = 180 - degreeO321 - degree1
        H1 = [(O1[0] + O3[0]) / 2, (O1[1] + O3[1]) / 2]
        H2 = [(O2[0] + O3[0]) / 2, (O2[1] + O3[1]) / 2]
        arc1_x, arc1_y = arc(turn_r, 180, degree3, O1[0], O1[1])
        arc2_x, arc2_y = arc(turn_r, degree4, 360, O2[0], O2[1])
        arc3_x, arc3_y = arc(turn_r, degree5, degree6, O3[0], O3[1])
        x = arc1_x + arc3_x + arc2_x
        y = arc1_y + arc3_y + arc2_y
    return [x, y]


# T' turn
def T2_turn(A, B, turn_r, TOP_EDGE):
    if TOP_EDGE:
        O1 = [A[0] + turn_r, A[1]]
        O2 = [B[0] - turn_r, B[1]]
        C = [(O1[0] + O2[0]) / 2, (O1[1] + O2[1]) / 2]
        O1O2 = ((O2[1] - O1[1]) ** 2 + (O2[0] - O1[0]) ** 2) ** .5
        O3C = ((2 * turn_r) ** 2 - (O1O2 / 2) ** 2) ** .5
        degree1 = math.degrees(math.atan(abs(O2[1] - O1[1]) / abs(O2[0] - O1[0])))
        degree2 = 90 - degree1
        radian2 = math.radians(degree2)
        # 我也不知道我算H1、H2两个点有什么用，就先放这里吧。
        H1 = [O1[0] + turn_r * math.cos(radian2), O1[1] + turn_r * math.sin(radian2)]
        H2 = [O2[0] + turn_r * math.cos(radian2), O2[1] + turn_r * math.sin(radian2)]
        # degreeO1O2O3 = math.degrees(math.atan((O1O2/2)/O3_C))
        arc1 = arc(turn_r, degree2, 180, O1[0], O1[1])
        arc1[0].reverse()
        arc1[1].reverse()
        arc2 = arc(turn_r, 0, degree2, O2[0], O2[1])
        arc2[0].reverse()
        arc2[1].reverse()
        t_line = [[H1[0], H2[0]], [H1[1], H2[1]]]
        x = arc1[0] + t_line[0] + arc2[0]
        y = arc1[1] + t_line[1] + arc2[1]
    else:
        O1 = [A[0] + turn_r, A[1]]
        O2 = [B[0] - turn_r, B[1]]
        C = [(O1[0] + O2[0]) / 2, (O1[1] + O2[1]) / 2]
        O1O2 = ((O2[1] - O1[1]) ** 2 + (O2[0] - O1[0]) ** 2) ** .5
        O3C = ((2 * turn_r) ** 2 - (O1O2 / 2) ** 2) ** .5
        degree1 = math.degrees(math.atan(abs(O2[1] - O1[1]) / abs(O2[0] - O1[0])))
        degree2 = 180 + 90 - degree1
        radian2 = math.radians(degree2)
        # 我也不知道我算H1、H2两个点有什么用，就先放这里吧。
        H1 = [O1[0] + turn_r * math.cos(radian2), O1[1] + turn_r * math.sin(radian2)]
        H2 = [O2[0] + turn_r * math.cos(radian2), O2[1] + turn_r * math.sin(radian2)]
        # degreeO1O2O3 = math.degrees(math.atan((O1O2/2)/O3_C))
        arc1 = arc(turn_r, 180, degree2, O1[0], O1[1])
        arc2 = arc(turn_r, degree2, 360, O2[0], O2[1])
        l_line = [[H1[0], H2[0]], [H1[1], H2[1]]]
        x = arc1[0] + l_line[0] + arc2[0]
        y = arc1[1] + l_line[1] + arc2[1]
    return [x, y]


# 只有直线倒车特性
def M_turn(A, B, turn_r, TOP_EDGE):
    if TOP_EDGE:
        O1 = [A[0] - turn_r, A[1]]
        O2 = [B[0] + turn_r, B[1]]
        C = [(O1[0] + O2[0]) / 2, (O1[1] + O2[1]) / 2]
        O1O2 = ((O2[1] - O1[1]) ** 2 + (O2[0] - O1[0]) ** 2) ** .5
        O3C = ((2 * turn_r) ** 2 - (O1O2 / 2) ** 2) ** .5
        degree1 = math.degrees(math.atan((O2[1] - O1[1]) / (O2[0] - O1[0])))
        degree2 = degree1 + 90
        radian2 = math.radians(degree2)
        # 我也不知道我算H1、H2两个点有什么用，就先放这里吧。
        H1 = [O1[0] + turn_r * math.cos(radian2), O1[1] + turn_r * math.sin(radian2)]
        H2 = [O2[0] + turn_r * math.cos(radian2), O2[1] + turn_r * math.sin(radian2)]
        # degreeO1O2O3 = math.degrees(math.atan((O1O2/2)/O3_C))
        arc1 = arc(turn_r, 0, degree2, O1[0], O1[1])
        arc2 = arc(turn_r, degree2, 180, O2[0], O2[1])
        t_line = [[H1[0], H2[0]], H1[1], H2[1]]
        x = arc1[0] + t_line[0] + arc2[0]
        y = arc1[1] + t_line[1] + arc2[1]
    else:
        O1 = [A[0] - turn_r, A[1]]
        O2 = [B[0] + turn_r, B[1]]
        C = [(O1[0] + O2[0]) / 2, (O1[1] + O2[1]) / 2]
        O1O2 = ((O2[1] - O1[1]) ** 2 + (O2[0] - O1[0]) ** 2) ** .5
        O3C = ((2 * turn_r) ** 2 - (O1O2 / 2) ** 2) ** .5
        degree1 = math.degrees(math.atan((O2[1] - O1[1]) / (O2[0] - O1[0])))
        degree2 = degree1 + 270
        radian2 = math.radians(degree2)
        # 我也不知道我算H1、H2两个点有什么用，就先放这里吧。
        H1 = [O1[0] + turn_r * math.cos(radian2), O1[1] + turn_r * math.sin(radian2)]
        H2 = [O2[0] + turn_r * math.cos(radian2), O2[1] + turn_r * math.sin(radian2)]
        # degreeO1O2O3 = math.degrees(math.atan((O1O2/2)/O3_C))
        arc1 = arc(turn_r, degree2, 360, O1[0], O1[1])
        arc2 = arc(turn_r, 180, degree2, O2[0], O2[1])
        l_line = [[H1[0], H2[0]], [H1[1], H2[1]]]
        x = arc1[0] + l_line[0] + arc2[0]
        y = arc1[1] + l_line[1] + arc2[1]
    return [x, y]


# 有转弯倒车特性
def M2_turn(A, B, turn_r, TOP_EDGE):
    if TOP_EDGE:
        O1 = [A[0] - turn_r, A[1]]
        O2 = [B[0] + turn_r, B[1]]
        C = [(O1[0] + O2[0]) / 2, (O1[1] + O2[1]) / 2]
        tran = (O2[1] - O1[1]) ** 2 + (O2[0] - O1[0]) ** 2
        O1O2 = tran ** .5
        O3C = ((2 * turn_r) ** 2 - (O1O2 / 2) ** 2) ** .5
        degree1 = math.degrees(math.atan((O2[1] - O1[1]) / (O2[0] - O1[0])))
        degree2 = degree1 + 90
        radian2 = math.radians(degree2)
        O3 = [C[0] + O3C * math.cos(radian2), C[1] + O3C * math.sin(radian2)]
        # 我也不知道我算H1、H2两个点有什么用，就先放这里吧。
        H1 = [(O3[0] + O1[0]) / 2, (O3[1] + O1[1]) / 2]
        H2 = [(O3[0] + O2[0]) / 2, (O3[1] + O2[1]) / 2]
        # degreeO1O2O3 = math.degrees(math.atan((O1O2/2)/O3_C))
        degreeO312 = math.degrees(math.atan(O3C / (O1O2 / 2)))
        degree3 = degree1 + degreeO312
        degree4 = 180 - (degreeO312 - degree1)
        degree5 = 180 + degree3
        degree6 = 180 + degree4
        arc1_x, arc1_y = arc(turn_r, 0, degree3, O1[0], O1[1])
        arc2_x, arc2_y = arc(turn_r, degree4, 180, O2[0], O2[1])
        arc3_x, arc3_y = arc(turn_r, degree5, degree6, O3[0], O3[1])
        x = arc1_x + arc3_x + arc2_x
        y = arc1_y + arc3_y + arc2_y
    else:
        O1 = [A[0] - turn_r, A[1]]
        O2 = [B[0] + turn_r, B[1]]
        C = [(O1[0] + O2[0]) / 2, (O1[1] + O2[1]) / 2]
        trans = (O2[1] - O1[1]) ** 2 + (O2[0] - O1[0]) ** 2
        O1O2 = trans ** .5
        O3C = ((2 * turn_r) ** 2 - (O1O2 / 2) ** 2) ** .5
        degree1 = math.degrees(math.atan((O2[1] - O1[1]) / (O2[0] - O1[0])))
        degree2 = degree1 + 270
        radian2 = math.radians(degree2)
        O3 = [C[0] + O3C * math.cos(radian2), C[1] + O3C * math.sin(radian2)]
        # 我也不知道我算H1、H2两个点有什么用，就先放这里吧。
        H1 = [(O3[0] + O1[0]) / 2, (O3[1] + O1[1]) / 2]
        H2 = [(O3[0] + O2[0]) / 2, (O3[1] + O2[1]) / 2]
        # degreeO1O2O3 = math.degrees(math.atan((O1O2/2)/O3_C))
        degreeO312 = math.degrees(math.atan(O3C / (O1O2 / 2)))
        degree3 = 360 - (degreeO312 - degree1)
        degree4 = 180 + degreeO312 + degree1
        degree5 = 180 - (degreeO312 - degree1)
        degree6 = degreeO312 + degree1
        arc1_x, arc1_y = arc(turn_r, degree3, 360, O1[0], O1[1])
        arc2_x, arc2_y = arc(turn_r, 180, degree4, O2[0], O2[1])
        arc3_x, arc3_y = arc(turn_r, degree6, degree5, O3[0], O3[1])
        x = arc2_x + arc3_x + arc1_x
        y = arc2_y + arc3_y + arc1_y
    return [x, y]


# 转弯显示功能整合数据,接收来自调度的转弯点列表，
# 选择调用相应的转弯算法，并将计算结果添加入列表。
# 将每一个转弯的返回值整合为一个列表。
# 代入数据，一个列表，以及车辆的机具特性。
# 以best_turn_list列表奇偶性分别选择相对应的上边界转弯以及下边界转弯。
# 添加一个奇偶性的变量，这样就可以引导相应的上边界转弯或下边界转弯方式选择。
def All_Turn(x_0, y_0, width, height, row_list, offset_width, path_width, turn_r, all_turn_name):
    all_turn = []
    turn = 0
    top_list, low_list = Rec_turn_point(x_0, y_0, width, height, offset_width, path_width)
    targ = len(row_list)
    for x in range(0, targ - 1):
        A = row_list[x]
        B = row_list[x + 1]
        if x % 2 == 0:
            TOP_EDGE = True
            if top_list[A][0] > top_list[B][0]:
                a, b = top_list[B], top_list[A]
            else:
                a, b = top_list[A], top_list[B]
            if all_turn_name[x] == "T":
                turn = T_turn(a, b, turn_r, TOP_EDGE)
            elif all_turn_name[x] == "T2":
                turn = T2_turn(a, b, turn_r, TOP_EDGE)
            elif all_turn_name[x] == "M":
                turn = M_turn(a, b, turn_r, TOP_EDGE)
            elif all_turn_name[x] == "M2":
                turn = M2_turn(a, b, turn_r, TOP_EDGE)
            elif all_turn_name[x] == "O":
                turn = O_turn(a, b, turn_r, TOP_EDGE)
            elif all_turn_name[x] == "U":
                turn = U_turn(a, b, turn_r, TOP_EDGE)
            elif all_turn_name[x] == "U2":
                turn = U2_turn(a, b, turn_r, TOP_EDGE)
        else:
            TOP_EDGE = False
            if low_list[A][0] > low_list[B][0]:
                a, b = low_list[B], low_list[A]
            else:
                a, b = low_list[A], low_list[B]
            if all_turn_name[x] == "T":
                turn = T_turn(a, b, turn_r, TOP_EDGE)
            elif all_turn_name[x] == "T2":
                turn = T2_turn(a, b, turn_r, TOP_EDGE)
            elif all_turn_name[x] == "M":
                turn = M_turn(a, b, turn_r, TOP_EDGE)
            elif all_turn_name[x] == "M2":
                turn = M2_turn(a, b, turn_r, TOP_EDGE)
            elif all_turn_name[x] == "O":
                turn = O_turn(a, b, turn_r, TOP_EDGE)
            elif all_turn_name[x] == "U":
                turn = U_turn(a, b, turn_r, TOP_EDGE)
            elif all_turn_name[x] == "U2":
                turn = U2_turn(a, b, turn_r, TOP_EDGE)
        all_turn.append(turn)
    return all_turn


def wgs84toutm(Long, Lat):
    grid_size = 100000.0
    WGS84_A = 6378137.0
    WGS84_B = 6356752.31424518
    WGS84_F = 0.0033528107
    WGS84_E = 0.0818191908
    WGS84_EP = 0.0820944379
    UTM_K0 = 0.9996
    UTM_FE = 500000.0
    UTM_FN_N = 0.0
    UTM_FN_S = 10000000.0
    UTM_E2 = (WGS84_E * WGS84_E)
    UTM_E4 = (UTM_E2 * UTM_E2)
    UTM_E6 = (UTM_E4 * UTM_E2)
    UTM_EP2 = (UTM_E2 / (1 - UTM_E2))
    RADIANS_PER_DEGREE = math.pi / 180
    a = WGS84_A
    eccSquared = UTM_E2
    k0 = UTM_K0

    # Make sure the longitude is between -180.00 .. 179.9
    LongTemp = (Long + 180) - int((Long + 180) / 360) * 360 - 180

    LatRad = Lat * RADIANS_PER_DEGREE
    LongRad = LongTemp * RADIANS_PER_DEGREE

    ZoneNumber = int((LongTemp + 180) / 6) + 1

    if ((Lat >= 56.0) & (Lat < 64.0) & (LongTemp >= 3.0) & (LongTemp < 12.0)):
        ZoneNumber = 32

    # Special zones for Svalbard
    if ((Lat >= 72.0) & (Lat < 84.0)):

        if ((LongTemp >= 0.0) & (LongTemp < 9.0)):
            ZoneNumber = 31
        if ((LongTemp >= 9.0) & (LongTemp < 21.0)):
            ZoneNumber = 33
        if ((LongTemp >= 21.0) & (LongTemp < 33.0)):
            ZoneNumber = 35
        if ((LongTemp >= 33.0) & (LongTemp < 42.0)):
            ZoneNumber = 37
    LongOrigin = (ZoneNumber - 1) * 6 - 180 + 3
    LongOriginRad = LongOrigin * RADIANS_PER_DEGREE
    eccPrimeSquared = (eccSquared) / (1 - eccSquared)

    N = a / math.sqrt(1 - eccSquared * math.sin(LatRad) * math.sin(LatRad))
    T = math.tan(LatRad) * math.tan(LatRad)
    C = eccPrimeSquared * math.cos(LatRad) * math.cos(LatRad)
    A = math.cos(LatRad) * (LongRad - LongOriginRad)

    M = a * ((1 - eccSquared / 4 - 3 * eccSquared * eccSquared / 64
              - 5 * eccSquared * eccSquared * eccSquared / 256) * LatRad
             - (3 * eccSquared / 8 + 3 * eccSquared * eccSquared / 32
                + 45 * eccSquared * eccSquared * eccSquared / 1024) * math.sin(2 * LatRad)
             + (15 * eccSquared * eccSquared / 256
                + 45 * eccSquared * eccSquared * eccSquared / 1024) * math.sin(4 * LatRad)
             - (35 * eccSquared * eccSquared * eccSquared / 3072) * math.sin(6 * LatRad))
    UTMEasting = k0 * N * (A + (1 - T + C) * A * A * A / 6 + (5 - 18 * T + T * T + 72 * C - 58 * eccPrimeSquared) \
                           * A * A * A * A * A / 120) + 500000.0

    UTMNorthing = k0 * (M + N * math.tan(LatRad) * (A * A / 2 + (5 - T + 9 * C + 4 * C * C) * A * A * A * A / 24 + \
                                                    (
                                                                61 - 58 * T + T * T + 600 * C - 330 * eccPrimeSquared) * A * A * A * A * A * A / 720))

    if (Lat < 0):
        # 10000000 meter offset for southern hemisphere-0
        UTMNorthing += 10000000.0
    UTMNorthing = UTMNorthing - 3373400
    UTMEasting = UTMEasting - 245000
    #	print(UTMEasting)
    #	print(UTMNorthing)
    return UTMEasting, UTMNorthing


# 实际地块摆正
def Standard_field(x, y):
    x_ = []
    y_ = []
    #	l1 = ((x[1]-x[0])**2+(y[1]-y[0])**2)**.5
    #	l2 = ((x[2]-x[1])**2+(y[2]-y[1])**2)**.5
    #	l3 = ((x[3]-x[2])**2+(y[3]-y[2])**2)**.5
    #	l4 = ((x[4]-x[3])**2+(y[4]-y[3])**2)**.5
    l1 = ((x[1] - x[0]) ** 2 + (y[1] - y[0]) ** 2) ** .5
    l2 = ((x[2] - x[0]) ** 2 + (y[2] - y[0]) ** 2) ** .5
    l3 = ((x[3] - x[0]) ** 2 + (y[3] - y[0]) ** 2) ** .5
    radian1 = math.asin((y[1] - y[0]) / l1)
    if x[2] - x[0] < 0:
        radian2 = math.pi - math.asin((y[2] - y[0]) / l2)
    else:
        radian2 = math.asin((y[2] - y[0]) / l2)
    if x[3] - x[0] < 0:
        radian3 = math.pi - math.asin((y[3] - y[0]) / l3)
    else:
        radian3 = math.asin((y[3] - y[0]) / l3)
    radian1_ = radian1 - radian1
    radian2_ = radian2 - radian1
    radian3_ = radian3 - radian1
    print("radian1", radian1)
    print("radian2", radian2)
    print("radian3", radian3)
    print("radian1_", radian1_)
    print("radian2_", radian2_)
    print("radian3_", radian3_)
    print("l1", l1)
    print("l2", l2)
    print("l3", l3)

    x_.append(20)
    x_.append(20 + l1 * math.cos(radian1_))
    x_.append(20 + l2 * math.cos(radian2_))
    x_.append(20 + l3 * math.cos(radian3_))
    x_.append(20)
    y_.append(20)
    y_.append(20 + l1 * math.sin(radian1_))
    y_.append(20 + l2 * math.sin(radian2_))
    y_.append(20 + l3 * math.sin(radian3_))
    y_.append(20)
    print("x_,y_", x_, y_)
    return x_, y_, radian1


# 数据旋转基础构件
def revert_field(x, y, radian1):
    l = ((x - 20) ** 2 + (y - 20) ** 2) ** .5
    if l == 0:
        x_ = 20
        y_ = 20
    else:
        if x - 20 < 0:
            radian = math.pi - math.asin((y - 20) / l)
        else:
            radian = math.asin((y - 20) / l)
        radian = radian + radian1
        x_ = 20 + l * math.cos(radian)
        y_ = 20 + l * math.sin(radian)
    return x_, y_


# 一级数据结构旋转
def revert_1_field(structure1, radian1):
    x_list = []
    y_list = []
    for x in range(0, len(structure1[0])):
        x_, y_ = revert_field(structure1[0][x], structure1[1][x], radian1)
        x_list.append(x_)
        y_list.append(y_)
    sturct1_ = [x_list, y_list]
    return sturct1_


# 二级数据结构旋转
def revert_2_field(structure2, radian1):
    structure2_ = []
    for x in range(0, len(structure2)):
        x_list = []
        y_list = []
        for y in range(0, len(structure2[x][0])):
            x_, y_ = revert_field(structure2[x][0][y], structure2[x][1][y], radian1)
            x_list.append(x_)
            y_list.append(y_)
        structure2_.append([x_list, y_list])
    return structure2_


# —— —— —— 调度相关 —— —— ——
# 当 (path_width/2) > turn_r，时调用
def U_length(A, B, turn_r):
    O1 = [A[0] + turn_r, A[1]]
    O2 = [B[0] - turn_r, B[1]]
    arc_length = turn_r * math.pi
    O1O2 = ((O1[0] - O2[0]) ** 2 + (O1[1] - O2[1]) ** 2) ** .5
    u_length = arc_length + O1O2
    return u_length


# 当 (path_width/2) == turn_r,时调用
def U2_length(A, B, turn_r):
    O1 = [A[0] + turn_r, A[1]]
    O2 = [B[0] - turn_r, B[1]]
    arc_length = turn_r * math.pi
    line_length = abs(A[1] - B[1])
    u_length = arc_length + line_length
    return u_length


# 当 (path_with/2) < turn_r, 且不可倒车时调用
def O_length(A, B, turn_r):
    O1 = [A[0] - turn_r, A[1]]
    O2 = [B[0] + turn_r, B[1]]
    O1O2 = ((O2[1] - O1[1]) ** 2 + (O2[0] - O1[0]) ** 2) ** .5
    O3C = (2 * turn_r) ** 2 - (O1O2 / 2) ** 2
    O3C = (O3C) ** .5
    radianO312 = math.atan(O3C / (O1O2 / 2))
    o_length = turn_r * math.pi + 4 * turn_r * radianO312
    return o_length


# 当 (path_width/2) < turn_r, 且可直线倒车时调用
def M_length(A, B, turn_r):
    O1 = [A[0] - turn_r, A[1]]
    O2 = [B[0] + turn_r, B[1]]
    O1O2 = ((O2[1] - O1[1]) ** 2 + (O2[0] - O1[0]) ** 2) ** .5
    m_length = math.pi * turn_r + O1O2
    return m_length


# 当 (path_width/2)<turn_r, 且可曲线倒车时调用
def M2_length(A, B, turn_r):
    m2_length = math.pi * turn_r
    return m2_length


# 当 (path_width/2)<turn_r, 且可曲线倒车时调用
def T_length(A, B, turn_r):
    t_length = math.pi * turn_r
    return t_length


# 当 (path_width/2)<turn_r, 且可直线倒车时调用
def T2_length(A, B, turn_r):
    O1 = [A[0] + turn_r, A[1]]
    O2 = [B[0] - turn_r, B[1]]
    O1O2 = ((O2[1] - O1[1]) ** 2 + (O2[0] - O1[0]) ** 2) ** .5
    t2_length = O1O2 + math.pi * turn_r
    return t2_length


# 引入是否可倒车，是否可曲线倒车控制参数（布尔值）
# curve reversing曲线倒车、straight line reversing 直线倒车
# 逻辑上可曲线倒车一定也可以直线倒车。且曲线倒车的转弯距离小于直线倒车的转弯距离。

def Turn_length(A, B, turn_r, curve, straight, not_reverse):
    turn_name = ""
    turn_length = 0
    path_width = B[0] - A[0]
    if (path_width / 2) < turn_r:
        if not_reverse:
            turn_name = "O"
            turn_length = O_length(A, B, turn_r)
        else:
            if curve:
                t2_length = T2_length(A, B, turn_r)
                m_length = M_length(A, B, turn_r)
                t_length = T_length(A, B, turn_r)
                m2_length = M2_length(A, B, turn_r)
                turn_length = min(t2_length, m_length, t_length, m2_length)
                if turn_length == m2_length:
                    turn_name = "M2"
                elif turn_length == m_length:
                    turn_name = "M"
                elif turn_length == t_length:
                    turn_name = "T"
                elif turn_length == t2_length:
                    turn_name = "T2"
            elif straight:
                t2_length = T2_length(A, B, turn_r)
                m_length = M_length(A, B, turn_r)
                turn_length = min(t2_length, m_length)
                if turn_length == t2_length:
                    turn_name = "T2"
                elif turn_length == m_length:
                    turn_name = "M"
    elif (path_width / 2) > turn_r:
        turn_name = "U"
        turn_length = U_length(A, B, turn_r)
    #  (path_width/2) == turn_r
    else:
        turn_name = "U2"
        turn_length = U2_length(A, B, turn_r)
    return turn_name, turn_length


# 统计整个作业的长度方面信息。包括实际作业路径长度，
# 非作业路径长度。
def All_length():
    pass