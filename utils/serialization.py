def save_file(path, res, file_name, file_type):
    file_name = f'{path}/{file_name}.{file_type}'
    with open(file_name, "wb") as f:
        return f.write(res.content)


def load_config():
    config_path = "/root/zlw/crawler_cnki/config.json"
    import json
    f = open(config_path, 'r', encoding='UTF-8')
    config = json.load(f)
    return config
