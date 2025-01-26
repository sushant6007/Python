#1 pd basics
import pandas as pd

data = pd.read_csv("2018_Central_Park_Squirrel_Census_Squirrel_Data.csv")
gray_s_count = len(data[data["Primary Fur Color"] == "Gray"])
black_s_count = len(data[data["Primary Fur Color"] == "Black"])
red_s_count = len(data[data["Primary Fur Color"] == "Cinnamon"])

print(gray_s_count)
print(black_s_count)
print(red_s_count)

data_dict = {"fur_colour":["Gray", "Black", "Cinnamon" ], "count":[gray_s_count, black_s_count, red_s_count]}

df = pd.DataFrame(data_dict)
df.to_csv("squirrel_count.csv")

#2 50 states game
import turtle

screen = turtle.Screen()
screen.title("U.S. States Game")

image = "blank_states_img.gif"
screen.addshape(image)

turtle.shape(image)

state_data = pd.read_csv("50_states.csv")
all_states = state_data.state.to_list()
guessed_state = []


while len(guessed_state) < 50:

    answer_state = screen.textinput(title=f"{len(guessed_state)}/50 States correct", prompt="what's another state name").title()
    
    if answer_state == "Exit":
        missing_states = []
        for state in all_states:
            if state not in guessed_state:
                missing_states.append(state)
        new_data = pd.DataFrame(missing_states)
        new_data.to_csv("States_to_Learn.csv")
        print(missing_states)
        break

    if answer_state in all_states:
        guessed_state.append(answer_state)
        t = turtle.Turtle()
        t.hideturtle()
        t.penup()
        selected_state = state_data[state_data.state == answer_state]
        t.goto(int(selected_state.x), int(selected_state.y))
        t.write(answer_state)
