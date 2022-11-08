import yaml


def config_read():
    with open('Data\\config.yml') as yml:
        config = yaml.safe_load(yml)
        yml.close()
    return config
