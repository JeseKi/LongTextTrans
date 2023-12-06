import React ,{useEffect , useState} from "react"
import "./App.css"
import 'bootstrap/dist/css/bootstrap.min.css';

import TransBtn from "./components/mainPage/transbtn";
import Output from "./components/mainPage/output";
import Input from "./components/mainPage/input";

import SettingsActivate from "./components/settingsPage/settings_activate";
import SettingsContainer from "./components/settingsPage/container";

function App() {
  const [output, setOutput] = useState("");
  const [activateSettings, setActivateSettings] = useState(false)
  const [service, setService] = useState("OpenAI");

  return (
    <div>
      <h1>长文本翻译器</h1>
      <div className='container'>
        <SettingsContainer activateSettings={activateSettings} setActivateSettings={setActivateSettings} />
        <SettingsActivate setActivateSettings={setActivateSettings} service={service} setService={setService}/>
        <Input setOutput />
        <TransBtn setOutput={setOutput} service={service}/>
        <Output output={output}/>
      </div>
    </div>
  );
}  

export default App;
