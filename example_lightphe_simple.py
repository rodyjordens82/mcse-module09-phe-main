import pandas as pd
from lightphe import LightPHE

# Gegevens inlezen
data_path = 'Generated_Questionnaire_Responses.csv'
df = pd.read_csv(data_path)

# Functies voor sleutelpaar en encryptie
def generate_keypair():
    cs = LightPHE(algorithm_name="Paillier")
    return cs

def encrypt_data(cs, data):
    return [cs.encrypt(x) for x in data]

def decrypt_data(cs, encrypted_data):
    return [cs.decrypt(x) for x in encrypted_data]

def safe_int_conversion(value, default=0):
    try:
        return int(value)
    except ValueError:
        return default

# Sleutelpaar genereren
cryptosystem = generate_keypair()

# Prepare a DataFrame to store the results
output_df = pd.DataFrame(columns=['Column', 'Original Data', 'Encrypted Data', 'Decrypted Sum'])

# Iterate over each column, encrypt, and demonstrate calculations
for column in df.columns:
    # Encrypt the column data
    column_data = df[column].tolist()
    column_data_numeric = [safe_int_conversion(x) for x in column_data]
    encrypted_data = encrypt_data(cryptosystem, column_data_numeric)

    # Perform homomorphic addition on the encrypted data
    encrypted_sum = encrypted_data[0]
    for enc in encrypted_data[1:]:
        encrypted_sum = encrypted_sum + enc

    # Decrypt the result
    decrypted_sum = cryptosystem.decrypt(encrypted_sum)

    # Store the results in a temporary DataFrame
    temp_df = pd.DataFrame({
        'Column': [column],
        'Original Data': [column_data],
        'Encrypted Data': [[str(e) for e in encrypted_data]],  # Convert encrypted data to strings for storage
        'Decrypted Sum': [decrypted_sum]
    })

    # Concatenate the temporary DataFrame to the output DataFrame
    output_df = pd.concat([output_df, temp_df], ignore_index=True)

# Save the output to a CSV file
output_file_path = 'C:/Users/rodyj/Documents/developer/lightphe/encrypted_results.csv'
output_df.to_csv(output_file_path, index=False)

print(f"Results saved to {output_file_path}")
