import React , {useEffect , useState} from "react";
import "./id_key_save.css"

export default function IdKeySave () {
    const [selected , setSeleted] = useState("")
    const [isShow, setIsShow] = useState(false)

    const handelShowChange = () => {
      setIsShow(!isShow)
      console.log(isShow)
    }
    useEffect(() => {
      const openaiKEYInput = document.getElementById('openaiKEY');
      const tencentCloudKeyInput = document.getElementById('myKEY')
      if (isShow) {
        openaiKEYInput.type = 'text'; // 显示密码
        tencentCloudKeyInput.type = 'text'
      } else {
        openaiKEYInput.type = 'password'; // 隐藏密码
        tencentCloudKeyInput.type = 'password'
      }
    }, [isShow]);
    

    const handleSelectChange = (event) => {
      setSeleted(event.target.value);
  };

    useEffect(() => {
        const savedID = localStorage.getItem("tencentCloudID");
        const savedKey = localStorage.getItem("tencentCloudKey");
        const savedOpenAIKEY = localStorage.getItem("openaiKey")
        const saveModel = localStorage.getItem("model")
        if (savedID || savedKey || savedOpenAIKEY || saveModel) {
          document.getElementById("myID").value = savedID;
          document.getElementById("myKEY").value = savedKey;
          document.getElementById("openaiKEY").value = savedOpenAIKEY
          setSeleted(saveModel || "")
        }
      }, []);
    
      const saveToLocalStorage = () => {
        const id = document.getElementById("myID").value;
        const key = document.getElementById("myKEY").value;
        const openaiKey = document.getElementById("openaiKEY").value;
        const model = document.getElementById("model").value
        localStorage.setItem("tencentCloudID", id);
        localStorage.setItem("tencentCloudKey", key);
        localStorage.setItem("openaiKey", openaiKey);
        localStorage.setItem("model", model)

        // console.log("Saved OpenAI Key:", localStorage.getItem("openaiKey"));
        // console.log("Saved ID:", localStorage.getItem("tencentCloudID"));
        // console.log("Saved Key:", localStorage.getItem("tencentCloudKey"));
        
        alert("保存成功！");
    };
    
    return(
        <div>
            <hr/>
            <h4>腾讯云ID-KEY设置</h4>
            <div>
            <span>ID :
            <input className='ID_KEY' type="text" placeholder="腾讯云ID" id="myID" /> 
            </span>
            <span>KEY :
            <input className='ID_KEY' type="password" placeholder="腾讯云KEY" id="myKEY" />
            </span>
            </div>
            <hr/>
            <h4>OpenAI设置</h4>
            <span>OpenAI-Key(支持多个OpenAIKey,只需将各个OpenAIKey用英语逗号分隔即可):
            <input className="ID_KEY" type="password" placeholder="OpenAIKey" id="openaiKEY"/>
            </span>
            <span>模型:&nbsp;&nbsp;&nbsp;
            <select className="button" style={{width: "10vw"}} value={selected} onChange={handleSelectChange} id="model">
              <option value="gpt-3.5-turbo-1106">gpt-3.5-turbo-1106</option>
              <option value="gpt-3.5-turbo">gpt-3.5-turbo</option>
              <option value="gpt-3.5-turbo-0613">gpt-3.5-turbo-0613</option>
              <option value="gpt-3.5-turbo-16k">gpt-3.5-turbo-16k</option>
              <option value="gpt-3.5-turbo-16k-0613">gpt-3.5-turbo-16k-0613</option>
              <option value="gpt-4">gpt-4</option>
              <option value="gpt-4-1106-preview">gpt-4-1106-preview (recommended)</option>
              <option value="gpt-4-0314">gpt-4-0314</option>
              <option value="gpt-4-0613">gpt-4-0613</option>
              <option value="gpt-4-32k">gpt-4-32k</option>
              <option value="gpt-4-32k-0314">gpt-4-32k-0314</option>
              <option value="gpt-4-32k-0613">gpt-4-32k-0613</option>
            </select>
            </span>
            <hr/>
            <button className='savebutton' style={{ fontSize: '0.8em' }} id="save_id_key" onClick={saveToLocalStorage}>保存</button>
            <button className="savebutton" style={{ fontSize: '0.8em', bottom: '10'}} id="show" onClick={handelShowChange}>显示Keys</button>
        </div>
    )
}