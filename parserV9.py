#!/usr/bin/python

from operator import itemgetter
import sys
import random
import math

duplications = 0
signalssent = 0


file = open("repel.txt","w")

pcounter = 0
dcounter = 0
ccounter = 0
mcounter = 0
scounter = 0
acounter = 0
rcounter = 0

p_dic = {}
cell_z_vals = {}
d_dic = {}
c_dic = {}
l_dic = {}
line_count = 0
for line in sys.stdin:
    if line_count != 0:
        continue
    line_count += 1
    cell_vals = line.split(" ")
    #split cells into their own component arrays
    #NOTE: FIX THIS TO MAKE THE CODE MORE SPACE EFFECIENT
    p_cell_vals = cell_vals[0:256]
    print(len(p_cell_vals))
    d_cell_vals = cell_vals[256:512]
    c_cell_vals = cell_vals[512:768]
    m_cell_vals = cell_vals[768:1024]
    s_cell_vals = cell_vals[1024:1280]
    a_cell_vals = cell_vals[1280:1536]
    r_cell_vals = cell_vals[1536:1792]
    l_cell_vals = cell_vals[1792:2048]
    #not lesion cells are ignored because thats not necessary for observation

    #Add Precursor cells
    i = 0
    for p in p_cell_vals:
        if int(p) > 0:
            y = (i % 16)*10 - 75
            x = (i // 16)*10 - 75
            z = random.uniform(-5.0,5.0)
            cell_z_vals[str(pcounter)] = z
            file.write("birth P "+str(pcounter)+" "+str(float(x))+","+str(float(y))+","+str(float(z))+'\n')
            #store opc by grid cell location
            key = repr([(i // 16),(i % 16)])

            if key in p_dic:
                p_dic[key].append(pcounter)
            else:
                p_dic[key] = [pcounter]


            pcounter = pcounter + 1
        i = i + 1

    #Add Duplication cells
    i = 0
    for d in d_cell_vals:
        if int(d) > 0:
            y = (i % 16)*10 - 75
            x = (i // 16)*10 - 75
            #file.write("birth D "+str(pcounter)+" "+str(float(x))+","+str(float(y))+'\n')
            pcounter = pcounter + 1
        i = i + 1

    #Add moving cells
    i = 0
    for c in c_cell_vals:
        if int(c) > 0:
            y = (i % 16)*10 - 75
            x = (i // 16)*10 - 75
            #file.write("birth C "+str(pcounter)+" "+str(float(x))+","+str(float(y))+'\n')
            pcounter = pcounter + 1
        i = i + 1

    #Add maturecells are
    i = 0
    for m in m_cell_vals:
        if int(m) > 0:
            y = (i % 16)*10 - 75
            x = (i // 16)*10 - 75
            cell_z_vals[str(pcounter)] = z
            file.write("birth P "+str(pcounter)+" "+str(float(x))+","+str(float(y))+","+str(float(z))+'\n')
            pcounter = pcounter + 1
        i = i + 1

    #Add inactive signals
    i = 0
    for s in s_cell_vals:
        if int(s) > 0:
            y = (i % 16)*10 - 75
            x = (i // 16)*10 - 75
            #file.write("birth S "+str(pcounter)+" "+str(float(x))+","+str(float(y))+'\n')
            pcounter = pcounter + 1
        i = i + 1

    #Add Attractor signals
    i = 0
    for a in a_cell_vals:
        if int(a) > 0:
            y = (i % 16)*10 - 75
            x = (i // 16)*10 - 75
            #file.write("birth A "+str(pcounter)+" "+str(float(x))+","+str(float(y))+'\n')
            pcounter = pcounter + 1
        i = i + 1

    #Add Repellant signals
    i = 0
    for r in r_cell_vals:
        if int(r) > 0:
            y = (i % 16)*10 - 75
            x = (i // 16)*10 - 75
            #file.write("birth R "+str(pcounter)+" "+str(float(x))+","+str(float(y))+'\n')
            pcounter = pcounter + 1
        i = i + 1

    #Add lesions
    i = 0
    for l in l_cell_vals:
        if int(l) > 0:
            y = (i % 16)*10 - 75
            x = (i // 16)*10 - 75
            file.write("birth L "+str(pcounter)+" "+str(float(x))+","+str(float(y))+'\n')
            #NOTE: SAME HERE
            key = repr([(i // 16),(i % 16)])
            if key in p_dic:
                print("OVERLAPPING OPC AND LESION AT "+key)
            if key in d_dic:
                d_dic[key].append(pcounter)
            else:
                d_dic[key] = [pcounter]
            pcounter = pcounter + 1
        i = i + 1

#write that setup is finished and pause playBack
file.write("finished_setup\n")
print("CONFIG OK")
cell_id_counter = 3000

# for key in p_dic:
#     print(key)
trace = open("meta_files/JustRepellent.txt","r")
trace.seek(0)


#give each differentiated cell a seperate target coordinate so overlap of Oligodendrocytes is not so drastic
# def getTargetDiffPosition(x, y, num_diff_in_cell):
#     x -= 5
#     y -= 5
#     x += (num_diff_in_cell % 2)*5 + 1
#     y += ((num_diff_in_cell % 2))*5 + 1
#     return [x,y]

#PROTOTYPE for differentiated cells
def getTargetDiffPosition(x, y, num_opc_in_cell):
    x -= 5
    y -= 5
    rand_x = random.uniform(0,10)
    rand_y = random.uniform(0,10)
    rand_z = random.uniform(-5.0,5.0)
    return [x+rand_x, y+rand_y, rand_z]
#give each cell a seperate target coordinate so overlap of OPC is not so drastic
# def getTargetPosition(x, y, num_opc_in_cell):
#     x -= 5
#     y -= 5
#     x += (num_opc_in_cell % 5)*2 + 1
#     y += ((num_opc_in_cell % 25) // 5)*2 + 1
#     return [x,y]

#Random position in cell PROTOTYPE
#last arguement not necessary just used to avoid changing other code
def getTargetPosition(x, y, num_opc_in_cell):
    x -= 5
    y -= 5
    rand_x = random.uniform(0,10)
    rand_y = random.uniform(0,10)
    rand_z = random.uniform(-5.0,5.0)
    return [x+rand_x, y+rand_y, rand_z]

#path interpolation of a moving OPC
def getPath(x_start, y_start, z_start, x_end, y_end, z_end, time_taken):
    #print("IN PATH")
    #print("X START "+str(x_start))
    #print("Y START "+str(y_start))
    #print("X END "+str(x_end))
    #print("Y END "+str(y_end))
    #print("TIME "+str(time_taken))
    x_path = []
    y_path = []
    z_path = []



    if (time_taken < 0.01):
        divi = 2
    elif (time_taken < 0.1):
        divi = 6
    else:
        divi = 10

    dz = abs(z_start - float(z_end))/float(divi)
    if (dz < 0.01):
        dz = 0.01
    dx = abs(x_start - float(x_end))/float(divi)
    if (dx < 0.01):
        dx = 0.01
    dy = abs(y_start - float(y_end))/float(divi)
    if (dy < 0.01):
        dy = 0.01
    #print("DX "+str(dx))
    #print("DY "+str(dy))

    if dx < 0.01:
        dx = 0
    if dy < 0.01:
        dy = 0
    if dz < 0.01:
        dz = 0

    x = x_start
    y = y_start
    z = z_start
    #print("STARTED X")
    if (x_end > x_start):
        while ((x < x_end) and ((x_end - x) > 0.01)):
            x+=dx
            x_path.append(x)
    else:
        while ((x > x_end)  and ((x - x_end) > 0.01)):
            x-=dx
            x_path.append(x)
    #print("FINISHED X")
    #print("STARTED Y")
    if(y_end > y_start):
        #for y in range(y_start, y_end):
        while ((y < y_end)  and ((y_end - y) > 0.01)):
            y+=dy
            y_path.append(y)
    else:
        while ((y > y_end)  and ((y - y_end) > 0.01)):
            y-=dy
            y_path.append(y)


    if(z_end > z_start):
        #for y in range(y_start, y_end):
        while ((z < z_end)  and ((z_end - z) > 0.01)):
            z+=dz
            z_path.append(z)
    else:
        while ((z > z_end)  and ((z - z_end) > 0.01)):
            z-=dz
            z_path.append(z)
    #print("FINISHED Y")

    if len(x_path) == 0:
        x_path.append(x_end)
    if len(y_path) == 0:
        y_path.append(y_end)
    if len(z_path) == 0:
        z_path.append(z_end)

    if (len(z_path) > len(x_path)) and (len(z_path) > len(y_path)):
        if len(x_path) > len(y_path):
            for z in range(0, len(x_path)-len(y_path)):
                y_path.append(y_path[len(y_path)-1])
            for z in range(0, len(z_path)-len(x_path)):
                x_path.append(x_path[len(x_path)-1])
                y_path.append(y_path[len(y_path)-1])
        else:
            for z in range(0, len(y_path)-len(x_path)):
                x_path.append(x_path[len(x_path)-1])
            for z in range(0, len(z_path)-len(y_path)):
                x_path.append(x_path[len(x_path)-1])
                y_path.append(y_path[len(y_path)-1])
    else:
        if len(x_path) > len(y_path):
            if (len(y_path) < len(z_path)):
                for z in range(0, len(z_path)-len(y_path)):
                    y_path.append(y_path[len(y_path)-1])
            else:
                for z in range(0, len(y_path)-len(z_path)):
                    z_path.append(z_path[len(z_path)-1])
            for z in range(0, len(x_path)-len(z_path)):
                z_path.append(z_path[len(z_path)-1])
                y_path.append(y_path[len(y_path)-1])
        else:
            if (len(x_path) < len(z_path)):
                for z in range(0, len(x_path)-len(x_path)):
                    x_path.append(x_path[len(x_path)-1])
            else:
                for z in range(0, len(x_path)-len(z_path)):
                    z_path.append(z_path[len(z_path)-1])
            for z in range(0, len(z_path)-len(y_path)):
                x_path.append(x_path[len(x_path)-1])
                y_path.append(y_path[len(y_path)-1])
    #print("FINISHED PATH")
    return x_path, y_path, z_path

#make static OPC grow in size as an animation similar to actual mitosis
def getGrowth(start_time, end_time, key, x, y, cell_id_counter):

    cell = p_dic[key][0]
    z = cell_z_vals[str(cell)]
    delta_time = end_time - start_time

    increment = delta_time/10

    rand_direction = random.uniform(0, 2*math.pi)
    rand_z_dir = random.uniform(0, 2*math.pi)
    x_inc = 0.3*math.sin(rand_direction)
    if (abs(x_inc) < 0.03):
        x_inc = 0
    y_inc = 0.3*math.cos(rand_direction)
    if(abs(y_inc) < 0.03):
        y_inc = 0
    z_inc = 0.3*math.sin(rand_z_dir)
    if(abs(z_inc) < 0.03):
        z_inc = 0

    if key in p_dic:
        p_dic[key].append(cell_id_counter+1)
        output.append((start_time,("birth P "+str(cell_id_counter)+" "+str(float(x))+","+str(float(y))+","+str(float(z))+'\n')))
    else:
        print("INVALID DUPLICATION AT "+key)

    new_time = start_time
    for i in range(0,5):
        output.append((new_time, ("grow "+str(cell)+"\n")))
        output.append((new_time, ("grow "+str(cell_id_counter)+"\n")))
        new_time += increment

    for i in range(0,5):
        output.append((new_time, ("shrink "+str(cell)+"\n")))
        output.append((new_time, ("shrink "+str(cell_id_counter)+"\n")))
        output.append((new_time, ("move "+str(cell_id_counter)+" "+str(float(x))+","+str(float(y))+","+str(float(z))+"\n")))
        new_time += increment
        y+=y_inc
        x+=x_inc
        z+=z_inc
    output.append((new_time, ("die P "+str(cell_id_counter)+" "+str(float(x))+","+str(float(y-0.4))+","+str(float(z))+'\n')))
    output.append((new_time,("birth S "+str(cell_id_counter+1)+" "+str(float(x))+","+str(float(y))+","+str(float(z))+'\n')))
    #print("ADDING "+str(cell_id_counter))
    moving_cell_pos[cell_id_counter+1] = [float(x), float(y-1)]
    cell_z_vals[str(cell_id_counter+1)] = float(z)
    #print("ADDED "+str(x)+" "+str(y-1))

def repair_process(lesion, init_time, end_time):
    d_time = (end_time - init_time)/float(10)
    c_time = init_time
    for i in range(0,5):
        output.append((c_time, ("partial "+str(lesion)+'\n')))
        print(str(c_time))
        c_time+=d_time


output = []
moving_cell_pos = {}
moving_cells = {}
num_diff_cells_in_square = {}
in_duplication = {}
in_repairing = {}
signal_list={}
time_list = []
counter = 0
time = 0;
last_time = 0;
#After initial setup we parse the meta file
for line in trace:
    counter += 1
    line = line.strip()
    comps = line.split()
    time = float(comps[0])
    if (time - last_time) > 0.1:
        output.append((time, "time "+str(time)+"\n"))
        last_time = time

    #while(len(time_list) != 0 and time_list[0] < time):
    #    del moving_cells[0]
    #    del time_list[0]
    #print(comps)
    if comps[1][:3] == "dup":

        cell_x = int(comps[7])
        cell_y = int(comps[8])
        x_start = cell_x*10 - 75
        y_start = cell_y*10 - 75
        key = repr([cell_x, cell_y])
        getGrowth(in_duplication[key], time, key, x_start, y_start, cell_id_counter)
        cell_id_counter+=2
        duplications+=1
        del in_duplication[key]
        # if key in p_dic:
        #     p_dic[key].append(cell_id_counter)
        #     output.append((time,("birth S "+str(cell_id_counter)+" "+str(float(x_start))+","+str(float(y_start))+'\n')))
        #     cell_id_counter+=1
        # else:
        #     print("INVALID DUPLICATION AT "+key)


    elif comps[1][:6] == "repair":
        cell_x = int(comps[7])
        cell_y = int(comps[8])
        x_start = cell_x*10 - 75
        y_start = cell_y*10 - 75
        key = repr([cell_x, cell_y])

        if key in d_dic:
            les = d_dic[key].pop()
        repair_process(les, in_repairing[key], time)
        #output.append("die "+str(opc)+'\n')
        output.append((time, ("repair "+str(les)+" "+str(x_start)+","+str(y_start)+'\n')))
        if key in signal_list:
            if signal_list[key] == "attract" or signal_list[key] == "repulse":
                output.append((time, ("remove_source "+comps[7]+","+comps[8]+" "+signal_list[key]+"\n")))
                del signal_list[key]
            else:
                print("NON IDENTIFIED SIGNAL: "+signal_list[key])
                sys.exit()
        else:
            print("HAHA you tried to repair a non-existent cell")
            sys.exit()

    elif (comps[1][:4] == "diff"):
        cell_x = int(comps[7])
        cell_y = int(comps[8])
        x_e = cell_x*10 - 75
        y_e = cell_y*10 - 75
        key = repr([cell_x, cell_y])

        if not key in in_repairing:
            in_repairing[key] = time
        #try and get one normal thing
        if key in p_dic:
            print(str(p_dic[key]))
            opc = p_dic[key].pop()
            z_val = cell_z_vals[str(opc)]
            del cell_z_vals[str(opc)]
            #update the number differentiated cells in a square
            if key in num_diff_cells_in_square:
                num_diff_cells_in_square[key]+=1
            else:
                num_diff_cells_in_square[key] = 1

            output.append((time, ("die S "+str(opc)+" "+str(x_e)+","+str(y_e)+","+str(z_val)+'\n')))
            x_e, y_e, z_e = getTargetDiffPosition(x_e, y_e, num_diff_cells_in_square[key])
            cell_id_counter+=1
            output.append((time, ("birth M "+str(cell_id_counter)+" "+str(x_e)+","+str(y_e)+","+str(z_e)+'\n')))
            cell_id_counter+=1

        #otherwise get one from the moving list
        elif key in moving_cells:
            start_time, opc = moving_cells[key][0]
            del moving_cells[key][0]

            num_opc_in_cell = 0

            if moving_cells[key] == []:
                del moving_cells[key]

            #x_start = cell_x*10 - 75
            #y_start = cell_y*10 - 75
            #print("GETTING "+str(opc))
            [x_start, y_start] = moving_cell_pos[opc]
            z_val = cell_z_vals[str(opc)]
            #print("GOT "+str(x_start)+" "+str(y_start))
            x_end, y_end, z_end = getTargetPosition(x_e, y_e, num_opc_in_cell)
            path = getPath(x_start, y_start, z_val, x_end, y_end, z_end, (time - start_time))
            dtime = (time - start_time)/float(len(path[0]))
            for x in range(0, len(path[0])):
                start_time += dtime
                output.append((start_time, ("move "+str(opc)+" "+str(float(path[0][x]))+","+str(float(path[1][x]))+","+str(float(path[2][x]))+'\n')))

            last_x = float(path[0][-1])
            last_y = float(path[1][-1])
            last_z = float(path[2][-1])
            #print("DOING: "+str(last_x)+" "+str(last_y))
            moving_cell_pos[opc] = [last_x, last_y]
            cell_z_vals[str(opc)] = last_z
            #print("DONE")
            #moving_cell_pos[opc] = [1,1]

            #update the number differentiated cells in a square
            if key in num_diff_cells_in_square:
                num_diff_cells_in_square[key]+=1
            else:
                num_diff_cells_in_square[key] = 1

            output.append((time+dtime, ("die S "+str(opc)+" "+str(x_e)+","+str(y_e)+","+str(z_val)+'\n')))
            x_e, y_e, z_e = getTargetDiffPosition(x_e, y_e, num_diff_cells_in_square[key])
            output.append((time, ("birth M "+str(cell_id_counter)+" "+str(x_e)+","+str(y_e)+","+str(z_e)+'\n')))
            cell_id_counter+=1

        #otherwise we're fucked
        else:
            print("ERROR!ERROR!MALFUNCTION!ERROR!EXTERMINATE!")
            sys.exit()
        print("die "+str(opc))

    elif comps[1][:5] == "helpA":
        cell_x = int(comps[7])
        cell_y = int(comps[8])
        x_start = cell_x*10 - 75
        y_start = cell_y*10 - 75
        key = repr([cell_x, cell_y])
        in_duplication[key] = time
        signalssent+=1

        # if key in p_dic:
        #     p_dic[key].append(cell_id_counter)
        #     output.append((time,("birth S "+str(cell_id_counter)+" "+str(float(x_start))+","+str(float(y_start))+'\n')))
        #     cell_id_counter+=1
        # else:
        #     print("INVALID DUPLICATION AT "+key)
        #
        # output.append((time,("attract "+str(float(x_start))+","+str(float(y_start))+'\n')))

    elif comps[1][:5] == "helpR":
        cell_x = int(comps[7])
        cell_y = int(comps[8])
        x_start = cell_x*10 - 75
        y_start = cell_y*10 - 75
        key = repr([cell_x, cell_y])
        in_duplication[key] = time
        signalssent+=1


        # if key in p_dic:
        #     p_dic[key].append(cell_id_counter)
        #     output.append((time,("birth S "+str(cell_id_counter)+" "+str(float(x_start))+","+str(float(y_start))+'\n')))
        #     cell_id_counter+=1
        # else:
        #     print("INVALID DUPLICATION AT "+key)
        #
        # output.append((time,("repulse "+str(float(x_start))+","+str(float(y_start))+'\n')))

    elif comps[1][:6] == "helpSR":
        if comps[3] == "NoChange":
            continue

        cell_x = int(comps[7])
        cell_y = int(comps[8])
        key = repr([cell_x, cell_y])
        if key in d_dic:

            if key in signal_list:
                if signal_list[key] == "repulse":
                    continue
                else:
                    output.append((time, ("remove_source "+comps[7]+","+comps[8]+" attract\n")))
                    del signal_list[key]

            output.append((time,("source_repulse "+comps[7]+","+comps[8]+"\n")))
            signal_list[key]= "repulse"

        else:
            print("SIGNAL FROM "+key+" \WITH NO LESION CELL PRESENT")

    elif comps[1][:6] == "helpS":
        if comps[3] == "NoChange":
            continue

        cell_x = int(comps[7])
        cell_y = int(comps[8])
        key = repr([cell_x, cell_y])
        if key in d_dic:

            if key in signal_list:
                if signal_list[key] == "attract":
                    continue
                else:
                    output.append((time, ("remove_source "+comps[7]+","+comps[8]+" repulse\n")))
                    del signal_list[key]

            output.append((time,("source_attract "+comps[7]+","+comps[8]+"\n")))
            signal_list[key] = "attract"
        else:
            print("SIGNAL FROM "+key+" \WITH NO LESION CELL PRESENT")


    elif comps[1][:4] == "come" or comps[1][:4] == "away":
        time = float(comps[0])
        #get start cell
        cell_x = int(comps[7])
        cell_y = int(comps[8])

        #get end cell
        target_x = int(comps[9])
        target_y = int(comps[10])
        #create key
        key = repr([cell_x, cell_y])
        t_key = repr([target_x, target_y])

        if key == t_key:
            continue
        #print(p_dic)
        #print(p_dic[key])
        #print(p_dic[t_key])
        #get the opc being reffered to
        if key in moving_cells:
            start_time, opc = moving_cells[key][0]
            z_val = cell_z_vals[str(opc)]
            del moving_cells[key][0]

            num_opc_in_cell = 0
            #add it to the new cell
            if t_key in moving_cells:
                num_opc_in_cell += len(moving_cells[t_key])
                moving_cells[t_key].append((time, opc))
            else:
                moving_cells[t_key] = [(time, opc)]

            if moving_cells[key] == []:
                del moving_cells[key]

            if t_key in p_dic:
                num_opc_in_cell += len(p_dic[t_key])
            #x_start = cell_x*10 - 75
            #y_start = cell_y*10 - 75
            #print("GETTING "+str(opc))
            [x_start, y_start] = moving_cell_pos[opc]
            #print("GOT "+str(x_start)+" "+str(y_start))
            x_e = target_x*10 - 75
            y_e = target_y*10 - 75
            x_end, y_end, z_end= getTargetPosition(x_e, y_e, num_opc_in_cell)
            path = getPath(x_start, y_start, z_val, x_end, y_end, z_end, (time - start_time))
            dtime = (time - start_time)/float(len(path[0]))
            for x in range(0, len(path[0])):
                start_time += dtime
                output.append((start_time, ("move "+str(opc)+" "+str(float(path[0][x]))+","+str(float(path[1][x]))+","+str(float(path[2][x]))+'\n')))

            last_x = float(path[0][-1])
            last_y = float(path[1][-1])
            last_z = float(path[2][-1])
            #print("DOING: "+str(last_x)+" "+str(last_y))
            moving_cell_pos[opc] = [last_x, last_y]
            cell_z_vals[str(opc)] = last_z
            #print("DONE")
            #moving_cell_pos[opc] = [1,1]

        elif key in p_dic:
            #remove it from its current cell
            opc = p_dic[key][0]
            x = 0

            while(opc < 256):
                if (x >= (len(p_dic[key]))):
                    print("LINE: "+str(counter)+"\nINVALID MOVE COMMAND AT: "+key+"\nLIST: "+str(p_dic[key])+"\nMOVING CELLS: "+str(moving_cells))
                    sys.exit()
                else:
                    opc = p_dic[key][x]
                    x+=1
            if (x!=0):
                del p_dic[key][x-1]
            else:
                del p_dic[key][x]
            if p_dic[key] == []:
                del p_dic[key]



            #add it to the new cell
            if t_key in moving_cells:
                moving_cells[t_key].append((time, opc))
            else:
                moving_cells[t_key] = [(time, opc)]
        else:
            print("ERROR: OPC does not exist in cell: "+key+" at Line: "+str(counter))
            sys.exit()
            #output.append("move "+str(opc)+" "+str(float(x_end))+","+str(float(y_end))+'\n')


output.sort(key=lambda tup: tup[0])

#get final time for progress bar
last_time = output[len(output)-1][0]
length_time = (0, ("LENGTH "+str(last_time)+"\n"))
output = [length_time] + output
#optimising pass to remove all cells that are caught round the edges or not there at all
def optimisise():
    for key in p_dic:
        for opc in p_dic[key]:
            print("NO")

#optimise()
file.seek(0,2)

for line in output:
    file.write(line[1])

print("DUPS: "+str(duplications)+" SIGNALS: "+str(signalssent))
