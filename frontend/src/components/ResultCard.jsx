import React from "react";
import ConfidenceBar from "./ConfidenceBar";

export default function ResultCard({ data }) {
  return (
    <div className="card">
      <h2>Result</h2>
      <p><b>Name:</b> {data.name || "N/A"}</p>
      <p><b>Email:</b> {data.email || "N/A"}</p>
      <p><b>Phone:</b> {data.phone || "N/A"}</p>
      <p><b>Skills:</b> {data.skills?.join(", ")}</p>
      <p><b>Experience:</b> {data.experience_years} years ({data.experience_level})</p>
      <p><b>Job Role:</b> {data.classification}</p>
      <ConfidenceBar confidence={data.confidence} />
    </div>
  );
}
