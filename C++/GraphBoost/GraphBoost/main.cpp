//=======================================================================
// Copyright 2001 Jeremy G. Siek, Andrew Lumsdaine, Lie-Quan Lee
// Copyright 2009 Trustees of Indiana University.
// Copyright 2001 Jeremy G. Siek, Andrew Lumsdaine, Lie-Quan Lee, 
//
// Distributed under the Boost Software License, Version 1.0. (See
// accompanying file LICENSE_1_0.txt or copy at
// http://www.boost.org/LICENSE_1_0.txt)
//
// NOTE: Based off of dijkstra-example.cpp
//=======================================================================
#include <boost/config.hpp>
#include <iostream>
#include <fstream>

#include <boost/graph/graph_traits.hpp>
#include <boost/graph/adjacency_list.hpp>
#include <boost/graph/dijkstra_shortest_paths_no_color_map.hpp>
#include <boost/property_map/property_map.hpp>

using namespace boost;

int main(int, char* [])
{
    typedef adjacency_list < listS, vecS, directedS,
        no_property, property < edge_weight_t, int > > graph_t;
    typedef graph_traits < graph_t >::vertex_descriptor vertex_descriptor;
    typedef std::pair<int, int> Edge;

    const int num_nodes = 10;
    enum nodes { A, B, C, D, E, F, G, H, J, K};
    char name[] = "ABCDEFGHJK";
    Edge edge_array[] = {
          Edge(A, B), Edge(A, C), Edge(A, F),
          Edge(B, C), Edge(B, D), Edge(B, K),
          Edge(C, D), Edge(C, F), Edge(C, J),
          Edge(D, E), Edge(D, K), 
          Edge(E, F), Edge(E, G),
          Edge(K, A), Edge(K, H),
    };
    int weights[] = { 7, 9, 14, 10, 15, 11, 2, 6, 9, 8, 1, 6, 7, 12, 9 };
    int num_arcs = sizeof(edge_array) / sizeof(Edge);
    graph_t g(edge_array, edge_array + num_arcs, weights, num_nodes);
    property_map<graph_t, edge_weight_t>::type weightmap = get(edge_weight, g);
    std::vector<vertex_descriptor> p(num_vertices(g));
    std::vector<int> d(num_vertices(g));
    vertex_descriptor s = vertex(A, g);

    dijkstra_shortest_paths_no_color_map(g, s,
        predecessor_map(boost::make_iterator_property_map(p.begin(), get(boost::vertex_index, g))).
        distance_map(boost::make_iterator_property_map(d.begin(), get(boost::vertex_index, g))));

    std::cout << "distances and parents:" << std::endl;
    graph_traits < graph_t >::vertex_iterator vi, vend;
    for (boost::tie(vi, vend) = vertices(g); vi != vend; ++vi) {
        std::cout << "distance(" << name[*vi] << ") = " << d[*vi] << ", ";
        std::cout << "parent(" << name[*vi] << ") = " << name[p[*vi]] << std::
            endl;
    }
    std::cout << std::endl;
    return 0;
}