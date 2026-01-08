import import_cycle_b

def a():
    return import_cycle_b.b()
