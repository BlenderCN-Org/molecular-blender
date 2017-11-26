#  Molecular Blender
#  Filename: find_planar_rings.py
#  Copyright (C) 2014 Shane Parker, Joshua Szekely
#
#  This file is part of Molecular Blender.
#
#  Molecular Blender is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 3, or (at your option)
#  any later version.
#
#  Molecular Blender is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Library General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with Molecular Blender; see COPYING.
#  If not, see <http://www.gnu.org/licenses/>.

from .util import Timer

import mathutils # TODO remove

# Creates a graph structure from list of atoms and bonds
def createGraph(atomlist,connectivitylist):
    graph = [ set() for x in range(len(atomlist)) ]

    for x,y in connectivitylist:
        graph[x].update(set([y]))
        graph[y].update(set([x]))

    return graph

# Check if vertices of loop are coplanar
def isPlanar(atomlist,cycle):
    if len(cycle) is 3:
        return True
    else:
        testlist = list(cycle)
        for x in range(3,len(testlist)):
            c1, c2, c3, c4 = [ atomlist[testlist[x-i]].position for i in range(4) ]
            v21 = c2 - c1
            v43 = c4 - c3
            v31 = c3 - c1
            v21.normalize()
            v43.normalize()
            v31.normalize()
            threshold = v31.dot(v21.cross(v43))
            if abs(threshold) > 0.1:
                return False
        return True

# Basic depth first search algorithm, pulled from the Internet
def DFS(graph, start, goal, pathrange=(2,7)):
    stack = [(start,[start])]
    while stack:
        (vertex,path) = stack.pop()
        # any successes after this point will add one to current length of path
        if len(path)+1 < pathrange[1]:
            for nextvert in graph[vertex] - set(path):
                if nextvert == goal:
                    if pathrange[0] <= len(path)+1 < pathrange[1]:
                        yield path + [nextvert]
                else:
                    stack.append((nextvert,path + [nextvert]))

# Finds all unique paths of a vertex back to itself
def findSpecificCycles(graph, vertex, pathrange=(2, 7)):
    cycles = []
    fixedcycles = []
    for goal in graph[vertex]:
        for path in DFS(graph,vertex,goal,pathrange=pathrange):
            if set(path) not in cycles:
                cycles.append(set(path))
                fixedcycles.append(path)
    return cycles,fixedcycles

# Finds all closed walks of with lengths bounded by path range. Defaults to paths
# of length > 2 and < 7
def findAllUniqueCycles(graph, pathrange=(2,7)):
    cycles = []
    for i in range(len(graph)):
        possibleCycles,extras = findSpecificCycles(graph,i,pathrange)
        for cycle in possibleCycles:
            if set(cycle) not in cycles and pathrange[0] < len(cycle) < pathrange[1]:
                cycles.append(set(cycle))
    return cycles

def orderedCycle(cycle, graph):
    """Returns ordered cycle corresponding to input cycle (i.e., undoes set() build)"""
    pathrange = (len(cycle), len(cycle)+1)
    extras, fixedcycles = findSpecificCycles(graph, list(cycle)[0], pathrange)
    for fc in fixedcycles:
        if set(fc) == cycle:
            return fc

def find_planar_cycles(molecule):
    """Return all planar cycles for plotting"""
    timer = Timer()

    atomlist = molecule.atoms
    bondlist = [(b.iatom.index, b.jatom.index) for b in molecule.bonds]
    timer.tick_print("generate lists")

    graph = createGraph(atomlist,bondlist)
    timer.tick_print("create graphs")

    cycles = findAllUniqueCycles(graph)
    timer.tick_print("find unique cycles")

    planarCycles = [x for x in cycles if isPlanar(atomlist,x)]
    timer.tick_print("check cycle planarity")

    orderedCycles = [ orderedCycle(x, graph) for x in planarCycles ]
    timer.tick_print("order cycles")

    return orderedCycles