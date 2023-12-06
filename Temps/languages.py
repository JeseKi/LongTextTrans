languages_data = """
zh（简体中文）：en（英语）、ja（日语）、ko（韩语）、fr（法语）、es（西班牙语）、it（意大利语）、de（德语）、tr（土耳其语）、ru（俄语）、pt（葡萄牙语）、vi（越南语）、id（印尼语）、th（泰语）、ms（马来语）
zh-TW（繁体中文）：en（英语）、ja（日语）、ko（韩语）、fr（法语）、es（西班牙语）、it（意大利语）、de（德语）、tr（土耳其语）、ru（俄语）、pt（葡萄牙语）、vi（越南语）、id（印尼语）、th（泰语）、ms（马来语）
en（英语）：zh（中文）、ja（日语）、ko（韩语）、fr（法语）、es（西班牙语）、it（意大利语）、de（德语）、tr（土耳其语）、ru（俄语）、pt（葡萄牙语）、vi（越南语）、id（印尼语）、th（泰语）、ms（马来语）、ar（阿拉伯语）、hi（印地语）
ja（日语）：zh（中文）、en（英语）、ko（韩语）
ko（韩语）：zh（中文）、en（英语）、ja（日语）
fr（法语）：zh（中文）、en（英语）、es（西班牙语）、it（意大利语）、de（德语）、tr（土耳其语）、ru（俄语）、pt（葡萄牙语）
es（西班牙语）：zh（中文）、en（英语）、fr（法语）、it（意大利语）、de（德语）、tr（土耳其语）、ru（俄语）、pt（葡萄牙语）
it（意大利语）：zh（中文）、en（英语）、fr（法语）、es（西班牙语）、de（德语）、tr（土耳其语）、ru（俄语）、pt（葡萄牙语）
de（德语）：zh（中文）、en（英语）、fr（法语）、es（西班牙语）、it（意大利语）、tr（土耳其语）、ru（俄语）、pt（葡萄牙语）
tr（土耳其语）：zh（中文）、en（英语）、fr（法语）、es（西班牙语）、it（意大利语）、de（德语）、ru（俄语）、pt（葡萄牙语）
ru（俄语）：zh（中文）、en（英语）、fr（法语）、es（西班牙语）、it（意大利语）、de（德语）、tr（土耳其语）、pt（葡萄牙语）
pt（葡萄牙语）：zh（中文）、en（英语）、fr（法语）、es（西班牙语）、it（意大利语）、de（德语）、tr（土耳其语）、ru（俄语）
vi（越南语）：zh（中文）、en（英语）
id（印尼语）：zh（中文）、en（英语）
th（泰语）：zh（中文）、en（英语）
ms（马来语）：zh（中文）、en（英语）
ar（阿拉伯语）：en（英语）
hi（印地语）：en（英语）
"""

import re
import json

# 正则表达式匹配格式为 lang_code（local_name）
lang_pattern = re.compile(r'(\w+|\w+-\w+)\（([^）]+)）')

# 假定languages_data是一个包含所有语言选项的长字符串
# languages_data = "zh（简体中文）：en（英语）、ja（日语）、ko（韩语）、..."

# 初始化一个空字典来存储语言映射
language_dict = {}

# 分割每一行并解析语言对
for line in languages_data.strip().split('\n'):
    # 使用正则表达式找到源语言
    source_match = lang_pattern.match(line)
    if source_match:
        source_code, source_name = source_match.groups()
        # 从行中找到所有目标语言
        targets = lang_pattern.findall(line)
        # 创建一个映射，其中每个目标语言都是一个字典，包含代码和名称
        language_dict[source_code] = [{'code': code, 'name': name} for code, name in targets]

# 将语言字典转换成JSON格式
languages_json = json.dumps(language_dict, ensure_ascii=False, indent=2)

# 打印或保存JSON数据
print(languages_json)
