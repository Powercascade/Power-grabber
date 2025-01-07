import os
def self_destruct():
    try:
        script_path = os.path.abspath(__file__)
        os.remove(script_path)
    except Exception as e:
        pass
if __name__ == "__main__":
    self_destruct()
