import React, { useState } from "react";
import "./input.css"

export default function Input() {
  const [showPlaceholder, setShowPlaceholder] = useState(true);
  const [file, setFile] = useState(null);

  // 定义一个函数，用来处理按钮的点击事件
  const handleClick = () => {
    // 创建一个隐藏的文件输入元素
    const input = document.createElement("input");
    input.type = "file";
    input.accept = ".txt"; // 只接受txt文件
    input.style.display = "none";
    document.body.appendChild(input);

    // 定义一个函数，用来处理文件输入元素的变化事件
    const handleChange = (e) => {
      // 获取用户选择的文件
      const file = e.target.files[0];
      // 更新状态变量
      setFile(file);
      // 移除文件输入元素
      document.body.removeChild(input);
    };

    // 给文件输入元素添加变化事件监听器
    input.addEventListener("change", handleChange);

    // 触发文件输入元素的点击事件，打开文件选择器
    input.click();
  };
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
      <div>
          <button onClick={handleClick}>选择一个txt文件</button>
          {file && <p>你选择了文件：{file.name}</p>}
      </div>
    </div>
  );
}  