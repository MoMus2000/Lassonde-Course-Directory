import networkx as nx
import pydot


g=nx.DiGraph()
g.add_edges_from([(1,2), (1,3), (1,4), (2,5), (2,6), (2,7), (3,8), (3,9),
                  (4,10), (5,11), (5,12), (6,13)])
p=nx.drawing.nx_pydot.to_pydot(g)
p.write_png('example.png')



# ##############
#   G = nx.Graph()
#     nodes_added = []
#     for nodes in arr:
#         G.add_node(nodes)
#         nodes_added.append(nodes)
#         pre_reqs = get_prerequisites(nodes)
#         time.sleep(1)
#         for pre_req in pre_reqs:
#             print(pre_req)
#             if(pre_req in nodes_added):
#                 # G.add_edge(nodes,pre_req)
#                 continue
#             G.add_node(pre_req)
#             G.add_edge(nodes,pre_req)
#     A = nx.to_agraph(G)
#     A.layout('dot', args='-Nfontsize=10 -Nwidth=".2" -Nheight=".2" -Nmargin=0 -Gfontsize=8')
#     A.draw('test.png')
#     pos = nx.spring_layout(G,k=0.7,iterations =5)
#     nx.dijkstra_path(G, arr[0], arr[len(arr)-1])
#     nx.draw(G,pos = pos,node_size=1200, node_color='lightblue', linewidths=0.25,font_size=10, font_weight='bold', with_labels=True, dpi=1000)
#     plt.plot()
#     plt.show()
# ###################