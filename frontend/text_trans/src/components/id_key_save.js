import React , {useEffect} from "react";
import "./id_key_save.css"

export default function IdKeySave () {
    useEffect(() => {
        const savedID = localStorage.getItem("tencentCloudID");
        const savedKey = localStorage.getItem("tencentCloudKey");
        if (savedID && savedKey) {
          document.getElementById("myID").value = savedID;
          document.getElementById("myKEY").value = savedKey;
        }
      }, []);
    
      const saveToLocalStorage = () => {
        const id = document.getElementById("myID").value;
        const key = document.getElementById("myKEY").value;
        localStorage.setItem("tencentCloudID", id);
        localStorage.setItem("tencentCloudKey", key);
        alert("保存成功！");
      };
    return(
        <div>
            <p style={{margin:0}}>↓在这里输入你的腾讯云ID和KEY↓</p>
            <div>
            <span>ID :</span>
            <input className='ID_KEY' type="text" placeholder="腾讯云ID" id="myID" /> 
            <span>KEY :</span>
            <input className='ID_KEY' type="password" placeholder="腾讯云KEY" id="myKEY"/>
            </div>
            <button className='savebutton' style={{ fontSize: '0.8em' }} id="save_id_key" onClick={saveToLocalStorage}>保存ID和KEY</button>
        </div>
    )
}