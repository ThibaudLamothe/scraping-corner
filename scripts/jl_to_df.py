import json
import pandas as pd


# Function to read jl file
def read_jl_file(file_name):
    values = []
    with open(file_name, 'rb') as f:
        line = '---'
        while len(line) > 1:
            line = f.readline()
            values.append(line)
    values = values[:-1]
    values = [json.loads(i) for i in values]
    df = pd.DataFrame(values)
    return df


if __name__ == "__main__":
    # Reading file
    my_jl_path = 'scrapped_data/actu_x_0.jl'
    df_jl = read_jl_file(my_jl_path)
    print(df_jl.shape)
