
"""
Functions that can be used in different stat.py files.
A very handy one is the make_bins functions. 

"""

import sys


#technology to RSSI column mapping

tech_to_rssi_map = {'GSM':'RXLEV_FdB', 'WCDMA':'SANCPICHRSCP_1', 'LTE':'ServingCellRSRPdBM_1'}
rssi_map = {'RXLEV_FdB':'RXLEV', 'SANCPICHRSCP_1':'RSCP', 'ServingCellRSRPdBM_1':'RSRP'}










#filter rows from dataframe
def filter_items_from_dataframe(dataframe, columns, items):
    i = 0
    for item in items:

    	#e.g ## remove unwanted range
		#pop_stats = pop_stats[pop_stats['Rssi_bins'] != '<105']
        dataframe = dataframe[dataframe[columns[i]] != item]
        i = i+1
    return dataframe







#Find and clean up instances where you have LRAS_23_1_2 ==> LRAS_23_1 ==> LRAS_23
def cleanup(column):
    import re
    i = 0
    j = 1
    
    while i < len(column)-1:
        row = column[i]
        pattern = re.compile(row + r'_\d+')
        
        if pattern.findall(column[j]):
            while (j < len(column)) and (pattern.findall(column[j])):
                column[j] = row
                j = j+1

            i = j
            j = j+1
            
        else:
            i = i+1
            j = j+1
        
    return column






def modifiedMovingAverage(data, window):
    import statistics as stats
    half_window = int(window//2)
    mma = []
    for current_index in range(len(data)):
        if half_window > current_index:
            start = 0
            end = current_index + half_window + 1
            d = data[start:end]
            mma.append(stats.mean(d))

        elif current_index + half_window > len(data) - 1:
            start = current_index - half_window
            end = len(data)
            d = data[start:end]
            mma.append(stats.mean(d))

        else:
            start = current_index - half_window
            end = current_index + half_window + 1
            d = data[start:end]
            mma.append(stats.mean(d))
    return mma










def addDummyValues(distanceResultList, RssiWattsList):
    i = 0
    
    while i+1 < len(distanceResultList):
        
        distanceBtwPoints = distanceResultList[i+1] - distanceResultList[i]
        if distanceBtwPoints > 0.100:
            intervals = int(distanceBtwPoints//10)
            for interval in range(intervals-1):
                distanceResultList.insert(i+1, distanceResultList[i]+0.010)
                RssiWattsList.insert(i+1, 1e-14)
                i=i+1
        else:
            i=i+1
    return list(zip(distanceResultList, RssiWattsList))





















class bins:
    """
    Had to make this class so i would be able to
    use the damn outside bin variable in another module
    """

    def __init__(self):
        pass




    def make_bins(self, binsize_start_end, column, ranges):
        """
        in this method we set a default argument, "optional_ranges", to none.
        this ranges argument is used if an external list of ranges is
        passed to this method. if one is not passed, the default is set to none
        and is passed to the make_bins function
        """

        bin_column = []
        
        if ranges is None:
            bin_size = int(binsize_start_end[0])
            start = int(binsize_start_end[1])
            end = int(binsize_start_end[2])
            ranges = [i for i in range(start, end+bin_size, bin_size)]
            


        #global outside_bin
        self.outside_bin = '<' + str(ranges[-1])
        
        i = 0

        for row in column:
            while i < len(ranges):
                if row <= ranges[i]:
                    bin_column.append(ranges[i])
                    break
                i = i+1
                
                if i == len(ranges):
                    bin_column.append(self.outside_bin)
                    break
            i = 0
        
        #global bin_column_len
        #thought of using this to specify len of bins
        #make use of it in formatting excel
        self.bin_column_len = len(bin_column)
        self.bin_values = ranges

        return bin_column





    def make_bins_method(self, column, optional_ranges=None):

        """
	    in this method we set a default argument, "optional_ranges", to none.
	    this ranges argument is used if an external list of ranges is
	    passed to this method. if one is not passed, the default is set to none
	    and is passed to the make_bins function.

	    also if a list of external ranges is passed, there is not need to 
	    create the gui to ask for binsize and start and end arguments
    	"""

        if optional_ranges is None:
            
            #if optional range is none, make a gui to get user-defined ranges
            import easygui

            make_bins_msg = 'Enter the Bin size, Start and Stop RSSI values'
            make_bins_title = 'Group RSSI into bins e.g 75, 85, 95'
            make_bins_field_names = ['Bin size (e.g. 10)', 'Start RSSI (e.g. 75)', 'Stop RSSI (e.g. 105)']

            make_bins_values = easygui.multenterbox(make_bins_msg, make_bins_title, make_bins_field_names)


            while make_bins_values is None:

                msg = """Do you want to exit? Click 'Continue' to exit or 'Cancel' to go back."""
                title = "Please confirm"

                if easygui.ccbox(msg, title):
                    sys.exit(0)
                else:
                    make_bins_values = easygui.multenterbox(make_bins_msg, make_bins_title, make_bins_field_names)


            if '' in make_bins_values:

                while '' in make_bins_values:

                    msg = "{} is a required field. Click 'Continue' to input missing value or 'Cancel' to exit".format(make_bins_field_names[make_bins_values.index('')])
                    title = 'Missing Value'


                    if easygui.ccbox(msg, title):
                        make_bins_values = easygui.multenterbox(make_bins_msg, make_bins_title, make_bins_field_names)
                    else:
                        sys.exit(0)

                    return self.make_bins(make_bins_values, column, optional_ranges)

            else:
                return self.make_bins(make_bins_values, column, optional_ranges)


        else:
            #else pass optional range to make_bin method
            return self.make_bins(0, column, optional_ranges)








