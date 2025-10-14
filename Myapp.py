import argparse

def get_r_data():
    # 创建解析器
    parser = argparse.ArgumentParser(description='处理 -r 参数')
    parser.add_argument('-r', type=int, help='要读取的数据')

    # 解析参数
    args = parser.parse_args()

    if args.read:
        return args.read
    else:
        print("未提供 -r 参数")

def get_n_data():
    # 创建解析器
    parser = argparse.ArgumentParser(description='处理 -r 参数')
    parser.add_argument('-n', type=int, help='要读取的数据')

    # 解析参数
    args = parser.parse_args()

    if args.read:
        return args.read
    else:
        print("未提供 -n 参数")
