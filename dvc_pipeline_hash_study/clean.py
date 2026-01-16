with open("raw_data.csv") as f:
    lines = f.readlines()

lines = [line.strip().upper() + "\n" for line in lines]

with open("cleaned_data.csv", "w") as f:
    f.writelines(lines)
    f.write("Newline")