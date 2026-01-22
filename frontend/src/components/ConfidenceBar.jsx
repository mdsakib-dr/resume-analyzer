import React from "react";
export default function ConfidenceBar({ confidence }) {
  const percent = Math.round(confidence * 100);
  return (
    <div>
      <p><b>Confidence:</b> {percent}%</p>
      <div className="confidence-bar">
        <div className="confidence-fill" style={{ width: percent + "%" }}></div>
      </div>
    </div>
  );
}
