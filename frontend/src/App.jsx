// import React from "react";

// import { useState } from "react";
// import axios from "axios";
// import Dropzone from "./components/Dropzone";
// import ResultCard from "./components/ResultCard";


// export default function App() {
//   const [file, setFile] = useState(null);
//   const [result, setResult] = useState(null);
//   const [loading, setLoading] = useState(false);
//   const [error, setError] = useState("");

//   const analyzeResume = async () => {
//     if (!file) {
//       setError("Please upload a PDF resume");
//       return;
//     }

//     try {
//       setLoading(true);
//       setError("");
//       const formData = new FormData();
//       formData.append("file", file);

//       const res = await axios.post(
//         "http://127.0.0.1:8000/analyze",
//         formData
//       );

//       setResult(res.data);
//     } catch (err) {
//       setError("Failed to analyze resume");
//     } finally {
//       setLoading(false);
//     }
//   };

//   return (
//     <div className="container">
//       <h1>AI Resume Analyzer</h1>
//       <Dropzone file={file} setFile={setFile} />

//       <button onClick={analyzeResume} disabled={loading}>
//         {loading ? "Analyzing..." : "Analyze Resume"}
//       </button>

//       {error && <p className="error">{error}</p>}
//       {result && <ResultCard data={result} />}
//     </div>
//   );
// }
import React, { useState } from "react";
import axios from "axios";
import Dropzone from "./components/Dropzone";
import ResultCard from "./components/ResultCard";
import API_URL from "./config";

export default function App() {
  const [file, setFile] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const clearResult = () => {
    setResult(null);
    setError("");
  };

  const analyzeResume = async () => {
    if (!file) {
      setError("Please upload a PDF resume");
      return;
    }

    try {
      setLoading(true);
      setError("");

      const formData = new FormData();
      formData.append("file", file);

     

      const res = await axios.post(
      `${API_URL}/analyze`,
      formData
      );

      setResult(res.data);
    } catch (err) {
      setError("Failed to analyze resume");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container">
      <h1>AI Resume Analyzer</h1>

      <Dropzone
        file={file}
        setFile={setFile}
        clearResult={clearResult}
      />

      {/* <button onClick={analyzeResume} disabled={loading || !file}>
        {loading ? "Analyzing..." : "Analyze Resume"}
      </button> */}

     <button onClick={analyzeResume} disabled={loading}>
        {loading ? "Analyzing..." : "Analyze Resume"}
     </button>
     

      {/* ✅ Loading Spinner */}
      {loading && <div className="spinner"></div>}

      {error && <p className="error">{error}</p>}

      {result && <ResultCard data={result} />}
    </div>
  );
}
