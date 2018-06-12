import copy



class ChanceNode:
    """

    """
    def __init__(self, node_mig_dict_forced, node_mig_dict_unforced,capex_values,tech_index, mig_matrix,
                 pen_curve, path_list, forcing_depth, start_year, max_year,pv):
        """

        :param node_mig_dict_forced:
        :param node_mig_dict_unforced:
        :param capex_values:
        :param tech_index:
        :param mig_matrix:
        :param pv_dict:
        :param pen_curve:
        :param path_list:
        :param forcing_depth:
        :param start_year:
        """
        import tumlknexpectimax.tree.nodes.max as max2

        self.START_YEAR = start_year
        self.MAX_YEAR = max_year
        self.node_mig_dict_forced = node_mig_dict_forced
        self.node_mig_dict_unforced = node_mig_dict_unforced
        self.capex_values_dict = capex_values
        self.techindex = tech_index
        self.mig_matrix = mig_matrix
        self.pen_curve = pen_curve
        self.path_list = path_list
        self.force_depth = int(forcing_depth)
        self.pv = pv
        self.current_year_maxer = max2.MaxNode(self.node_mig_dict_forced, self.node_mig_dict_unforced,self.capex_values_dict
                                          , self.techindex, self.mig_matrix, self.pen_curve, self.path_list,self.force_depth,self.START_YEAR, self.MAX_YEAR,self.pv)
        pass

    def depthCount(self,lst):

        maxdepth = 0
        while True:
            if lst == 'NONE':
                return maxdepth
            elif not lst:
                return maxdepth
            else:
                lst = lst.pop(-1)
                maxdepth+=1

    def chancer(self, node_technology,depth,children,prob_churn):
        """

        :param type:
        :param node_technology:
        :param depth:
        :param children:
        :param churn_rate:
        :param prob_churn:
        :return:
        """

        child_details_churn = self.current_year_maxer.maximizer('MAXCHURN',node_technology,depth, children,0.1,prob_churn)
        chance_cf_churn = child_details_churn[0]
        child_list1 = child_details_churn[1:]
        child_details_nochurn = self.current_year_maxer.maximizer('MAXNOCHURN',node_technology,depth, children, 0.0,prob_churn)
        chance_cf_nochurn = child_details_nochurn[0]
        child_list2 = child_details_nochurn[1:]
        # TODO: CHECK IF LEN WORKS
        try:
            countchurn = copy.deepcopy(child_list1)
            countnochurn = copy.deepcopy(child_list2)
            if self.depthCount(countchurn) < self.depthCount(countnochurn):
                return [prob_churn*chance_cf_churn+(1-prob_churn)*chance_cf_nochurn,child_details_churn]
            else:
                return [prob_churn*chance_cf_churn+(1-prob_churn)*chance_cf_nochurn,child_details_nochurn]
        except Exception as e:
            print('Exception is', e)
