with open('/home/user/KHW_230619/kh_2/class.yaml', 'w') as f:
    data = {
        'path': '/home/user/KHW_230619/kh_2/1500_bicycle_bed',
        'train':'images/train',
        'val': 'images/val',
        'nc': len(label_dic),
        'names': label_dic,
    }
    yaml.safe_dump(data, f)