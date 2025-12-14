# P vs Chess
Simple game we made for fun. It features a Plants Vs Zombie Heroes' style of gameplay and it requires 2 players. It is a strategic card battler inspired by the chess pieces and built with the Pyxel retro game engine.

![Demo](/screenshots/Chess2.png)

## How to play
It's a turn-based stategy game where two players face off using cards representing chess pieces. Each player starts with:
- 20 HP(King health)
- A deck of 15 cards (8 Pawns, 2 Bishops, 2 Knights, 2 Rooks, 1 Queen)
- **8 Money** per round to spend on cards

Players alternate placing cards from their hand onto their side of the 5-slot board. The round will continue when both payers can no longer play cards.
In the **Battle Phase** all cards attack simultaneously based on their type:
- Cards deal damage according to their attack patterns
- Cards lose HP when attacked
- Excee damage hits the KING
- Cards with **0 hp** are destroyed

## Card Types
- **Pawn**: Attacks directly ahead, has 2HP, deals 1HP of damage and costs 1.
- **Bishop**: Retrigger (triggers adjacent allies' attacks, takes 1 self-damage), has 3HP and costs 3.
- **Knight**: L-Shape (attacks both diagonal positions), has 3HP, deals 4HP of damage and costs 4.
- **Rook**: Attacks directly ahead, has 5HP, deals 4HP of damage and costs 4.
- **Queen**: Area(splits damage across center and adjacent positions), deals 6HP of damage and costs 8.

## Run

 

Install Pyxel:

```bash

pip install pyxel

```

 

Run the program:

```bash

python main.py

```
