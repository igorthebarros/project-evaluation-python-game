# 🕹️ 2D Platformer Game - PyGame Zero

A simple 2D platformer built with [PyGame Zero](https://pygame-zero.readthedocs.io/en/stable/), featuring:
- Character selection screen  
- Side-scrolling scenario  
- Running animations  
- Jumping mechanics  
- Enemy spawning and animation  


# Developer's comments

Hi! This is my first attempt creating a game using PyGame Zero.


1. The character has three states: stand, run1, and run2. The running animation switches between run1 and run2.

2. Enemies also have animated sprites (enemy_run1, enemy_run2), which alternate as they move.

3. Background scrolling is achieved by looping the background image as the player moves.

4. All game state and transition logic (menu, level 1, etc.) is handled using simple state variables like game_state.

5. The jump mechanic is implemented using a velocity/gravity simulation.

6. Collision and enemy interaction logic can be extended in future updates.

7. Sound and background music can be added using sounds and music objects from PyGame Zero.

---

## 🎮 How to Run the Game

### Prerequisites
Make sure you have **Python 3.8+** and **pgzero** installed.

Install PyGame Zero using pip:
```bash
pip install pgzero

---

#### Once the dependencies are installed, run the main file:

pgzrun intro.py