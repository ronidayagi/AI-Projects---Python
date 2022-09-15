import sys
import numpy
import csv
import random
import math

coun={} # represent a map of the countie and list of it neighbors
def read_csv (csv_file):

    with open(csv_file, newline='\n', encoding='UTF8') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for line in reader:
            if (line[0] not in coun):
                coun[line[0]] = []
            if (line[0]==line[1] or line[1] in coun[line[0]]):
                continue
            coun[line[0]].append(line[1])


def cost (from_,to_):
    from_= from_.strip()
    country_from = from_[-2:]
    to_ = to_.strip()
    country_to = to_[-2:]
    if country_to == country_from : return 1
    else : return 2


def heuristic (node,goal):
    node = node.strip()
    country_from = node[-2:]
    goal = goal.strip()
    country_to = goal[-2:]
    if country_to == country_from : return 1
    else : return 2


def A_star(start, dest):
    "the A* search algorithm with heuristic"
    explored = set() # already evaluated nodes
    tentative = [start] # tentative nodes to be evaluated
    path = {} # the map of navigated nodes (node:previous)
    g_score = {} # Cost from start along best known path
    f_score = {} # g_score(n) + heuristic(n)

    g_score[start] = 0
    f_score[start] = 0

    while (len(tentative)>0):
        current = tentative.pop(0)
        if (current==dest):
            return A_path_recurse(path,current)
        explored.add(current)
        if current not in coun.keys():
            continue
        for nb in coun[current]:
            if nb not in g_score: g_score[nb] = sys.maxsize
            g_nb = g_score[current] + cost(current,nb)
            if ((nb not in explored and nb not in tentative) or g_nb < g_score[nb]):
                path[nb] = current
                g_score[nb] = g_nb
                f_score[nb] = g_score[nb] + heuristic(nb,dest)
                if (nb not in tentative):
                    tentative.append(nb)
                    tentative.sort(key=lambda x: f_score[x])

    return None



def A_path_recurse (path,node):
    if node in path:
        recurse = A_path_recurse(path,path[node])
        recurse.append(node)
        return recurse
    else:
        ret = []
        ret.append(node)
        return ret

explored_hc = set() # already evaluated nodes
max_N=20
path_hc=[]

def hill_recurse(current,dest,count_N,g_score_current):
    global path_hc
    path_hc.append(current)
    if current==dest:
        return
    if count_N>max_N:
        return
    explored_hc.add(current)
    g_score={}
    f_score={}
    tentative=[]
    for nb in coun[current]:
        if nb in explored_hc:
            continue
        tentative.append(nb)
        g_score[nb] = g_score_current + cost(current, nb)
        f_score[nb] = g_score[nb] + heuristic(nb, dest)
    if len(tentative)==0:
        return
    tentative.sort(key=lambda x: f_score[x])
    opt_list = [tentative[0]]
    for_rand=f_score[tentative.pop(0)]
    while (len(tentative)>0 and f_score[tentative[0]]==for_rand):
        opt_list.append(tentative.pop(0))
    next=opt_list[random.randint(0, len(opt_list) - 1)]
    hill_recurse(next,dest,count_N+1,g_score[next])
#opt list זו רשימה של שכנים אופציונאליים להתקדם אליהם שלכולם יש את הציון הכי גבוה
#בודקים מבין כל השכנים ברשימה האופציונלית למי יש את הציון הגבוה, ומבין כל אלה עם אותו ציון גבוה לוקחים אחד רנדומלי ואליו מתקדמים


def hill_climing(start,dest):
    global path_hc
    for i in range(0,5):
        path_hc = []
        hill_recurse(start, dest, 0, 0)
        if path_hc[-1]==dest:
            return path_hc
    return None





def K_beam(start,dest):
    path_beam = {}
    nbrs = []
    global K_beam_DO
    currents = [start]
    g_score = {start:0}
    f_score = {start:heuristic(start,dest)}

    explored_beam = set()  # already evaluated nodes

    while True:
        tentative= {}
        for curr in currents:
            if curr not in coun: continue
            for nb in coun[curr]:
                if nb == dest:
                    path_beam[nb]=curr
                    return [A_path_recurse(path_beam, nb), nbrs]
                if nb in explored_beam: continue
                explored_beam.add(nb)
                g_scr = g_score[curr] + cost(curr, nb)
                if (nb in tentative and g_score[nb] <= g_scr):
                    continue
                g_score[nb] = g_scr
                f_score[nb] = g_score[nb] + heuristic(nb, dest)
                tentative[nb] = curr
        if len(tentative)==0:
            return None
        tentative = {k:v for k,v in sorted(tentative.items(), key=lambda item: f_score[item[0]])}
        currents = []
        for i in range(3 if len(tentative) >= 3 else len(tentative)):
            item = tentative.popitem()
            currents.append(item[0])
            path_beam[item[0]]=item[1]
        nbrs.append(currents)



def simulated_annealing(start,dest):
    # path=[start]
    path=[[start, 1., True]]
    current=start
    t=100
    T=1
    while t>0:
        E_current = heuristic(current, dest)
        options=coun[current]
        if len(options)==0:
            break
        next=random.choice(options)
        if next==dest:
            path.append([next, 1., True])
            return path
        E_next=heuristic(next,dest)
        deltaE=E_current-E_next
        if deltaE>0:
            current=next
            path.append([current, 1.0, True])
        else:
            prob = math.exp(deltaE / T)
            if prob>=random.random():
                current=next
                path.append([current, prob, True])
                T=T-0.05
                if T<=0:
                    return None
            else:
                path.append([current, prob, False])
        t=t-1
    return None


def calc_fitness(population, fitness, dest):
    for i in range(0,len(population)):
        if population[i][-1] != dest:
            fitness.append(0.)
            continue
        count=0
        for j in range(0,len(population[i])-1):
           count+=cost(population[i][j],population[i][j+1])
        fitness.append(1./count)

def mutation(child,dest):
    pickP=random.randint(1,len(child)-1)
    if child[pickP - 1] not in coun: return False
    x=coun[child[pickP - 1]]
    if len(x) == 0: return False
    if dest in x:
        child[pickP] = dest
        while len(child) > pickP + 1:
            child.pop(-1)
        return True
    if pickP >= len(child) - 1:
        if child[-1]==dest: return False
        child[pickP] = x[0]
        return True
    y=child[pickP + 1]
    for i in range(0,len(x)):
        if y in coun[x[i]]:
            child[pickP]=x[i]
            return True
    return False

def get_rand_sol(start, dest):
    path=[start]
    cur = start
    while cur != dest:
        if cur not in coun: return path
        nb = coun[cur]
        if nb == None or len(nb) == 0: return path
        cur = random.choice(nb)
        while cur in path:
            nb.remove(cur)
            if len(nb) == 0: return path
            cur = random.choice(nb)
        path.append(cur)
    return path

def genetic_algo(start,dest):
    pop_size = 10
    population=[]
    fitness=[]
    max_it = 100
    gen_DO = []

    while len(population) < pop_size and max_it > 0:
        solution = hill_climing(start, dest)
        if solution != None:
            if solution not in population:
               population.append(solution)
        max_it -= 1

    while len(population) < pop_size:
        population.append(get_rand_sol(start, dest))

    itterations = 10
    while itterations > 0:
        gen_DO.append(population.copy())
        itterations-=1
        calc_fitness(population, fitness, dest)
        new_population=[]
        best=fitness.index(max(fitness))
        best_sol = population[best]
        if fitness[best]>=0.5:
            return [best_sol, gen_DO]
        while len(population) > 1:
            p1=random.choices(population=range(0,len(population)),weights=fitness)[0]
            parent1=population.pop(p1)
            fitness.pop(p1)
            p2 = random.choices(population=range(0, len(population)), weights=fitness)[0]
            parent2=population.pop(p2)
            fitness.pop(p2)
            intsec=list(set(parent1[1:-1]) & set(parent2[1:-1])) #finding a common county between two parents
            if len(intsec)==0:
                new_population.append(parent1)
                new_population.append(parent2)
                continue
            crossover=random.choices(population=intsec) #if there is more than 1 common county, take one of them randomly
            i1=parent1.index(crossover[0])
            i2=parent2.index(crossover[0])
            child1=parent1[:i1]+parent2[i2:]
            child2=parent2[:i2]+parent1[i1:]
            mutation(child1,dest)
            mutation(child2,dest)
            if child1 in new_population:
                new_population.append(parent1)
            else:
                new_population.append(child1)
            if child2 in new_population:
                new_population.append(parent2)
            else:
                new_population.append(child2)
        population=new_population.copy()

    if best_sol[-1] == dest:
        return [best_sol, gen_DO]
    else:
        return[None, gen_DO]





def print_paths(paths,search_method,detail_output):
    if search_method==3:
        if detail_output == False:
            new_paths = []
            for p in paths:
                if p == None:
                    new_paths.append(None)
                    continue
                t_path = []
                for i in p:
                    if i[2] == True: t_path.append(i[0])
                new_paths.append(t_path)
            paths=new_paths
        else:
            detail_output = False
    K_Gen_beam = []
    if search_method==4 or search_method==5:
        np = []
        for p in paths:
            if p == None:
                np.append(None)
                K_Gen_beam.append(None)
            else:
                np.append(p[0])
                K_Gen_beam.append(p[1])
        paths = np

    max = 0
    for i,row in enumerate(paths):
        if row is None:
            paths[i]=['no path found']
            row = paths[i]
        if (row is not None and len(row)>max):
            max = len(row)

    for row in paths:
        if (len(row)<max):
           x = max-len(row)
           last = row[-1]
           for i in range(x):
            row.append(last)

    if detail_output==False:
        for i in range(max):
            print('{', end="")
            for j,list in enumerate(paths):
              if (j==0):
                   print(list[i], end="")
              else:
                  print(" ; "  ,list[i], end="")
            print('}')
    else:
        if search_method==1:
            for i in range(max):
                print('{', end="")
                for j, list in enumerate(paths):
                    if i == 1:
                        if (j == 0):
                            print(list[i] + "(" + heuristic(list[i], list[max - 1]).__str__() + ")", end="")
                        else:
                            print(" ; ", list[i] + "(" + heuristic(list[i], list[max - 1]).__str__() + ")", end="")
                    else:
                        if (j == 0):
                            print(list[i], end="")
                        else:
                            print(" ; ", list[i], end="")
                print('}')
        if search_method==2:
            for i in range(max):
                print('{', end="")
                for j, list in enumerate(paths):
                    if (j == 0):
                        print(list[i], end="")
                    else:
                        print(" ; ", list[i], end="")
                print('}')
        if search_method==4:
            for i in range(max):
                print('{', end="")
                for j, list in enumerate(paths):
                    if (j == 0):
                        print(list[i], end="")
                        if K_Gen_beam[j] != None and i < len(K_Gen_beam[j]): print(" >>",K_Gen_beam[j][i], end="")
                    else:
                        print(" ; ", list[i], end="")
                        if K_Gen_beam[j] != None and i < len(K_Gen_beam[j]): print(" >>",K_Gen_beam[j][i], end="")
                print('}')
        if search_method==5:
            for i in range(max):
                print('{', end="")
                for j, list in enumerate(paths):
                    if (j == 0):
                        print(list[i], end="")
                    else:
                        print(" ; ", list[i], end="")
                print('}')
            print("\nGenetic Iteration Populations:")
            for i,pths in enumerate(K_Gen_beam):
                print("Search {}:".format(i+1))
                if pths == None:
                    print("None")
                    continue
                for j,pop in enumerate(pths):
                    print("Iteration {}:".format(j+1))
                    print(pop)


def  fun_for_path(starting_locations,goal_locations,search_method:'A_star=1'):
    read_csv("adjacency.csv")
    for i,s in enumerate(starting_locations):
        if s not in coun:
            return None
        starting_locations[i] = s
    for i,s in enumerate(goal_locations):
        if s not in coun:
            return None
        goal_locations[i] = s
    funcs = {1:A_star,2:hill_climing,3:simulated_annealing,4:K_beam, 5:genetic_algo}
    final_paths = []
    for i,start in enumerate(starting_locations):
        final_paths.append(funcs[search_method](start,goal_locations[i]))
    return final_paths


def find_path (starting_locations,goal_locations,search_method:'A_star=1',detail_output:'boolean'):
    paths=fun_for_path(starting_locations,goal_locations,search_method)
    print_paths(paths,search_method,detail_output)




find_path( ['Washington County, UT', 'Chicot County, AR', 'Fairfield County, CT'],
           ['San Diego County, CA' , 'Bienville Parish, LA', 'Rensselaer County, NY'],4,True)
