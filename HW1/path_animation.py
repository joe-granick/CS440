import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation
import a_star as a

start_x, start_y = 2, 4
goal_x, goal_y = 4, 4

test_path = [
            [True, True, True, True, True],
            [True, True, False, True, True],
            [True, True, False, False, True],
            [True, True, False, False, True],
            [True, True, True, False, True]
            ]
        
        

repeated_test_maze = a.aStar(path=test_path, start_x=start_x, start_y=start_y, goal_x=goal_x, goal_y=goal_y)
repeated_test_maze.a_star_repeated()
x,y=[],[]

#for node in repeated_test_maze.get_trajectory()[0]:
x.append(2)
y.append(4)
x.append(3)
y.append(4)
x.append(4)
y.append(4)
fig,ax=plt.subplots()
line,=ax.plot(x,y)
def update(num,x,y,line):
    line.set_data(x[:num],y[:num])
    return line,

ani = animation.FuncAnimation(fig,update,len(x), interval=10,
                            fargs=[x,y,line],blit=True)
plt.show()
# if __name__ == "__main__":
#     fig = plt.figure()
#     ani = FuncAnimation(fig, animate, interval=1000)
#     plt.show()