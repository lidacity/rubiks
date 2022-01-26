#!env/bin/python

import sys

from Solver import Solver

Solver1 = Solver(Log=True, Colored=True)
#Solver1 = Solver()
#Solver1.SetCube("OOROYRORRYWWYGWYYWBGGBOGBBGYWWYBWYYWGBBGRBGGBRRORWOROO")
#Solver1.SetCube("OGRYOYYOOBBOOWOGWYBBGWBGRBRWRBWYBGGOWRWWGYGYYBRWRRORGY")
#Solver1.SetCube("OBBOYYWWRWWROORGOGBRYBBGWRYBGORRYBGYWWGBGYOBYRYOGWWROG")

Shuffle = Solver1.Shuffle()
Scramble = Solver1.Scramble(Shuffle)

#Preparation, Solve, Pattern, Orientation = Solver1.Solve(Method="Beginner")
#Preparation, Solve, Pattern, Orientation = Solver1.Solve(Method="CFOP")
Preparation, Solve, Pattern, Orientation = Solver1.Solve(ID="Don't cross line") #Kociemba

Solver1.SaveReport("solve.html", Scramble=Scramble, Preparation=Preparation, Solve=Solve, Pattern=Pattern, Orientation=Orientation)
