import base64

def obfuscate_file(file_path, iterations=3):
    with open(file_path, 'r') as file:
        code = file.read()
    
    for _ in range(iterations):
        code = base64.b64encode(code.encode('utf-8')).decode('utf-8')
        code = f"exec(base64.b64decode('{code}').decode('utf-8'))"
    
    obfuscated_code = f"""
import base64
{code}
"""
    with open(file_path, 'w') as file:
        file.write(obfuscated_code)
    
    print("Obfuscation complete.")

if __name__ == "__main__":
    obfuscate_file(__file__)