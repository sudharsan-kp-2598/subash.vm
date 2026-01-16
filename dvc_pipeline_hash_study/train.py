with open("cleaned_data.csv") as f:
    lines = f.readlines()

lines.append("MODEL_READY - folks\n")

with open("model.txt", "w") as f:
    f.writelines(lines)
 