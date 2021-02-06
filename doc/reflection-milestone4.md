# Reflection 
## Authors: Mitchie Zhao, Jordon Lau, Kaicheng Tan, Daniel Ortiz


### What have we implemented?
Our [mental health in tech dashboard](https://dsci532-viz-g8.herokuapp.com) consists of 3 graphs under the “General Overview” tab: a geographical map of the USA, a histogram for age distribution, and a bar chart for interference with work. There are three plots under the “Company Support” tab: a boxplot for mental health consequences, a normalized bar chart for company support information, and a heatmap for discussion between coworkers and supervisors.  Filtering options include a slider for age range selection, drop-down menus for state and company size, and options for filtering gender, tech company and remote work. 


### What is not yet implemented? 
After coding and deployment, there is not any obvious bug in our App. The previously mentioned formatting and mapping issues have been fixed in Milestone 4. Compared to the initial proposal that we came up with in Milestone 1, all the pie charts were replaced by the (normalized) bar charts, since `Altair` does not support pie chart plotting. We also decided not to plot separate bar charts but all in one normalized bar chart to better visualize the responses for questions regarding company support information.


### Reflection on Feedback
* **Has it been easy to use your app?**

Both feedback from our peers and TA indicated that the mental health in tech App has a clear general layout, with good choices of graphs. The filter options are easy to understand and use, making the visualization more flexible. 
However, some feedback mentioned that there were repeating states in the dropdown menu, and this issue has been fixed in Milestone 3 and 4. 

* **Are there recurring themes in your feedback on what is good and what can be improved?**

As for improvements, we received suggestions about layout of map and plots under each tab to better utilize the space. More clear information such as user instruction, plot description, fixed axis and labels have also been suggested by our TA and peers to improve the App. These comments were addressed during the process of App development and we were able to make our App more user friendly and informative by Milestone 4.

* **Is there any feedback (or other insight) that you have found particularly valuable during your dashboard development?**

We found the most valuable feedback to be the mapping of the graphs: in addition to aligning the y-axis of each plot and reducing the empty space. We have also relocated the graphs under the “General Overview” tab to emphasize more on the geographical map for better and more clear visualization. The full-screen formatting display issue has also been fixed now.

