


from common import *
from common import browseFile
from handy_functions import filter_items_from_dataframe, cleanup, bins

from format_excel_file import format_excel_file




class compute_count_summary:

	def __init__(self):
		pass
		



	def compute_count_summary(self, input_file=None, optional_ranges=None):
		
		#this allows for the method to 
		#be call with an optional input file
		if input_file is None:
			input_file = browseFile('Select Count summary file')

			self.count_summary = input_file

			#check file extension and create dataframe
			if self.count_summary.endswith('.csv'):
				self.count_summary = pd.read_csv(self.count_summary)
			else:
				self.count_summary = pd.read_excel(self.count_summary)
		else:
			#meaning a workbook sheet was passed as input file
			data = input_file.values 
			cols = next(data)
			rows = list(data)


			self.count_summary = pd.DataFrame(rows, columns=cols)

		

		if input_file:
			

			#dictionary mapping column headers names to data type
			column_headers = {"<class 'str'>":'Sites', "<class 'numpy.float64'>":'Rssi'}




			#check the 2nd and 3rd columns in Inspected_points dataframe, find out the data type
			#if 'str', header should be sectors; if 'float', header should be RSSI
			#as mapped in the dictionary
			a = type(self.count_summary[self.count_summary.columns[1]][2])
			a = str(a)
			b = type(self.count_summary[self.count_summary.columns[2]][2])
			b = str(b)



			
			#change column headers to dictionary mapping
			self.count_summary.columns = ['Inspected_points', column_headers[a], column_headers[b]]


			#filter sectors of 'Off grid' and 'Null'
			self.count_summary = filter_items_from_dataframe(self.count_summary, ['Sites', 'Sites'], ["Off Grid", "Null"])


			#sort dataframe by sectors
			self.count_summary = self.count_summary.sort_values(by='Sites')
			
			
			#splice sectors column at the last underscore
			sectors_splice = [ row[:row.rfind("_")] for row in self.count_summary['Sites'].tolist() ]


			#clean up sites to remove any other underscore
			sectors_splice = cleanup(sectors_splice)


			#replace sectors column with cleaned spliced values
			self.count_summary['Sites'] = sectors_splice


			#multiply Rssi by -1 to make it positive 
			#(so that the pivot table can be in ascending order e.g from 75 to 105
			# instead of -105 to -75)
			self.count_summary['Rssi'] = self.count_summary['Rssi'] * -1
			

			#round up Inspected_points values to whole numbers
			#count_summary['Inspected_points'] = count_summary['Inspected_points'].round(0)


			#instantiate bins class
			bin_object = bins()


			#add an additional column an group RSSI by bins
			self.count_summary['Rssi_bins'] = bin_object.make_bins_method(self.count_summary['Rssi'].tolist(), optional_ranges)
			
			
			## remove unwanted range
			self.count_summary = self.count_summary[self.count_summary['Rssi_bins'] != bin_object.outside_bin]


			#create pivot table, values == sum of Inspected_points
			count_summary_pivot = pd.pivot_table(self.count_summary, index='Sites', columns='Rssi_bins', values='Inspected_points', fill_value=0, aggfunc='count')

			
			#do a cumulative sum on the column values
			count_summary_pivot = count_summary_pivot.cumsum(axis=1)


			
			return count_summary_pivot







	def format_count_summary(self):

		output_dataframe = self.compute_count_summary()

		#add totals of each column
		output_dataframe.loc['Total']= output_dataframe.sum(numeric_only=True, axis=0)

		output_filename = easygui.filesavebox()
		
		if not output_filename.endswith('.xlsx'):
			output_filename = output_filename + '.xlsx'

		output_dataframe.to_excel(output_filename, index = True)

		return format_excel_file(output_filename, use_comma=True)