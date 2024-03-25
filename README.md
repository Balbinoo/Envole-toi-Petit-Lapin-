# Envole toi Petit Lapin !

This is a simple flappy bird type game implemented in Python using Pygame library. The game is controlled by a sensor connected to a STM32 NUCLEO-32 development board.

### How to Play
The objective of the game is to guide the flying rabbit through gaps between pipes.
Press the spacebar to start the game and make the rabbit fly.
The rabbit's position is controlled by a sensor connected to a STM32 NUCLEO-32 development board.
As the game progresses, the pipes will move faster, making it more challenging to navigate through the gaps.
The game ends if the rabbit collides with a pipe.
Press spacebar to restart the game after it's over.

### Requirements
- Python 3.x
- Pygame library
- STM32 NUCLEO-32 development board
- Serial connection to the computer (Adjust the COM port in the code)

### Installation
- Clone the repository:
- $ git clone https://github.com/Balbinoo/Envole-toi-Petit-Lapin-.git

### Install the required dependencies:
- $ pip install pygame
- $ pip install pyserial

- Connect the sensor to the STM32 NUCLEO-32 development board and ensure it is properly connected to the computer via serial port.

### Run the game:
- $ python3 jeuControleCapteur.py

### Images of the game:

![turbo_lapin](https://github.com/mia-ajuda/Frontend/assets/54644626/adaac168-e27f-4c90-9cde-30a98d33fb4d)
![scenario2](https://github.com/mia-ajuda/Frontend/assets/54644626/6706ac6e-6d49-4d81-98b5-34a91119beec)
![jeu](https://github.com/mia-ajuda/Frontend/assets/54644626/34df5250-dc98-46f9-9068-cdcf07fa6a4a)
![WhatsApp Image 2024-03-25 at 11 27 46](https://github.com/mia-ajuda/Frontend/assets/54644626/42bb6c44-4f0f-4dbb-a592-3b289a715298)



