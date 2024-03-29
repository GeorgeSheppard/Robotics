# -*- coding: utf-8 -*-
"""
Created on Thu Feb  7 17:09:08 2019

@author: William
"""
input_nodes = 4
output_nodes = 2
max_layers = 6
max_layers += 1 #1 more than the number of hidden layers
initial_nodes = 6
initial_nodes += 1
maximum_nodes = 500
initial_links = 10
initial_links += 1
maximum_links = maximum_nodes*(input_nodes+1+output_nodes)+input_nodes*output_nodes

proportionality = 10.

min_link_change = 1
max_link_change = 5 #actually the range
max_link_change += 1
min_node_change = 1
max_node_change = 3 #actually the range
max_node_change += 1

regular_layer_bias = 0.8
in_out_layer_bias = 1-regular_layer_bias
#input_layer_weights = in_out_layer_bias*input_nodes/(input_nodes+output_nodes)
#output_layer_weights = in_out_layer_bias*output_nodes/(input_nodes+output_nodes)

number_nets = 100
repeats = 2
max_steps = 1000
save_rate = 20

#drawing the net
screen_width = 1000
screen_height = 800
pixel_per_layer = screen_width/(max_layers+1)
node_radius = 10
node_width = 1
link_width = 1
