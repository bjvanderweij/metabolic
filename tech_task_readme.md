# Welcome to the Metabolic Software coding assignment repo
This repository gives a basic setup and information for our coding assignments. If you have any questions, please don't hesitate to reach out to us.

## Questions and feedback?
You can reach us at software@metabolic.nl. 

### Steps to complete the assignment
1. Understand the task requirements, and ask questions, if any.
2. Understand the data format & schema, and ask questions, if any.
3. Fork this repository https://github.com/SystemicBV/rivm2016
4. Implement the task in your preferred tech stack.
5. Update the README.md with the instructions to setup the assignment.
6. Check in all your work in the cloned repo and do not forget to try out the instructions yourself.
7. Submit the assignment as a link to your cloned repo. 
Email to software@metabolic.nl, with the subject "Task < ID > Submission for < Role >". 

# Tech task 1 - Backend Developer
## Language independent GraphQL Service - RIVM2016 impacts data

## Task
1. Create a (set of) script(s)/program(s) in your preferred language(s) that build and populate this database. Use any database you like. Use any libraries you like, including libraries that handle migrations and seeds if you want.
2. Create a simple GraphQL server in your preferred language(s) that will connect to this database and serve data according to the schema included in the schema.gql file.
3. Build a (very) simple Dockerfile to wrap your server into a container.

## Evaluation Criteria
Your assignment will be judged on how you implemented the task, not what tech stack you used as long as you can explain why you used this stack. We will look at the data model you used (which does not have to be the one provided), how you import the data and how you crafted the server.

Your assignment will not be judged on the type of database you choose, so feel free to use SQLite or the like. You can also use a noSQL database of any type you like, as long as you can explain your decisions.

Submit your best-effort assignment within the agreed upon deadline. If you need to make any changes after the dead line, please email us with appropriate justification.


## Files
### README.md
In this file, write your instructions to setup the assignment submission.
### data/rivm2016.csv
A subset of the 2016 impact data for the Netherlands as compiled by the RIVM.
### rivm2016_csv_format.pdf
Data format of the csv file mentioned above
### schema.gql
Schema of the GraphQl service to be implemented
### Dockerfile
Placeholder script to setup the docker Container
### docker-compose.yml
Placeholder script to setup the docker services 
