with open('/home/user/KHW_230619/semi_chair/class.yaml', 'w') as f:
    data = {
        'path': '/home/user/KHW_230619/semi_chair/Semi_chair',
        'train':'images/train',
        'val': 'images/val',
        'nc': len(label_dic),
        'names': label_dic,
    }
    yaml.safe_dump(data, f)