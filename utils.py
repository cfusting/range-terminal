def get_experiment_class_and_name(cls):
    name = cls.__name__
    print('Experiment: ' + name)
    return cls, name
