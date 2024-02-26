import a_star
import grid_world
import s_node
import random

random.seed(1)
trials = 1000

fwd_results = []
bkw_results = []
large_g_results = []
adapt_results = []

for i in range(1,100):
    grid = grid_world.GridWorld(50,50)
    grid.create_maze()
    grid.set_start_goal()
    start_x, start_y = grid.start_x(), grid.start_x()
    goal_x, goal_y = grid.goal_x(), grid.goal_y()
    test_path = grid.get_path()

    print(start_x,start_y,goal_x,goal_y)
    fwd_test_maze = a_star.aStar(path=test_path,
                            start_x=start_x,start_y=start_y,
                            goal_x=goal_x, goal_y=goal_y)
    
    a_star_fwd = fwd_test_maze.a_star_fwd()
    fwd_results.append(fwd_test_maze.get_expanded())

    bkw_test_maze = a_star.aStar(path=test_path,
                            start_x=start_x,start_y=start_y,
                            goal_x=goal_x, goal_y=goal_y)
    a_star_bkw = bkw_test_maze.a_star_bkw()
    bkw_results.append(bkw_test_maze.get_expanded())
    
    adapt_test_maze = a_star.aStar(path=test_path,
                            start_x=start_x,start_y=start_y,
                            goal_x=goal_x, goal_y=goal_y)
    a_star_adapt = adapt_test_maze.a_star_adaptive()
    adapt_results.append(adapt_test_maze.get_expanded()) 

    sum_fwd,count_fwd = 0,0
    sum_bkw,count_bkw = 0,0
    sum_adpt,count_adpt = 0,0

for i in fwd_results:
    sum_fwd += i
    count_fwd+=1
for i in bkw_results:
    sum_bkw += i
    count_bkw+=1
for i in adapt_results:
    sum_adpt += i
    count_adpt+=1
print("fwd A* avg node expanded: ", sum_fwd/count_fwd) 
print("bkw A* avg node expanded: ", sum_bkw/count_bkw)
print("adpt A* avg node expanded: ", sum_adpt/count_adpt )   


