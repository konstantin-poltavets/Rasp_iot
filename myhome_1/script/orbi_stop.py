if __name__ == "__main__": # Local Run
    import orbitrack
else: # Module Run, When going production - delete if/else
    from . import orbitrack

import os
def main():
    orbitrack.main().loop_stop()
    print("STOP MQTT Orbitrack")
#os.system('taskkill /f /im 7132 /T')