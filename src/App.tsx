import { useState } from "react";
import axios from "axios";

function App() {

  const [file, setFile] = useState<File | null>(null);
  const [jobDesc, setJobDesc] = useState("");
  const [result, setResult] = useState("");
  const [score, setScore] = useState(0);

  const [chatInput, setChatInput] = useState("");
  const [chatResponse, setChatResponse] = useState("");

  const [loading, setLoading] = useState(false);

  // RESUME UPLOAD
  const uploadResume = async () => {

    if (!file) return;

    setLoading(true);

    const formData = new FormData();
    formData.append("file", file);
    formData.append("job_description", jobDesc);

    try {
      const res = await axios.post(
  `${import.meta.env.VITE_API_URL}/upload-resume`,
  formData
);

      setResult(res.data.result);
      setScore(res.data.score);

    } catch (err) {
      setResult("Error processing resume");
    }

    setLoading(false);
  };


  // CHAT
  
  const sendChat = async () => {

    const formData = new FormData();
    formData.append("message", chatInput);

    const res = await axios.post(
  `${import.meta.env.VITE_API_URL}/chat`,
  formData
  );

    setChatResponse(res.data.response);
  };


  // PDF DOWNLOAD

  const downloadPDF = async () => {

    const formData = new FormData();
    formData.append("result", result);

    const res = await axios.post(
  `${import.meta.env.VITE_API_URL}/download-pdf`,
  formData,
  { responseType: "blob" }
  );

    const url = window.URL.createObjectURL(new Blob([res.data]));
    const link = document.createElement("a");
    link.href = url;
    link.setAttribute("download", "report.pdf");
    document.body.appendChild(link);
    link.click();
  };

  return (
    <div style={{ padding: "20px" }}>

      <h1>🚀 AI Career Assistant</h1>

      {/* FILE */}
      <input
        type="file"
        onChange={(e) => {
          if (e.target.files) setFile(e.target.files[0]);
        }}
      />

      <br /><br />

      {/* JOB DESCRIPTION */}
      <textarea
        placeholder="Paste Job Description"
        value={jobDesc}
        onChange={(e) => setJobDesc(e.target.value)}
        rows={8}
        cols={80}
      />

      <br /><br />

      <button onClick={uploadResume}>
        {loading ? "Analyzing..." : "Upload & Analyze"}
      </button>

      <br /><br />

      <h3>ATS Score: {score}/100</h3>

      {/* RESULT */}
      <textarea
        value={result}
        readOnly
        rows={15}
        cols={80}
        style={{
          backgroundColor: "white",
          color: "black",
          padding: "10px",
          border: "1px solid #ccc",
          whiteSpace: "pre-wrap"
        }}
      />

      <br />

      <button onClick={downloadPDF}>
        📄 Download PDF Report
      </button>

      <hr />

      {/* CHAT */}
      <h2>💬 Chat with AI</h2>

      <textarea
        value={chatInput}
        onChange={(e) => setChatInput(e.target.value)}
        rows={3}
        cols={80}
      />

      <br />

      <button onClick={sendChat}>
        Send
      </button>

      <br /><br />

      <textarea
        value={chatResponse}
        readOnly
        rows={8}
        cols={80}
        style={{
          backgroundColor: "#f0f0f0",
          color: "black",
          padding: "10px"
        }}
      />

    </div>
  );
}

export default App;
