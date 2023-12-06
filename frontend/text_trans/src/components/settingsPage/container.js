import React from "react";
import "./container.css"

import IdKeySave from "./id_key_save";
import SettingsUnactivate from "./settings_unactivate";

export default function SettingsContainer ({activateSettings, setActivateSettings}) {
    const containerClass = `settingsContainer${activateSettings ? " visible" : ""}`;

    return (
        <div className={containerClass}>
            <h2>设置</h2>
            <IdKeySave />
            <SettingsUnactivate setActivateSettings={setActivateSettings}/>
        </div>
    )
}