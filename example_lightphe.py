import pandas as pd
from lightphe import LightPHE

# Gegevens inlezen
data_path = '../lightphe/Generated_Questionnaire_Responses.csv'
df = pd.read_csv(data_path)

# Sleutelpaar genereren
def generate_keypair():
    cs = LightPHE(algorithm_name="Paillier")
    return cs

def encrypt_data(cs, data):
    return [cs.encrypt(x) for x in data]

cryptosystem = generate_keypair()

# Versleutel alle kolommen
encrypted_columns = {}
for column in df.columns:
    column_data = df[column].apply(lambda x: int(x) if str(x).isdigit() else 0)
    encrypted_columns[column] = encrypt_data(cryptosystem, column_data)

# Geëncrypteerde gegevens opslaan in een CSV-bestand
encrypted_df = pd.DataFrame(encrypted_columns)
encrypted_df.to_csv('../lightphe/encrypted_data.csv', index=False)

import requests

url = 'https://serviceprovider.com/upload_encrypted_data'
files = {'file': open('../lightphe/encrypted_data.csv', 'rb')}
response = requests.post(url, files=files, verify=True)

if response.status_code == 200:
    print("Data successfully sent to service provider.")
else:
    print("Failed to send data.")

# Aanname: De serviceprovider voert deze code uit

def homomorphic_addition(cs, encrypted_data):
    encrypted_sum = encrypted_data[0]
    for enc in encrypted_data[1:]:
        encrypted_sum = encrypted_sum + enc
    return encrypted_sum

# Voorbeeld van een berekening op versleutelde data
encrypted_df = pd.read_csv('C:/path_to_received/encrypted_data.csv')

# Homomorfe optelling uitvoeren
cs = LightPHE(algorithm_name="Paillier")
results = {}
for column in encrypted_df.columns:
    encrypted_data = [cs.ciphertext_from_bytes(bytes.fromhex(x)) for x in encrypted_df[column]]
    encrypted_sum = homomorphic_addition(cs, encrypted_data)
    results[column] = encrypted_sum

# Resultaten opslaan in een CSV-bestand
results_df = pd.DataFrame.from_dict(results, orient='index', columns=['Encrypted Sum'])
results_df.to_csv('C:/path_to_send/encrypted_results.csv')

url = 'https://zorgaanbieder.com/upload_encrypted_results'
files = {'file': open('C:/path_to_send/encrypted_results.csv', 'rb')}
response = requests.post(url, files=files, verify=True)

if response.status_code == 200:
    print("Encrypted results successfully sent back to healthcare provider.")
else:
    print("Failed to send encrypted results.")

# Resultaten inlezen
results_df = pd.read_csv('../lightphe/encrypted_results.csv')

# Ontsleutelen van de gegevens
def decrypt_data(cs, encrypted_data):
    return [cs.decrypt(x) for x in encrypted_data]

decrypted_results = {}
for column in results_df.index:
    encrypted_sum = cs.ciphertext_from_bytes(bytes.fromhex(results_df.loc[column, 'Encrypted Sum']))
    decrypted_sum = cryptosystem.decrypt(encrypted_sum)
    decrypted_results[column] = decrypted_sum

# Resultaten weergeven
for column, decrypted_sum in decrypted_results.items():
    print(f"Column: {column}, Decrypted Sum: {decrypted_sum}")
