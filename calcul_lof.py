import math
import Queue
#Calculate the distance of each point
def getdisance(data,datalen):
    #print data
    dismatrix = [[0 for i in range(datalen)] for i in range(datalen)]
    
    for i in range(datalen-1):
        for j in range(i+1,datalen):
            dis = 0
            for l in range(len(data[0])):
                #print("i:",i," j:",j," k:",k)
                dis = dis + (data[i][l]-data[j][l])*(data[i][l]-data[j][l])
            dis = math.sqrt(dis)
            dismatrix[i][j] = dis
            dismatrix[j][i] = dis
    return dismatrix


#Calculate the K distance of each point
def getk_distance(matrix,datalen,k):
    kdis = [0 for i in range(datalen)]
    for i in range(datalen):
        pq = Queue.PriorityQueue(k)
        for j in range(datalen):
            if i!=j:
                if pq.full() == False:
                    pq.put(matrix[i][j]*-1)
                else:
                    kdis[i] = pq.get()
                    if matrix[i][j]*-1>kdis[i]:
                        pq.put(matrix[i][j]*-1)
                    else:
                        pq.put(kdis[i])
        kdis[i] = pq.get()*-1
    print("kids:",kdis)
    return kdis

#Calculate reachable disdance of each point
def getreach_distance(matrix,datalen,kdis):
    reachdis_matrix = [[0 for i in range(datalen)] for i in range(datalen)]
    for i in range(datalen):
        for j in range(datalen):
            if i==j:
                reachdis_matrix[i][j] = 0
            else:
                if matrix[i][j] > kdis[j]:
                    reachdis_matrix[i][j] = matrix[i][j]
                else:
                    reachdis_matrix[i][j] = kdis[j]
    #print("reachdis_matrix:"reachdis_matrix)
    return reachdis_matrix


#Calculate local reachable density of each point
def getlrd(reachdis_matrix,matrix,datalen,minpts):
    lrd = [0 for i in range(datalen)]
    for i in range(datalen):
        lrdpq = Queue.PriorityQueue(minpts)
        for j in range(datalen):
            if i!=j:
                if lrdpq.full() == False:
                    lrdpq.put([matrix[i][j]*-1,j])
                else:
                    temp = lrdpq.get()
                    if matrix[i][j]*-1 > temp[0]:
                        lrdpq.put([matrix[i][j]*-1,j])
                    else:
                        lrdpq.put(temp)
        while not lrdpq.empty():
            temp = lrdpq.get()
            lrd[i] = lrd[i] + reachdis_matrix[i][temp[1]]
        lrd[i] = minpts/(lrd[i]+0.001)

    print("lrd:",lrd)
    return lrd

                        
#Calculate LOF of each point
def getlof(data,k,minpts):
    datalen = len(data)
    dismatrix = getdisance(data,datalen)
    kdis = getk_distance(dismatrix,datalen,k)
    reach_mat = getreach_distance(dismatrix,datalen,kdis)
    lrd = getlrd(reach_mat,dismatrix,datalen,minpts)

    lof = [0 for i in range(datalen)]
    for i in range(datalen):
        lofpq = Queue.PriorityQueue(minpts)
        for j in range(datalen):
            if i!=j:
                if lofpq.full() == False:
                    lofpq.put([dismatrix[i][j]*-1,j])
                else:
                    temp = lofpq.get()
                    if dismatrix[i][j]*-1 > temp[0]:
                        lofpq.put([dismatrix[i][j]*-1,j])
                    else:
                        lofpq.put(temp)
        while not lofpq.empty():
            temp = lofpq.get()
            lof[i] = lof[i] + lrd[temp[1]]
        lof[i] = (lof[i]/minpts)/lrd[i]

    print"lof:",lof
    return lof

if __name__ == '__main__':
    K = 3
    MinPts = 3
    #test data
    psdata = [[55,88,40,62,75],
              [40,85,45,65,75],
              [55,80,40,58,75],
              [45,88,42,62,70],
              [55,82,38,66,78],
              [55,50,99,99,20],
              [58,70,40,60,80],
              [0,0,0,0,0]]
    print "psdata len:",len(psdata)
    pslof = getlof(psdata,K,MinPts)

	