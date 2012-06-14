#!/usr/bin/python
import random
import os
import sys
import time
import copy

# generates n random sequences of tuples as the sorting networks
def genRandSolutions(numSolutions):
   solutions = []

   for i in range(numSolutions):
      solutions.append([])
      randVal = random.randint(5,100)
      for j in range(randVal):
         randX = random.randint(0,15)
         randY = random.randint(0,15)
         # generate tuples with different elements
         while randY == randX:
            randY = random.randint(0,15)
         tempTup = (randX,randY)
         solutions[i].append(tempTup)
   return solutions


# generates a list of inital inputs
def genInputs(numInputs):
   numEles = 16
   inputs = []
   pop = [0]*numEles

   for i in range(1,numEles+1):
      pop[i-1] = i

   for i in range(numInputs):
      tempList = random.sample(pop,numEles)
      inputs.append(tempList) 

   return inputs

def getBestSol(solutions,fitness,fileobj,genNum,fileSol,totalGens):
   bestSolScore = 0.0
   bestSol = []
   bestSolLen = 0
   avgSolScore = 0.0
   avgSolLen = 0
   for i in range(len(fitness)):
      avgSolScore += fitness[i]
      avgSolLen += len(solutions[i])
      if (fitness[i] > bestSolScore):
         bestSolScore = fitness[i]
         bestSol = solutions[i]
         bestSolLen = len(solutions[i])
   avgSolScore = avgSolScore/len(fitness)
   avgSolLen = avgSolLen/float(len(fitness))
   fileobj.write('Best solution score:\t' + str(bestSolScore)+'\t')
   fileobj.write('Best solution len:\t' + str(bestSolLen)+'\n')
   if genNum == totalGens-1:
      fileSol.write('Best solution\n')
      fileSol.write(str(bestSol)+'\n')
   print 'Best solution score: ' + str(bestSolScore) +'\tAvg solution score: '+str(avgSolScore)
   print 'Best solution len: ' + str(bestSolLen) + '\tAvg solution len: ' + str(avgSolLen)


def solutionFitness(solutions,inputs):
   # part 1
   # create a list counts. These counts represent how many
   # inputs each solution sorted correctly 
   countList = [0.0]*len(solutions)
   for i in range(len(solutions)):
      for j in range(len(inputs)):
         countList[i] += sortCheck2(solutions[i],inputs[j])
      countList[i] = countList[i]/len(inputs)

   # part 2
   # first find the maximum length of the longest network
   maxSolLength = 0
   for i in range(len(solutions)):
      if len(solutions[i]) > maxSolLength:
         maxSolLength = len(solutions[i])

   lenList = [0]*len(solutions)
   for i in range(len(solutions)):
      lenList[i] = len(solutions[i])/float(maxSolLength)
      lenList[i] = 1-lenList[i]
     
   # create fitness based on number of correctly sorted inputs
   # and the length of the sorting network
   fitList = [0.0]*len(solutions)
   #sortWeight = 0.99
   sortWeight = 0.999
   lenWeight = 1.0 - sortWeight

   for i in range(len(solutions)):
      fitList[i] = (sortWeight*countList[i]) + (lenWeight*lenList[i])

   return fitList


def inputFitness(solutions,inputs):
   # keeps count of the number of solutions that fail to sort 
   # input correctly
   countList = [0]*len(inputs)
   for i in range(len(inputs)):
      for j in range(len(solutions)):
         if sortCheck(solutions[j],inputs[i]) == False:
            countList[i] += 1
      countList[i] = countList[i]/float(len(solutions))
   return countList

 
# checks to see if a network sorts an input list correctly
def sortCheck2(sortNetwork,inputlist):
   sortedByNet = copy.deepcopy(inputlist)
   for i in range(len(sortNetwork)):
      a,b = sortNetwork[i]
      if a < b:
         if sortedByNet[a] > sortedByNet[b]:
            sortedByNet[a],sortedByNet[b] = sortedByNet[b],sortedByNet[a] 
      else:
         if sortedByNet[a] < sortedByNet[b]:
            sortedByNet[a],sortedByNet[b] = sortedByNet[b],sortedByNet[a] 
   
   count = 0.0
   miss = 0
   for i in range(len(sortedByNet)-1):
      if sortedByNet[i] <= sortedByNet[i+1]:
         count += 1.0
      else:
         miss +=1
   score = count/(len(sortedByNet)-1)
   return score  

# old sort checker
def sortCheck(sortNetwork,inputlist):
   sortedByNet = copy.deepcopy(inputlist)
   # sorts the input list based on the sorting network
   for i in range(len(sortNetwork)):
      a,b = sortNetwork[i]
      if a < b:
         if sortedByNet[a] > sortedByNet[b]:
            sortedByNet[a],sortedByNet[b] = sortedByNet[b],sortedByNet[a] 
      else:
         if sortedByNet[a] < sortedByNet[b]:
            sortedByNet[a],sortedByNet[b] = sortedByNet[b],sortedByNet[a] 
         
   # now check the sorted list and see if it is sorted correctly
   for i in range(len(sortedByNet)-1):
      if sortedByNet[i] > sortedByNet[i+1]:
         return False
   return True
  
 
def selectForSurvival(solutions,fitnessVals,SurviveRate):
   sumFitnessVal = 0
   survivedSols = []

   for i in range(len(fitnessVals)):
      sumFitnessVal += fitnessVals[i]

   for i in range(int(len(solutions)*SurviveRate)):
      randVal = random.uniform(0.0,sumFitnessVal)
      curSlice = 0.0
      j = 0 
      hitFlag = False
      while (hitFlag == False):
         curSlice += fitnessVals[j]
         if curSlice >= randVal:
            survivedSols.append(solutions[j])
            hitFlag = True
         j += 1
   return survivedSols


# uses the "cut and splice" crossover variant
def crossover(numSolutions,survivors,k):
   numOffspring = k
   
   offspring = []
   for i in range(0,numOffspring,2):
      parentA = random.randint(0,len(survivors)-1)
      parentB = random.randint(0,len(survivors)-1)
      if len(survivors[parentA]) == 1:
         cutPos1 = 0
      else:    
         cutPos1 = random.randint(0,len(survivors[parentA])-1)
      if len(survivors[parentB]) == 1:
         cutPos2 = 0
      else:
         cutPos2 = random.randint(0,len(survivors[parentB])-1)
      offspring.append(survivors[parentA][:cutPos1] + survivors[parentB][cutPos2:])
      offspring.append(survivors[parentB][:cutPos2] + survivors[parentA][cutPos1:])
      if (offspring[i] == [] or offspring[i+1] == []):
         print 'hit_crossover'
   return offspring

def addBestToOffspring(numNetworks,offspring,networks,fitness):
   
   numAddNets = numNetworks - len(offspring)
   bestFit = [0.0]*numAddNets
   bestFitIndx = [0]*numAddNets
   # loops through and finds the fittess networks
   for j in range(numAddNets):
      for i in range(len(fitness)):
         if bestFit[j] < fitness[i]:
            bestFit[j] = fitness[i]
            bestFitIndx[j] = i
      fitness.pop(bestFitIndx[j])
      fitness.insert(bestFitIndx[j],0.0)
  
   bestNets = []
   for i in range(numAddNets):
      bestNets.append(networks[bestFitIndx[i]])
   return bestNets + offspring


def mutate(solutions):
   mProb = 0.001
   newSols = []
   for i in range(len(solutions)):
      newSols.append([])
      for j in range(len(solutions[i])):
         randVal = random.random()
         if randVal < mProb:
            # flip a coin, if < 0.5, flip tuple
            randVal2 = random.random()
            if randVal2 < 0.5:
               randX = random.randint(0,15)
               randY = random.randint(0,15)
               while randY == randX:
                  randY = random.randint(0,15)
               tempTup = (randX,randY)
               newSols[i].append(tempTup)
            else:
               newSols[i].append(solutions[i][j])
         else: 
            newSols[i].append(solutions[i][j])
      if len(newSols[i]) == 0:
         print 'hit mutate'
         newSols[i].append(solutions[i][0])
         print newSols[i] 
 
   return newSols


def mutateForInputs(inputs):
   mProb = 0.3
   
   for i in range(len(inputs)):
      randVal = random.random()
      if randVal < mProb:
         inputs.pop(i)
         newInput = genInputs(1)
         inputs.insert(i,newInput[0])
   return inputs


def crossoverForInputs(numInputs,survivors):
   numOffspring = numInputs - len(survivors)
   offspring = []
   for i in range(0,numOffspring,2): 
      parentA = random.randint(0,len(survivors)-1)
      parentB = random.randint(0,len(survivors)-1) 
      cutPos = random.randint(0,len(survivors[parentA])-1)
      offspring.append(survivors[parentA][:cutPos] + survivors[parentB][cutPos:])
      offspring.append(survivors[parentB][cutPos:] + survivors[parentA][:cutPos])
   return survivors + offspring

def checkForDuplicates(networks):
   newNets = []
   for i in range(len(networks)):
      newNets.append([])
      if len(networks[i]) == 1:
         newNets[i].append(networks[i][0])
      else: 
         for j in range(len(networks[i])-1):
            if networks[i][j] != networks[i][j+1]:
               newNets[i].append(networks[i][j])
   return newNets   
      
def getInputs(inputs,inputfile):
   for i in range(len(inputs)):
      inputfile.write(str(inputs[i])+'\n')



def main():
   numSolutions = 100
   numInputs = 50
   numGenerations = 2500
   solSurviveRate = 0.5
   inputSurviveRate = 0.5
   k = int(numSolutions*0.5)
   initSols = genRandSolutions(numSolutions)
   initInputs = genInputs(numInputs)
   sortNetworks = initInputs 
   FILE1 = open('BestNetworkValuesTest.txt','w')
   FILE2 = open('BestSolution.txt','w')
   FILE3 = open('finalInputPop.txt','w')

   for i in range(numGenerations):
      FILE1.write(str(i)+'\t')
      print "generation " + str(i)
      solFitVals = solutionFitness(initSols,initInputs)
      inputFitVals = inputFitness(initSols,initInputs)
      getBestSol(initSols,solFitVals,FILE1,i,FILE2,numGenerations)
      survivedSols = selectForSurvival(initSols,solFitVals,solSurviveRate)
      crossoverSols = crossover(numSolutions,survivedSols,k)
      offspring = addBestToOffspring(numSolutions,crossoverSols,initSols,solFitVals)
      mutateSols = mutate(offspring)
      initSols = mutateSols
   
      survivedInputs = selectForSurvival(initInputs,inputFitVals,inputSurviveRate)
      crossoverInputs = crossoverForInputs(numInputs,survivedInputs)
      mutateInputs = mutateForInputs(crossoverInputs) 
      initInputs = mutateInputs
      if i == numGenerations-1:
         getInputs(initInputs,FILE3)            
    
 
   FILE1.close()
   FILE2.close()
   FILE3.close()
main()
