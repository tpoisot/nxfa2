#! /usr/bin/python

import networkx as nx
import scipy as sp
import numpy as np
import random

import matplotlib.pyplot as plt

## Read a food web with > 100 nodes
FW = nx.read_edgelist('web.edges', create_using= nx.DiGraph())

## Plotting using the FR layout
#nx.draw_spring(FW)
#plt.show()

## Utility functions
def eucl_dist(a,b):
	"""
	Euclidean distance
	"""
	Di = [(a[i]-b[i])**2 for i in xrange(len(a))]
	return np.sqrt(np.sum(Di))

aa = list(FW.edges_iter(data=False))
print aa[0][1]

## Now the layout function
def forceatlas2_layout(G, iterations = 10, linlog = False, pos = None, nohubs = False, kr = 0.001):
	"""
	Options values are

	g                The graph to layout
	iterations       Number of iterations to do
	linlog           Whether to use linear or log repulsion
	random_init      Start with a random position
	                 If false, start with FR
	avoidoverlap     Whether to avoid overlap of points
	degreebased      Degree based repulsion
	"""
	# We add attributes to store the current and previous convergence speed
	for n in G:
		G.node[n]['prevcs'] = 0
		G.node[n]['currcs'] = 0
	# Initial layout
	if pos is None:
		pos = nx.random_layout(G)
	# Iterations
	for iteration in xrange(iterations):
		# We get a shuffled list of edges
		ShuffledEdgeList = list(G.edges_iter(data=False))
		random.shuffle(ShuffledEdgeList)
		for CurrentEdge in ShuffledEdgeList:
			Xa = pos[CurrentEdge[0]]
			Xb = pos[CurrentEdge[1]]
			# Repulsion force
			Fr = kr*(((G.degree(CurrentEdge[0])+1)*(G.degree(CurrentEdge[1])+1))/float(eucl_dist(Xa,Xb)+0.01))
			# Attraction force
			Fa = eucl_dist(Xa,Xb)
			# If no hubs
			Fa = Fa/float(G.degree(CurrentEdge[0])+1)
			# If lin-log
			if linlog:
				Fa = np.log(1+Fa)
	# Return the layout
	return pos

pos = forceatlas2_layout(FW)
#nx.draw(FW, forceatlas2_layout(FW))
#plt.show()
