import copy 
import time
#Дано поле 4х4 из квадратов, у которых одна сторона белая, а другая черная. В начальном состоянии часть квадратов 
#расположена вверх белой стороной, а часть черной. Игрок, выбирая определенный квадрат, переворачивает его и его 
#соседей по вертикали и горизонтали. Таким последовательными действиями необходимо добиться целевого состояния 
#(например, все квадраты повернуты белой стороной). Пример головоломки можно посмотреть по следующей ссылке
#http://flashroom.ru/games988.html.

# Узел графа
class Node: 
  def __init__(self, state, depth, parent):
    self.parent = parent # указатель на родительский узел
    self.state = state # состояние данного узла в пространстве состояний
    self.depth = depth # глубина узла

# Пошаговый вывод
def PrintPath(node, elapsed_time):
  depth = node.depth
  states = []
  while (node.parent is not None):
    states.insert(0, node.state)
    node = node.parent
  states.insert(0, node.state)
  with open('./output.txt', mode='w', encoding='utf-8') as file:
    file.write('elapsed time: {} seconds\ndepth: {}\n'.format(elapsed_time, depth))
    for state in states:
      for row in state:
        file.write('{}{}{}{}\n'.format(row[0], row[1], row[2], row[3]))
      file.write('\n')
 
# Раскрытие узла
def Expand(node):
  fringe_tail = []
  for i in range(0, 4):
    for j in range(0, 4):
      state = copy.deepcopy(node.state)
      state[i][j] = abs(state[i][j] - 1)
      if i > 0:
        state[i-1][j] = abs(state[i-1][j] - 1)
      if i < 3:
        state[i+1][j] = abs(state[i+1][j] - 1)
      if j > 0:
        state[i][j-1] = abs(state[i][j-1] - 1)
      if j < 3:
        state[i][j+1] = abs(state[i][j+1] - 1)
      fringe_tail.append(Node(state, depth=node.depth + 1, parent=node))
  return fringe_tail

# Поиск в графе целевого состояния
def GraphSearch():
  init_state = [[1,0,0,1], 
                [0,0,0,0],
                [0,0,0,0],
                [1,0,0,1]]
  target_state=[[0,0,0,0], 
                [0,0,0,0],
                [0,0,0,0],
                [0,0,0,0]] 
  #init_state = [[0,0,0,0], 
  #              [0,0,0,0],
  #              [0,0,0,0],
  #              [0,0,0,0]]
  #target_state=[[1,1,1,1], 
  #              [1,0,0,1],
  #              [1,0,0,1],
  #              [1,1,1,1]] 
  target_hash = hash(str(target_state)) 
  closed = set() # множество развернутых узлов
  fringe = [] # периферия в виде стека
  start_time = time.clock()
  fringe.append(Node(init_state, depth=0, parent=None))
  while True:
    if len(fringe) == 0:
      return 'Failure'
    node = fringe.pop()
    # Достигли целевого состояния?
    if target_hash == hash(str(node.state)):
      PrintPath(node, time.clock() - start_time)
      return 'Success'
    if str(node.state) not in closed:
      closed.add(str(node.state))
      fringe += Expand(node)
    print(node.depth)
  return

print(GraphSearch())