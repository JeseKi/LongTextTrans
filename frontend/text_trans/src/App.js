import React ,{useEffect , useState} from "react"
import axios from "axios";

import "./App.css"
import 'bootstrap/dist/css/bootstrap.min.css';

import TransBtn from "./components/mainPage/transbtn"; // 选择语言,发送请求,更新输出等
import Output from "./components/mainPage/output"; // 输出框
import Input from "./components/mainPage/input"; // 输入框

import SettingsActivate from "./components/settingsPage/settings_activate"; // 选择服务,是否打开设置页面等
import SettingsContainer from "./components/settingsPage/container"; // 设置页面

function App() {
  const [output, setOutput] = useState("");
  const [activateSettings, setActivateSettings] = useState(false)
  const [service, setService] = useState("OpenAI");
  const [accumulatedContent, setAccumulatedContent] = useState("");
  const [haveDone, setHaveDone] = useState(0)
  const [file, setFile] = useState(null);
  const [filePath, setFilePath] = useState("")
  
  return (
    <div>
      <h1>长文本翻译器</h1>
      <div className='container'>
        <SettingsContainer activateSettings={activateSettings} setActivateSettings={setActivateSettings} />
        <SettingsActivate setActivateSettings={setActivateSettings} service={service} setService={setService}/>
        <Input setFile={setFile} />
        <TransBtn setOutput={setOutput} service={service} setAccumulatedContent={setAccumulatedContent} setHaveDone={setHaveDone} filePath={filePath} file={file}/>
        <Output output={output} accumulatedContent={accumulatedContent} setAccumulatedContent={setAccumulatedContent} haveDone={haveDone} setHaveDone={setHaveDone} setFilePath={setFilePath} file={file}/>
      </div>
    </div>
  );
}  

export default App;
