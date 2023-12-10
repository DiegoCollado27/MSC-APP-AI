import argparse
import numpy as np
import pandas as pd
import sys

def predict (input):
    """
    Generates the prediction.
    In this case, it generates a random price.

    @param input: the input dataframe.
    @return a dataframe with two columns: ID and price.
    """
    np.random.seed(1)
    output = pd.DataFrame()
    output['Id'] = input['Id']
    output['Precio'] = np.random.randint(100000, 500000, size=len(input))
    return output


if __name__ == '__main__':

    # Creates a parser to receive the input argument.
    parser = argparse.ArgumentParser()
    parser.add_argument('file', help='Path to the data file.')
    args = parser.parse_args()

    # Read the argument and load the data.
    try:
        data = pd.read_csv(args.file)
    except:
        print("Error: the input file does not have a valid format.", file=sys.stderr)
        exit(1)

    # Computes the predictions.
    # NOTE: this stage is simulated.
    output = predict(data)

    # Writes the output.
    print('Id,Precio')
    for r in output.itertuples():
        print(f'{r.Id},{r.Precio}')
