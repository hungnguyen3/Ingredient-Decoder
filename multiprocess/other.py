import multiprocessing as mp

def print_oh_no(q, name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Oh No! {name}')  # Press Ctrl+F8 to toggle the breakpoint.
    q.put(100)
