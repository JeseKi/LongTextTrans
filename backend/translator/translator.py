from typing import List ,Callable
import json

from utils.logger import Logger

logger = Logger()

class Translator():
    def __init__(self) -> None:
        pass

    async def elementsTranslate(
                          self,
                          text: str, 
                          source_lang: str,
                          target_lang: str,
                          split_callback: Callable[[str , int], List[str]], # 多数翻译API都限制单次请求的文本长度
                          translate_callback: Callable[..., str],# 翻译API,输入参数不限,但是需要返回字符串
                          isStream: bool = False, # 翻译API返回的内容是否是流式
                          max_length: int = 5500,
                          *args, **kwargs
                        ):
        """
        将字符串进行翻译,并以流式返回结果
        参数:
        - text: 需要进行翻译的字符串
        - source_lang: 源语言
        - target_lang: 目标语言
        - split_callback: 用于分割字符串的回调函数,需传入源文本和分割的每一段的最大长度,返回一个数组
        - translate_callback: 用于翻译字符串的回调函数
        - isStream: 翻译API返回的内容是否是流式
        - max_lenth: 每一段所分割的长度
        - *args, **kwargs: 传递给 translate_callback 的额外参数
        :return: 流式结果
        """
        # i = 0
        split_texts = await split_callback(text, max_length)
        for element in split_texts:
            # 异步迭代 _openai_translate 的结果并逐个产生
            if isStream:
                async for translation in translate_callback(element, source_lang, target_lang, *args, **kwargs):
                    yield json.dumps(translation)
            else :
                translation = await translate_callback(element, source_lang, target_lang, *args, **kwargs)
                yield json.dumps(translation)
            # 日志
            # i += 1
            # logger.event_time_log(f"向服务端发送请求第{i}次",False)
            # time.sleep(1)

    async def splitText(self,text: str, maxlenth: int = 5500) -> List[str]:
        """
        分割字符串
        参数:
        - text: 字符串
        :return: 分割后的每个元素均符合长度的字符串数组
        """
        # 计算文本长度
        text_length = len(text)
        text_segments = []
        # 根据文本长度计算需要分成几部分，使用天花板除法确保分割完全
        num_partitions = -(-text_length // maxlenth)
        
        # 如果文本已经足够短，不需要分割，直接返回包含原文本的列表
        if num_partitions == 1:
            return [text]
        
        last_split_point = 0  # 上一次分割点的索引
        for i in range(1, num_partitions):
            # 计算每一部分的理论分割长度
            partition_length = i * text_length // num_partitions
            # 在分割点前找最近的句号，保证句子完整性
            period_index = text.rfind('.', last_split_point, partition_length)
            
            # 如果找不到句号，就在计算出的分割点长度处直接分割
            if period_index == -1:
                split_point = partition_length
            else:
                # 如果找到了句号，分割点后移一位，包含句号
                split_point = period_index + 1
            
            # 打印分割点信息，用于调试
            start = max(0, split_point - 10)  # 确保开始不会低于文本开头
            end = min(len(text), split_point + 10)  # 确保结束不会超过文本结尾
            print(f"Splitting at position {split_point}: {text[start:split_point]}|{text[split_point:end]}...")
            
            # 将当前分割的文本段添加到段列表中
            text_segments.append(text[last_split_point:split_point])
            last_split_point = split_point  # 更新上一次分割点的索引
        
        # 将最后剩余的文本作为最后一个段落添加到列表中
        text_segments.append(text[last_split_point:])
        
        return text_segments  # 返回分割后的文本段列表