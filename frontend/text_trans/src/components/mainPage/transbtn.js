import React ,{useEffect , useState} from "react"
import axios from "axios"

import "./transbtn.css"
import languageData from './languages.json'

export default function TransBtn ( {setOutput , service , setAccumulatedContent , setHaveDone , file} ) {
    const [sourceLang , setSourceLang] = useState("en");
    const [targetLang , setTargetLang] = useState("zh");
    const [targetOptions , setTargetOptions] = useState([])
    // 上传文件
    const onFileUpload = async (file, sourceLang, targetLang,) => {
      const formData = new FormData();

      formData.append('file', file)
      const payload = {
        service: service,
        source_lang: sourceLang,
        target_lang: targetLang,
        tencentCloudID: localStorage.getItem("tencentCloudID"),
        tencentCloudKey: localStorage.getItem("tencentCloudKey"),
        api_key: localStorage.getItem('openaiKey'),
        rpm: localStorage.getItem('rpm'),
        model: localStorage.getItem('model')
      };

      formData.append("data", JSON.stringify(payload));
  
      try {
          const response = await axios.post("http://localhost:8000/upload/", formData, {
              headers: {
                  'Content-Type': 'multipart/form-data'
              }
          });
          console.log(response.data);
          // Handle the response from the server here
      } catch (error) {
          console.error("Error uploading file and text:", error);
      }
  };
    // 及时更新语言选项
    useEffect(() => {
      if (languageData[sourceLang]) {
        setTargetOptions(languageData[sourceLang]);
      }
    }, [sourceLang]);

    const fetchData = async (input, sourceLang, targetLang, setOutput) => {

      // 腾讯云服务
      if (service === "TencentCloud") {
      const url = "http://127.0.0.1:8000/api/tencent_translate";

      try {
        const text = new TextEncoder().encode(input)
        const encodedText = btoa(String.fromCharCode(...text))
        const response = await fetch(url, {
              method: 'POST',
              headers: {
                  'Content-Type': 'application/json'
              },
              body: JSON.stringify({
                  text: encodedText,
                  source_lang: sourceLang,
                  target_lang: targetLang,
                  ID: localStorage.getItem('tencentCloudID'),
                  Key: localStorage.getItem('tencentCloudKey')
              })
          });
          
          const reader = response.body.getReader();
          console.log('response:',response)
          let result = '';
          console.log("result:"+result)
          while (true) {
            const { done, value } = await reader.read();
            if (done) break;
        
            // 解码当前读取的数据块
            const chunk = new TextDecoder().decode(value);
        
            // 拼接到之前的结果
            result += chunk;
        
            // 立即处理当前累积的结果
            console.log("transbtn:",result);
            setOutput(result);  // 在这里更新输出
        }

      } catch (error) {
          console.error('Fetch error:', error);
      }
    }
        // OpenAI服务
        if (service === "OpenAI") {
          const url = "http://127.0.0.1:8000/api/openai_translate";

            try {
              const text = new TextEncoder().encode(input)
              const encodedText = btoa(String.fromCharCode(...text))
              const response = await fetch(url, {
                  method: 'POST',
                  headers: {
                      'Content-Type': 'application/json'
                  },
                  body: JSON.stringify({
                      model: localStorage.getItem('model'),
                      text: encodedText,
                      source_lang: sourceLang,
                      target_lang: targetLang,
                      api_key : localStorage.getItem('openaiKey'),
                      rpm : localStorage.getItem('rpm')
                  })
              });

              const reader = response.body.getReader();
              let result = '';
              console.log("result:" + result);
              while (true) {
                  const { done, value } = await reader.read();
                  if (done) break;
              
                  // Decode the current chunk
                  const chunk = new TextDecoder().decode(value);
              
                  // Replace the previous result with the new chunk
                  result = chunk;  // Replace, don't append
              
                  // Immediately process the current accumulated result
                  console.log("transbtn:", result);
                  setOutput(result);  // Update the output here
              }
              

          } catch (error) {
              console.error('Fetch error:', error);
          }
      } 
 
  };
  

    const translate = () => { // 发起请求
      if (!file) {
        const currentInput = document.getElementById("input").value;
        const currentSourceLang = document.getElementById("sourceLang").value;
        const currentTargetLang = document.getElementById("targetLang").value;
        if (currentInput === ""){
          alert("输入框不能为空")
          return 
        }

        setOutput("")
        setAccumulatedContent("")
        setHaveDone(0)

        fetchData(currentInput, currentSourceLang, currentTargetLang, setOutput);
      }
      if (file) {
        setHaveDone(0)
        const currentSourceLang = document.getElementById("sourceLang").value;
        const currentTargetLang = document.getElementById("targetLang").value;
        onFileUpload(file, currentSourceLang, currentTargetLang)
        console.log("发送文件")
      }
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