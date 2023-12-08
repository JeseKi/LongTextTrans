import React, { useState, useEffect } from "react";

export default function Output({ output , accumulatedContent , setAccumulatedContent}) {

    useEffect(() => {
        // 使用换行符分割字符串
        const parts = output.split('\n');
        parts.forEach(part => {
            try {
                if (part.trim() !== '') {
                    const outputData = JSON.parse(part);
                    if (outputData.message === true) {
                        // 累积 content
                        setAccumulatedContent(prevContent => prevContent + outputData.content);
                    }
                }
            } catch (error) {
                // 错误处理
            }
        });
    }, [output]);
    

    return (
        <div>
            <textarea 
                className='text_container' 
                placeholder="这里将出现等会翻译后的文本" 
                readOnly 
                id="output" 
                value={accumulatedContent}
            />
        </div>
    )
}
