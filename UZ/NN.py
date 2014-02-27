import math
import random
import string
import sys

def normaliziraj(sb, uz):
    return [float(sb)/5, float(uz)/100]

class NN:
  def __init__(self, NI, NH, NO):
    self.ni = NI + 1
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

  # loadiranje NN
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

def neuro(argv):
    #############       ZID         ######################
    ######################################################
    if argv[0] == 'treniraj_zid':
      # broj elemenata NN je fiksiran na 2 2 1
        br_input = 2
        br_hidden = 2
        br_output = 1
        # inicijalizira se NN
        n = NN(br_input, br_hidden, br_output)

        # generiranje data seta za treniranje
        data_set = []
        broj = 40 # mijenjati po potrebi
        # broj elemenata kada je zid
        for i in range(broj):
            SB = random.randrange(0, 6)
            UZ = random.randrange(1, 31) # UZ kod zida je [1-30]
            TAR = 1 # target 1 > zid
            data_set.append([normaliziraj(SB, UZ), [TAR]])
        # broj elemenata kada nije zid
        for j in range(broj):
            SB = random.randrange(1, 6)
            UZ = random.randrange(31, 100) # UZ kod praznog prostora [31 - 100] // UZ ogranicen na max 100
            TAR = 0 # target 0 > prazan prostor
            data_set.append([normaliziraj(SB, UZ), [TAR]])       

        # treniranje NN
        n.train(data_set)

        # spremanje NN u 'NNZid' datoteku
        n.save_nn('zid', [br_input, br_hidden, br_output])


    if argv[0] == 'test_zid':

        # loadiranje istrenirane NN gdje je argv[1] ime datoteke gdje je spremljena NN
        f = open(argv[1], 'r')
        br_input = int(f.readline().strip('\n'))
        br_hidden = int(f.readline().strip('\n'))
        br_output = int(f.readline().strip('\n'))

        inputWeights = []
        for i in range(br_input + 1):
            temp = f.readline().strip('\n')
            temp = temp.split(',')
            temp = [float(i) for i in temp]
            inputWeights.append(temp)

        outputWeights = []
        for i in range(br_hidden):
            temp = f.readline().strip('\n')
            outputWeights.append(float(temp))
        f.close()

        net = NN(br_input, br_hidden, br_output)
        net.set_weights(inputWeights, outputWeights)


        # ako je vise od dva argumenta (ime datoteke gdje je spremljena NN) onda se pretpostavlja da se testira samo jedan unos gdje je argv[2] = SB vrijednost, argv[3] = UZ vrijednost
        if len(argv) > 2:
          print net.runNN(normaliziraj(argv[2], argv[3]))
        else: 
        # ako nema vise od dva vrsi se testiranje na nasumicno generiranom data setu
          test_set = []
          for x in range(30):
              SB = random.randint(1, 6)
              UZ = random.randint(1, 100)
              if UZ < 30:
                  TAR = 1
              else:
                  TAR = 0
              test_set.append([normaliziraj(SB, UZ), [TAR]]) 

          net.test(test_set)

    #############       RUPA   (ne radi)##################
    ######################################################
    if argv[0] == 'treniraj_rupa':
        br_input = 2
        br_hidden = 2
        br_output = 1
        n = NN(br_input, br_hidden, br_output)

        data_set = []
        broj = 100
        for i in range(broj):
            SB = 3
            UZ = random.randrange(1, 100)
            TAR = 1
            data_set.append([normaliziraj(SB, UZ), [TAR]])

        temp = range(1, 3) + range(4, 6)
        for j in range(broj):
            SB = random.choice(temp)
            UZ = random.randrange(1, 100)
            TAR = 0
            data_set.append([normaliziraj(SB, UZ), [TAR]])       

        n.train(data_set, max_iterations=10000)

        n.save_nn('rupa', [br_input, br_hidden, br_output])

    if argv[0] == 'test_rupa':

        f = open('NNZid', 'r')
        br_input = int(f.readline().strip('\n'))
        br_hidden = int(f.readline().strip('\n'))
        br_output = int(f.readline().strip('\n'))

        inputWeights = []
        for i in range(br_input + 1):
            temp = f.readline().strip('\n')
            temp = temp.split(',')
            temp = [float(i) for i in temp]
            inputWeights.append(temp)

        outputWeights = []
        for i in range(br_hidden):
            temp = f.readline().strip('\n')
            outputWeights.append(float(temp))
        f.close()

        net = NN(br_input, br_hidden, br_output)
        net.set_weights(inputWeights, outputWeights)


        test_set = []
        for x in range(30):
            SB = random.randint(1, 6)
            UZ = random.randint(1, 100)
            if SB == 3:
                TAR = 1
            else:
                TAR = 0
            test_set.append([normaliziraj(SB, UZ), [TAR]]) 

        net.test(test_set)


if __name__ == '__main__':
    neuro(sys.argv[1:])
