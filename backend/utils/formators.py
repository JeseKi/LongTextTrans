def convert_to_list(input_str: str) -> list:
    if input_str:
        # 分割字符串并去除空白字符
        return [item.strip() for item in input_str.split(',')]
    else:
        # 如果输入为空，则返回空列表
        return []