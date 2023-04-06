import math
import time
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import filedialog

class cars:
    def __init__(self, position, wheel, horizontal):
        self.position = position  
        self.wheel = wheel
        self.horizontal = horizontal

    def drive(self):
        wheel_radian = math.radians(self.wheel)
        horizontal_radian = math.radians(self.horizontal)
        self.position[0] = self.position[0] + math.cos(wheel_radian+horizontal_radian) + math.sin(wheel_radian)*math.sin(horizontal_radian)
        self.position[1] = self.position[1] + math.sin(wheel_radian+horizontal_radian) - math.sin(wheel_radian)*math.cos(horizontal_radian)
        horizontal_radian = horizontal_radian - math.asin(2*math.sin(wheel_radian)/6)
        self.horizontal = math.degrees(horizontal_radian)

    def turn(self, angle):
        tmp = angle
        if( (-40) <= tmp and tmp <= 40 ):
            self.wheel = tmp
        else:
            print("illegal wheel angle")

def inrange(point,margin1,margin2):

    x1 = margin1[0]
    x2 = margin2[0]
    if(x1>x2):
        t = x1
        x1 = x2
        x2 = t
    
    y1 = margin1[1]
    y2 = margin2[1]
    if(y1>y2):
        t = y1
        y1 = y2
        y2 = t
    
    if(x1 <= point[0] and point[0] <= x2):
        if(y1 <= point[1] and point[1] <= y2):
            return True
        return False
    else:
        return False

def direction(start,end,horizontal):

    if( -90 < horizontal and horizontal < 0 ):
        if(end[0]-start[0] > 0):
            if(end[1]-start[1] < 0):
                return True
    elif( horizontal == 0 ):
        if(end[0]-start[0] > 0):
                return True
    elif( 0 < horizontal and horizontal < 90 ):
        if(end[0]-start[0] > 0):
            if(end[1]-start[1] > 0):
                return True
    elif( horizontal == 90 ):
         if(end[1]-start[1] > 0):
                return True
    elif( 90 < horizontal and horizontal < 180 ):
        if(end[0]-start[0]<0):
            if(end[1] - start[1] > 0):
                return True
    elif( horizontal == 180 ):
        if(end[0]-start[0] < 0):
                return True
    elif( 180 < horizontal and horizontal < 270 ):
        if(end[0]-start[0]<0):
            if(end[1] - start[1] < 0):
                return True
    elif( horizontal == 270 or horizontal == -90):
        if(end[1]-start[1] < 0):
                return True
    
    return False

def collision(wall,car_position):
    #print("detect")
    for i in range(len(wall)-1):
        a = 0
        b = 0
        d = 4
        if(wall[i][0]-wall[i+1][0] == 0):
            a = 1
            b = 0
            c = wall[i][0]*-1
        elif(wall[i][1]-wall[i+1][1] == 0):
            a = 0
            b = 1
            c = wall[i][1]*-1
        else:
            a = wall[i][1]-wall[i+1][1]
            b = (wall[i][0]-wall[i+1][0])*-1
            c = (a*wall[i][0]+b*wall[i][1])*-1
        d = abs(a*car_position[0]+b*car_position[1]+c)/(a**2+b**2)**0.5
        #print(i,d,[ (b**2*car_position[0]-a*b*car_position[1]-a*c)/(a**2+b**2), (-1*a*b*car_position[0]+a**2*car_position[1]-b*c)/(a**2+b**2) ])
        if(d<3 and inrange([ (b**2*car_position[0]-a*b*car_position[1]-a*c)/(a**2+b**2), (-1*a*b*car_position[0]+a**2*car_position[1]-b*c)/(a**2+b**2) ],wall[i],wall[i+1])):
            return True
    return False

def sensor_distance(wall,car_horizontal,car_position):

    first = True
    min_d=0
    xy=[]
    for i in range(len(wall)-1):
        x = 0
        y= 0
        if(car_horizontal == 90 or car_horizontal == 270 ):
            if(wall[i][0]-wall[i+1][0] == 0):
                continue
            x = car_position[0]
            k2 = (wall[i][1]-wall[i+1][1]) / (wall[i][0]-wall[i+1][0])
            c2 = wall[i][1] - k2 * wall[i][0]
            y = k2 * x + c2
        elif(car_horizontal == 0 or car_horizontal == 180):
            if(wall[i][1]-wall[i+1][1] == 0):
                continue
            y = car_position[1]
            k2 = (wall[i][1]-wall[i+1][1]) / (wall[i][0]-wall[i+1][0])
            c2 = wall[i][1] - k2 * wall[i][0]
            x = (y - c2)/ k2
        elif(wall[i][0]-wall[i+1][0] == 0):
            #car cant be horizontal 
            x = wall[i][0]
            k1 = math.tan(math.radians(car_horizontal))
            c1 = car_position[1] - k1 * car_position[0]
            y = k1 * x + c1
        elif(wall[i][1]-wall[i+1][1] == 0):
            #car cant be horizontal
            y = wall[i][1]
            k1 = math.tan(math.radians(car_horizontal))
            c1 = car_position[1] - k1 * car_position[0]
            x = (y - c1)/ k1     
        else:
            k1 = math.tan(math.radians(car_horizontal))
            k2 = (wall[i][1]-wall[i+1][1]) / (wall[i][0]-wall[i+1][0])
            c1 = car_position[1] - k1 * car_position[0]
            c2 = wall[i][1] - k2 * wall[i][0]
            x = (-1 * (c1 - c2)) / (k1 - k2)
            y = k1 * x + c1

        if(inrange([x,y],wall[i],wall[i+1])):
            if(direction(car_position,[x,y],car_horizontal)):
                d_x = x -car_position[0]
                d_y = y - car_position[1]
                d = d_x**2 + d_y**2
                d = d ** 0.5
                if(first):
                    min_d = d
                    xy = [x,y]
                    first = False
                elif(d<min_d):
                    min_d = d
                    xy = [x,y]
    #print(min_d,xy)
    return(min_d)

class weights:
    def __init__(self, weight, weight_out, max_angle, min_angle,max_distance,min_distance):
        self.weight = weight  
        self.weight_out = weight_out
        self.max_angle = max_angle
        self.min_angle = min_angle
        self.max_distance = max_distance
        self.min_distance = min_distance

def normalize(max_data,min_data,data):
    return (data-min_data)/(max_data-min_data)

def denormalize(max_data,min_data,normalized_data):
    return (max_data-min_data)*normalized_data + min_data

def sigmoid(x):
    z = math.exp(-x)
    sig = 1 / (1 + z)
    return sig

def foreward(weight,weight_output,data):
    y = [] 
    for w in weight:
            y.append( sigmoid(-1*w[0]+data[0]*w[1]+data[1]*w[2]+data[2]*w[3]) )
    
    output = -1*weight_output[0]
    for i in range(len(y)):
        output = output + y[i]*weight_output[i+1]
    output = sigmoid(output)

    y.append(output)

    return y

def mlp(node_num,learning_rate,filepath):

    file = open(filepath,mode='r')
    datas = []
    max_angle = -40
    min_angle = 40
    max_distance = 0
    min_distance = 100
    for line in file:
        for i in range(3):
            distance = float(line.split(" ")[i])
            if(distance>max_distance):
                max_distance = distance
            if(distance<min_distance):
                min_distance = distance
        angle = float(line.split(" ")[3])
        if(angle > max_angle):
            max_angle = angle
        if(angle < min_angle):
            min_angle = angle
    file.close()

    file = open(filepath,mode='r')
    for line in file:
        datas.append([normalize(max_distance,min_distance,float(line.split(" ")[0])), normalize(max_distance,min_distance,float(line.split(" ")[1])), normalize(max_distance,min_distance,float(line.split(" ")[2])), round(float(line.split(" ")[3]),0)])
    file.close()

    # init
    weight = []
    weight_output = []
    for i in range(0,node_num):
        weight.append([-1, -1, -1, -1])

    for i in range(0,node_num+1):
        weight_output.append( -1 )

    deviation = True
    epoch = 0

    while(epoch<100 and deviation):
        #print(epoch)
        #deviation = False
        epoch = epoch+1

        for data in datas:
            # foreward
            y = foreward(weight,weight_output,data)

            # Back propagation
            output = y[len(y)-1]
            delta_output = (normalize(max_angle,min_angle,data[3])-output)*output*(1-output)
            delta = []
            for i in range(0,len(y)-1):
                delta.append( y[i]*(1-y[i])*delta_output*weight_output[i+1] )

            for i in range(len(weight)):
                weight[i][0] = weight[i][0] + learning_rate * delta[i] * -1
                weight[i][1] = weight[i][1] + learning_rate * delta[i] * data[0]
                weight[i][2] = weight[i][2] + learning_rate * delta[i] * data[1]
                weight[i][3] = weight[i][3] + learning_rate * delta[i] * data[2]

            weight_output[0] = weight_output[0] + learning_rate * delta_output * -1
            for i in range(1,len(weight_output)):
                weight_output[i] = weight_output[i] + learning_rate * delta_output * y[i-1]

            # if <10 angle no longer training
            #y = foreward(weight,weight_output,data)
            #if( abs( y[len(y)-1]-normalize(max_angle,min_angle,data[3]) ) > 0.125 ):
            #    deviation = True
    
    result = weights(weight,weight_output,max_angle,min_angle,max_distance,min_distance)
    return result

def graph(filepath1,filepath2,result1_label):

    result = mlp(12,0.3,filepath2)
    result1_label.configure(text='Traing:OK')

    car = None
    goal = []
    wall = []
    file = open(filepath1,mode='r')

    init_parameter = []
    count_line = 1
    for line in file:
        if(count_line==1):
            init_parameter.append(int(line.split(",")[0]))
            init_parameter.append(int(line.split(",")[1]))
            init_parameter.append(0)
            init_parameter.append(int(line.split(",")[2]))
            car = cars( [init_parameter[0],init_parameter[1] ], init_parameter[2]  , init_parameter[3] )
        elif(count_line<=3):
            goal.append( [int(line.split(",")[0]),int(line.split(",")[1])] )
        else:
            wall.append( [int(line.split(",")[0]),int(line.split(",")[1])] )
        count_line = count_line + 1

    plt.ion()

    figure, ax = plt.subplots(figsize=(10, 8))
    sensor_txt = figure.text( 0.02, 0.5, "Front: 0\nRight45: 0\nLeft45: 0", fontsize=10)
    figure.subplots_adjust(left=0.25)

    x = car.position[0]
    y = car.position[1]
    point, = ax.plot(car.position[0],car.position[1], color='red', marker='o')
    lbl_point = ax.text(car.position[0],car.position[1],str(car.position),fontsize =10)

    draw_circle = plt.Circle((car.position[0],car.position[1]), 3,fill=False, color='red')
    ax.add_patch(draw_circle)
    
    direct_x = [car.position[0],car.position[0]+ 4*math.cos(math.radians(car.horizontal))]
    direct_y = [car.position[1],car.position[1]+ 4*math.sin(math.radians(car.horizontal))]
    direct, =  ax.plot(direct_x,direct_y, color='red')

    goal_zone = [ goal[0], [goal[0][0],goal[1][1]], goal[1], [goal[1][0],goal[0][1]], goal[0] ]
    #print(goal_zone)
    for i in range(len(goal_zone)-1):
        goalx = [goal_zone[i][0], goal_zone[i+1][0]]
        goaly = [goal_zone[i][1], goal_zone[i+1][1]]
        #print(goalx,goaly)
        ax.plot(goalx,goaly, color='green')

    for i in range(len(wall)-1):
        wallx = [wall[i][0], wall[i+1][0]]
        wally = [wall[i][1], wall[i+1][1]]
        #print(wallx,wally)
        ax.plot(wallx,wally, color='blue')
    
    walkpath_4d=""
    walkpath_6d=""
    input()
    while(1):
        front_d = round(sensor_distance(wall,car.horizontal,car.position),4)
        right_d = round(sensor_distance(wall,car.horizontal-45,car.position),4)
        left_d = round(sensor_distance(wall,car.horizontal+45,car.position),4)

        data = [front_d, right_d, left_d]
        y = foreward(result.weight,result.weight_out,data)
        output = y[len(y)-1]
        output= denormalize(result.max_angle,result.min_angle,output)
        car.wheel = output
        #print(car.wheel)
        car.drive()
        
        if(collision(wall,car.position)):
            break
            #car.__init__( [init_parameter[0],init_parameter[1] ], init_parameter[2]  , init_parameter[3] ) 

        walkpath_4d = walkpath_4d+str(front_d)+" "+str(right_d)+" "+str(left_d)+" "+str(car.wheel)+"\n"
        walkpath_6d = walkpath_6d+str(car.position[0])+" "+str(car.position[1])+" "+str(front_d)+" "+str(right_d)+" "+str(left_d)+" "+str(car.wheel)+"\n"

        point.set_xdata(car.position[0])
        point.set_ydata(car.position[1])

        lbl_point.set_position((car.position[0], car.position[1]))
        lbl_point.set_text(str(car.position))

        sensor_txt.set_text("Front: " + str(front_d) + "\nRight: " + str(right_d) + "\nLeft: " + str(left_d))

        draw_circle.center = car.position
        
        direct.set_xdata([car.position[0],car.position[0]+ 4*math.cos(math.radians(car.horizontal))])
        direct.set_ydata([car.position[1],car.position[1]+ 4*math.sin(math.radians(car.horizontal))])

        figure.canvas.draw()
        figure.canvas.flush_events()
        if(inrange(car.position,goal[0],goal[1])):
            f = open("walkpath4d.txt", "a")
            f.write(walkpath_4d)
            f.close()
            f = open("walkpath6d.txt", "a")
            f.write(walkpath_6d)
            f.close()
            break
        time.sleep(0.1)

    plt.ioff()
    plt.show()

def file_path(file_entry):
    file_path = filedialog.askopenfilename()
    file_entry.delete(0,"end")
    file_entry.insert(0, file_path)

def main():
    window = tk.Tk()
    window.title('Perceptron')
    window.geometry('320x180')

    file_label = tk.Label(window, text='Init Data(.txt)')
    file_label.grid(row=1, column=1)
    file_entry = tk.Entry(window)
    file_entry.grid(row=1, column=2)
    file_btn = tk.Button(window, text='...',command=lambda: file_path(file_entry))
    file_btn.grid(row=1, column=3)

    file2_label = tk.Label(window, text='Train Data(.txt)')
    file2_label.grid(row=2, column=1)
    file2_entry = tk.Entry(window)
    file2_entry.grid(row=2, column=2)
    file2_btn = tk.Button(window, text='...',command=lambda: file_path(file2_entry))
    file2_btn.grid(row=2, column=3)

    result1_label = tk.Label(window)
    result1_label.grid(row=3, column=2)

    check_btn = tk.Button(window, text='Go Car',command=lambda: graph(file_entry.get(),file2_entry.get(),result1_label))
    check_btn.grid(row=4, column=2)

    window.mainloop()

if __name__ == '__main__':
    main()
