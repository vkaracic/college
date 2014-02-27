import math
import random
import string
import sys

# normalizacija unosa NN po formuli za Max-Min normalizaciji
# primjer: http://www.cs.sunysb.edu/~cse634/ch6NN.pdf
def normaliziraj(sb, uz):
    return [float(sb)/5, float(uz)/100]

class NN:
  def __init__(self, NI, NH, NO):
    self.ni = NI + 1 # dodatak za bias
    self.nh = NH
    self.no = NO
    
    self.ai, self.ah, self.ao = [],[], []
    self.ai = [1.0]*self.ni
    self.ah = [1.0]*self.nh
    self.ao = [1.0]*self.no

    self.wi = makeMatrix (self.ni, self.nh)
    self.wo = makeMatrix (self.nh, self.no)

    randomizeMatrix ( self.wi, -0.2, 0.2 )
    randomizeMatrix ( self.wo, -2.0, 2.0 )

    self.ci = makeMatrix (self.ni, self.nh)
    self.co = makeMatrix (self.nh, self.no)
    
  def runNN (self, inputs):
    if len(inputs) != self.ni-1:
      print 'incorrect number of inputs'
    
    for i in range(self.ni-1):
      self.ai[i] = inputs[i]
      
    for j in range(self.nh):
      sum = 0.0
      for i in range(self.ni):
        sum +=( self.ai[i] * self.wi[i][j] )
      self.ah[j] = sigmoid (sum)
    
    for k in range(self.no):
      sum = 0.0
      for j in range(self.nh):        
        sum +=( self.ah[j] * self.wo[j][k] )
      self.ao[k] = sigmoid (sum)
      
    return self.ao
      
      
  
  def backPropagate (self, targets, N, M):

    output_deltas = [0.0] * self.no
    for k in range(self.no):
      error = targets[k] - self.ao[k]
      output_deltas[k] =  error * dsigmoid(self.ao[k]) 
   
    for j in range(self.nh):
      for k in range(self.no):
        change = output_deltas[k] * self.ah[j]
        self.wo[j][k] += N*change + M*self.co[j][k]
        self.co[j][k] = change

    hidden_deltas = [0.0] * self.nh
    for j in range(self.nh):
      error = 0.0
      for k in range(self.no):
        error += output_deltas[k] * self.wo[j][k]
      hidden_deltas[j] = error * dsigmoid(self.ah[j])
    
    for i in range (self.ni):
      for j in range (self.nh):
        change = hidden_deltas[j] * self.ai[i]
        self.wi[i][j] += N*change + M*self.ci[i][j]
        self.ci[i][j] = change
        
    error = 0.0
    for k in range(len(targets)):
      error = 0.5 * (targets[k]-self.ao[k])**2
    return error
        
        
  def weights(self):
    print 'Input weights:'
    for i in range(self.ni):
      print self.wi[i]
    print
    print 'Output weights:'
    for j in range(self.nh):
      print self.wo[j]
    print ''


  # spremanje NN
  # Format spremanja NN:
  #   broj input cvorova
  #   broj skrivenih cvorova
  #   broj output cvorova
  #   tezina veza cvorova inputa
  #       tezine pojedinih cvorova odvojene zarezom
  #       cvorovi odvojeni novim redom
  #   tezine veza skrivenih cvorova odvojeni novim redom
  def save_nn(self, koncept, NN):
    if koncept == 'zid':
        f = open('NNZid', 'w')
    elif koncept == 'rupa':
        f = open('NNRupa', 'w')
    for i in NN:
      f.write(str(i))
      f.write('\n')
    for i in range(self.ni):
      f.write(str(self.wi[i][0]))
      f.write(',')
      f.write(str(self.wi[i][1]))
      f.write('\n')
    for j in range(self.nh):
      f.write(str(self.wo[j][0]))
      f.write('\n')
    f.close()

  # postavljanje ucitanih tezina iz datoteke
  # dio loadiranja NN
  def set_weights(self, wi, wo):
    for i in range(self.ni):
      self.wi[i] = wi[i]
    for j in range(self.nh):
      self.wo[j] = [wo[j]]

  def test(self, patterns):
    for p in patterns:
      inputs = p[0]
      print 'Inputs:', p[0], '-->', self.runNN(inputs), '\tTarget', p[1]
  
  def train (self, patterns, max_iterations = 1000, N=0.5, M=0.1):
    for i in range(max_iterations):
      for p in patterns:
        inputs = p[0]
        targets = p[1]
        self.runNN(inputs)
        error = self.backPropagate(targets, N, M)
      if i % 50 == 0:
        print 'Combined error', error

def sigmoid (x):
  return math.tanh(x)
  
def dsigmoid (y):
  return 1 - y**2

def makeMatrix ( I, J, fill=0.0):
  m = []
  for i in range(I):
    m.append([fill]*J)
  return m
  
def randomizeMatrix ( matrix, a, b):
  for i in range ( len (matrix) ):
    for j in range ( len (matrix[0]) ):
      matrix[i][j] = random.uniform(a,b)

def neuro(SB, UZ):
    #############       ZID         ######################
    ######################################################

    # POCETAK procesa ucitavanja NN iz datoteke NNZid
      # ucitavanje strukture NN
      f = open('NNZid', 'r')
      br_input = int(f.readline().strip('\n'))
      br_hidden = int(f.readline().strip('\n'))
      br_output = int(f.readline().strip('\n'))

      # ucitavanje input tezina
      inputWeights = []
      for i in range(br_input + 1):
          temp = f.readline().strip('\n')
          temp = temp.split(',')
          temp = [float(i) for i in temp]
          inputWeights.append(temp)

      # ucitavanje output tezina
      outputWeights = []
      for i in range(br_hidden):
          temp = f.readline().strip('\n')
          outputWeights.append(float(temp))
      f.close()

      # stvaranje NN po ucitanim parametrima
      net = NN(br_input, br_hidden, br_output)
      net.set_weights(inputWeights, outputWeights)

      # pokretanje NN i testiranje za trazene vrijednosti
      rezultat = net.runNN(normaliziraj(SB, UZ))

      # peglanje rezultata
      if rezultat[0] > 0.5:
        return 1
      else:
        return 0
