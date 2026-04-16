import { useEffect, useState } from "react";
import { api } from "./api";

function App() {
  const [message, setMessage] = useState("Loading...");
  useEffect(() => {
    api.get("/")
      .then((res) => setMessage(res.data.message))
      .catch(() => setMessage("Failed to connect to backend"));
  }, []);
  return (
    <div style={{padding:"2rem", fontFamily:"Arial"}}>
      <h1>InsightDocs Frontend</h1>
      <p>Frontend is running successfully.</p>
      <p>{message}</p>
    </div>
  );
}

export default App;
