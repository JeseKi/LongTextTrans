import React ,{useEffect , useState} from "react"
import "./transbtn.css"
import languageData from './languages.json'

import { Dropdown, DropdownButton } from 'react-bootstrap';

export default function TransBtn ( {setOutput , service} ) {
    const [sourceLang , setSourceLang] = useState("en");
    const [targetLang , setTargetLang] = useState("zh");
    const [targetOptions , setTargetOptions] = useState([])

    useEffect(() => {
      
      if (languageData[sourceLang]) {
        setTargetOptions(languageData[sourceLang]);
      }
    }, [sourceLang]);
    const fetchData = async (input, sourceLang, targetLang, setOutput) => {
      if (service === "TencentCloud") {
      const url = "http://127.0.0.1:8000/api/tencent_translate";
  
      try {
          const response = await fetch(url, {
              method: 'POST',
              headers: {
                  'Content-Type': 'application/json'
              },
              body: JSON.stringify({
                  text: input,
                  source_lang: sourceLang,
                  target_lang: targetLang
              })
          });
  
          const reader = response.body.getReader();
          let result = '';
          while (true) {
              const { done, value } = await reader.read();
              if (done) break;
              result += new TextDecoder().decode(value);
          }
          console.log(result);
          setOutput(result); // 使用 setOutput 更新数据
      } catch (error) {
          console.error('Fetch error:', error);
      }
    }
  };
  

    const translate = () => { // 发起请求
        const currentInput = document.getElementById("input").value;
        const currentSourceLang = document.getElementById("sourceLang").value;
        const currentTargetLang = document.getElementById("targetLang").value;
      
        fetchData(currentInput, currentSourceLang, currentTargetLang, setOutput);
      };

    return (
        <div>
            <div className='button_container'>
            <span className='lang_button_container'>
            <span>源语言</span>
            <select className="button" id="sourceLang" value={sourceLang} onChange={(e) => setSourceLang(e.target.value)}>
              {Object.keys(languageData).map(lang => (
                <option key={lang} value={lang}>{languageData[lang][0].name}</option>
              ))}
            </select>

            </span>
            <button className='button' id="trans" onClick={translate}>翻译</button>
            <span className='lang_button_container'>
              <span>目标语言</span>
              <select className='button' id="targetLang" onChange={(e) => setTargetLang(e.target.value)}>
                {targetOptions.map(lang => (
                  <option key={lang.code} value={lang.code}>{lang.name}</option>
                ))}
              </select>
            </span>
            </div>
            <div style={{display:'none'}}>翻译中...</div>
        </div>
    )
}