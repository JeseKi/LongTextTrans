import React, { useState, useEffect } from "react";

export default function Output({ output , accumulatedContent , setAccumulatedContent, haveDone , setHaveDone , setFilePath , file}) {

    useEffect(() => {
    
        const bootstrapAlert = (message, type) => {
            const alertPlaceholder = document.getElementById('liveAlertPlaceholder');
            if (!alertPlaceholder) {
                console.error('Alert placeholder not found');
                return;
            }
        
            // 假如弹出的消息相同则自动屏蔽
            const existingAlerts = Array.from(alertPlaceholder.children);
            const alreadyDisplayed = existingAlerts.some(alert => alert.textContent.includes(message));
            if (alreadyDisplayed) {
                // If an alert with the same message is found, do not create a new one
                return;
            }
        
            // 如果不存在相同的消息,就进行弹出
            const wrapper = document.createElement('div');
            wrapper.innerHTML = [
                `<div class="alert alert-${type} alert-dismissible fade show" role="alert" style="max-width: 50%; margin-left: auto; margin-right: auto;">`,
                `   <strong>${message}</strong>`,
                '   <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>',
                '</div>'
            ].join('');
        
            alertPlaceholder.append(wrapper);
        
            // 10s后消失
            setTimeout(() => {
                if (wrapper.firstChild) {
                    wrapper.firstChild.classList.add('fade-out');
                    setTimeout(() => {
                        wrapper.firstChild.remove();
                    }, 500); // Duration should match CSS animation duration
                }
            }, 10000); // Time before starting fade-out
        }
    
        // 使用换行符分割字符串
        const parts = output.split('\n');
        parts.forEach(part => {
            try {
                if (part.trim() !== '') {
                    const outputData = JSON.parse(part);
                    console.log("part:",part)
                    if (outputData.file_path) {
                        setFilePath(outputData.file_path);
                        console.log("文件路径:",outputData.file_path)
                    };
                    try{
                        const contextData = JSON.parse(outputData.context);
                        if (contextData.message === true) {
                            // 累积 content
                            setAccumulatedContent(prevContent => prevContent + contextData.content);
                            setHaveDone(outputData.have_done);
                        };
                        if (contextData.message === false) {
                            bootstrapAlert(contextData.err, 'danger');  // 使用 Bootstrap alert
                            setHaveDone(outputData.have_done);
                        };
                        if (contextData.info) {
                            bootstrapAlert(contextData.info, 'warning');  // 使用 Bootstrap alert
                        };
                    }
                    catch{
                        
                    }
                }
            } catch (error) {
                console.error("Error in processing output:", error);
            }
        });
    }, [output]);
    
    

    return (
        <div>
            <div id="liveAlertPlaceholder"></div>
            <div>
                {haveDone}%
            </div>
            <textarea 
                className='text_container' 
                style={{display : file ? "none" : ""}}
                placeholder="这里将出现等会翻译后的文本" 
                readOnly 
                id="output" 
                value={accumulatedContent}
            />
        </div>
    )
}
