#!/usr/bin/env python
# coding: utf-8

# # **FLOORPLANING** 

# In[2]:




import random
import matplotlib 
import matplotlib.pyplot as plt 
import math
import time


#--------------------------Given set of input block dimensions---------------------------------#

block_dimensions=[[1, 10, 5,8, 6,4, 13,5, 11],
                  [2, 10, 3,8, 4, 4, 9, 5, 6],
                  [3, 5, 8, 7, 6, 3, 13, 2, 20],
                  [4, 7, 8, 10, 6, 8, 7, 9, 6],
                  [5, 3, 2, 1, 7, 2, 4, 5, 1]]
    
#-----------------------------------Connectivity matrix--------------------------------#

connectivity_matrix =[[0, 1, 1, 0, 0],
                      [1, 0, 1, 1, 0],
                      [1, 1, 0, 1, 1],
                      [0, 1, 1, 0, 1],
                      [0, 0, 1, 1, 0]]

#-----------------Obtaining block ids from given input-Block_dimensions----------------#
block_ids=[]
for i in range(len(block_dimensions)):
  block_ids.append(block_dimensions[i][0])


# **initial_polish_exp:** Creates initial polish expression

# In[3]:


def initial_polish_exp(no_of_ip_blocks):
  len_pol_exp = 2*no_of_ip_blocks - 1
  polish_expression = []
  c=0
  for i in range(len_pol_exp):
      
        if (i%2 == 0 and i != 0 and i != 1):
            if (c%2==0):
               polish_expression.append('H')
            else:
               polish_expression.append('V')
            c=c+1
            
        elif (i == 0 or i == 1):
            polish_expression.append(i+1)
            j = 3
       
        else:
            polish_expression.append(j)
            j = j+1
            
  return (polish_expression)


# **postorder_to_inorder**: This module converts polish expression which is postorder traversal to inorder traversal. **checking_if_done** is helper module for this conversion.

# In[4]:


def checking_if_done(polish_exp_temp, inorder, done, done_index):
    
    for i in range(len(done)):
        if (polish_exp_temp[i] in inorder):
            done_index = i + 1
        else:
            break

    return done_index

def postorder_to_inorder(polish_exp_temp,operators,operands):

    inorder = []
    num_stack = []
    char_stack = []
    num = 1
    done = [0]*len(polish_exp_temp)
    done_index = 0

    i = 0
    while (len(inorder)<len(polish_exp_temp)):

        x = polish_exp_temp[i]

        if ( (x in operands) and (num == 1) ):
            inorder.append(x)
            num = 0
            i = checking_if_done(polish_exp_temp,inorder,done,done_index)
            num_stack=[]
            char_stack=[]
        elif ((x in operands) and (num == 0) ):
            num_stack.append(x)
            i = i + 1

        elif ((x in operators) and ((len(num_stack) - 1) == (len(char_stack)))):
            inorder.append(x)
            num = 1
            i = checking_if_done(polish_exp_temp,inorder,done,done_index)
            if (len(num_stack)>0):
                inorder.append(num_stack[0])
                num = 0
                i = checking_if_done(polish_exp_temp,inorder,done,done_index)

            num_stack=[]
            char_stack=[]

        elif ((x in operators) and ((len(num_stack) - 1) != (len(char_stack)))):
            char_stack.append(x)
            i = i + 1

    return inorder



# **move1:** Subfunction of **perturb** method, exchanges two operands that have no other operands in between

# In[5]:


def move1(pol_exp):
 
    polish_exp_temp = pol_exp[:]
    len_exp = len(polish_exp_temp)
    operands=[]

    for i in polish_exp_temp:
      if (i !='H' and i!='V'):
        operands.append(i)

    i1=random.randint(0,len(operands)-1)
    node1=operands[i1]
    if (i1==len(operands)-1):
      node2=operands[i1-1]
    else:
      node2=operands[i1+ 1]
    
    for j in range(len_exp):
      if (node1==polish_exp_temp[j]):
        loc1=j
      if (node2==polish_exp_temp[j]):
        loc2=j   

    polish_exp_temp[loc1]=node2
    polish_exp_temp[loc2]=node1
    
    return polish_exp_temp
    


# **move2:** Subfunction of perturb method, complements a series of operators between two operands

# In[6]:


def move2(polish_exp):

    polish_exp_temp = polish_exp[:]
    len_chain = []
    loc = []
    
    for i in range(0,len(polish_exp_temp)-1):
      if (polish_exp_temp[i]=='H' or polish_exp_temp[i]=='V'):
        loc.append(i)
        len_chain.append(1)
        j=i+1
        if (j==len(polish_exp_temp)):
          break
        while (polish_exp_temp[j]=='H' or polish_exp_temp[j]=='V'):
          len_chain[len(loc)-1]=len_chain[len(loc)-1]+1
          j=j+1
          if (j == len(polish_exp_temp) ):
                    break

    len_loc = len(loc)
    rand_loc = 0

    if (len_loc>1):
        rand_loc = random.randint(0, len_loc-1)

    i = loc[rand_loc]
    while (i < (loc[rand_loc] + len_chain[rand_loc] )):
        if(polish_exp_temp[i] == 'V'):
            polish_exp_temp[i] = 'H'
        elif(polish_exp_temp[i] == 'H'):
            polish_exp_temp[i] = 'V'
        i = i + 1

    return polish_exp_temp


# **move3:** Subfunction of **perturb** method, exchanges adjacent operand and operator if the resulting expression is still normalized polish expression

# In[7]:


def move3(polish_exp):
    
    polish_exp_temp = polish_exp[:]
    len_exp = len(polish_exp_temp)

    operator = ['H','V']
    pol = range(1,len_exp+1)
    location=[]

    for i in range(len_exp-1):
      if (polish_exp_temp[i] in operator and polish_exp_temp[i+1] in pol):
          location.append(i)
      elif (polish_exp_temp[i] in pol and polish_exp_temp[i+1] in operator):
          location.append(i)

    r=random.randint(0,len(location)-1)
    loc=location[r]
    temp=polish_exp_temp[loc]
    polish_exp_temp[loc]=polish_exp_temp[loc+1]
    polish_exp_temp[loc+1]=temp

    return ( polish_exp_temp)


# **balloting_property**: Checks if given polish expression satisfies balloting property i.e., Number of operands > Number of operators

# In[8]:


def balloting_property(polish_exp):
  polish_exp_temp=polish_exp[:]
  count1=0
  count2=0
  for i in range(0,len(polish_exp)-1):
    if (polish_exp[i]=='H' or polish_exp[i]=='V'):
      count1=count1+1
    else:
      count2=count2+1

  if (count2>count1):
    return 0
  else:
    return 1




# **normalizes_exp**: Checks if given polish expression is normaized or not. That means no two adjacent operators has to be same. 

# In[9]:


def normalized_exp(polish_exp):
  
  
  for i in range(0,len(polish_exp)-1):
    if ((polish_exp[i]=='H' and polish_exp[i+1]=='H') or (polish_exp[i]=='V' and polish_exp[i+1]=='V')):
      return 1
    
  return 0
   


# **check_if_binary_slicing_tree**: This Module checks if given polish expression is Binary slicing tree

# In[10]:


def check_if_binary_slicing_tree(pol_exp):
  operands=[]
  operators=[]
  ch=0;cv=0
  update=pol_exp[:]
  if pol_exp[2] not in ['H', 'V']:
    return 1
  for i in range(len(pol_exp)):
    if pol_exp[i] not in ['H', 'V']:
      operands.append(pol_exp[i])
    elif (pol_exp[i]=='H'):
      operators.append('H'+str(ch))
      update[i]='H'+str(ch)
      ch=ch+1
    else:
      operators.append('V'+str(cv))
      update[i]='V'+str(cv)
      cv=cv+1
 
  pol=postorder_to_inorder(update,operators, operands)
 
  
  check1=pol[0::2]
  check2=pol[1::2]

  
  if (check1!=operands and check2!=operators):
    return 1
  else:
    return 0
     


# **perturb**: Performs different pertubation moves, it chooses moves randomly and also makes sure that polish expression doesn't violate balloting property and remains normalized. It also ensures that polish expression is a binary slicing tree.

# In[11]:


def perturb(polish_expression):

    polish_exp_temp = polish_expression[:]
    move_no = random.randint(1,3)
    #move_no=3
    if (move_no == 1):
        polish_exp_temp1 = move1(polish_exp_temp)
    elif (move_no == 2):
        polish_exp_temp1 = move2(polish_exp_temp)
    else:
        polish_exp_temp1= move3(polish_exp_temp)
        while (balloting_property(polish_exp_temp1) == 1 or normalized_exp(polish_exp_temp1) == 1
           or check_if_binary_slicing_tree(polish_exp_temp1) ==1):
            #print(1)

            polish_exp_temp1= move3(polish_exp_temp)
    
    return (polish_exp_temp1)
print(perturb([1,2,'H',3,'V',4,'H',5,'V']))


# **H1_dimension**: Subfunction of area method, given two blocks which are operands and are horziontally sliced then it computes minimum possible resulting area of combination. Then returns the dimensions of the combined block which is then added to stack in area module.

# In[12]:


def H1_dimension(block1,block2,block_dimensions,sizes, combined_size):
  

  w1s= block_dimensions[block1-1][1::2] 
  h1s= block_dimensions[block1-1][2::2] 
  w2s= block_dimensions[block2-1][1::2] 
  h2s= block_dimensions[block2-1][2::2] 

  
  areas=[]
  temp=[]
  for i in range(len(w1s)):
    temp=[]
    for j in range(len(w1s)):
      temp.append(max(w1s[i],w2s[j])*(h1s[i]+h2s[j]))
    areas.append(temp)

  min=areas[0][0]
  h=0;k=0;
  for i in range(len(areas)):
    for j in range(len(areas)):
      
       if (areas[i][j]<min):
           min=areas[i][j]
           h=i
           k=j
  
  w2=w2s[k]
  h1=h1s[h]
  h2=h2s[k]
  w1=w1s[h]

  t=[ w1, h1]
  sizes.append(t)
  
  q=[ w2, h2]
  sizes.append(q)
  
  dim=[]
  dim.append(max(w1,w2))
  dim.append(h1+h2)
  combined_size.append(t)
  combined_size.append(q)
  combined_size.append([max(w1,w2), h1+h2])

  return (dim, sizes, combined_size)


# **H2_dimension:** Subfunction of area method, given one block which is top in the stack and that being a operand and other being combined block in stack and are horziontally sliced then it computes minimum possible resulting area of combination. Thereafter, it returns minimum possible dimensions to area module which adds resulting combined block onto stack.

# In[13]:


def H2_dimension(block1, block2, block_dimensions,sizes, combined_size):
  w1s= block_dimensions[block1-1][1::2] 
  h1s= block_dimensions[block1-1][2::2]
  w2=block2[0]
  h2=block2[1]

  areas=[]
  for i in range(len(w1s)):
    areas.append(max(w1s[i],w2)*(h1s[i]+h2))
  
  m=areas[0]
  k=0
  for i in range(len(areas)):
    if (m>areas[i]):
      m=areas[i]
      k=i
  w1=w1s[k]
  h1=h1s[k]
  t=[ w1, h1]
  sizes.append(t) 
  dim=[]
  dim.append(max(w1,w2))
  dim.append(h1+h2)
 
  combined_size.append(t)
  combined_size.append(dim)
  return dim, sizes, combined_size


# **H3_dimension:** Subfunction of area method, given two blocks which are combined blocks popped out from stack and are horziontally sliced then it computes minimum possible resulting area of combination and returns that to area module.

# In[14]:


def H3_dimension(block1,block2, combined_size):
  dim=[]
  dim.append(max(block1[0],block2[0]))
  dim.append(block1[1]+block2[1])
  
  combined_size.append(dim)
  return dim, combined_size
  


# **V1_dimension:** Subfunction of area method, given two blocks which are operands and are vertically sliced in polish expression then it computes minimum possible resulting area of combination and returns its dimensions.

# In[15]:


def V1_dimension(block1,block2,block_dimensions,sizes, combined_size):
   
  w1s= block_dimensions[block1-1][1::2] 
  h1s= block_dimensions[block1-1][2::2] 
  w2s= block_dimensions[block2-1][1::2] 
  h2s= block_dimensions[block2-1][2::2] 
  areas=[]
  temp=[]
  for i in range(len(w1s)):
    temp=[]
    for j in range(len(w1s)):
      temp.append((w1s[i]+w2s[j])*max(h1s[i],h2s[j]))
    areas.append(temp)

  mm=areas[0][0]
  n=0;m=0;

  for ii in range(len(areas)):
    for jj in range(len(areas)) :
       
       if (areas[ii][jj]<mm):
            mm=areas[ii][jj]
            n=ii
            m=jj
  
  w1=w1s[n]
  w2=w2s[m]
  h1=h1s[n]
  h2=h2s[m]
  t=[ w1, h1]
  sizes.append(t)
  q=[ w2, h2]
  sizes.append(q)
   
  combined_size.append(t)
  combined_size.append(q)


  dim=[]
  dim.append(w1+w2)
  dim.append(max(h1,h2))
  combined_size.append(dim)

  return dim, sizes, combined_size


# **V2_dimension:** Subfunction of area method, given one block which is operand and other being combined block and are vertically sliced in polish expression then it computes minimum possible resulting area of combination and returns its dimensions.

# In[16]:


def V2_dimension(block1, block2, block_dimensions, sizes, combined_size):
  w1s= block_dimensions[block1-1][1::2] 
  h1s= block_dimensions[block1-1][2::2] 

  w2=block2[0]
  h2=block2[1]

  areas=[]
  for i in range(len(w1s)):
    
    areas.append(max(h1s[i],h2)*(w1s[i]+w2))
  
  m=areas[0]
  k=0
  for i in range(len(areas)):
    if (m>areas[i]):
      m=areas[i]
      k=i
  w1=w1s[k]
  h1=h1s[k]
  
  t=[ w1 ,h1]
  sizes.append(t)

  combined_size.append(t)
  dim=[]
  dim.append(w1+w2)
  dim.append(max(h1,h2))
  combined_size.append(dim)
  return dim, sizes, combined_size
  


# **V3_dimension:** Subfunction of area method, given two blocks which are combined blocks popped out from stack and are vertically sliced in polish expression then it computes minimum possible resulting area of combination and returns its dimensions.

# In[17]:


def V3_dimension(block1,block2, combined_size):
  dim=[]

  dim.append(block1[0]+block2[0])
  dim.append(max(block1[1],block2[1]))
  combined_size.append(dim)
  return dim, combined_size


# Creating a tree of polish expression whose each node holds its dimension, block id, its coordinates and information about the nodes which are left and right to it.

# In[18]:


class node:
    
    def __init__(self, x):
        
        self.id = x                 #holds block id of current node
        self.left = None            #Information about node which is left of current node
        self.right = None           #Information about node which is right of current node
        self.coord = None           #Holds coordinates of current node
        self.dim = None             #Holds dimensions of current node

class Tree:
    
    def buildTree(self, inorder, postorder):
        
        if not inorder or not postorder:
            return None
        
        root = node(postorder.pop())
        inorderIndex = inorder.index(root.id)

        root.right = self.buildTree(inorder[inorderIndex+1:], postorder)
        root.left = self.buildTree(inorder[:inorderIndex], postorder)

        return root




# **get_coordinates**: This module calculates coordinates of blocks by traversing through tree (inorder traversal) and adds offsets accordingly such that no two blocks overlaps.

# In[19]:


def get_coordinates(root, combined_size, polish_exp_temp, co_ord, operands):

    if (root.id in operands):
        co_ord[root.id - 1] = root.coord

    if (root.left == None and root.right == None):
        return co_ord

    if (root.id[0] == 'H'):
        root.left.coord = root.coord
        root.right.coord = [root.coord[0], root.coord[1] + combined_size[polish_exp_temp.index(root.left.id)][1]]

        co_ord = get_coordinates(root.left,  combined_size, polish_exp_temp, co_ord, operands)
        co_ord = get_coordinates(root.right,  combined_size,  polish_exp_temp, co_ord, operands)

    if (root.id[0] == 'V'):
        root.left.coord = root.coord
        root.right.coord = [root.coord[0] + combined_size[polish_exp_temp.index(root.left.id)][0], root.coord[1]]

        co_ord = get_coordinates(root.left,  combined_size, polish_exp_temp, co_ord, operands)
        co_ord = get_coordinates(root.right,  combined_size, polish_exp_temp, co_ord, operands)    

    return co_ord


# **area**: Method that computes overall optimized and minimum area occupied by the given polish expression.

# In[20]:



def area(polish_exp, block_dimensions):
  stack=[]
  sizes=[]
  combined_size=[]
  combined_size_list=[]
  updated_operators=[]
  v=0
  h=0
  updated_pol_exp=polish_exp[:]
 
  for i in range(len(polish_exp)):

    if (polish_exp[i]!='H' and polish_exp[i]!='V'):
      stack.append(polish_exp[i])
      
    elif (polish_exp[i]=='H'):
      top=stack.pop()
      bottom=stack.pop()
      
      if (top in polish_exp and bottom in polish_exp):
       
         a,sizes,combined_size=H1_dimension(bottom,top, block_dimensions,sizes,combined_size) 
         stack.append(a)
        
         
      elif (top in polish_exp ):
    
         a,sizes, combined_size=H2_dimension(top, bottom, block_dimensions,sizes, combined_size)
      
         stack.append(a)
         
        
      elif (bottom in polish_exp):
      
         a,sizes, combined_size=H2_dimension(bottom,top,block_dimensions,sizes, combined_size)
         stack.append(a)
        
      else :
  
         a, combined_size=H3_dimension(bottom,top,combined_size)
         stack.append(a)
         
      combined_size_list.append('H' + str(h))
      updated_operators.append(('H' + str(h)))
      updated_pol_exp[i] = 'H' + str(h)
      h=h+1
         
    else:
      
      right=stack.pop()
      left=stack.pop()
      
      if (right in polish_exp and left in polish_exp):

         a,sizes, combined_size=V1_dimension(left,right, block_dimensions,sizes, combined_size)
         stack.append(a)
        
         
      elif (right in polish_exp ):
    
         a,sizes, combined_size=V2_dimension(right,left,block_dimensions,sizes, combined_size)
        
         stack.append(a)
      
      elif (left in polish_exp):
        
         a,sizes, combined_size=V2_dimension(left,right,block_dimensions,sizes, combined_size)
         stack.append(a)
     
       
      else :
      
         a, combined_size=V3_dimension(left,right, combined_size)
         stack.append(a)
         
    
      combined_size_list.append('V' + str(v))
      updated_operators.append(('V' + str(v)))
      updated_pol_exp[i] = 'V' + str(v)
      v=v+1
         
  L=stack.pop()
  operands=[]

  for i in polish_exp:
    if i not in ['H', 'V']:
      operands.append(i)
  
  pol_ish=updated_pol_exp[:]
 

  inpo=postorder_to_inorder(updated_pol_exp, updated_operators, operands)
 
  root = Tree().buildTree( inpo, pol_ish)
  root.dim=L[:]
  root.coord = [0,0]
  co_ord = [[0,0]]*len(operands)
  

  
  co_ord = get_coordinates(root, combined_size, updated_pol_exp, co_ord, operands)

  return L,  L[0]*L[1],  sizes, co_ord
    


# **wirelength**: This module computes wirelengths between two connected blocks

# In[21]:


def wirelength(adj_matrix, block_dimensions, node_coord, polish_expression):
    
    weight = 0
    n = len(adj_matrix[0])
    operands=[]
    wires=[]
    for k in polish_expression:
      if k not in ['H', 'V']:
        operands.append(k)

    for i in range(n):

        x1 = node_coord[i][0] + (block_dimensions[i][0])/2
        y1 = node_coord[i][1] + (block_dimensions[i][1])/2
        

        for j in range(n):
            if (adj_matrix[i][j] !=0):
                x2 = node_coord[j][0] + (block_dimensions[j][0])/2
                y2 = node_coord[j][1] + (block_dimensions[j][1])/2
                dist = math.sqrt((x2-x1)**2 + (y2 - y1)**2)
                weight = weight + dist*adj_matrix[i][j]
                wires.append([operands[i], operands[j], dist])

    return weight, wires


# **cost_func**: Computes cost which is 0.5(Area) + 0.5(Wirelen)

# In[22]:




def cost_func(polish_expression, block_dimensions, adj_matrix):
    
    size, area_of_block, selected_dim, co_ord = area(polish_expression[:], block_dimensions)
    wirelen, wires_connection = wirelength(adj_matrix, selected_dim, co_ord, polish_expression)

    cost = 0.5*area_of_block + 0.5*wirelen 

    return cost,size, area_of_block, co_ord, selected_dim, wires_connection


# **simulated_annealing**: Algorithm to determine floorplan of given blocks which has variable block dimensions

# In[ ]:


def simulated_annealing(adj_matrix, block_ids, block_dimensions):
 no_of_ip_blocks=len(block_ids)                                    # No of ip blocks is same as number of nodes
 cursolution=initial_polish_exp(no_of_ip_blocks)
 noded = dict()
 loop=0
 pol_exp=cursolution[:]
 init_temp_arr=[]

 while (loop < 5):
       pol_exp=perturb(pol_exp)
       cst, size, area_temp, coord_temp, sizes, wires = cost_func(pol_exp, block_dimensions, adj_matrix)
       init_temp_arr.append(cst)
       loop = loop + 1

 size, area_temp, sizes, coord_temp  = area(pol_exp,block_dimensions)
 
 print("\n Initial Polish Expression ", pol_exp)
 print("\n Initial Size " + str(area_temp) +  " = "+ str(size[0]) +  "x" +str(size[1]))

 fig = plt.figure() 
 ax = fig.add_subplot(111) 
 number_of_colors= len (pol_exp)
 colors = ["#"+''.join([random.choice('0123456789ABCDEF') for j in range(6)])
            for i in range(number_of_colors)] 
 operands=[]
 for i in pol_exp:
   if  i not in ['H', 'V']:
     operands.append(i)

 op=block_ids
 for i in range(len(operands)):
    
               rect = matplotlib.patches.Rectangle((coord_temp[op.index(operands[i])][0], 
                                                    coord_temp[op.index(operands[i])][1]), 
                                                   sizes[i][0], 
                                                   sizes[i][1], 
                                                   facecolor = colors[i], edgecolor = '000000',
                                                   label = operands[i]) 
           
               ax.add_patch(rect) 
               ax.text(coord_temp[op.index(operands[i])][0] + 0.1, 
                       coord_temp[op.index(operands[i])][1] + 0.1,
                       operands[i], fontsize = 13)
               ax.text(coord_temp[op.index(operands[i])][0] + 1, 
                       coord_temp[op.index(operands[i])][1] + 1,
                       sizes[i], fontsize = 10)
            
 plt.xlim([0, size[0]+10]) 
 plt.ylim([0, size[1]+10]) 

 plt.title('Initial Floorplanning') 
 plt.savefig("Initial_Floorplanning",dpi=1000)
 plt.show()

 i = 0
 sum = 0
 while (i<4):
       sum = sum + abs(init_temp_arr[i+1] - init_temp_arr[i])
       i = i+1
       
 avg_cost = sum/4
 #initial_temperature = -avg_cost/math.log(0.9)
       
 #print ("\n Initial Temperature calculated:",initial_temperature)
 initial_temperature=100  
 tempfact = 0.9
 #temperature = initial_temperature
 temperature =400
 temp_iteration = 1
   
 polish_exp = pol_exp[:]
 polish_exp_temp = polish_exp[:]
 reject = 0
 temp_reject = 0
   
 cost, size, _area, _coord, selected_dim, wires  = cost_func(polish_exp, block_dimensions,adj_matrix) # Initial cost (at t=0)
 cost_temp = 0
 size_temp = 0
 best_size = size
 best_cost = cost
 best_area = _area
 best_coord = _coord
 best_polish_exp = polish_exp_temp[:]
 best_dim=selected_dim
 best_connections = wires[:]
 N = len(adj_matrix[0])
 no_of_moves = 0
 uphill  = 0
 arealist=[]
 costlist=[]

 timeout = time.time() + 3600
 while (temperature > (initial_temperature/100000) and time.time()<timeout): # Until the temperature reaches 0.5, keep iterating

       polish_exp_temp  = perturb(polish_exp_temp)
       no_of_moves = no_of_moves + 1

       cost_temp, size_temp, area_temp, coord_temp, selected_dim_temp, wires_temp = cost_func(polish_exp_temp, block_dimensions,adj_matrix)
       costlist.append(cost_temp)
       #arealist.append(area_temp)
       if (cost < best_cost):
           best_cost = cost
           best_size = size
           best_polish_exp = polish_exp[:]
           best_area = _area
           best_dim= selected_dim[:]
           arealist.append(_area)
           best_connections= wires[:]
           #costlist.append(best_cost)
           best_coord = _coord[:]

       delta_cost = cost_temp - cost


       if (delta_cost <= 0):
           cost = cost_temp
           size = size_temp
           _area = area_temp
           wires = wires_temp[:]
           selected_dim = selected_dim_temp[:]
           polish_exp = polish_exp_temp[:]
           _coord = coord_temp[:]
           reject = 0
           temp_reject = 0
       elif (math.exp(-(delta_cost/temperature)) < random.uniform(0,1)):
           cost = cost_temp
           size = size_temp
           _area = area_temp
           wires = wires_temp[:]
           selected_dim = selected_dim_temp[:]
           polish_exp = polish_exp_temp[:]
           _coord = coord_temp[:]
           reject = 0
           temp_reject = 0
           uphill = uphill + 1
       else:
           reject = reject + 1
       if (uphill > N or no_of_moves>2*N):
               
           uphill = 0
           no_of_moves = 0
           temp_reject = temp_reject + 1
           temperature = temperature*math.pow(tempfact,temp_iteration) 
           temp_iteration = temp_iteration + 1 
 plt.figure(figsize=(16,9))
 plt.plot(arealist)
 plt.xlabel('Accepted temperature')
 plt.ylabel('Area')
 plt.show()
 plt.figure(figsize=(16,9))
 plt.plot(costlist)
 plt.xlabel('Iterations')
 plt.ylabel('Cost')
 plt.savefig("Floorplanning_Cost_vs_Iterations.png",dpi=1000)
 plt.show()

 return best_polish_exp, best_area, best_coord, best_size, temperature, best_dim, best_connections, best_cost
 
 

best_pol_exp, best_area, best_coord, best_size, temperature, sel_dim, best_connections, best_cost =simulated_annealing(connectivity_matrix, block_ids, block_dimensions)  

operands=[]

fig = plt.figure() 
ax = fig.add_subplot(111) 
for i in best_pol_exp:
   if  i not in ['H', 'V']:
     operands.append(i)
number_of_colors= len (best_pol_exp)
colors = ["#"+''.join([random.choice('0123456789ABCDEF') for j in range(6)])
            for i in range(number_of_colors)] 

op=block_ids
for i in range(len(operands)):
    
               rect = matplotlib.patches.Rectangle((best_coord[op.index(operands[i])][0], 
                                                    best_coord[op.index(operands[i])][1]), 
                                                   sel_dim[i][0], 
                                                   sel_dim[i][1], 
                                                   facecolor = colors[i], edgecolor = '000000',
                                                   label = operands[i]) 
           
               ax.add_patch(rect) 
               ax.text(best_coord[op.index(operands[i])][0] + 0.1, 
                       best_coord[op.index(operands[i])][1] + 0.1,
                       operands[i], fontsize = 13)
               ax.text(best_coord[op.index(operands[i])][0] + 1, 
                       best_coord[op.index(operands[i])][1] + 1,
                       sel_dim[i], fontsize = 10)
            
plt.xlim([0,  best_size[0]+10]) 
plt.ylim([0, best_size[1]+10]) 

plt.title('Final Floorplanning') 
plt.savefig("Final_Floorplanning",dpi=1000)
plt.show()

print ("Area of Floorplan ="+ str(best_area)+"sq units" )
#print(best_area, best_pol_exp,sel_dim, best_coord  )
print("Preferred Polish Expression",best_pol_exp)
print(" Wire connections between blocks:")
print(best_connections)
print("Cost of floorplan =",best_cost)


# **Inference**
# 
#  I got the following floorplan whose area is 182 sq units.
# ![182 (2).JPG](data:image/jpeg;base64,/9j/4AAQSkZJRgABAQEAkACQAAD/4ShCRXhpZgAATU0AKgAAAAgACAALAAIAAAAmAAAIegESAAMAAAABAAEAAAExAAIAAAAmAAAIoAEyAAIAAAAUAAAIxgE7AAIAAAAMAAAI2odpAAQAAAABAAAI5pydAAEAAAAYAAARauocAAcAAAgMAAAAbgAAEYIc6gAAAAgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAFdpbmRvd3MgUGhvdG8gRWRpdG9yIDEwLjAuMTAwMTEuMTYzODQAV2luZG93cyBQaG90byBFZGl0b3IgMTAuMC4xMDAxMS4xNjM4NAAyMDIxOjAzOjE0IDE1OjQyOjIwAEhhcnNoaXRoYSBTAAAGkAMAAgAAABQAABFAkAQAAgAAABQAABFUkpEAAgAAAAM1OQAAkpIAAgAAAAM1OQAAoAEAAwAAAAEAAQAA6hwABwAACAwAAAk0AAAAABzqAAAACAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAMjAyMTowMzoxNCAxMzoyOTozMwAyMDIxOjAzOjE0IDEzOjI5OjMzAAAASABhAHIAcwBoAGkA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OTkvMDIvMjItcmRmLXN5bnRheC1ucyMiPjxyZGY6bGk+SGFyc2hpdGhhIFM8L3JkZjpsaT48L3JkZjpTZXE+DQoJCQk8L2RjOmNyZWF0b3I+PC9yZGY6RGVzY3JpcHRpb24+PHJkZjpEZXNjcmlwdGlvbiB4bWxuczp4bXA9Imh0dHA6Ly9ucy5hZG9iZS5jb20veGFwLzEuMC8iPjx4bXA6Q3JlYXRvclRvb2w+V2luZG93cyBQaG90byBFZGl0b3IgMTAuMC4xMDAxMS4xNjM4NDwveG1wOkNyZWF0b3JUb29sPjx4bXA6Q3JlYXRlRGF0ZT4yMDIxLTAzLTE0VDEzOjI5OjMzLjU4OTwveG1wOkNyZWF0ZURhdGU+PC9yZGY6RGVzY3JpcHRpb24+PC9yZGY6UkRGPjwveDp4bXBtZXRhPg0KICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAg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tP8A0rkr2evGNI/5O88Q/wDYn2n/AKVyUAez0UUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAJ96vK7r9l74VXniC71ybwVpr6vdT/abi7w2+ST+83zV6rRQB5/qXwH8A6x4jttfvfC9jca1bbfJvGVt6bfu/wAVd6qBFVV4UU+igDxf4yf8ln+Cn/YUv/8A0javaK8X+Mn/ACWf4Kf9hS//APSNq9ooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAK8Y0j/k7zxD/wBifaf+lclez14xpH/J3niH/sT7T/0rkoA9nooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigDxf4yf8AJZ/gp/2FL/8A9I2r2ivF/jJ/yWf4Kf8AYUv/AP0javaKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACvGNI/5O88Q/wDYn2n/AKVyV7PXjGkf8neeIf8AsT7T/wBK5KAPZ6KKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooA8X+Mn/JZ/gp/wBhS/8A/SNq9orxf4yf8ln+Cn/YUv8A/wBI2r2igAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigArxjSP+TvPEP/Yn2n/pXJXs9eMaR/yd54h/7E+0/wDSuSgD2eiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAoqOTd5bbPvY+WvnfwF8QfiLp/xa8d+F/Fer6fqsGnaEur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)
# 
# 
# Its not necessary that every execution will give same area because moves are chosen randomly. It may happen that even for same number of iterations we may get different minimum areas. 
