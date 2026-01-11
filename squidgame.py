from pitop import Button, LED
from time import sleep, time
import random
import threading

btn1 = Button("D0")  # Connect Button 1 to digital port D0
btn2 = Button("D1")  # Connect Button 2 to digital port D1

red_led = LED("D2")
green_led = LED("D3")
yellow_led = LED("D4")

cntr1 = 0
cntr2 = 0
goal = 100
current_color = "green"
game_running = True

def set_light(color):
    global current_color
    current_color = color
    red_led.off()
    green_led.off()
    yellow_led.off()
    
    if color == "red":
        red_led.on()
    elif color == "green":
        green_led.on()
    elif color == "yellow":
        yellow_led.on()

def rng_cycle():
    global game_running
    while game_running:
        sleep(3)
        val = random.random()
        if val < 0.4:
            set_light("red")
        elif val < 0.9:
            set_light("green")
        else:
            set_light("yellow")

def handle_press(player_num):
    global cntr1, cntr2
    change = 0
    
    if current_color == "red":
        change = -5
    elif current_color == "yellow":
        change = 1
    elif current_color == "green":
        change = 2
        
    if player_num == 1:
        cntr1 += change
        print(f"Player 1: {cntr1}")
    else:
        cntr2 += change
        print(f"Player 2: {cntr2}")

screen.display_text("Game Starting! Light is GREEN.")
set_light("green")

timer_thread = threading.Thread(target=rng_cycle, daemon=True)
timer_thread.start()

btn1.when_pressed = lambda: handle_press(1)
btn2.when_pressed = lambda: handle_press(2)

try:
    while cntr1 < goal and cntr2 < goal:
        sleep(0.1) # Keep the main thread alive
    
    game_running = False
    winner = "Player 1" if cntr1 >= goal else "Player 2"
    screen.display_text(f"GAME OVER! {winner} wins!")
    red_led.off()
    green_led.off()
    yellow_led.off()

except KeyboardInterrupt:
    game_running = False


