from networkx import *
P=dict()
P['A']=['1','2','1','1','1','1','1','1','1','1','1','3','12','4','23','55','6']
P['B']=['1','5','7','23','12','32','11','6','5','7','23','12','32','11','6','5','7','23','12','32','11','6','5','7','23','12','32','11','6','5','7','23','12','32','11','6']
P['C']=['1','8','2','33','12','54','23','13','8','2','33','12','54','23','13','8','2','33','12','54','23','13','8','2','33','12','54','23','13','8','2','33','12','54','23','13']
P['D']=['1','4','5','12','44','32','123','4','5','12','44','32','123','4','5','12','44','32','123','4','5','12','44','32','123','4','5','12','44','32','123','4','5','12','44','32','123']
def personal_pk(P,user,alpha,t):
    pk=dict()
    G=multigraph.MultiGraph()
    for i,j in P.items():
        for k in j:
            G.add_edge(i,k)
    pk = {x:0 for x in G.nodes()}
    pk[user]=1
    for i in range(0,t):
        tmp={x:0 for x in G.nodes()} 
        for j in G.nodes():
            N=len(G.edges(j))
            for k in G.edges(j):
                tmp[k[1]]+=alpha*pk[j]/float(N)
        tmp[user]+=1-alpha
        pk=tmp
    #print G.edges()
    return pk

def swap(a,b):
    tmp=a
    a=b
    b=tmp
    return a,b
def sort(scoredocs):
    scoredocs=scoredocs.items()
    while 1:
        flag=0
        for i in range(0,len(scoredocs)-1):
            if  scoredocs[i][1]<scoredocs[i+1][1]:
                tmp=scoredocs[i]
                scoredocs[i]=scoredocs[i+1]
                scoredocs[i+1]=tmp
                flag=1
        if flag==0:
            break
    for i,j in scoredocs:
        print (j)
    return scoredocs            
print sort(personal_pk(P,'A',0.85,50))        
    
