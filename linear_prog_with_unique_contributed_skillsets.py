#Objective is to maximize the overall utility gain of the platofrm considering both the utility of the 
#tasks and volunteers(workers) side utilities. The contraints are:
#-Each volunteer is assigned to only 1 task (atmost)
#- The summation of payments given to the assigned volunteers  of a task is 
# always less than the task's budget
#- For each task, the union of skills contributed by assigned volunteers 
# should be a superset of the task's skills, then only that task is said "complete".
#However, ContributedSkills(v1,t) <intersection> ContributedSkills(v2,t) 
# ...<intersection>... ContributedSkills(vn,t) = NULL.
#NOTE: The code to find "union" of skills following the contraint(3) is the first 
#ever trial. MIP has no direct functionality to find "union" of sets. Also, to the best of 
#of our knowledge, this is the first ever available code (in MIP) which model 
#Skill-oriented task assignment problem with budget requirements. 



#Import necessary packages
from mip import *
from task import *
from vol import *

#Utility function to calculate utility of each volunteer for each task
def util_v(tasks, volunteers):
    utilv = {}
    for v in volunteers:
        u = []
        for t in tasks:
            u.append(t.Budget * v.get_willingness())
        utilv[v.Id] = u
    return utilv

#Utility function to calculate utility of each task for each volunteer
def util_t(tasks, volunteers):
    utilt = {}
    for t in tasks:
        u = []
        for v in volunteers:
            common_skills = list((matching_skills(t, v)))
            u.append(len(common_skills)/v.Price)
        utilt[t.Id] = u
    return utilt

#Utility function to calculate the matching skills between a task and a volunteer
def matching_skills(task, volunteer):
    task_skill_set = set(task.Skills)
    common_skills = task_skill_set.intersection(set(volunteer.Skills))
    return common_skills


# Main function
if __name__ == '__main__':
    # Get all tasks and their unique skills
    tasks, unique_skills_tasks = get_all_tasks_and_skills("tasks_toy.csv", 2)
    
    # Keep a track of all skills per tasks
    taskSkill={}
    for t in tasks:
        taskSkill[t.Id]=t.Skills
    print("Task Skills:",taskSkill)
    
    # Get all volunteers and their unique skills
    volunteers, unique_skills_volunteers = get_all_volunteers("volunteer_toy.csv", 11)

    # Calculate the skills contributed by each volunteer for each task
    contributedSkills={}
    skillMatch = {}
    assigned_volunteers={}
    for t in tasks:
        for v in volunteers:
            skillMatch[t.Id, v.Id] = matching_skills(t, v)
            
    # Calculate the utility of each task for each volunteer and the utility of each volunteer for each task
    utilt = util_t(tasks, volunteers)
    utilv = util_v(tasks, volunteers)

    # Starting the modelling of optimization function
    UT = UV = 0
    prob = mip.Model('Model_name (VTASBR)', sense=mip.MINIMIZE)

    # Create decision variables
    x = [[prob.add_var(var_type=mip.BINARY)
          for v in range(len(volunteers))] for t in range(len(tasks))]

    # Constraints
    # 1. Each volunteer is assigned to only 1 task
    for v in volunteers:
        prob += mip.xsum(x[t.Id][v.Id] for t in tasks) <= 1

    # 2. Add constraint that for any task, the summation of payments given to the assigned volunteers is always less than the task's budget
    for t in tasks:
        prob += mip.xsum(v.Price * x[t.Id][v.Id]
                         for v in volunteers) <= t.Budget

    # 3. Add constraint that for any task, the union of skills contributed by assigned volunteers should be a superset of the task's skills
    for t in tasks:
        picked_volunteers = [v for v in volunteers if x[t.Id][v.Id] == 1]
        skill_sets=set()
        vol=[]
        for v in picked_volunteers:
            new_skills=set(skillMatch[t.Id, v.Id])-skill_sets
            if new_skills:
                skill_sets=skill_sets.union(new_skills)
                contributedSkills[t.Id,v.Id]=new_skills
                vol.append(v)
        assigned_volunteers[t.Id]=vol
        if skill_sets:
            union_of_skills = set().union(*skill_sets)
            if union_of_skills >= set(t.Skills):
                prob += mip.xsum(len(list(union_of_skills))*x[t.Id][v.Id] for v in assigned_volunteers[t.Id]) >=1
                
                
    # Objective function
    UT += mip.xsum([utilt[t.Id][v.Id] * mip.xsum([x[t.Id][v.Id]
                   for t in tasks]) for v in volunteers])

    UV += mip.xsum([utilv[v.Id][t.Id] * mip.xsum([x[t.Id][v.Id]
                   for v in volunteers]) for t in tasks])

   
    prob.objective = mip.maximize(0.5 * UT + 0.5 * UV)
    
    
    # Solve the MIP model
    prob.optimize()

    # Print results
    if prob.num_solutions:
        for t in range(len(tasks)):
            vol=assigned_volunteers[t]
            for v in range(len(vol)):
                if x[t][v].x >= 0.99:
                    print(
                        f'Volunteer {vol[v].Id} is assigned to Task {tasks[t].Id} covering skills{contributedSkills[tasks[t].Id,vol[v].Id]}')
                    # print(f'Skills of task: {tasks[t].Id} is {taskSkill[tasks[t].Id]}')
                    updated_Skills=set(taskSkill[tasks[t].Id])-set(contributedSkills[tasks[t].Id,vol[v].Id])
                    taskSkill[tasks[t].Id]=list(updated_Skills)
        print(f'Utility score: {prob.objective_value:.2f}')
                    
    else:
        print('No solution found')
        
        
    count=0
    for t in taskSkill:
        if len(taskSkill[t])==0:
            count=count+1
            
    print(f'Total {count} tasks are complete') 