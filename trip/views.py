from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from userDb.models import Person
from .models import Trip, Job
from django.views.decorators.http import require_http_methods,require_GET,require_POST
from django.views.decorators.csrf import csrf_exempt
from math import *

#################################


# encoding:utf-8

"""
    Solution for Travelling Salesman Problem using Differential Evolution.
    Encoding Methods used as shown in paper: http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.258.7026&rep=rep1&type=pdf

    -Ayush Chopra
"""

from operator import attrgetter
import random
import sys
import copy

INF = 10000


class Graph:
    def __init__(self, amount_vertices):
        self.edges = {}  # dictionary of edges
        self.vertices = set()  # set of vertices
        self.amount_vertices = amount_vertices  # amount of vertices

    # adds a edge linking "src" in "dest" with a "cost"
    def add_edge(self, src, dest, cost=0):
        # checks if the edge already exists
        if not self.exists_edge(src, dest):
            self.edges[(src, dest)] = cost
            self.vertices.add(src)
            self.vertices.add(dest)

    # checks if exists a edge linking "src" in "dest"
    def exists_edge(self, src, dest):
        return True if (src, dest) in self.edges else False

    # shows all the links of the graph
    def show_graph(self):
        print('Showing the graph:\n')
        for edge in self.edges:
            print('%d linked in %d with cost %d' % (edge[0], edge[1], self.edges[edge]))

    # returns total cost of the path
    def get_cost_path(self, path):

        total_cost = 0
        for i in range(self.amount_vertices - 1):
            try:
                total_cost += self.edges[(path[i], path[i + 1])]
            except:
                print self.edges
                print path
                total_cost += self.edges[(path[i], path[i + 1])]

        # add cost of the last edge
        total_cost += self.edges[(path[self.amount_vertices - 1], path[0])]
        return total_cost

    # gets random unique paths - returns a list of lists of paths
    def get_random_paths(self, max_size):

        random_paths, list_vertices = [], list(self.vertices)

        initial_vertice = random.choice(list_vertices)
        if initial_vertice not in list_vertices:
            print('Error: initial vertice %d not exists!' % initial_vertice)
            sys.exit(1)

        list_vertices.remove(initial_vertice)
        list_vertices.insert(0, initial_vertice)

        # for i in range(max_size):
        while len(random_paths) < max_size:
            list_temp = list_vertices[1:]
            random.shuffle(list_temp)
            list_temp.insert(0, initial_vertice)

            if list_temp not in random_paths:
                random_paths.append(list_temp)

        return random_paths


def get_swap_sequence(permutation_1, permutation_2):
    """
    Function takes two permutations as input and returns the
    Swap Sequence for the difference of the two permutations.
    works like (-)
    """
    ss = []
    temp = copy.copy(permutation_1)
    # print permutation_1
    # print permutation_2
    for ix in range(len(temp)):
        if temp[ix] != permutation_2[ix]:
            # perform a swap operation
            swap_operation = (ix, permutation_1.index(permutation_2[ix]))
            ss.append(swap_operation)

            # swapping
            holder_var = temp[swap_operation[0]]
            temp[swap_operation[0]] = temp[swap_operation[1]]
            temp[swap_operation[1]] = holder_var
    return ss


def operate_swap_sequence(permutation, swap_sequence):
    """
    Function takes a permutation and a swap sequence and returns the
    new permutation with the swap sequence applied on the original permutation.
    works like (+)
    """
    temp = copy.copy(permutation)
    holder_var = 0

    for ix in range(len(swap_sequence)):
        # swap the positions in the permutation as per the swap operations
        try:
            holder_var = temp[swap_sequence[ix][0]]
            temp[swap_sequence[ix][0]] = temp[swap_sequence[ix][1]]
            temp[swap_sequence[ix][1]] = holder_var
        except:
            print swap_sequence, ix, "ERROR"
            exit(0)

    return temp


class Point:
    def __init__(self, dim):
        self.dim = dim
        self.point = []
        self.cost = INF


class DE:
    def __init__(self, cr=0.9, f=0.5, num_iterations=10, number_of_nodes=1, type_val=1, population=10, graph=None):
        random.seed()
        self.dim = number_of_nodes
        self.cr = cr
        self.f = f
        self.num_iterations = num_iterations
        self.iteration = 0
        self.type = type_val
        self.population = population
        self.points = [Point(self.dim) for px in range(self.population)]
        self.graph = graph

        solutions = self.graph.get_random_paths(self.population)

        for sol in range(len(solutions)):
            self.points[sol].point = solutions[sol]
            self.points[sol].cost = self.graph.get_cost_path(self.points[sol].point)

    def get_leader(self):
        top_point = sorted(self.points, key=lambda x: x.cost)[0]
        return top_point

    def iterate(self):
        l = self.get_leader();
        for ix in range(self.population):
            x = self.points[ix]
            [a, b, c] = random.sample(self.points, 3)
            while x == a or x == b or x == c:
                [a, b, c] = random.sample(self.points, 3)

            # R = random.random() * x.dim
            y = Point(dim=self.dim)
            if random.random() < self.cr:
                diff = get_swap_sequence(b.point, c.point)
                ss = []
                for so in diff:
                    if random.random() < self.f:
                        ss.append(so)
                y.point = operate_swap_sequence(a.point, ss)
            else:
                y.point = x.point

            # for px in range(self.dim):
            #     if random.random() < self.cr or px == R:
            #         pass
            #     else:
            #         y.point[px] = x.point[px]

            y.cost = self.graph.get_cost_path(y.point)
            if y.cost < x.cost:
                self.points[ix] = y
        self.iteration += 1

    def simulate(self):
        pnt = self.get_leader()
        # print 'Initial best value of: ' + str(pnt.cost)
        while self.iteration < self.num_iterations:
            self.iterate()
        pnt = self.get_leader()
        # print 'Final best value of: ' + str(pnt.cost)
        # print ""
        return pnt.cost


if __name__ == "__main__":
    # creates the Graph instance
    number_of_nodes = 10
    g = Graph(amount_vertices=number_of_nodes)
    random.seed()

    # This graph is in the folder "images" of the repository.
    # for ix in range(number_of_nodes):
    #     for iy in range(number_of_nodes):
    #         if ix != iy:
    #             g.add_edge(ix, iy, 5*random.random())

    g.add_edge(0, 1, 4.86114254708)
    g.add_edge(0, 2, 3.1598221043)
    g.add_edge(0, 3, 2.74801787826)
    g.add_edge(0, 4, 2.94243679928)
    g.add_edge(0, 5, 3.25632483794)
    g.add_edge(0, 6, 2.88248149602)
    g.add_edge(0, 7, 3.20876807488)
    g.add_edge(0, 8, 2.12635932593)
    g.add_edge(0, 9, 4.60485843387)
    g.add_edge(1, 0, 2.59137583216)
    g.add_edge(1, 2, 6.84056377492)
    g.add_edge(1, 3, 3.92212293383)
    g.add_edge(1, 4, 5.05460971544)
    g.add_edge(1, 5, 3.09078171786)
    g.add_edge(1, 6, 3.44677623991)
    g.add_edge(1, 7, 0.354333041599)
    g.add_edge(1, 8, 6.4655963088)
    g.add_edge(1, 9, 4.20674346753)
    g.add_edge(2, 0, 4.12759186032)
    g.add_edge(2, 1, 6.45662688544)
    g.add_edge(2, 3, 0.264693166171)
    g.add_edge(2, 4, 1.29046073234)
    g.add_edge(2, 5, 1.04985013674)
    g.add_edge(2, 6, 0.310607524582)
    g.add_edge(2, 7, 5.84311603502)
    g.add_edge(2, 8, 2.1570440059)
    g.add_edge(2, 9, 0.719787217762)
    g.add_edge(3, 0, 1.02227330102)
    g.add_edge(3, 1, 6.52139957848)
    g.add_edge(3, 2, 1.44862581316)
    g.add_edge(3, 4, 5.94961198405)
    g.add_edge(3, 5, 2.44990248537)
    g.add_edge(3, 6, 2.96687061616)
    g.add_edge(3, 7, 6.69242196917)
    g.add_edge(3, 8, 5.76060542771)
    g.add_edge(3, 9, 0.174949461355)
    g.add_edge(4, 0, 3.75460667898)
    g.add_edge(4, 1, 6.56909499376)
    g.add_edge(4, 2, 5.28690422355)
    g.add_edge(4, 3, 6.26271492397)
    g.add_edge(4, 5, 3.71267997319)
    g.add_edge(4, 6, 1.12397892634)
    g.add_edge(4, 7, 0.420789955855)
    g.add_edge(4, 8, 2.45697916283)
    g.add_edge(4, 9, 3.60840278292)
    g.add_edge(5, 0, 2.89834610867)
    g.add_edge(5, 1, 5.97012693093)
    g.add_edge(5, 2, 6.30212306228)
    g.add_edge(5, 3, 4.04004696841)
    g.add_edge(5, 4, 3.10245279092)
    g.add_edge(5, 6, 1.83839307494)
    g.add_edge(5, 7, 3.14753021634)
    g.add_edge(5, 8, 2.96294949101)
    g.add_edge(5, 9, 3.76076885547)
    g.add_edge(6, 0, 4.75411301645)
    g.add_edge(6, 1, 4.36347382203)
    g.add_edge(6, 2, 3.49653584693)
    g.add_edge(6, 3, 2.2276280612)
    g.add_edge(6, 4, 3.41747052449)
    g.add_edge(6, 5, 3.06274198245)
    g.add_edge(6, 7, 2.32077182203)
    g.add_edge(6, 8, 5.8905142537)
    g.add_edge(6, 9, 4.29676008316)
    g.add_edge(7, 0, 4.09031945913)
    g.add_edge(7, 1, 1.77789359987)
    g.add_edge(7, 2, 1.84395978054)
    g.add_edge(7, 3, 2.91317977828)
    g.add_edge(7, 4, 3.07324936741)
    g.add_edge(7, 5, 3.56326482916)
    g.add_edge(7, 6, 4.25906044052)
    g.add_edge(7, 8, 0.340076260808)
    g.add_edge(7, 9, 5.95853625141)
    g.add_edge(8, 0, 4.74634374359)
    g.add_edge(8, 1, 3.42527176206)
    g.add_edge(8, 2, 2.59217031255)
    g.add_edge(8, 3, 6.28886324982)
    g.add_edge(8, 4, 2.8762113778)
    g.add_edge(8, 5, 4.210001783)
    g.add_edge(8, 6, 6.85455861064)
    g.add_edge(8, 7, 6.99542571993)
    g.add_edge(8, 9, 0.17868231627)
    g.add_edge(9, 0, 5.86495621123)
    g.add_edge(9, 1, 0.655448596701)
    g.add_edge(9, 2, 1.79538962633)
    g.add_edge(9, 3, 1.04160729197)
    g.add_edge(9, 4, 1.81241260526)
    g.add_edge(9, 5, 2.23675980505)
    g.add_edge(9, 6, 5.52218536387)
    g.add_edge(9, 7, 3.94802824024)
    g.add_edge(9, 8, 6.14470143783)

    import time

    val = 0
    for trial in range(10):
        start = time.clock()
        de = DE(num_iterations=100, number_of_nodes=number_of_nodes, type_val=1, graph=g, population=25)
        val += de.simulate()
    print "time", (time.clock() - start)
   # print val/10.0


##################################

def distance(lon1,lat1,lon2,lan2):

	dlon = lon2 - lon1 
	dlat = lat2 - lat1 
	a = (sin(dlat/2))^2 + cos(lat1) * cos(lat2) * (sin(dlon/2))^2 
	c = 2 * atan2( sqrt(a), sqrt(1-a) ) 
	d = 6373 * c 
	return dist


def find_worker(src,radius):
	worker = Person.objects.get(isWorker=True)
	wlist ={}
	for w in workers:
		if distance(workers["source"],src) < radius
			wlist.add(w)

@csrf_exempt
def getJobs(request):
	response_data = {}
	input = request.POST
	
	try:
		jobs = Job.objects.get(uid = input['uid'])

		response_data["jobs"] = jobs
	except:
		response_data["success"] = "0"
		return response_data
	else:

		response_data["success"] = "1"
		return response_data


@csrf_exempt
@require_POST
def addTrip(request):
	response_data = {}
	input = request.POST

	try:
		obj = Person.objects.get(uid = input['uid'])
		Trip.objects.create(uid=input['uid'],lon1= input["lon1"],lat1 = input["lat1"],lon2 = input["lon2"],lat2 = input["lon2"],budget = input["budget"],weight = input["weight"],desc=input["desc"])
		dist = distance(input["lon1"],input["lat1"],input["lon2"],input["lat2"])

		radius = 0.1*distance
		wlist = find_worker(input["source"],radius)

		print wlist

	except:
		response_data["success"] = "0"
		return response_data
	else:

		response_data["success"] = "1"
		return response_data

def addJob(request):
	response_data ={}
	input = request.POST

	try:
		own = Person.objects.get(uid = input['uid'])
		work = Person.objects.get(uid = input['wid'])
		trip = Trip.objects.get(tid = input['tid'])
		Job.objects.create(tid=trip,uid=own,wid=work,amt = input['amt'])

	except:
		response_data["success"] = "0"
		return response_data
	else:

		response_data["success"] = "1"
		return response_data

def rendermap(request):
	input = request.POST
	response_data = {}
	uid = input['uid']
	src = input['source']
	dest = input['destination']


# @csrf_exempt
# @require_POST
# def checkstatus(request):
# 	response_data = {}
# 	input = request.POST
# 	uid = input['uid']
# 	try:
# 		response_data['lat'], response_data['long'] = 







