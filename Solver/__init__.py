import datetime

from jinja2 import Environment, FileSystemLoader

#https://github.com/Wiston999/python-rubik
from rubik_solver import utils

from rubiks_cube_image import GetRaw

from Solver import Rotate
from Solver import RCR3D
from Solver import Patterns


class Solver(object):

 def __init__(self, Log=False, Colored=False, Size=300):
  self.Log = Log
  self.Colored = Colored
  self.Size = Size
  self.SetCube()


 def SetCube(self, Cube=None):
  if Cube is None:
   self.Cube = list('YYYYYYYYYBBBBBBBBBRRRRRRRRRGGGGGGGGGOOOOOOOOOWWWWWWWWW')
  elif isinstance(Cube, (str, tuple)) and len(Cube) == 54:
   self.Cube = list(Cube)
  elif isinstance(Cube, list) and len(Cube) == 54:
   self.Cube = Cube
  else:
   self.Cube = None
  self.Default = self.Cube.copy()


 def Shuffle(self):
  return list(Rotate.Shuffle())


 def Scramble(self, Commands):
  if self.Log:
   print("Default Cube:")
   self.Print()
   print()
   print(f"Scramble ({len(Commands)}): {Commands}")
   print()
  return self.Change(Commands)


 #https://egorovegor.ru/python-color-printing/
 def GetColor(self, Name):
  Colors = {
   "O": f"\033[0m\033[48;5;208m  \033[0m",
   "B": f"\033[0m\033[48;5;021m  \033[0m",
   "R": f"\033[0m\033[48;5;196m  \033[0m",
   "W": f"\033[0m\033[48;5;254m  \033[0m",
   "Y": f"\033[0m\033[48;5;227m  \033[0m",
   "G": f"\033[0m\033[48;5;046m  \033[0m",
  }
  return Colors[Name] if self.Colored else Name


 def Print(self):
  Size = 3
  Result = []
  SquareIndex = 0
  Indent = Size * " " * (2 if self.Colored else 1)
  Rows = Size * 3
  for Row in range(1, Rows + 1):
   Line = []
   if Row <= Size:
    Line.append(f"{Indent}")
    for Col in range(1, Size + 1):
     Color = self.GetColor(self.Cube[SquareIndex])
     Line.append(f"{Color}")
     SquareIndex += 1
   elif Row > Rows - Size:
    Line.append(f"{Indent}")
    for Col in range(1, Size + 1):
     Color = self.GetColor(self.Cube[SquareIndex])
     Line.append(f"{Color}")
     SquareIndex += 1
   else:
    InitSquareIndex = SquareIndex
    LastCol = Size * 4
    for Col in range(1, LastCol + 1):
     Color = self.GetColor(self.Cube[SquareIndex])
     Line.append(f"{Color}")
     if Col == LastCol:
      SquareIndex += 1
     elif Col % Size == 0:
      SquareIndex += (Size * Size) - Size + 1
     else:
      SquareIndex += 1
    if Row % Size:
     SquareIndex = InitSquareIndex + Size
   Result.append("".join(Line))
  print("\n".join(Result))


 def Change(self, Commands):
  Result = []
  for i, Command in enumerate(Commands):
   if self.Log:
    print(f"Command {i + 1}: {Command}")
   Steps = RCR3D.Get(Command)
   Result.append( (Command, Steps, self.Cube, GetRaw(self.Cube, self.Size, Command=Command)) )
   for j, Step in enumerate(Steps):
    self.Cube = Rotate.Get(self.Cube, Step)
    if self.Log:
     if len(Steps) > 1:
       print(f"  RCR3D {j + 1}: {Step}")
     self.Print()
   if self.Log:
    print()
  return Result


 def GetOrientation(self):
  Result = self.Cube.copy()
  Y = Rotate.GetOrientationY(Result)
  for Command in Y:
   Result = Rotate.Get(Result, Command)
  R = Rotate.GetOrientationR(Result)
  return Y + R


 def GetSolve(self, Name, Commands):
  if self.Log and Commands:
   print(f"{Name} ({len(Commands)}): {Commands}")
  Result = self.Change(Commands)
  if self.Log:
   print()
  return Result


 def Solve(self, Method='Kociemba', ID='Default'):
  self.Method = Method
  self.Pattern = ID
  if self.Log:
   print("Cube:")
   self.Print()
   print()
  # ориентировать кубик
  Preparation = self.GetSolve("Orientation", self.GetOrientation())
  # сборка кубика для RCR3D
  Solve = self.GetSolve(f"Method {Method}", [str(Item) for Item in utils.solve("".join(self.Cube), Method)])
  # сборка шаблона
  Pattern = self.GetSolve(f"Pattern {ID}", Patterns.Get(ID))
  # ориентировать кубик
  Orientation = self.GetSolve("Orientation", self.GetOrientation())
  #
  #if self.Log:
  # print(f"Solve ({len(Preparation + Solve + Pattern + Orientation)}): {Preparation + Solve + Pattern + Orientation}")
  return Preparation, Solve, Pattern, Orientation


 def SaveReport(self, FileName, Scramble=None, Preparation=None, Solve=None, Pattern=None, Orientation=None):
  Env = Environment(loader=FileSystemLoader(__name__))
  Template = Env.get_template("Report.html")
  HTML = Template.render(DateTime=datetime.datetime.now(), InitCube=GetRaw(self.Default, self.Size), Solve=[("Scramble", Scramble), ("Preparation", Preparation), (f"Solve {self.Method}", Solve), (f"Pattern {self.Pattern}", Pattern), ("Orientation", Orientation)], FinalCube=GetRaw(self.Cube, self.Size))
  with open(FileName, "w") as File:
   File.write(HTML)

