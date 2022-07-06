import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
import random
import math
import pandas as pd

pd.options.mode.chained_assignment = None

import networkx as nx
import graphviz
import numpy as np
import matplotlib.pyplot as plt 
import networkx as nx
from networkx.drawing.nx_pydot import to_pydot

from networkx.drawing.nx_pydot import to_pydot


def get_row_index(df, values):
    """ 
    Get index positions of values in dataframe
    
    `Required` 
    :param df: Panda dataframe
    :param values: data structure with values to search
    """
    for value in values:
        listOfPos = list()
        # Get bool dataframe with True at positions where the given value exists
        result = df.isin([value])
        # Get list of columns that contains the value
        seriesObj = result.any()
        columnNames = list(seriesObj[seriesObj == True].index)
        # Iterate over list of columns and fetch the rows indexes where value exists
        for col in columnNames:
            rows = list(result[col][result[col] == True].index)
            for row in rows:
                listOfPos.append(row)
                return listOfPos
        # Return a list of tuples indicating the positions of value in the dataframe
    return listOfPos

def try_upload(raw_data):
    #hacky solution for loading example data
    if raw_data == 'example1':
        df = pd.read_excel(r'./uploads/example_data/1.xlsx')
    elif raw_data == 'example2':
        df = pd.read_excel(r'./uploads/example_data/2.xlsx')
    elif raw_data == 'example3':
        df = pd.read_excel(r'./uploads/example_data/3.xlsx')
    
    # load data depending on file type
    else:
        try:
            df = pd.read_csv(raw_data)
        except:
            df = pd.read_excel(raw_data)
    #remove meta information before column headers
    try:
        header_row_index = get_row_index(df, ['Time', 'time', 'Subject', 'subject', 'Status', 'Behavior'])[0]
        df = df.iloc[header_row_index:]
        df.columns = df.iloc[0]
        df = df.iloc[1:]
    except:
        pass
    
    #make column headers lowercase and substitute whitespace
    df.columns = [x.lower() for x in df.columns]
    df.columns = df.columns.str.replace(' ','_')

    response = ''
    success = True

    #return error message and instructions if time, subject, behavior or status are not present
    if 'time' not in df.columns:
        response += 'Required column \"Time\" is missing\n'
        success = False
    if 'subject' not in df.columns:
        response += 'Required column \"Subject\" is missing\n'
        success = False
    if 'behavior' not in df.columns:
        response += 'Required column \"Behavior\" is missing\n'
        success = False

    return (response,success)

def handle_upload(raw_data):
    #hacky solution for loading example data
    if raw_data == 'example1':
        df = pd.read_excel(r'./uploads/example_data/1.xlsx')
    elif raw_data == 'example2':
        df = pd.read_excel(r'./uploads/example_data/2.xlsx')
    elif raw_data == 'example3':
        df = pd.read_excel(r'./uploads/example_data/3.xlsx')
    
    # load data depending on file type
    else:
        try:
            df = pd.read_csv(raw_data)
        except:
            df = pd.read_excel(raw_data)
    
    #remove meta information before column headers
    try:
        header_row_index = get_row_index(df, ['Time', 'time', 'Subject', 'subject', 'Status', 'Behavior'])[0]
        df = df.iloc[header_row_index:]
        df.columns = df.iloc[0]
        df = df.iloc[1:]
    except:
        pass
    
    #make column headers lowercase and substitute whitespace
    df.columns = [x.lower() for x in df.columns]
    df.columns = df.columns.str.replace(' ','_')

    #convert time to float if excel gives string objects
    df.time = df.time.astype(float)

    #if dataset contains only two individuals and modifier_1 not included, add corresponding modifier_1
    #if 'modifier_1' not in df.columns and len(df.subject.unique()) == 2:
    #    df['modifier_1'] = df.subject.unique()[0]
    #    df['modifier_1'] = np.where(df['subject'] == df.subject.unique()[0], df.subject.unique()[1], df['modifier_1'])

    #add missing columns
    if 'modifier_1' not in df.columns:
        df['modifier_1'] = 'unknown'
    if 'behavioral_category' not in df.columns:
        df['behavioral category '] = 'No behavioral categories present'
    if 'status' not in df.columns:
        df['status'] = 'unknown'
    if 'total_length' not in df.columns:
        df['total_length'] = df['time'].iloc[-1]


    #fill empty values with some 'unknown' value
    df.behavioral_category.fillna('unknown', inplace=True)

    return(df)

def preview(data):
    preview = data.head().to_html()
    return preview

def column_headers(data):
    return data.columns.tolist()


def interaction_network(df, threshold=1):
    """
    Create a network showing the interactions between different fish in the dataset. 
    An edge is drawn or increased by 1 for each row in the dataframe where 'subject' 
    and 'modifier_1' refer to the same individuals.
    
    `Required`
    :param df: The dataframe containing the behavior data
    
    `Optional`
    :threshold: Threshold for edges to be displayed 
    
    """
    
    #remove behavior with no interaction partner and irrelevant data
    interactions_df = df[df.modifier_1.notna()]
    interactions_df = interactions_df[['subject', 'modifier_1']]

    
    #create a dataframe for the edges 
    edges_df = interactions_df.groupby(['subject', 'modifier_1']).size().to_frame(name='records').reset_index()

    #remove edges below the threshold
    edges_df = edges_df[edges_df.records >= threshold]
    
    #add tuples and records as attributes for the network generation
    edges_df['tuples'] = list(zip(edges_df.subject, edges_df.modifier_1))
    edge_attributes_label = dict(zip(edges_df.tuples, edges_df.records))
    
    #change for edge weight
    edges_df.records = edges_df.records * 3 / edges_df.records.max()
    edge_attributes_weight = dict(zip(edges_df.tuples, edges_df.records))
    
    #create directed graph with networkx
    G = nx.DiGraph()
    G.add_edges_from(edges_df.tuples)
    
    #edge labels
    nx.set_edge_attributes(G, edge_attributes_label, name='label')
    
    #edge weight
    nx.set_edge_attributes(G, edge_attributes_weight, name='penwidth')
    
    # make random file extension
    rand = random.randint(0,255)

    #graphviz
    G_dot_string = to_pydot(G).to_string()
    G_dot = graphviz.Source(G_dot_string)
    G_dot.format = 'svg'



    #storage vars
    localhost = 'http://localhost:8000/'
    store = 'uploads/interactions/interactions' + str(rand)
    G_dot.render(store + '.gv', view=False)
    domain = 'https://tiba-352011.ey.r.appspot.com:8000'
    location = localhost + store + '.gv.svg'

    return location
    
def get_fish_ids(df):
    fish_ids = df.subject.unique().tolist()
    fish_ids = [x for x in fish_ids if str(x) != 'nan']
    return fish_ids

def dataplot(df, behavior):
    """
    Plot single behaviors or behavioral categories.
    
    `Required`
    :param df: Dataframe containing the behavior data
    :param behavior: The single behavior or behavioral category to plot
    
    `Optional`
    :param show_avg: display average line
    :param show_grid: display grid
    """
    
    #get fish ids and initial empty figure for the plot
    fish_ids = get_fish_ids(df)
    fig = plt.figure(figsize=(9,7))
    average = pd.DataFrame()
    highest_plot = 0
    
    #loop over all fish_ids and plot their amount of selected interactions 
    for fish in fish_ids:
        fish_df = df[df.subject == fish] 
        if 'behavioral_category' in df:
            categories = fish_df[fish_df.behavioral_category == behavior]
            behaviors = fish_df[fish_df.behavior == behavior]
            fish_df = categories.append(behaviors)
        else:
            fish_df = fish_df[fish_df.behavior == behavior]
        if(len(fish_df)+1>highest_plot):
            highest_plot = len(fish_df)+1
        sum_of_rows = range(1,len(fish_df)+1)
        plt.plot(fish_df.time, sum_of_rows, label=fish)   
    #reset colour cycle 
    plt.gca().set_prop_cycle(None)
    
    #loop over all fish ids and make a dotted line to the end if the fish is not doing any new 
    #behaviors but some other fish are or some time is left
    for fish in fish_ids:
        fish_df = df[df.subject == fish]
        if 'behavioral_category' in df:
            categories = fish_df[fish_df.behavioral_category == behavior]
            behaviors = fish_df[fish_df.behavior == behavior]
            fish_df = categories.append(behaviors)
        else:
            fish_df = fish_df[fish_df.behavior == behavior]
        plt.plot([fish_df.time.max(),df.time.max()], [len(fish_df),len(fish_df)],':')
    plt.gca().set_prop_cycle(None)
    
    #loop over all fish ids and make the beginning  before the first behavior of the fish
    for fish in fish_ids:
        fish_df = df[df.subject == fish]
        if 'behavioral_category' in df:
            categories = fish_df[fish_df.behavioral_category == behavior]
            behaviors = fish_df[fish_df.behavior == behavior]
            fish_df = categories.append(behaviors)
        else:
            fish_df = fish_df[fish_df.behavior == behavior]
        plt.plot([0,fish_df.time.min()], [0,1],':')
       
    #add legend and edge labels
    plt.legend()
    plt.xlabel("Time", fontsize=18, labelpad=10)
    plt.ylabel("|" + str(behavior) + "|", fontsize=18, labelpad=10)
    
    #make frequency of yticks dependent on size of the highest plot
    if highest_plot < 11:
        yticks = range(0,highest_plot)
    elif highest_plot < 26:
        yticks = range(0,highest_plot, 2)
    elif highest_plot < 51:
        yticks = range(0,highest_plot, 5)
    elif highest_plot < 101:
        yticks = range(0,highest_plot, 10)
    elif highest_plot < 201:
        yticks = range(0,highest_plot, 20)
    else:
        yticks = range(0,highest_plot, 50)
    plt.yticks(yticks)
    
    plt.grid(linestyle='-', linewidth=0.2)
 
    # make random file extension
    rand = random.randint(0,255)

    #storage vars
    localhost = 'http://localhost:8000/'
    store = 'uploads/plots/plot_' + str(rand) + '.gv.svg'

    plt.savefig(store, format='png', bbox_inches='tight')
    url = localhost + store

    #bucket_name = os.environ.get('BUCKET_NAME',app_identity.get_default_gcs_bucket_name())
    #client = storage.Client(project='tiba-352011')
    #bucket = client.bucket(bucket_name)
    #blob = bucket.blob('interactions_' + str(rand) + '.png')
    
    #temporarily save image to buffer
    #buf = io.BytesIO()
    #fig.savefig(buf, format='png', bbox_inches='tight')

    #upload buffer contents to gcs
    #blob.upload_from_string(
    #        but.getvalue(),
    #        content_type='image/png')

    #buf.close()

    #gcs url to uploaded matplotlib image
    #url = blob.public_url
    
    return url


def transition_network(
        df,
        option,
        min_edge_count,
        with_status,
        normalized,
        colored,
        colored_edge_thickness,
        color_hue,
        node_color_map,
        node_size_map,
        node_label_map
        ):
    """Input parameters are the behavior file, the specification if the user wants to see the behaviors itself 
    or the behavior cycle of the behavioral categories and the minimal count for a edge to be displayed. 
    This cycle is calculated by splitting the boris-file for each fish and then increasing the edge count for each 
    successing behavior. In the end, the edge count is normalized in [0,1] for each node where edges come from 
    so we have kind of a probability of which behavior follows which behavior"""
    
    local_df = df

    #display tab
    data = option
    multiplication_factor = colored_edge_thickness
    behaviour_key = ''
    colour_value = ''
    
    #reduce tab
    remove_list_cat = [] 
    remove_list = []
    remove_id_list = []
    min_count = min_edge_count
    rmv_id = ''
    add_id = ''
    rmv_bhvr = ''
    add_bhvr =  ''
   
    #node tab
    hue = color_hue 
    node_colour= node_color_map
    node_size = node_size_map
    node_label= node_label_map
    sort_by= 'amount'
    
    fish_ids = get_fish_ids(df)
    fish_ids_after_removal = fish_ids
    successor_list = []

    #prepare dataframe with user input
    #first check if the user wants so see the behaviors or the behavioral categories
    if data == 'behavioral_category':
        #reset list of removed behaviors
        remove_list.clear()
        local_df['chosen_data'] = local_df['behavioral_category']
        
        
        #remove and add behavioral categories
        if rmv_bhvr:
            remove_us = rmv_bhvr.split('\'')
            for x in remove_us:
                if x in local_df.chosen_data.unique() and (len(remove_list_cat)+1 < len(local_df.chosen_data.unique())):
                    remove_list_cat.append(x)
        
        if add_bhvr:
            add_us = add_bhvr.split('\'')
            for x in add_us:
                if x in df.behavioral_category.unique() and x in remove_list_cat:
                    remove_list_cat.remove(x)
        
        #display removed behaviors and create new reduced dataframe
        if remove_list_cat:
            for x in remove_list_cat:
                local_df = local_df.drop(local_df[local_df.behavioral_category == x].index)
    else:
        #reset list of removed behavioral categories
        remove_list_cat.clear()
        local_df['chosen_data'] = local_df['behavior']
        #print all behaviors
       
        #add and remove behaviors
        if rmv_bhvr:
            remove_us = rmv_bhvr.split('\'')
            for x in remove_us:
                if x in local_df.chosen_data.unique() and (len(remove_list)+1 < len(local_df.chosen_data.unique())):
                    remove_list.append(x)            
        if add_bhvr:
            add_us = add_bhvr.split('\'')
            for x in add_us:
                if x in df.chosen_data.unique() and x in remove_list:
                    remove_list.remove(x)  
        if remove_list:
            for x in remove_list:
                local_df = local_df.drop(df[df.chosen_data == x].index)
   
    #remove IDs
    if rmv_id:
        remove_ids = rmv_id.split('\'')
        for x in remove_ids:
            if x in fish_ids and len(remove_id_list)+1 < len(fish_ids):
                remove_id_list.append(x)
    if add_id:
        add_ids = add_id.split('\'')
        for x in add_ids:
            if (x in fish_ids or x in df.modifier_1.unique()) and x in remove_id_list:
                remove_id_list.remove(x)
    if remove_id_list:
        fish_ids_after_removal = [x for x in fish_ids if x not in remove_id_list]
    
    
    #loop through dataframe for each fish and add behavior and successor
    for fish in fish_ids_after_removal:
        id_frame = local_df[local_df.subject == fish]  
        if not (with_status):
            id_frame = id_frame.drop(id_frame[id_frame.status == 'STOP'].index)
        i=0
        k=i+1
        while i < len(id_frame)-1:
            successor_list.append((id_frame.chosen_data.iloc[i], id_frame.status.iloc[i], id_frame.chosen_data.iloc[k], id_frame.status.iloc[k]))
            k+=1
            i+=1
    #lets make an edgelist with behavior and successor
    successor_df = pd.DataFrame(successor_list, columns=['action_1', 'status_1', 'action_2', 'status_2'])
    if (with_status):
        successor_df['plain_behavior'] = successor_df['action_1']
        successor_df['action_1'] = successor_df['action_1'] + ' ' + successor_df['status_1']
        successor_df['action_2'] = successor_df['action_2'] + ' ' + successor_df['status_2']
    else:
        successor_df = successor_df.replace(to_replace="POINT", value="")
    
    successor_df['tuples'] = list(zip(successor_df.action_1, successor_df.action_2))
    successor_df = successor_df.groupby(successor_df.columns.tolist()).size().to_frame(name='records').reset_index()
    
    #normalize the records in [0,1] so that all together are 1 for each action
    behavior_ids = successor_df.action_1.unique().tolist()
    edges_df = pd.DataFrame()
    for action in behavior_ids:
        action_frame = successor_df[successor_df.action_1 == action]
        if(normalized):    
            sum_of_successors = action_frame.records.sum()
            action_frame['normalized'] = action_frame.records.div(sum_of_successors).round(2)
        edges_df = edges_df.append(action_frame)   
    

    #erase edges below min_count
    try:
        if(normalized and min_count):
            edges_df = edges_df[edges_df.normalized > float(min_count)]
        elif not normalized and min_count:    
            edges_df = edges_df[edges_df.records > float(min_count)]
    except: 
        pass
    
    # add average and total time
    times_list = get_total_and_avg_time(df, fish_ids_after_removal)
    times_df = pd.DataFrame(times_list, columns=['action_1', 'total_time', 'avg_time'])
    
    #work on the nodes(behaviors) of the graph so we can later set node-attributes for graphviz
    nodes_df = edges_df[['action_1', 'records']]
    nodes_df = edges_df.groupby('action_1')['records'].sum().to_frame(name='records').reset_index()
    nodes_df = pd.merge(times_df, nodes_df, on='action_1', how='outer')
    nodes_df.columns = ['node', 'total_time', 'avg_time', 'record']
    
    #if a behavior occurs only once/ as last behavior maybe of an animal it is not counted
    if not (with_status):
        nodes_df.record = nodes_df.record.fillna(1)
    #round results
    nodes_df.total_time = nodes_df.total_time.round(2)
    nodes_df.avg_time = nodes_df.avg_time.round(2)
        
    #merge nodes with amount and times in the dataframe for the tuples so 
    #they can be displayed inside the node as label
    labels_1 = nodes_df.copy()
    labels_1.columns = ['action_1', 'total_time_1', 'avg_time_1', 'record_1']
    edges_df = pd.merge(edges_df, labels_1, on='action_1', how='left')
    labels_2 = nodes_df.copy()
    labels_2.columns = ['action_2', 'total_time_2', 'avg_time_2', 'record_2']
    edges_df = pd.merge(edges_df, labels_2, on='action_2', how='left') 
    
    if(node_label == 'amount'):
        edges_df['action_1'] = edges_df['action_1'] + " - " + edges_df['record_1'].astype(str)
        edges_df['action_2'] = edges_df['action_2'] + " - " + edges_df['record_2'].astype(str)
        edges_df['tuples'] = list(zip(edges_df['action_1'],edges_df['action_2']))
        nodes_df['node'] = nodes_df['node'] + " - " + nodes_df['record'].astype(str)
    elif(node_label == 'total_time'):
        edges_df['action_1'] = edges_df['action_1'] + " - " + edges_df['total_time_1'].astype(str)
        edges_df['action_2'] = edges_df['action_2'] + " - " + edges_df['total_time_2'].astype(str)
        edges_df['tuples'] = list(zip(edges_df['action_1'],edges_df['action_2']))
        nodes_df['node'] = nodes_df['node'] + " - " + nodes_df['total_time'].astype(str)
    elif(node_label == 'avg_time'):
        edges_df['action_1'] = edges_df['action_1'] + " - " + edges_df['avg_time_1'].astype(str)
        edges_df['action_2'] = edges_df['action_2'] + " - " + edges_df['avg_time_2'].astype(str)
        edges_df['tuples'] = list(zip(edges_df['action_1'],edges_df['action_2']))
        nodes_df['node'] = nodes_df['node'] + " - " + nodes_df['avg_time'].astype(str)
    
    if(sort_by == 'amount'):
        nodes_df = nodes_df.sort_values(by='record', ascending=False)
    elif(sort_by == 'total_time'):
        nodes_df = nodes_df.sort_values(by='total_time', ascending=False)
    else:
        nodes_df = nodes_df.sort_values(by='avg_time', ascending=False)
    
    # print behavior nodes and amount
    
    
    #logarithmic normalization of record, avg_time and total_time 
    nodes_df.record = (np.log(nodes_df.record)-np.log(nodes_df.record.min()))/(np.log(nodes_df.record.max())-np.log(nodes_df.record.min()))
    nodes_df.total_time = nodes_df.total_time+1
    nodes_df.total_time = (np.log(nodes_df.total_time)-np.log(nodes_df.total_time.min()))/(np.log(nodes_df.total_time.max())-np.log(nodes_df.total_time.min()))
    nodes_df.avg_time = nodes_df.avg_time+1
    nodes_df.avg_time = (np.log(nodes_df.avg_time)-np.log(nodes_df.avg_time.min()))/(np.log(nodes_df.avg_time.max())-np.log(nodes_df.avg_time.min()))
    
    nodes_attributes_avg_time = dict(zip(nodes_df.node, nodes_df.avg_time))

    
    #node sizes dependent on user input and then a dictionary 
    #for node height and width is created to give it to graphviz
    if(node_size == 'amount'):
        nodes_width = dict(zip(nodes_df.node, nodes_df.record*3))
        nodes_height = dict(zip(nodes_df.node, nodes_df.record*1.4))
    elif (node_size == 'total_time'):
        nodes_width = dict(zip(nodes_df.node, nodes_df.total_time*3))
        nodes_height = dict(zip(nodes_df.node, nodes_df.total_time*1.4))
    elif (node_size == 'avg_time'):
        nodes_width = dict(zip(nodes_df.node, nodes_df.avg_time*3))
        nodes_height = dict(zip(nodes_df.node, nodes_df.avg_time*1.4))
        
    #node colour dependent on user input, values are normalized with np.log and then a dictionary
    #for node colour is created to give it to graphviz later
    hue = hue/360
    if(node_colour == 'amount'):
        nodes_df['colour'] = str(hue)+" "+ nodes_df['record'].astype(str) + " 1"
        nodes_colour = dict(zip(nodes_df.node, nodes_df.colour))
    elif (node_colour == 'total_time'):
        nodes_df['colour'] = str(hue)+" "+ nodes_df['total_time'].astype(str) + " 1"
        nodes_colour = dict(zip(nodes_df.node, nodes_df.colour))
    elif (node_colour == 'avg_time'):
        nodes_df['colour'] = str(hue)+" "+ nodes_df['avg_time'].astype(str) + " 1"
        nodes_colour = dict(zip(nodes_df.node, nodes_df.colour))
    
    #create directed graph
    G = nx.DiGraph()
    G.add_edges_from(edges_df.tuples)
    
    #create label and weight for edges
    if(normalized):
        edge_attributes_label = dict(zip(edges_df.tuples, edges_df.normalized))
        edges_df.normalized = edges_df.normalized * 3
        if(colored):
            edges_df.normalized = edges_df.normalized * multiplication_factor
        edge_attributes_weight = dict(zip(edges_df.tuples, edges_df.normalized))
    else:
        edge_attributes_label = dict(zip(edges_df.tuples, edges_df.records))
        #normalize logarithmic
        edges_df.records = (np.log(edges_df.records)-np.log(edges_df.records.min()))/(np.log(edges_df.records.max())-np.log(edges_df.records.min()))
        edges_df.records = edges_df.records + 0.1
        edge_attributes_weight = dict(zip(edges_df.tuples, edges_df.records/edges_df.records.max()))
        if(colored):
            edge_attributes_weight = dict(zip(edges_df.tuples, multiplication_factor * edges_df.records/edges_df.records.max()))
    
    #set edge attributes
    nx.set_edge_attributes(G, edge_attributes_weight, name='penwidth')
    nx.set_edge_attributes(G, edge_attributes_label, name='label')
    
    #set node attributes
    nx.set_node_attributes(G, nodes_width, name='width')
    nx.set_node_attributes(G, nodes_height, name='height')
    if not with_status:
        nx.set_node_attributes(G, nodes_colour, name='fillcolor')
    nx.set_node_attributes(G, 'filled', name='style')
    #create list with all nodes and give each a distinct color
    if(colored):
        unique_nodes = nodes_df.node
        color_list = ['orangered1', 
                      'orange1', 
                      'orchid1', 
                      'palegreen', 
                      'paleturquoise4', 
                      'slategray3', 
                      'darkseagreen2', 
                      'yellowgreen', 
                      'burlywood', 
                      'khaki', 
                      'red',
                      'gold',
                      'turquoise', 
                      'darkgoldenrod2', 
                      'deeppink2',
                      'silver',
                      'aqua',
                      'bisque',
                      'aquamarine2',
                      'beige',
                      'azure4']
        
        try:
            unique_node_colours
        except NameError:
            var_exists = False
        else:
            var_exists = True

        if not (var_exists): 
            unique_node_colours = dict(zip(unique_nodes, color_list))
        
        if(behaviour_key):
            unique_node_colours[behaviour_key] = colour_value
        
        nx.set_node_attributes(G, unique_node_colours, name='fillcolor')
        # give same color to all edges outgoing from the same node
        edges_df['edge_color'] = 'white'
        for key in unique_node_colours.keys():
            edges_df['edge_color'] = np.where(edges_df['action_1'] == key, unique_node_colours.get(key), edges_df['edge_color'])
    
        distinct_edge_colors = dict(zip(edges_df.tuples, edges_df.edge_color))
        nx.set_edge_attributes(G, distinct_edge_colors, name='color')
 
    # add avg time as node attribute
    nx.set_node_attributes(G, nodes_attributes_avg_time, name='avg_time')
    
    #graphviz
    G_dot_string = to_pydot(G).to_string()
    G_dot = graphviz.Source(G_dot_string)
    G_dot.format = 'svg'
    
    # make random file extension
    rand = random.randint(0,255)

    #storage vars
    localhost = 'http://localhost:8000/'
    store = 'uploads/transitions/transitions' + str(rand)
    G_dot.render(store + '.gv', view=False)
    domain = 'https://tiba-352011.ey.r.appspot.com:8000'
    location = localhost + store + '.gv.svg'


    return location
    
def get_total_and_avg_time(df, fish_ids):
    df = df[['time', 'subject', 'chosen_data', 'status']]
    behavior_ids = df.chosen_data.unique().tolist()
    time_list = []
    for behavior in behavior_ids:
        behavior_df = df[df.chosen_data == behavior]
        total = 0
        avg = 0
        for fish in fish_ids:
            id_frame = behavior_df[behavior_df.subject == fish]
            stop_total = id_frame[id_frame.status == 'STOP'].time.sum()
            start_total = id_frame[id_frame.status == 'START'].time.sum()
            total = total + stop_total - start_total
        occurences = len(behavior_df[behavior_df.status == 'START'].index)
        if (math.isnan(occurences) or (occurences < 1)):
            occurences = 1
        if (total == 0.0):
            avg = 0.0
        else:
            avg = total / occurences
        time_list.append((behavior, total, avg))
    return time_list


