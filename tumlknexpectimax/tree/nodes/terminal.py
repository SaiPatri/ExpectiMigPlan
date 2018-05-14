class TerminalNode:
    def __init__(self, pv_dict,pen_curve,start_year):
        self.pv_dict = pv_dict
        self.pen_curve = pen_curve
        self.START_YEAR = start_year
        pass

    def terminal_node(self,node_technology,depth,churn_rate):
        """
        Here we return the cashflow at the terminal nodes. The terminal nodes do not have any capex.
        :param node_technology:
        :param depth:
        :param pen_curve:
        :param churn_rate:
        :return:
        """
        # Returning total cashflow from terminal node
        if churn_rate == 0:
            return self.pv_dict[node_technology][self.pen_curve][self.START_YEAR+depth]
        else:
            return self.pv_dict[node_technology][self.pen_curve+'_churn'][self.START_YEAR+depth]

