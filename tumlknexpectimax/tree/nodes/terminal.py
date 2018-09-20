class TerminalNode:

    def __init__(self,pen_curve,start_year,customers,pv):
        self.pen_curve = pen_curve
        self.START_YEAR = start_year
        self.pv = pv
        self.customers = customers
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
        # Find out the number of customers!!

        # Returning total cashflow from terminal node
        if churn_rate == 0:
            terminal_pv_no_churn = self.pv.PV_no_churn(self.START_YEAR, depth, self.customers[depth], node_technology)
            return terminal_pv_no_churn
            # return self.pv_dict[node_technology][self.pen_curve][self.START_YEAR+depth]
        else:
            # print(self.START_YEAR,depth,churn_rate,self.customers[depth],node_technology)
            terminal_pv_churn = self.pv.PV_churn(self.START_YEAR,depth,churn_rate,self.customers[depth],node_technology)
            return terminal_pv_churn
            # return self.pv_dict[node_technology][self.pen_curve+'_churn'][self.START_YEAR+depth]
