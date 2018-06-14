"""
Create a json file in a human readable format for better storing of output.
then read the json file and create the graphs
"""
import json
import os
class OutputJSON:
    """
    Creates the json file for expectimax output
    migration_year_dict will be topmost dict
    migration_dict[year_of_migration] = is_ftth_dict
    is_ftth_dict[ftth_flag] = pen_curve_dict
    pen_curve_dict = {'Cons Pen Curve':cons_mig_info_dict,'Likely Pen Curve':likely_mig_info_dict,'Aggr Pen Curve':aggr_mig_info_dict}
    cons/likely/aggr_mig_info_dict = {'Expected_NPV':,'':,'migration_path':,'year_to_final_tech':,'migration_years':,'final_data_rate':}
    """
    JSON_OUTPUT_PATH =  os.path.join(os.getcwd(),"..")
    def __init__(self,json_file_name):
        self.path_to_json = os.path.join(self.JSON_OUTPUT_PATH,json_file_name+'.json')

        self.is_ftth_dict = {}

        self.cons_migration_info_dict = {}
        self.likely_migration_info_dict = {}
        self.aggr_migration_info_dict = {}

    def build_mig_dict(self,pen_curve,expected_npv, action_list, final_migration_year, mig_years, max_data_rate, time_taken):
        """
        Builds mig_info_dict
        :return:
        """

        if pen_curve not in ["Cons PV", "Likely PV", "Aggr PV"]:
            raise KeyError
        if pen_curve == "Cons PV":
            dict_to_push = self.cons_migration_info_dict
        elif pen_curve == "Likely PV":
            dict_to_push= self.likely_migration_info_dict
        else:
            dict_to_push = self.aggr_migration_info_dict

        dict_to_push["NPV_expected"] = expected_npv
        dict_to_push["mig_path"] = action_list
        dict_to_push["year_to_final_tech"] = final_migration_year
        dict_to_push["mig_years"] = mig_years
        dict_to_push["final_data_rate"] = max_data_rate
        dict_to_push["total_time"] = time_taken

        return dict_to_push

    def dump_to_json(self,dict_to_dump):
        # check if the file is present
        if os.path.exists(self.path_to_json):
            os.remove(self.path_to_json)
        mig_values = [{"is_ftth_and_force":tuple_key[0],"depth_to_force_100mbps_migrations": tuple_key[1],"migration_info":mig_info} for tuple_key,mig_info in dict_to_dump.items()]
        with open(self.path_to_json, 'w') as jsonfile:
            json.dump(mig_values,jsonfile,indent=4)






