from tumlknexpectimax.tree.nodes.chance import ChanceNode
from tumlknexpectimax.tree.nodes.terminal import TerminalNode

class MaxNode:

    def __init__(self, node_mig_dict_forced, node_mig_dict_unforced,capex_values,tech_index, mig_matrix, pv_dict,
                 pen_curve, path_list, forcing_depth, start_year, max_year):
        """

        """
        self.START_YEAR = start_year
        self.MAX_YEAR = max_year
        self.node_mig_dict_forced = node_mig_dict_forced
        self.node_mig_dict_unforced = node_mig_dict_unforced
        self.capex_values_dict = capex_values
        self.techindex = tech_index
        self.mig_matrix = mig_matrix
        self.pv_dict = pv_dict
        self.pen_curve = pen_curve
        self.path_list = path_list
        self.force_depth = int(forcing_depth)

        pass

    def maximizer(self, type, node_technology,depth,children,churn_rate,prob_churn):
        """

        :param type:
        :param node_technology:
        :param depth:
        :param children:
        :param churn_rate:
        :param prob_churn:
        :return:
        """
        current_year = self.START_YEAR+depth
        capex_rev_terminal = 0
        if current_year == self.MAX_YEAR:   # If we have reached max year we should hit a terminal node
            terminal = TerminalNode(self.pv_dict,self.pen_curve,self.START_YEAR)
            if depth < 10:
                capex_rev_terminal = -(self.capex_values_dict['Electronic Cost'][self.techindex[node_technology]])
            return [sum([terminal.terminal_node(node_technology,dep,churn_rate) for dep in range(depth, 2038-self.START_YEAR)])+capex_rev_terminal, depth, node_technology,'NONE', []]    # Returns the value of the PV cashflow along with a list of the [depth, technology_of_terminal, child_of_terminal, previous_list]
        elif node_technology in [4,5,6,7,8,11,12,13]:
            # TODO: Need to check here if we can try to find the sum value of the remainder years and whether it affects our decision
            terminal = TerminalNode(self.pv_dict,self.pen_curve,self.START_YEAR)
            if depth < 10:
                capex_rev_terminal = -(self.capex_values_dict['Electronic Cost'][self.techindex[node_technology]])
            return [sum([terminal.terminal_node(node_technology,dep,churn_rate) for dep in range(depth, 2038-self.START_YEAR)])+capex_rev_terminal, depth, node_technology,'NONE', []]
        else:
            next_year_chancer = ChanceNode(self.node_mig_dict_forced, self.node_mig_dict_unforced, self.capex_values_dict, self.techindex, self.mig_matrix, self.pv_dict, self.pen_curve, self.path_list, self.force_depth,self.START_YEAR, self.MAX_YEAR)
            max_derived_cf = -1000000000
            temp_dict = {}
            max_child_tech = node_technology
            max_child_list = []
            if depth >= self.force_depth-1:
                current_child_list = self.node_mig_dict_forced[node_technology]
            else:
                current_child_list = self.node_mig_dict_unforced[node_technology]
            for child_technology in current_child_list:

                if child_technology is node_technology:

                    if depth == 10: # child_technology is node_technology
                        capex_rev = -(self.capex_values_dict['Electronic Cost'][self.techindex[node_technology]])
                    else:
                        capex_rev = 0
                else:
                    if depth == 10:

                        capex_rev = -self.capex_values_dict['Electronic Cost'][self.techindex[node_technology]] -self.mig_matrix[self.techindex[child_technology]][self.techindex[node_technology]]
                    else:
                        capex_rev = -self.mig_matrix[self.techindex[child_technology]][self.techindex[node_technology]]

                if type is 'MAXNOCHURN':
                    child_details = next_year_chancer.chancer('Chance', child_technology, depth+1, current_child_list, 0, prob_churn)
                else:
                    child_details = next_year_chancer.chancer('Chance', child_technology, depth+1, current_child_list, 0.1, prob_churn)

                future_cf = child_details[0]
                if isinstance(child_details[1:][0],list):

                    child_list_maxnodes = child_details[1:][0]
                else:
                    child_list_maxnodes = child_details[1:]
                if churn_rate == 0:
                    curr_cf = self.pv_dict[node_technology][self.pen_curve][current_year]
                else:
                    curr_cf = self.pv_dict[node_technology][self.pen_curve+'_churn'][current_year]

                derived_cf = capex_rev+curr_cf+future_cf
                temp_dict[child_technology] = child_list_maxnodes
                if derived_cf > max_derived_cf:
                    max_derived_cf = derived_cf
                    max_child_tech = child_technology
                    max_child_list = temp_dict[max_child_tech]
            self.path_list.append(max_child_list)

            return [max_derived_cf, depth, node_technology, max_child_tech, max_child_list]
