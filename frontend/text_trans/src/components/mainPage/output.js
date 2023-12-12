import React, { useState, useEffect } from "react";

export default function Output({ output , accumulatedContent , setAccumulatedContent, haveDone , setHaveDone}) {

    useEffect(() => {
    
        const bootstrapAlert = (message, type) => {
            const alertPlaceholder = document.getElementById('liveAlertPlaceholder');
            if (!alertPlaceholder) {
                console.error('Alert placeholder not found');
                return;
            }
        
            // Check if an alert with the same message is already displayed
            const existingAlerts = Array.from(alertPlaceholder.children);
            const alreadyDisplayed = existingAlerts.some(alert => alert.textContent.includes(message));
            if (alreadyDisplayed) {
                // If an alert with the same message is found, do not create a new one
                return;
            }
        
            // If no existing alert with the same message, create a new alert
            const wrapper = document.createElement('div');
            wrapper.innerHTML = [
                `<div class="alert alert-${type} alert-dismissible fade show" role="alert" style="max-width: 50%; margin-left: auto; margin-right: auto;">`,
                `   <strong>${message}</strong>`,
                '   <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>',
                '</div>'
            ].join('');
        
            alertPlaceholder.append(wrapper);
        
            // Remove the alert with fade-out effect after 3 seconds
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
                    const contextData = JSON.parse(outputData.context);
                    if (contextData.message === true) {
                        // 累积 content
                        setAccumulatedContent(prevContent => prevContent + contextData.content);
                        setHaveDone(outputData.have_done);
                    }
                    if (contextData.message === false) {
                        bootstrapAlert(contextData.err, 'danger');  // 使用 Bootstrap alert
                        setHaveDone(outputData.have_done);
                    }
                    if (contextData.info) {
                        bootstrapAlert(contextData.info, 'warning');  // 使用 Bootstrap alert
                    }
                    if (outputData.message == "OK"){
                        console.log("OK")
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
                placeholder="这里将出现等会翻译后的文本" 
                readOnly 
                id="output" 
                value={accumulatedContent}
            />
        </div>
    )
}
