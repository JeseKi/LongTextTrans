import React, {useState , useEffect} from "react";

import "./settings_activate.css"
export default function SettingsActivate ({setActivateSettings , service , setService}) {

    const activateSettings = () => {
        setActivateSettings(true);
    }

    const changeService = (event) => {
        const newService = event.target.value;
        setService(newService);
        localStorage.setItem("service", newService);
    };

    useEffect(() => {
       const savedService = localStorage.getItem("service");
       if (savedService) {
           setService(savedService);
       }
    }, []);

    return (
        <div>
            <button className="button settings_activate" id="activate" onClick={activateSettings}>
                设置
            </button>
            <span>
            <h4 style={{display: "inline"}}>当前模式:</h4>
            <select className="button" style={{width:"5vw"}} value={service} onChange={changeService}>
                <option value={"OpenAI"}>OpenAI</option>
                <option value={"TencentCloud"}>腾讯云</option>
            </select>
            </span>
        </div>
    )
}