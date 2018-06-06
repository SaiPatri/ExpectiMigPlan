"""
File: xls_parser.py
Functionality: Uses panda to parse input data excel file for different technology
Author: Sai Kireet Patri
Copyright: Technische Universitaet Muenchen
"""

import pandas as pd
import os


class Parser:

    CURRENT_WORKING_DIR = os.path.join(os.getcwd(),'excel_data')
    # CURRENT_WORKING_DIR = os.path.join(os.getcwd(),'excel_data')

    def __init__(self):

        pass

    def xls_parse_residential(self, data_file):

        """
        Parses the residential input excel file and converts to pandas dictionary. More functions will be added
        later for other files
        :param data_file: name of the data file to parse
        :return: parsed panda data-frame of each of the worksheets.
        """

        file_path = os.path.join(self.CURRENT_WORKING_DIR,data_file)
        excel_file1 = pd.ExcelFile(file_path)
        parsed_adsl_0 = excel_file1.parse('ADSL').set_index('Year') # 'ADSL'
        parsed_fttc_1 = excel_file1.parse('FTTC_2_STAGE_GPON').set_index('Year') # 'FTTC_2_Stage_GPON'
        parsed_fttb_2 = excel_file1.parse('FTTB_2_STAGE_XGPON').set_index('Year') # 'FTTB_2_STAGE_XGPON_MIG'
        parsed_fttb_3 = excel_file1.parse('FTTB_1_STAGE_UDWDM_GF').set_index('Year') # 'FTTB_2_STAGE_WDMPON_GF'
        parsed_ftth_4 = excel_file1.parse('FTTH_2_STAGE_UDWDM').set_index('Year') # 'FTTH_2_STAGE_UDWDM'
        parsed_ftth_5 = excel_file1.parse('FTTH_2_STAGE_XGPON').set_index('Year') # 'FTTH_2_STAGE_XGPON'
        parsed_fttc_6_force = excel_file1.parse('FTTC_2_STAGE_GPON_FORCE').set_index('Year') # 'FTTC_2_Stage_GPON_FORCE'
        parsed_fttb_7_force = excel_file1.parse('FTTB_2_STAGE_XGPON_FORCE').set_index('Year') # 'FTTB_2_STAGE_XGPON_FORCE'
        parsed_fttb_8_force = excel_file1.parse('FTTB_1_STAGE_UDWDM_FORCE').set_index('Year') # 'FTTB_1_STAGE_UDWDM_FORCE'
        parsed_fttc_hybridpon_9 = excel_file1.parse('FTTC_Hybridpon').set_index('Year')# FTTC_Hybridpon
        parsed_fttb_hybridpon_10 = excel_file1.parse('FTTB_Hybridpon').set_index('Year')# FTTB_Hybridpon
        parsed_ftth_hybridpon_11 = excel_file1.parse('FTTH_Hybridpon').set_index('Year')# FTTH_Hybridpon
        parsed_fttc_hybridpon_force_12 = excel_file1.parse('FTTC_Hybridpon_FORCE').set_index('Year')# FTTC_Hybridpon_FORCE
        parsed_fttb_hybridpon_force_13 = excel_file1.parse('FTTB_Hybridpon_FORCE').set_index('Year')# FTTB_Hybridpon_FORCE

        capex_values = excel_file1.parse('CAPEX').set_index('Technology Name') # CAPEX
        mig_matrix = excel_file1.parse('MIG_MATRIX').set_index('Technology') # MIG_MATRIX
        return parsed_adsl_0,parsed_fttc_1,parsed_fttb_2, parsed_fttb_3, parsed_ftth_4, parsed_ftth_5, parsed_fttc_6_force, parsed_fttb_7_force, parsed_fttb_8_force, parsed_fttc_hybridpon_9, parsed_fttb_hybridpon_10, parsed_ftth_hybridpon_11, parsed_fttc_hybridpon_force_12, parsed_fttb_hybridpon_force_13,capex_values, mig_matrix

    def xls_parse_business(self, data_file):

        """
        Parses the residential input excel file and converts to pandas dictionary. More functions will be added
        later for other files
        :param data_file: name of the data file to parse
        :return: parsed panda data-frame of each of the worksheets.
        """

        file_path = os.path.join(self.CURRENT_WORKING_DIR,data_file)
        excel_file1 = pd.ExcelFile(file_path)
        parsed_adsl_0 = excel_file1.parse('ADSL').set_index('Year') # 'ADSL'
        parsed_fttc_1 = excel_file1.parse('FTTC_GPON_25').set_index('Year') # 'FTTC_2_Stage_GPON'
        parsed_fttb_2 = excel_file1.parse('FTTB_XGPON_50').set_index('Year') # 'FTTB_2_STAGE_XGPON_MIG'
        parsed_fttb_3 = excel_file1.parse('FTTB_UDWDM_50').set_index('Year') # 'FTTB_2_STAGE_WDMPON_GF'
        parsed_ftth_4 = excel_file1.parse('FTTH_UDWDM_100').set_index('Year') # 'FTTH_2_STAGE_UDWDM'
        parsed_ftth_5 = excel_file1.parse('FTTH_XGPON_100').set_index('Year') # 'FTTH_2_STAGE_XGPON'
        parsed_fttc_6_force = excel_file1.parse('FTTC_GPON_100').set_index('Year') # 'FTTC_2_Stage_GPON_FORCE'
        parsed_fttb_7_force = excel_file1.parse('FTTB_XGPON_100').set_index('Year') # 'FTTB_2_STAGE_XGPON_FORCE'
        parsed_fttb_8_force = excel_file1.parse('FTTB_UDWDM_100').set_index('Year') # 'FTTB_1_STAGE_UDWDM_FORCE'
        parsed_fttc_hybridpon_9 = excel_file1.parse('FTTC_Hybridpon_25').set_index('Year')# FTTC_Hybridpon
        parsed_fttb_hybridpon_10 = excel_file1.parse('FTTB_Hybridpon_50').set_index('Year')# FTTB_Hybridpon
        parsed_ftth_hybridpon_11 = excel_file1.parse('FTTH_Hybridpon_100').set_index('Year')# FTTH_Hybridpon
        parsed_fttc_hybridpon_force_12 = excel_file1.parse('FTTC_Hybridpon_100').set_index('Year')# FTTC_Hybridpon_FORCE
        parsed_fttb_hybridpon_force_13 = excel_file1.parse('FTTB_Hybridpon_100').set_index('Year')# FTTB_Hybridpon_FORCE

        capex_values = excel_file1.parse('CAPEX').set_index('Technology Name') # CAPEX
        mig_matrix = excel_file1.parse('MIG_MATRIX').set_index('Technology') # MIG_MATRIX
        return parsed_adsl_0,parsed_fttc_1,parsed_fttb_2, parsed_fttb_3, parsed_ftth_4, parsed_ftth_5, parsed_fttc_6_force, parsed_fttb_7_force, parsed_fttb_8_force, parsed_fttc_hybridpon_9, parsed_fttb_hybridpon_10, parsed_ftth_hybridpon_11, parsed_fttc_hybridpon_force_12, parsed_fttb_hybridpon_force_13,capex_values, mig_matrix


if __name__ == "__main__":
    parsed = Parser()
    adsl0,fttc1, fttb2, fttb3, ftth4, ftth5, fttc6force, fttb7force, fttb8force, fttchybrid9,fttbhybrid10,ftthhybrid11,fttchybridforce12,fttbhybridforce13, capex, mig_capex = parsed.xls_parse_business('input_data_business.xlsx')
    max_year = 2038
    current_year = 2018
    pen_curve = 'Aggr PV'
    # print sum([fttc1.loc[year][pen_curve] for year in range(current_year,max_year+1)])
    print(mig_capex.iloc[13][10])



