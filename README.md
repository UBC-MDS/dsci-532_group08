# Mental Health in Tech Industry reporting app
* authors: Mitchie Zhao, Jordon Lau, Kaicheng Tan, Daniel Ortiz

A data science project for DSCI 532 (Data Visualization II); a course in the Master of Data Science program at the University of British Columbia. You can find the reporting app [here](https://dsci532-viz-g8.herokuapp.com/).

## About

Alex is a policy maker working for the government of the United States. He wants to understand if mental health has become a major problem among employees from tech companies. He wants to be able to explore the [Mental Health in Tech Survey dataset](https://www.kaggle.com/osmi/mental-health-in-tech-survey) visually to compare the general situations of mental health issues for people in tech, both geographically and demographically, and find out the most relevant factors that can justify his intention to improve current labor contract policies.

## App description

The Mental Health in Tech Industry dashboard contains two tabs. Three graphs under the “General Overview” tab: a geographical map of the USA, a histogram for age distribution, and a bar chart for interference with work. There are also three plots under the “Company Support” tab: a boxplot for mental health consequences, a normalized bar chart for company support information, and a heatmap for discussion between coworkers and supervisors. Filtering options include a slider for age range selection, drop-down menus for state and company size, and options for filtering gender, tech company and remote work.

## Dependencies

- altair==4.1.0
- dash==1.18.1
- dash-bootstrap-components==0.11.1
- pandas==1.1.5
- vega_datasets
- plotly==4.14.3
- gunicorn


## App sketch
![](img/dashboard_sketch1.png)
![](img/dashboard_sketch2.png)

