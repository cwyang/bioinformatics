# Copyright (C) 2017 Greenweaves Software Pty Ltd

# This is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with GNU Emacs.  If not, see <http://www.gnu.org/licenses/>

# BA7C Implement Additive Phylogeny
from BA7B import ComputeLimbLength

class Tree(object):
    def __init__(self,N):
        self.N=N
        self.nodes=list(range(N))
        self.edges={}
    def link(self,start,end,weight=1):         
        self.half_link(start,end,weight)
        self.half_link(end,start,weight)
        
    def half_link(self,a,b,weight):
        if not a in self.nodes:
            self.nodes.append(a)        
        if a in self.edges:
            self.edges[a].append((b,weight))
        else:
            self.edges[a]=[(b,weight)]
            
    
           
    def print(self,includeNodes=False):
        self.nodes.sort()
        if includeNodes:
            print (self.nodes)
        for node in self.nodes:
            if node in self.edges:
                for edge in self.edges[node]:
                    end,weight=edge
                    print ('{0}->{1},{2}'.format(node,end,weight))
                    
    def next_node(self):
        self.N+=1
        return self.N-1
    
def AdditivePhylogeny(D,n,T=None):
    
    def find_ik():
        '''
        Find three leaves such that Di,k = Di,n + Dn,k
        '''
        for i in range(n-1):
            for k in range(n-1):
                print('i={0},k={1},D_ik={2},D_in={3},d_nk={4}'.format(i,k,D[i][k],D[i][n-1],D[n-1][k]))
                if D[i][k]==D[i][n-1]+D[n-1][k]:
                    return (i,k)
        print ('not found')
        
    def Node(x,i,k):
        '''
        the (potentially new) node in T at distance x from i on the path between i and k
        '''
        print('Node: x={0},i={1},k={2}'.format(x,i,k))
        for drow in D:
            print (', '.join([str(d) for d in drow])) 
        print ('Path from i[{0}] to k[{1}] has length {2}'.format(i,k,D[i][k]))
        if D[i][k]==x:
            print ('Found k={0}'.format(k))
            return k
        elif D[i][k]>x:
            result= T.next_node()
            print ('New={0}'.format(result))
            return result
    
    def AddNode(v,limbLength):
        '''
         link leaf n back to T by creating a limb (v, n) of length limbLength
         '''
        print('Addnode {0}, at length {2} from {1}'.format(n,v,limbLength))
        T.link(n,v,limbLength)
    
     
    if T==None:
        T=Tree(n)
   
    if n==2:
        T.link(0,1,D[0][1])
        T.print(includeNodes=True)
        return T
    else:
        limbLength=ComputeLimbLength(n-1,n-1,D)
        print('limbLength={0}'.format(limbLength))
        for j in range(n-1):
            D[n-1][j]-=limbLength
            D[j][n-1]=D[n-1][j]
        i,k=find_ik()
        x=D[i][n-1]
        DD=[dd[:] for dd in D]
        T=AdditivePhylogeny(DD,n-1,T)
        print('i={0},n={1},k={2},x={3},limb length={3}'.format(i,n,k,x,limbLength))
        for drow in D:
            print (', '.join([str(d) for d in drow]))
        v=Node(x,i,k)
        print ('v={0}'.format(v))
        AddNode(v,limbLength)
        return T
    
if __name__=='__main__':
    n=4
    D=[[0,   13,  21,  22],
        [13,  0 ,  12,  13],
        [21,  12 , 0 ,  13],
        [22 , 13 , 13,  0]]
    AdditivePhylogeny(D,n).print()