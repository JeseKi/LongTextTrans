import React from "react";

import "./settings_unactivate.css"

export default function SettingsUnactivate ({setActivateSettings}) {
    const changeDisplay = () => {
        setActivateSettings(false)
    }

    return (
        <button className="button unactivate" onClick={changeDisplay}>
            关闭
        </button>
    )
}