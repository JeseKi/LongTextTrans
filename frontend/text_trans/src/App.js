import React ,{useEffect , useState} from "react"
import "./App.css"

import IdKeySave from "./components/id_key_save";
import TransBtn from "./components/transbtn";
import Output from "./components/output";
import Input from "./components/input";

function App() {
  const [output, setOutput] = useState("");
  return (
    <div>
      <h1 style={{ textAlign: 'center' }}>长文本翻译器</h1>
      <div className='container'>
        <IdKeySave />
        <Input setOutput />
        <TransBtn setOutput={setOutput}/>
        <Output output={output}/>
      </div>
    </div>
  );
}  

export default App;
