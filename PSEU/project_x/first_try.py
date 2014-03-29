# -*- coding: utf-8 -*-
import networkx as nx

def import_file():
	G = nx.DiGraph()
	f = open('Svi.txt', 'r')
	for line in f:
		koncept1, veza, koncept2, nl = line.split('\t')
		G.add_edge(koncept1,koncept2)
	
	roots=[n for n in G.nodes() if G.in_degree(n)==0]
	leafs=[n for n in G.nodes() if G.out_degree(n)==0]
	#print(roots)
	# test = nx.dfs_tree(G, 'Leinonen')
	# print(test.edges())

	test2 = nx.shortest_path(G, roots[0], leafs[0])
	print(test2)

	SG = G.subgraph('e-ucenje')
	#print(SG.nodes())

def main():
	import_file()
main()