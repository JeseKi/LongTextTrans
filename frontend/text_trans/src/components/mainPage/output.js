import React, { useState, useEffect } from "react";

export default function Output({ output , accumulatedContent , setAccumulatedContent, haveDone , setHaveDone}) {


    useEffect(() => {
        // 使用换行符分割字符串
        const parts = output.split('\n');
        parts.forEach(part => {
            try {
                if (part.trim() !== '') {
                    const outputData = JSON.parse(part);
                    const contextData = JSON.parse(outputData.context)
                    if (contextData.message === true) {
                        // 累积 content
                        setAccumulatedContent(prevContent => prevContent + contextData.content);
                        setHaveDone(outputData.have_done)
                    }
                    if (contextData.message === false) {
                        alert(contextData.err)
                    }
                }
            } catch (error) {
                // 错误
            }
        });
    }, [output]);
    

    return (
        <div>
            <div>
                {haveDone}%
            </div>
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
