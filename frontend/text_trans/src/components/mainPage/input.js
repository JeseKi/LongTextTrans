import React, { useState } from "react";
import "./input.css"

export default function Input() {
  const [showPlaceholder, setShowPlaceholder] = useState(true);

  const handleFocus = () => {
    setShowPlaceholder(false);
  };

  const handleBlur = () => {
    if (!document.getElementById("input").value) {
      setShowPlaceholder(true);
    }
  };

  const handleFileDragOver = (e) => {
    e.preventDefault(); // 阻止默认行为
  };
  
  const handleFileDrop = (e) => {
    e.preventDefault(); // 阻止默认行为
    const file = e.dataTransfer.files[0]; // 获取拖入的文件
    if (file) {
      const reader = new FileReader();
      reader.onload = (e) => {
        document.getElementById("input").value = e.target.result;
      };
      reader.readAsText(file); // 读取文件内容
    }
  };
  
  return (
    <div>
      <p>源文本</p>
      <textarea
        className='text_container'
        placeholder={showPlaceholder ? "在这里输入文字或拖入文件" : ""}
        id="input"
        onFocus={handleFocus}
        onBlur={handleBlur}
        onDragOver={handleFileDragOver}
        onDrop={handleFileDrop}
      />
    </div>
  );
}  