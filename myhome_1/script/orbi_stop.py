if __name__ == "__main__": # Local Run
    import orbitrack
else: # Module Run, When going production - delete if/else
    from . import orbitrack

orbitrack.main().loop_stop()