import React, { useState } from "react";

import "./input.css"

export default function Input({setFile}) {
  const [showPlaceholder, setShowPlaceholder] = useState(true);
  // 上传文件
  const onFileChange = (e) => {
    setFile(e.target.files[0]);
};

  const handleFocus = () => {
    setShowPlaceholder(false);
  };

  const handleBlur = () => {
    if (!document.getElementById("input").value) {
      setShowPlaceholder(true);
    }
  };
  
  return (
    <div>
      <p>源文本</p>
      <textarea
        className='text_container'
        placeholder={showPlaceholder ? "在这里输入文字" : ""}
        id="input"
        onFocus={handleFocus}
        onBlur={handleBlur}
      />
    <div class="mb-3">
      <label for="formFile" class="form-label">选择一个txt文件</label>
      <input class="form-control" type="file" id="formFile" accept=".txt" onChange={onFileChange}/>
    </div>

    </div>
  );
}  