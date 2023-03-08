#Import necessary packages
from mip import *
from task import *
from vol import *

#Utility function to calculate utility of each volunteer for each task
def util_v(tasks, volunteers):
    utilv = {}
    for v in volunteers:
        # print("VID,------>",v.Id)
        u = []
        for t in tasks:
            u.append(t.Budget * v.get_willingness())
        utilv[v.Id] = u
    return utilv

#Utility function to calculate utility of each task for each volunteer
def util_t(tasks, volunteers):
    utilt = {}
    for t in tasks:
        # print("TID------>",t.Id)
        u = []
        for v in volunteers:
            common_skills = list((matching_skills(t, v)))
            # print("common skills---",common_skills)
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
    tasks, unique_skills_tasks = get_all_tasks_and_skills(
        "code_to_generate_data/task_data.csv", 5)
    
    #Keep a track of all skills per tasks
    taskSkill={}
    for t in tasks:
        taskSkill[t.Id]=t.Skills
    print("Task Skills:",taskSkill)
    
    # Get all volunteers and their unique skills
    volunteers, unique_skills_volunteers = get_all_volunteers(
        "code_to_generate_data/volunteer_data.csv", 10)

    # Calculate the skills contributed by each volunteer for each task
    skillMatch = {}
    for t in tasks:
        for v in volunteers:
            skillMatch[t.Id, v.Id] = matching_skills(t, v)

    
    # Calculate the utility of each task for each volunteer and the utility of each volunteer for each task
    utilt = util_t(tasks, volunteers)
    utilv = util_v(tasks, volunteers)


    #STARTING THE MODELLING OF OPTIMIZATION FUNCTION
    UT = UV = 0
    prob = mip.Model('VTASBR', sense=mip.MINIMIZE)

    # Create decision variables
    x = [[prob.add_var(var_type=mip.BINARY)
          for v in range(len(volunteers))] for t in range(len(tasks))]


    # Constraints
    # 1. Each volunteer is assigned to only 1 task
    for v in volunteers:
        prob += mip.xsum(x[t.Id][v.Id] for t in tasks) <= 1

    #2. Each task is assigned to at least one volunteer
    #for t in tasks:
        #prob += mip.xsum(x[t.Id][v.Id] for v in volunteers) >= 1

    # 3. Add constraint that for any task, the summation of payments given to the assigned volunteers is always less than the task's budget
    for t in tasks:
        prob += mip.xsum(v.Price * x[t.Id][v.Id]
                         for v in volunteers) <= t.Budget

    
    # 4. Add constraint that for any task, the union of skills contributed by assigned volunteers should be a superset of the task's skills
    for t in tasks:
        assigned_volunteers = [v for v in volunteers if x[t.Id][v.Id] == 1]
        skill_sets = [set(skillMatch[t.Id, v.Id]) for v in assigned_volunteers]
        if skill_sets:
            union_of_skills = set().union(*skill_sets)
            if union_of_skills >= set(t.Skills):
                prob += mip.xsum(len(list(union_of_skills))*x[t.Id][v.Id] for v in assigned_volunteers) >=1
        

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
        for v in range(len(volunteers)):
            for t in range(len(tasks)):
                if x[t][v].x >= 0.99:
                    print(
                        f'Volunteer {volunteers[v].Id} is assigned to Task {tasks[t].Id} covering skills{skillMatch[tasks[t].Id,volunteers[v].Id]}')
        print(f'Objective value: {prob.objective_value:.2f}')
    else:
        print('No solution found')
        
        
    count=0
    for t in taskSkill:
        if len(taskSkill[t])==0:
            count=count+1
            
    print(f'Total {count} tasks are complete') 
            
