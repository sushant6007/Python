import pandas

data = pandas.read_csv("2018_Central_Park_Squirrel_Census_Squirrel_Data.csv")
gray_s_count = len(data[data["Primary Fur Color"] == "Gray"])
black_s_count = len(data[data["Primary Fur Color"] == "Black"])
red_s_count = len(data[data["Primary Fur Color"] == "Cinnamon"])

print(gray_s_count)
print(black_s_count)
print(red_s_count)

data_dict = {"fur_colour":["Gray", "Black", "Cinnamon" ], "count":[gray_s_count, black_s_count, red_s_count]}

df = pandas.DataFrame(data_dict)
df.to_csv("squirrel_count.csv")

