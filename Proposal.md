# Proposal of Mental Health in Tech Industry Reporting App

* Authors: Mitchie Zhao, Jordon Lau, Kaicheng Tan, Daniel Ortiz

### Section 1: Motivation and purposes 

The mental health conditions of people in the tech workplace have increasingly been a concern in recent years, while many employees suffer from mental health issues. Therefore, it is of great importance to identify the main factors that associate with mental health conditions, and help the government and organizations understand why supporting mental health is essential. In hope of enhancing mental health support in the tech field, we propose to develop a data visualization app based on recent survey data to show the mental health conditions in the tech workplace in the US, address the linked factors, and the companies’ support for their employees’ mental health. With our app, the users can also navigate to a specific state of interest within the US to view and compare the frequencies of mental health conditions in the tech workplace.


### Section 2: Description of the data

The dataset used for our app was originally from a survey conducted by the Open Sourcing Mental Illness team in 2014, which was posted publicly on Kaggle. With more than 1,200 responses collected, only the responses from the United States were selected for the visualization. 

* The `state` column indicates the survey takers’ geographical locations, and will be used as a filter tool to selectively visualize the state(s) of interest. 

* The `tech_company` column indicates if the company is primarily in the tech industry or non-tech industry.

* The `Age`, `Gender` and `family_history` columns describe the demographic factors that may influence the mental health conditions in the tech workplace. `Age` and `Gender` can also be selected to filter the results.

* The `no_employees`, `benefits`, `care_options`,  and `wellness_program` columns provide information about factors affecting mental health within the companies. `no_employees` will be re-divided into 3 categories: small-scale (0-100 employees), medium-scale (100-1000 employees), and large-scale (more than 1000 employees) for company size filtering. 

* In addition, `seek_help`, `mentalhealthinterview`, `anonymity`, `mentalhealthconsequence` and `physicalhealthconsequence` columns reflect the tech field employees’ attitude towards mental health conditions. 
