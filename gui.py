

print('Ready')
from common import browseFile


#from area_stats module import compute_area_stats class
from area_stats import compute_area_stats
from pop_stats import compute_pop_stats
from count_summary import compute_count_summary
from sites_config import sites_config

from combined_statistics import group_prediction_stats

#for prediction stats
#create objects using the classes
area_stats_calculation = compute_area_stats()
pop_stats_calculation = compute_pop_stats()
count_summary_calculation = compute_count_summary()
sites_config = sites_config()
perform_multiple_stats = group_prediction_stats()


#for dt analysis
from dt_barchart import dt_barchart
from dt_graph import dt_graph

barchart = dt_barchart()
graph = dt_graph()




from tkinter import *
from tkinter import ttk 



root = Tk()
root.geometry('390x230')



#tk variables

#frame 1
#set variable types for the different checkboxes
area_checkbox_var = IntVar()
pop_checkbox_var = IntVar()
count_checkbox_var = IntVar()
sites_config_checkbox_var = IntVar()
use_area_ranges_checkbox_var = IntVar()



#frame 2
#set variable types for the different checkboxes
graph_checkbox_var = IntVar()
pdf_checkbox_var = IntVar()
cdf_checkbox_var = IntVar()

#selected_technology = lambda: barchart.get_technology(select_technology_var)









menubar = Menu(root)

menubar.add_command(label="Load file", command=lambda: perform_multiple_stats.load_combined_excel_file())


# create a pulldown menu, and add it to the menu bar
statistics = Menu(menubar, tearoff=0)



#add the different methods/functions to the statistics submenu
statistics.add_command(label="Area", command=lambda: area_stats_calculation.format_area_stats())

statistics.add_command(label="Population", command=lambda: pop_stats_calculation.format_pop_stats())

statistics.add_command(label="Count Summary", command=lambda: count_summary_calculation.format_count_summary())

statistics.add_command(label="Sites config", command=lambda: sites_config.format_sites_config())

statistics.add_separator()

menubar.add_cascade(label="Statistics", menu=statistics)


dt_analysis = Menu(menubar, tearoff=0)

dt_analysis.add_command(label="Graph", command=lambda: graph.format_graph())

#dt_analysis.add_command(label="Bar chart", command=lambda: barchart.create_barchart(selected_technology() ))

dt_analysis.add_command(label="Bar Chart - PDF", command=lambda: barchart.format_barchart(pdf=1))

dt_analysis.add_command(label="Bar Chart - CDF", command=lambda: barchart.format_barchart(cdf=1))

menubar.add_cascade(label="DT Analysis", menu=dt_analysis)


menubar.add_command(label="Help")






#create different font sizes from tkinter Font
normal_font = font.Font(size=11)
small_font = font.Font(family='Helvetica', size=7)




frame = LabelFrame(root, text='Prediction Statistics')
frame.grid(row=0, column=0, padx=15, pady=15)
frame['font'] = normal_font








#create checkboxes for area, population, count summary and use area ranges
sites_config_checkbox = Checkbutton(frame, text='Sites', variable=sites_config_checkbox_var, onvalue=1, offvalue=0)
sites_config_checkbox.grid(row=1, column=0, sticky=W, padx=15)
sites_config_checkbox['font'] = normal_font

area_checkbox = Checkbutton(frame, text='Area', variable=area_checkbox_var, onvalue=1, offvalue=0)
area_checkbox.grid(row=2, column=0, sticky=W, padx=15)
area_checkbox['font'] = normal_font

pop_checkbox = Checkbutton(frame, text='Population', variable=pop_checkbox_var, onvalue=1, offvalue=0)
pop_checkbox.grid(row=3, column=0, sticky=W, padx=15)
pop_checkbox['font'] = normal_font

count_checkbox = Checkbutton(frame, text='Count Summary', variable=count_checkbox_var, onvalue=1, offvalue=0)
count_checkbox.grid(row=4, column=0, sticky=W, padx=15)
count_checkbox['font'] = normal_font

use_area_ranges_checkbox = Checkbutton(frame, text='Use RSSI ranges in Area\n as Pop and Count ranges', variable=use_area_ranges_checkbox_var, onvalue=1, offvalue=0)
use_area_ranges_checkbox.grid(row=6, column=0, sticky= W, padx=15)
use_area_ranges_checkbox.select()
use_area_ranges_checkbox['font'] = small_font


#get a list of the current value of checkbox i.e checked or unchecked, and the labels
#this will be passed to the combined prediction object/method
checkbox_variables = [sites_config_checkbox_var, area_checkbox_var, pop_checkbox_var, count_checkbox_var, use_area_ranges_checkbox_var]
checkbox_labels = ['sites', 'area', 'population', 'count_summary', 'use_area_ranges']


#run button computes the combined stats for area, pop, count
#run_button = Button(frame, text="Run", relief="groove", width=10, command=lambda: perform_multiple_stats.which_pred(checkbox_variables, checkbox_labels))
prediction_stats_checkboxes = lambda: perform_multiple_stats.group_checkbox_states(checkbox_variables, checkbox_labels)
#print(prediction_stats_checkboxes)
#run_button = Button(frame, text="Run", relief="groove", width=10, command=lambda: 
#                    perform_multiple_stats.which_pred(perform_multiple_stats.group_checkbox_states(checkbox_variables, checkbox_labels)))

run_button = Button(frame, text="Run", relief="groove", width=10, command=lambda: perform_multiple_stats.which_pred( prediction_stats_checkboxes() ))
run_button.grid(row=5, column=0, sticky=W, padx=18, pady=7)







##------------ FRAME 2 --------------------##





frame1 = LabelFrame(root, text='DT Anaylsis')
frame1.grid(row=0, column=1, padx=15, pady=15)
frame1['font'] = normal_font






#select_technology = ttk.Combobox(frame1, value=technology_values, width=12, textvariable = select_technology_var, state='readonly')
#select_technology.grid(row=1, column=0, sticky=W, padx=15)



#create checkboxes for area, population, count summary and use area ranges




graph_checkbox = Checkbutton(frame1, text='Graph', variable=graph_checkbox_var, onvalue=1, offvalue=0)
graph_checkbox.grid(row=0, column=0, sticky=W, padx=15)
graph_checkbox['font'] = normal_font


#barchart_label = Label(frame1, text='Bar Chart')
#barchart_label.grid(row=1, column=0, sticky=W, padx=15)
#barchart_label['font'] = small_font



pdf_checkbox = Checkbutton(frame1, text='PDF', variable=pdf_checkbox_var, onvalue=1, offvalue=0)
pdf_checkbox.grid(row=2, column=0, sticky=W, padx=15)
pdf_checkbox['font'] = normal_font


cdf_checkbox = Checkbutton(frame1, text='CDF', variable=cdf_checkbox_var, onvalue=1, offvalue=0)
cdf_checkbox.grid(row=3, column=0, sticky=W, padx=15)
cdf_checkbox['font'] = normal_font


#get a list of the current value of checkbox i.e checked or unchecked, and the labels
#this will be passed to the combined prediction object/method
dt_checkbox_variables = [graph_checkbox_var, pdf_checkbox_var, cdf_checkbox_var]
dt_checkbox_labels = ['graph', 'PDF', 'CDF']


#run button computes the combined stats for area, pop, count
#run_button = Button(frame, text="Run", relief="groove", width=10, command=lambda: perform_multiple_stats.which_pred(checkbox_variables, checkbox_labels))
dt_prediction_stats_checkboxes = lambda: perform_multiple_stats.group_checkbox_states(dt_checkbox_variables, dt_checkbox_labels)




#run_button = Button(frame1, text="Run", relief="groove", width=10, command=lambda: print(select_technology_var.get()))

run_button_2 = Button(frame1, text="Run", relief="groove", width=10, command=lambda: perform_multiple_stats.which_pred( dt_prediction_stats_checkboxes() ))
run_button_2.grid(row=4, column=0, sticky=W, padx=18, pady=14)


empty_label = Label(frame1, text='')
empty_label.grid(row=5, column=0)
empty_label['font'] = normal_font

empty_label = Label(frame1, text='')
empty_label.grid(row=6, column=0)
empty_label['font'] = normal_font






#display the menu
root.config(menu=menubar)

mainloop()




