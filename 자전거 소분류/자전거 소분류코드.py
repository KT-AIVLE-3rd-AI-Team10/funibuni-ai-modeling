with open('/home/user/KHW_230619/semi_bicycle/class.yaml', 'w') as f:
    data = {
        'path': '/home/user/KHW_230619/semi_bicycle/semi_bicycle',
        'train':'images/train',
        'val': 'images/val',
        'nc': len(label_dic),
        'names': label_dic,
    }
    yaml.safe_dump(data, f)