import NMS_Server
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) # Add the project root directory to sys.path

if __name__ == "__main__":
    NMS_Server.main()