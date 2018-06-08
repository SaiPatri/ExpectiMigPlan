import copy
import tumlknexpectimax.tree.nodes.max as max1

class TreeBuilder:
    """

    """
    # self.node_mig_dict_forced, self.node_mig_dict_unforced, self.capex_values_dict, self.techindex, self.mig_matrix, self.pv_dict, self.pen_curve, self.path_list, self.force_depth,self.START_YEAR, self.MAX_YEAR
    def __init__(self,node_mig_dict_forced, node_mig_dict_unforced,capex_values,tech_index, mig_matrix,
                 pen_curve, path_list, forcing_depth, start_year, max_year,present_value_gen):
        """
        """
        self.node_mig_dict_forced = node_mig_dict_forced
        self.node_mig_dict_unforced = node_mig_dict_unforced
        self.capex_values = capex_values
        self.tech_index = tech_index
        self.mig_matrix = mig_matrix
        self.pen_curve = pen_curve
        self.path_list = path_list
        self.forcing_depth = forcing_depth
        self.START_YEAR = start_year
        self.MAX_YEAR = max_year
        self.pv = present_value_gen

        pass

    def depthCount(self, tree_list):
        maxdepth = 0
        while True:
            if tree_list == 'NONE':
                return maxdepth
            elif not tree_list:
                return maxdepth
            else:
                tree_list = tree_list.pop(-1)
                maxdepth+=1

    def build_mini_tree(self,action_list,node_mig_dict,start_tech,churn_prob, pen_curve):
        # start_tech = 1
        # TODO: import tree.build_tree
        maxim = max1.MaxNode(self.node_mig_dict_forced, self.node_mig_dict_unforced,self.capex_values,self.tech_index, self.mig_matrix,
                 self.pen_curve, self.path_list, self.forcing_depth, self.START_YEAR, self.MAX_YEAR,self.pv)

        expectidetails_churn = maxim.maximizer('MAXCHURN',start_tech,0,node_mig_dict[start_tech],0.1,churn_prob)
        max_cf_churn = expectidetails_churn[0]
        child_list_cfchurn = expectidetails_churn[1:]
        expectidetails_nochurn = maxim.maximizer('MAXNOCHURN',start_tech,0,node_mig_dict[start_tech],0.0,churn_prob)
        max_cf_nochurn = expectidetails_nochurn[0]
        child_list_cfnochurn = expectidetails_nochurn[1:]
        intermediate_cf = churn_prob*max_cf_churn + (1-churn_prob)*max_cf_nochurn
        # print('------------Penetration Curve: ',pen_curve, '-----------------')
        # print('On the topmost node, expected cashflow with churn is', max_cf_churn)
        # print('On the topmost node, expected cashflow without churn is', max_cf_nochurn)
        # print('Maxchurn nodes children are ', child_list_cfchurn)
        # print( 'Maxnochurn nodes children are', child_list_cfnochurn)

        # TODO: TEST IF THIS LEN WORKS
        treechurn = copy.deepcopy(child_list_cfchurn)
        treenochurn = copy.deepcopy(child_list_cfnochurn)
        if self.depthCount(treechurn) < self.depthCount(treenochurn):
            child_path_list = child_list_cfchurn
        else:
            child_path_list = child_list_cfnochurn


        # child_path_list = child_list_cfchurn
        # TODO: WHAT THE FUCKKKKKKK DO YOU WANT FROM HERE?!?!?!?!?!
        # TODO: ANSWER--- I need the final expected NPV+ path taken by the children
        if child_path_list == child_list_cfchurn:

            toptree = copy.deepcopy(expectidetails_churn)
        else:
            toptree = copy.deepcopy(expectidetails_nochurn)

        while True:
            if toptree[3] == 'NONE':
                action_list.append(toptree[2])
                break
            else:
                action_list.append(toptree[2])
                toptree = toptree.pop(-1)

        return intermediate_cf, child_path_list[2], action_list
