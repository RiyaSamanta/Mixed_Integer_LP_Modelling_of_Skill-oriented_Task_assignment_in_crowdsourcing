Mixed_Integer_LP_Modelling_of_Skill-oriented_Task_assignment_in_crowdsourcing


Objective is to maximize the overall utility gain of the platofrm considering both the utility of the 
tasks and volunteers(workers) side utilities. The contraints are:
-Each volunteer is assigned to only 1 task (atmost)
- The summation of payments given to the assigned volunteers  of a task is  always less than the task's budget
- For each task, the union of skills contributed by assigned volunteers  should be a superset of the task's skills, then only that task is said "complete".

There are two variation of the approaches:
1.ContributedSkills(v1,t) <intersection> ContributedSkills(v2,t) ...<intersection>... ContributedSkills(vn,t) is not equal to NULL. 
This means for every assigned worker may contribute skill(s) which are not unique that is also covered by other assigned workers of the same task. This assumption is
followed in "linear_prog_with_repetitive_contributed_skills.py" 


 2. ContributedSkills(v1,t) <intersection> ContributedSkills(v2,t) ...<intersection>... ContributedSkills(vn,t) is  NULL. 
This means for every assigned worker may contribute skill(s) which are unique that are not covered by other assigned workers of the same task. This assumption is
followed in "linear_prog_with_unique_contributed_skillsets.py" 


Two toy datasets (task_data and volunteer_data) ahve also been added to quickly get started with the execution and test the results. One may also use their own datasets. But for that the task.py and vol.py files are needed to be modified (according to the attributes/feature detailing).

#NOTE: The code to find "union" of skills following the contraint(3) is the first ever trial. MIP has no direct functionality to find "union" of sets. 
Also, to the best of our knowledge, this is the first ever available code (in MIP) which model "Skill-oriented task assignment problem with budget requirements". 


Readers/coders/resaerchers are welcomed to reuse this code.This work is a part of a recently submitted paper to IEEE CLOUD 2023 conference. Please cite the following paper for this. 
Riya et al. "Serverless-assisted Task Assignment in Skill-based Volunteer Crowdsourcing", IEEE CLOUD conference (2023) (submitted).

For any help, feel free to drop a message or contact me through my mail:
study.riya1792@gmail.com
