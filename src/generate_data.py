import pandas as pd
import numpy as np

def generate_dataset(n=1000):
    np.random.seed(42)

    data = {
        "packet_size": np.random.randint(100, 1500, n),
        "failed_logins": np.random.randint(0, 10, n),
        "request_frequency": np.random.randint(1, 500, n),
    }

    df = pd.DataFrame(data)

    # Create label
    df["Label"] = df.apply(lambda row: 
        1 if (row["failed_logins"] > 5 or row["request_frequency"] > 300) else 0, axis=1
    )

    return df