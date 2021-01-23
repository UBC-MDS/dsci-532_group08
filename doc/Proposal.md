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




### Section 3: Research questions and usage scenarios
#### Research questions

We are interested in answering the following questions through our app:

- Severity and interference of mental health conditions 
  - How common and widespread are mental health conditions?
  - Do mental health issues interfere with work?
  - Do mental health issues originate from work? (or is it a pre-existing condition?)
- Demographic factors that affect mental health conditions 
  - Which demographic group is more susceptible to risks of acquiring mental health conditions?
  - Do gender, age, or genetic predispositions have an affect? 
- Company involvement for mental health conditions
  - Are employees concerned about anonymity when seeking mental health help in their workplace?
  - Are companies communicating the mental health care options they provide for employees?
  - Are employees comfortable with raising mental health concerns to their coworkers or supervisors? 
  - Are people concerned with raising mental health conditions during interviews? 
- Mental health prevalence in tech versus other industries
  - Does the company size have an effect when implementing mental health programs for their employees?
  - Do tech company employees have a greater proportion of individuals with mental health conditions relative to other industries?
- Mental Health differences from state to state
  - Are there any states that employees are more willing to communicate their conditions with other coworkers or supervisors?
  - Are mental health conditions more prevalent in certain states?

#### Usage Scenario
Alex is a policymaker working for the government of the United States. He wants to understand if mental health has become a major problem among employees from tech companies. He wants to be able to explore the Mental Health in Tech Survey dataset visually to compare the general situations of mental health issues for people in tech, both geographically and demographically, and find out the most relevant factors that can justify his intention to improve current labor contract policies. 

With the "Mental health in tech survey reporting app", Alex should be able to:
- Filter the data geographically (i.e. by states) and demographically (i.e. by gender, age, family mental health history)
- Have an overview of how common (widespread) the mental health issues are
- Understand if the mental health condition originates from work
- Understand how well companies are doing in helping their employees with mental health issues.

By using the app, Alex may realize that the problem varies greatly by states, possibly due to the fact that different states have different policies regarding protecting laborers. He may conduct additional research on states that perform particularly well and compare with those performing poorly to see what is missing.
