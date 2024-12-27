#!/bin/env python3
'''
Python implementation of transitive reduction.
'''

from dataclasses import dataclass
from pprint import pprint, pformat



Node = object
'''A node within a directed graph.'''

@dataclass(slots=True, frozen=True)
class Link:
	'''
	A uni-directional link between two nodes in a directed graph.
	'''
	first: Node
	'''First node.'''
	second: Node
	'''Second node.'''

NodeAdjs = dict[Node, set[Node]]
'''Lookup of nodes and their associated sets of nodes toward which they are
directly linked.'''

NodeDegs = dict[Node, int]
'''Lookup of nodes and their "degrees" of depth within a directed graph.

A node's degree is equal to the number of nodes directly preceding it.
If a node has no prior nodes in a graph, then it has degree 0.'''

def node_adjs(links: set[Link]) -> NodeAdjs:
	'''
	Dictionary relating nodes in a directed graph to the nodes toward which
	they're linked.
	
	:return: Generated lookup.
	:param links: Directed links between nodes, representing a directed graph.
	
	This function basically provides a different stucture for the node
	relationships in `links`. It has no special behavior if `links` represents
	a graph with circular relationships.
	
	>>> acyclic_links = set([
	... 	Link(first='A', second='B'),
	... 	Link(first='B', second='Z'),
	... 	Link(first='Z', second='H'),
	... 	Link('D', 'A'),
	... 	Link('E', 'Z'),
	... 	Link('B', 'F'),
	... 	Link('F', 'Z'),
	... ])
	>>> na = node_adjs(acyclic_links)
	>>> na['A']
	{'B'}
	>>> sorted(na['B'])
	['F', 'Z']
	>>> na['D']
	{'A'}
	>>> na['E']
	{'Z'}
	>>> na['F']
	{'Z'}
	>>> na['Z']
	{'H'}
	>>> na['H']
	set()
	
	Nothing special happens with :py:func:`node_adjs` if it processes a set of
	links with circular relationships.
	
	>>> cyclical_links = set([
	... 	Link('A', 'B'),
	... 	Link('B', 'Z'),
	... 	Link('Z', 'A'),
	... 	Link('D', 'A'),
	... 	Link('E', 'Z'),
	... 	Link('B', 'F'),
	... 	Link('F', 'Z'),
	... ])
	>>> na = node_adjs(cyclical_links)
	>>> sorted(na['B'])
	['F', 'Z']
	>>> na['F']
	{'Z'}
	>>> na['Z']
	{'A'}
	>>> na['A']
	{'B'}
	
	Using :py:func:`node_adjs` on an empty set of inter-node links results in
	an empty lookup.
	
	>>> empty_links = set()
	>>> na = node_adjs(empty_links)
	>>> na
	{}
	
	A self-referencing link has no special effect on the output of
	:py:func:`node_adjs`.
	
	>>> selfref_links = set([
	... 	Link('C', 'C'),
	... 	Link('B', 'D'),
	... 	Link('D', 'B'),
	... ])
	>>> na = node_adjs(selfref_links)
	>>> na['C']
	{'C'}
	'''
	na = NodeAdjs()
	for link in links:
		if not link.first in na:
			na[link.first] = set()
		if not link.second in na:
			na[link.second] = set()
		na[link.first].add(link.second)
	return na

class TopoSortError(Exception):
	'''
	Exception raised if topological sorting of the nodes in a set of links
	fails.
	'''
	def __init__(self, unp_nodes: set[Node]):
		'''
		Constructor.
		
		:param unp_nodes: Nodes not processed by the failed topological sort
			operation.
		'''
		self.unp_nodes = sorted(unp_nodes)
		self.message = ('topological sort operation failed; '
			f'unprocessed nodes = {self.unp_nodes}')
	def __str__(self):
		return self.message

def node_degs(node_adjs: NodeAdjs) -> NodeDegs:
	'''
	Lookup relating nodes to their degrees of depth within a directed graph.
	
	:return: Generated lookup.
	:param node_adjs: Lookup of nodes and the nodes toward which they are
		linked.
	
	.. todo::
	   
	   What happens if there are circular relationships? Will there just be
	   nodes that, during resolution in :py:func:`topo_sorted_nodes`, won't
	   have their degrees subtracted all the way to zero?
	
	>>> acyclic_links = set([
	... 	Link('A', 'B'),
	... 	Link('B', 'Z'),
	... 	Link('Z', 'H'),
	... 	Link('D', 'A'),
	... 	Link('E', 'Z'),
	... 	Link('B', 'F'),
	... 	Link('F', 'Z'),
	... ])
	>>> na = node_adjs(acyclic_links)
	>>> nd = node_degs(na)
	>>> sorted(nd.items())
	[('A', 1), ('B', 1), ('D', 0), ('E', 0), ('F', 1), ('H', 1), ('Z', 3)]
	
	The sum of all depth values in the returned dictionary should be equal to
	the number of elements in the set-values of the dictionary returned from
	:py:func:`node_adjs`, which is equal to the number of original links in the
	dictionary from :py:func:`node_adjs`.
	
	>>> deg_sum = sum(nd.values())
	>>> total_num_adjs = sum([len(adjs) for node, adjs in na.items()])
	>>> deg_sum == total_num_adjs
	True
	
	>>> cyclical_links = set([
	... 	Link('A', 'B'),
	... 	Link('B', 'Z'),
	... 	Link('Z', 'A'),
	... 	Link('D', 'A'),
	... 	Link('E', 'Z'),
	... 	Link('B', 'F'),
	... 	Link('F', 'Z'),
	... ])
	>>> na = node_adjs(cyclical_links)
	>>> nd = node_degs(na)
	>>> sorted(nd.items())
	[('A', 2), ('B', 1), ('D', 0), ('E', 0), ('F', 1), ('Z', 3)]
	>>> deg_sum = sum(nd.values())
	>>> total_num_adjs = sum([len(adjs) for node, adjs in na.items()])
	>>> deg_sum == total_num_adjs
	True
	'''
	nd = NodeDegs({node: 0 for node in node_adjs})
	for node, adjs in node_adjs.items():
		for adj in adjs:
			nd[adj] += 1
	return nd

def topo_sorted_nodes(links: set[Link], verbosity: int = 0) -> tuple:
	'''
	Topologically sorts nodes in a directed graph represented by
	uni-directional links between nodes.
	
	:return: List of topologically sorted nodes from `links`.
	:param links: Directed links between nodes, representing a directed graph.
	:param verbosity: Level of debug verbosity.
	:raise TopoSortError: Sorting operation failed.
	
	>>> acyclic_links = set([
	... 	Link('A', 'B'),
	... 	Link('B', 'Z'),
	... 	Link('Z', 'H'),
	... 	Link('D', 'A'),
	... 	Link('E', 'Z'),
	... 	Link('B', 'F'),
	... 	Link('F', 'Z'),
	... ])
	>>> sorted_nodes = topo_sorted_nodes(acyclic_links)
	
	There are a few possible ways to sort these nodes, so a one-to-one
	comparison between the expected and actual node lists is unfeasible.
	
	.. graphviz::
	   
	   D -> A -> B -> Z -> H;
	   B -> F;
	   E -> Z;
	
	>>> sorted_nodes.index('A') < sorted_nodes.index('Z')
	True
	>>> sorted_nodes.index('E') < sorted_nodes.index('H')
	True
	
	>>> circular_links = set([
	... 	Link('A', 'B'),
	... 	Link('B', 'Z'),
	... 	Link('Z', 'A'),
	... 	Link('D', 'A'),
	... 	Link('E', 'Z'),
	... 	Link('B', 'F'),
	... 	Link('F', 'Z'),
	... ])
	>>> sorted_nodes = topo_sorted_nodes(circular_links)
	Traceback (most recent call last):
		...
	dap.TopoSortError: topological sort operation failed; unprocessed nodes = ['A', 'B', 'F', 'Z']
	
	.. graphviz::
	   
	   D -> A -> B -> Z -> A;
	   E -> Z;
	   B -> F -> Z;
	'''
	
	unp_nodes = set()
	for link in links:
		unp_nodes |= set([link.first, link.second])
	na = node_adjs(links)
	nd = node_degs(na)
	
	# initialize the queue with the nodes that already have degree 0
	q = [node for node, deg in nd.items() if deg == 0]
	assert len(set(q)) == len(q), \
		'expected initial queue to have unique values'
	
	# perform sort operation
	sorted_nodes = []
	while q:
		n = q.pop(0)
		assert n in unp_nodes
		unp_nodes.remove(n)
		assert not n in sorted_nodes
		sorted_nodes.append(n)
		assert n in na
		for x in na[n]:
			assert x in nd
			assert nd[x] > 0
			nd[x] -= 1
			if nd[x] == 0:
				q.append(x)
	
	# if there are any nodes that haven't been processed ("visited"), then they
	# were not all sorted
	if unp_nodes:
		raise TopoSortError(unp_nodes)
	
	# if the nodes have been sorted, then confirm that the nodes of every
	# link are indeed in the correct relative order; this is automatically
	# removed when debug assertions are turned off
	for link in links:
		assert sorted_nodes.index(link.first) < sorted_nodes.index(link.second)
	
	return sorted_nodes

def dfs(na: NodeAdjs, start: Node) -> set[Node]:
	'''
	Performs a depth-first search of nodes in a directed graph.
	
	:param na: Dictionary of nodes and each of their associated sets of
		immediately-next nodes, toward which they are linked.
	:param start: Node at which to begin search.
	
	This implementation was copied and adapted from :cite:p:`scheufler:2021` on
	May 16, 2024.
	'''
	visited: set[Node] = set()
	stack: list[Node] = [start]
	while stack:
		node = stack.pop()
		if node in visited:
			continue
		visited.add(node)
		for n in na.get(node, set()):
			if not n in visited:
				stack.append(n)
	return {n for n in visited if n != start}
	
def transitive_reduction(links: set[Link], verbosity: int = 0) -> set[Link]:
	'''
	Calculates the transitive reduction for a directed graph.
	
	:return: Links representing the same graph as `links` but with as few edges
		as possible.
	:param links: Uni-directional inter-node links forming a directed graph.
	:param verbosity: Level of debug verbosity.
	:raise TopoSortError: Graph represented by `links` is not acyclic.
	
	.. attention::
	   
	   A transitive reduction *is* possible for a directed graph with cycles,
	   but it is not be supported by this function.
	
	This implementation was copied and adapted from :cite:p:`scheufler:2021` on
	May 16, 2024.
	
	>>> minimal_links = set([
	... 	Link('A', 'B'),
	... 	Link('B', 'C'),
	... 	Link('A', 'D'),
	... 	Link('P', 'Q'),
	... 	Link('P', 'R'),
	... 	Link('Q', 'S'),
	... 	Link('S', 'T'),
	... 	Link('D', 'T'),
	... 	Link('B', 'T'),
	... ])
	>>> redundant_links = set([
	... 	Link('A', 'C'),
	... 	Link('P', 'S'),
	... 	Link('P', 'T'),
	... ])
	>>> minimal_links & redundant_links
	set()
	>>> links = minimal_links | redundant_links
	>>> tr = transitive_reduction(links, verbosity=2)
	>>> tr == minimal_links
	True
	
	The resultant reduced graph must cover all of the same nodes as the
	original graph.
	'''
	sn = topo_sorted_nodes(links, verbosity) # raises exception if not acyclic
	na = node_adjs(links)
	descendants: dict[Node, set[Node]] = dict()
	checkCount: dict[Node, int] = dict()
	reduced_links: set[Link] = set()
	for u in sn:
		u_adjs = na.get(u, set())
		for v in na.get(u, set()):
			
			if not v in u_adjs:
				continue
			if not v in descendants:
				_visited = dfs(na, v)
				descendants[v] = _visited
			u_adjs = {d for d in u_adjs if not d in descendants[v]}
			
			# ~ checkCount[v] = max(checkCount[v]-1,0) if v in checkCount else 0
			# ~ assert checkCount[v] >= 0, checkCount[v]
			# ~ if checkCount[v] == 0:
				# ~ descendants = {_v:e for _v,e in descendants.items() if v != _v}
			
			# can the code block above be severely reduced and simplified?
			descendants = {_v:e for _v,e in descendants.items() if v != _v}
			
		for v in u_adjs:
			_matching_links = list(filter(lambda x: x.first == u
				and x.second == v, links))
			assert len(_matching_links) == 1
			reduced_links.add(_matching_links[0])
	return reduced_links
