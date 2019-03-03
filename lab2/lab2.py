
#Дано поле 4х4 из квадратов, у которых одна сторона белая, а другая черная. В начальном состоянии часть квадратов 
#расположена вверх белой стороной, а часть черной. Игрок, выбирая определенный квадрат, переворачивает его и его 
#соседей по вертикали и горизонтали. Таким последовательными действиями необходимо добиться целевого состояния 
#(например, все квадраты повернуты белой стороной). Пример головоломки можно посмотреть по следующей ссылке
#http://flashroom.ru/games988.html.
# Алгоритм SMA*

import copy 
import time

# Ограничение по памяти
FRINGE_MAX_SIZE = 3

# Узел графа
class Node: 
  def __init__(self, state, Gx, Hx, parent):
    self.parent = parent # указатель на родительский узел
    self.state = state # состояние данного узла в пространстве состояний
    self.Gx = Gx # стоимость до данного узла (или глубина)
    self.Fx = Gx + Hx # стоимость пути до цели через данный узла
  def __eq__(self, other):
    return (self.state == other.state)

# Пошаговый вывод
def PrintPath(node, elapsed_time):
  depth = node.Gx
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

# Вставка узла в приоритетную очередь
def fringeInsert(node, fringe):
  isInsert = False
  for i in range(0, len(fringe)):
    if node.Fx <= fringe[i].Fx:
      fringe.insert(i, node)
      isInsert = True
      break
  if not isInsert:
    fringe.append(node)
  return

# Раскрытие узла
def Expand(node, fringe, closed):
  for i in range(0, 4):
    for j in range(0, 4):
      # Генерируем дочернее состояние
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
      # Оценка эвристикой
      gx = node.Gx + 1 # стоимость пути до данного узла (или глубина)
      hx = 0 # стоимость пути до цели от данного узла (по умолчанию 0)
      if state[0][0] is 1 and state[0][1] is 1 and state[1][0] is 1: # 1 1
        hx += 1                                                      # 1 0
      if state[0][3] is 1 and state[0][2] is 1 and state[1][3] is 1:      # 1 1
        hx += 1                                                           # 0 1
      if state[3][0] is 1 and state[3][1] is 1 and state[2][0] is 1: # 1 0
        hx += 1                                                      # 1 1
      if state[3][3] is 1 and state[3][2] is 1 and state[2][3] is 1:      # 0 1
        hx += 1                                                           # 1 1
      if 0 < sum([state[0][0],state[0][1],state[1][0]]) < 3 or 0 < sum([state[0][3],state[0][2],state[1][3]]) < 3 or 0 < sum([state[3][0],state[3][1],state[2][0]]) < 3 or 0 < sum([state[3][3],state[3][2],state[2][3]]) < 3 or 1 in [state[1][1],state[1][2],state[2][1],state[2][2]]:
        hx += 5                                                          
  # Добавляем дочерний узел в fringe
      successor = Node(state, Gx=gx, Hx=hx, parent=node)
      # Если имеется узел с таким же состоянием в fringe
      inFringe = False
      for item in fringe:
        if successor == item:
          if successor.Fx < item.Fx:
            item.Gx = successor.Gx
            item.Fx = successor.Fx
            item.parent = successor.parent
            inFringe = True
            break
      if inFringe: # то раскрываем дальше
        continue
      # Если имеется узел с таким же состоянием в closed
      inClosed = False
      for c in range(0, len(closed)):
        if successor == closed[c]:
          if successor.Fx < closed[c].Fx:
            closed[c].Gx = successor.Gx
            closed[c].Fx = successor.Fx
            closed[c].parent = successor.parent
            # Перемещаем узел из closed в fringe
            fringeInsert(closed.pop(c), fringe)
            inClosed = True
            # Память закончилась?
            if len(fringe) > FRINGE_MAX_SIZE:
              bad_node = fringe.pop()
              bad_node.parent.Fx = bad_node.Fx
            break
      if inClosed: # то раскрываем дальше
        continue
      # Иначе вставляем узел в fringe
      fringeInsert(successor, fringe)
      # Память закончилась?
      if len(fringe) > FRINGE_MAX_SIZE:
        bad_node = fringe.pop()
        bad_node.parent.Fx = bad_node.Fx
  return

def SMA():
  init_state = [[0,0,0,0], 
                [0,1,1,0],
                [0,1,1,0],
                [0,0,0,0]]
  #init_state = [[0,1,1,1], 
  #              [1,1,1,1],
  #              [0,1,1,0],
  #              [0,1,1,1]]
  #init_state = [[1,1,0,0], 
  #              [1,0,1,0],
  #              [0,1,1,1],
  #              [0,0,1,0]]
  #init_state = [[1,1,1,1], 
  #              [1,1,1,1],
  #              [1,1,1,1],
  #              [1,1,1,1]]
  target_state=[[0,0,0,0], 
                [0,0,0,0],
                [0,0,0,0],
                [0,0,0,0]] 
  closed = [] # множество обработанных узлов
  fringe = [] # периферия (приоритетная очередь)
  fringe.append(Node(init_state, Gx=0, Hx=0, parent=None))
  start_time = time.clock()
  while True:
    if len(fringe) == 0:
      return 'Failure'
    # Извлекаем узел с наименьшей оценкой
    node = fringe.pop(0)
    # Достигли целевого состояния?
    if target_state == node.state:
      PrintPath(node, time.clock() - start_time)
      return 'Success'
    # Желаемая глубина поиска
    #if node.Gx == 5:
    #  continue
    if node not in closed:
      closed.append(node) 
      Expand(node, fringe, closed)
    print(node.Gx)
  return


print(SMA())



#БОЛЕЕ ПРОСТОЙ ВАРИАНТ:
#ПЕРЕДЕЛАТЬ ЛАБ1: ИЗМЕНЯТЬ ВСЕ ЦВЕТА ПО ВЕРТИКАЛИ И ДИАГОНАЛИ ДО КОНЦА
#ЭВРИСТИКА:
#  1) КОЛИЧЕСТО КЛЕТОК ОДНОГО ЦВЕТА ПО ВЕРТИКАЛИ И ГОРИЗОНТАЛИ
#  2) ЕСЛИ НА ТЕКУЩУЮ КЛЕТКУ КЛИКАЛИ УЖЕ В ТЕКУЩЕЙ ВЕТКЕ ДЕРЕВА ВЫШЕ, ТО ВТОРОЙ РАЗ МОЖНО НЕ КЛИКАТЬ (ОТБРАСЫВАЕМ)
#  3) ПРОВЕРИТЬ ГИПОТЕЗУ: ЛЮБОЕ РЕШЕНИЕ В ТАКОЙ ЗАДАЧЕ МОЖЕТ БЫТЬ НАЙДЕНО ЗА 16 ХОДОВ
