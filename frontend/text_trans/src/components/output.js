import React , {useState , useEffect} from "react";

export default function Output ({ output }) {
    return (
        <div>
            <textarea className='text_container' placeholder="这里将出现等会翻译后的文本" readOnly id="output" value={output}/>
        </div>
    )
}