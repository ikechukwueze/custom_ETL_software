


from common import *
from common import browseFile
from format_excel_file import *
from format_excel_file import format_excel_file
from format_barchart import format_barchart
from format_graph import format_graph



#import classes from respective modules
from area_stats import compute_area_stats
from pop_stats import compute_pop_stats
from count_summary import compute_count_summary
from sites_config import sites_config

from dt_barchart import dt_barchart
from dt_graph import dt_graph


#create objects
area_stats_calculation = compute_area_stats()
pop_stats_calculation = compute_pop_stats()
count_summary_calculation = compute_count_summary()
sites_config = sites_config()

dt_barchart = dt_barchart()
dt_graph = dt_graph()



class group_prediction_stats:

	def __init__(self):
		#self.checkboxes = checkboxes
		#self.checkbox_labels = checkbox_labels
		pass




	def group_checkbox_states(self, checkboxes, checkbox_labels):
		
		self.checkboxes = checkboxes	
		self.checkbox_labels = checkbox_labels
		
		
		checkbox_state = {}
		checkbox_current_state = []

		
		#iterate through checkbox var from gui and use the .get() method
		#to get the states i.e checked/uncheck == 1/0 then append to list
		for checkbox in self.checkboxes:
			checkbox_current_state.append(checkbox.get())
		
		
		#create a key/value map using checkbox_current_state values
		#map the values to the checkbox_labels names i.e area:1, pop:0 etc
		for i in range(len(checkbox_current_state)):
			key = self.checkbox_labels[i]
			value = checkbox_current_state[i]
			
			checkbox_state[key] = value
		#print(checkbox_state)
		return checkbox_state #dictionary of labels and check states




	def load_combined_excel_file(self):
		#self.multiple_sheets = multiple_sheets
		combined_workbook = browseFile()
		
		if combined_workbook is not None:
			#load the combined workbook in read only mode for memory efficiency
			self.combined_workbook = load_workbook(combined_workbook, read_only=True)

			#get a list of all the sheet names in the workbook
			self.combined_workbook_sheets = self.combined_workbook.sheetnames





	



	#what sort of silly name is "which pred"? smh
	def which_pred(self, checked_predictions):
		
		#this method requires checkbox vars, labels from gui module
		#self.checkboxes = checkboxes
		#self.checkbox_labels = checkbox_labels
		
		#the method is called from above
		#recall, self.group_checkbox_states() returns a dictionary
		#checked_predictions = self.group_checkbox_states()


		#lists to store the computed stats output and headers for the tables
		combined_stats_output = []
		combined_stats_headers = []

		combined_barchart_output = []
		combined_barchart_headers = []

		combined_graph_output = []
		combined_graph_headers = []


		#area stat ranges has been set to None because its value is only available
		#as self.area_ranges after the compute_area_stats method is run
		area_stat_ranges = None

		has_prediction_stats=False
		if ('sites' or 'area' or 'population' or 'count_summary') in checked_predictions.keys():

			if checked_predictions['sites'] and 'sites' in self.combined_workbook_sheets:

				sites_df = sites_config.compile_sites_config(input_file=self.combined_workbook['sites'])
				
				combined_stats_output.append(sites_df)
				combined_stats_headers.append('SITES CONFIG')




		
			if checked_predictions['area'] and 'area' in self.combined_workbook_sheets:

				area_df = area_stats_calculation.compute_area_stats(input_file=self.combined_workbook['area'])
				area_stat_ranges = area_stats_calculation.area_ranges
				
				combined_stats_output.append(area_df)
				combined_stats_headers.append('AREA')
				print('done with area')


			#check if use_area_ranges is checked and if area_stats_ranges has a value i.e is not None
			if checked_predictions['use_area_ranges'] and area_stat_ranges is not None:

				if checked_predictions['population'] and 'population' in self.combined_workbook_sheets:
					
					#call the compute stats method with the optional range
					pop_df = pop_stats_calculation.compute_pop_stats(input_file=self.combined_workbook['population'], optional_ranges=area_stat_ranges)

					combined_stats_output.append(pop_df)
					combined_stats_headers.append('POPULATION')
					print('done with pop')


				if checked_predictions['count_summary'] and 'count summary' in self.combined_workbook_sheets:
					
					#call the compute stats method with the optional range
					count_summary_df = count_summary_calculation.compute_count_summary(input_file=self.combined_workbook['count summary'], optional_ranges=area_stat_ranges)

					combined_stats_output.append(count_summary_df)
					combined_stats_headers.append('COUNT SUMMARY')
					print('done with count')

				

			else:
				if checked_predictions['population'] and 'population' in self.combined_workbook_sheets:
					
					pop_df = pop_stats_calculation.compute_pop_stats(input_file=self.combined_workbook['population'])
					combined_stats_output.append(pop_df)
					combined_stats_headers.append('POPULATION')
					print('done with pop')


				if checked_predictions['count_summary'] and 'count summary' in self.combined_workbook_sheets:
					
					count_summary_df = count_summary_calculation.compute_count_summary(input_file=self.combined_workbook['count summary'])
					combined_stats_output.append(count_summary_df)
					combined_stats_headers.append('COUNT SUMMARY')
					print('done with count')

			if len(combined_stats_headers) > 0:
				has_prediction_stats = True

		barchart_data = graph_data = False
		if ('CDF' or 'PDF' or 'graph') in checked_predictions.keys() and (checked_predictions['CDF'] or checked_predictions['PDF'] or checked_predictions['graph']):
			pdf = checked_predictions['PDF']
			#print(pdf)
			cdf = checked_predictions['CDF']
			#print(cdf)
			graph = checked_predictions['graph']

			

			optional_bin_values = None
			for sheetname in self.combined_workbook_sheets:
				if cdf or pdf:
					barchart_data = True
					barchart = dt_barchart.create_barchart(input_file=self.combined_workbook[sheetname], pdf=pdf, cdf=cdf, column_header=sheetname, optional_bin_values=optional_bin_values)
					combined_barchart_output.append(barchart)
					combined_barchart_headers.append(sheetname)

					optional_bin_values = dt_barchart.new_bin_values
				
			#	if graph:
			#		graph_data = True
			#		graph_df = dt_graph.create_graph(input_file=self.combined_workbook[sheetname], column_header=sheetname)
			#		combined_graph_output.append(graph_df)
			#		combined_graph_headers.append(sheetname)
			
			if graph:
				for sheetname in self.combined_workbook_sheets:
					graph_data = True
					if barchart_data:
						data_from_barchart = dt_barchart.useful_chart_data
						graph_df = dt_graph.create_graph(input_file=0, data_from_barchart=data_from_barchart , column_header=sheetname)
					#print(sheetname)
					else:
						graph_df = dt_graph.create_graph(input_file = self.combined_workbook[sheetname], column_header=sheetname)
					combined_graph_output.append(graph_df)
					combined_graph_headers.append(sheetname)


		




		#concatenate the resulting dataframes to form a table
		#setting axis=1 combines them side by side, sort=True, sorts values
		#if (len(combined_stats_output) > 0) or (len(combined_graph_output) > 0) or (len(combined_barchart_output) > 0):
		if has_prediction_stats:
			#print(combined_stats_headers)

			#if 'SITES CONFIG' or 'AREA' or 'POPULATION' or 'COUNT SUMMARY' in combined_stats_headers:
				#print('formatting')

			save_as_file = easygui.filesavebox(title='Save result as', filetypes='*.xlsx')
			if not save_as_file.endswith('.xlsx'):
				save_as_file = save_as_file + '.xlsx'

			p = pd.concat(combined_stats_output, keys=combined_stats_headers, sort=True, axis=1)

			#add totals of each column
			p.loc['Total']= p.sum(numeric_only=True, axis=0)
			p.to_excel(save_as_file, sheet_name='Prediction Stats', index=True)
			format_excel_file(save_as_file, has_combined_stats=True, use_comma=True)
			
			
		if barchart_data or graph_data:
			
			save_as_file = easygui.filesavebox(title='Save result as', filetypes='*.xlsx')
			if not save_as_file.endswith('.xlsx'):
				save_as_file = save_as_file + '.xlsx'

			writer = pd.ExcelWriter(save_as_file, engine='xlsxwriter')
			
			if barchart_data:
				p = pd.concat(combined_barchart_output, sort=True, axis=1)
				p.to_excel(writer, sheet_name='Bar Chart', index=True)
				#writer.save()
				#format_barchart(save_as_file)
				print('Done saving bar chart')
				
			
			if graph_data:
				p = pd.concat(combined_graph_output, sort=False, axis=1)
				p.to_excel(writer, sheet_name='Graph', index=True)
				#writer.save()
				#format_graph(save_as_file)
				
				print('Done saving graph')
				
			
			writer.save()
			if barchart_data:
				format_barchart(save_as_file)
			if graph_data:
				format_graph(save_as_file)

			format_excel_file(save_as_file)
			print('Done formatting excel')
			

			



			
			
			
			#p.to_excel(save_as_file, index=True)

			#if barchart_data:
			#	format_barchart(save_as_file)
			#	format_excel_file(save_as_file)
			#else:
			#	format_excel_file(save_as_file, True)
				






