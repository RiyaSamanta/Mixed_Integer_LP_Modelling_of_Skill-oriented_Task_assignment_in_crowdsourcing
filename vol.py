import csv
import numpy as np
import math
import random
# Set the seed
np.random.seed(10)



class Volunteer:
    def __init__(self, id, skill, pay,eff,bias):
        self.Id = id
        self.Skills = skill
        self.Skills.sort()
        # self.prof = np.random.dirichlet(np.ones(len(self.Skills)), size=1)[0]
        self.Price = pay
        self.eff = eff
        # self.eff = .80
        self.bias=bias
        # self.bias=0.5
        # self.update_user_skill_proff_map()
        
  
    def get_willingness(self):
         omega= self.eff+self.bias
         W=1 / (1 + math.exp(-omega))
         return W
     
    def get_utility(self,tasks):
        util_map={}
        utility=[]
        
        for task in tasks:
            w=self.get_willingness()
            u=task.Budget*w
            utility.append(u)
            
        util_map[self.Id]=utility
        return util_map
    
    def get_vol_skill_mapper(self,tasks):
        mapper = {}
        skillMapper={}
       
        for task in tasks :
            id = task.Id
            row = []
            matchedSkill=[]
            # print("******************",self.Skills)
            for skill in self.Skills :
                # print("skill picked s",skill)
                if skill in task.Skills:
                    matchedSkill.append(skill)
                    row.append(1)
                else :
                    row.append(0)
                # sum_[]=(sum(row))
            mapper[id]=row
            skillMapper[id]=matchedSkill     
        return mapper,skillMapper
        
        
    def __repr__(self):
        return "[" + str(self.Id) +  ":"  +  str(self.Skills) + ":" + str(self.Price) + ":" + str(self.eff) + ":" + str(self.bias) +"]"
        

def get_all_volunteers(filename,v_size):
    Unique_skills = set()
    records = []
    content=open(filename,'r').readlines()
    content=content[1:]
    random.shuffle(content)
    content=content[:v_size]
    i=0
    for line in content:
        line=line.replace("\"","")
        row=line.split(",")
        # id=int(row[0])
        id=i
        i=i+1
        pay=float(row[-3])
        eff=float(row[-2])
        bias=float(row[-1])
        skills=row[1:-3]
        # skills=set(skills)
        # skills=list(skills)
        records.append(Volunteer(id,skills,pay,eff,bias))
        for skill in skills:
              Unique_skills.add(skill)     
    return records, Unique_skills

# if __name__ == '__main__':
#     volunteers,_ = get_all_volunteers("volunteer.csv")
    
    # for i in volunteers:
    #     print(i)
