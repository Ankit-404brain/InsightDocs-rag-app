import { useEffect, useState } from "react";
import { listDocuments, uploadDocument } from "./api/documents";
import { queryRAG } from "./api/documents";

function App() {
  const [file, setFile] = useState<File | null>(null);
  const [documents, setDocuments] = useState<any[]>([]);
  const [query, setQuery] = useState("");
  const [answer, setAnswer] = useState("");
  const [sources, setSources] = useState<any[]>([]);
  const [uploading, setUploading] = useState(false);
  const [asking, setAsking] = useState(false);

  const loadDocuments = async () => {
    try {
      const data = await listDocuments();
      setDocuments(data);
    } catch (err) {
      console.error("Failed to load documents:", err);
    }
  };

  const ask = async () => {
    if (!query.trim()) return;
    setAsking(true);
    setAnswer("");
    setSources([]);
    try {
      const res = await queryRAG(query);
      setAnswer(res.answer);
      setSources(res.sources || []);
    } catch (err: any) {
      setAnswer("Error: " + (err?.response?.data?.detail || err.message || "Query failed"));
    } finally {
      setAsking(false);
    }
  };

  useEffect(() => {
    loadDocuments();
    const interval = setInterval(loadDocuments, 3000);
    return () => clearInterval(interval);
  }, []);

  const handleUpload = async () => {
    if (!file) return;
    setUploading(true);
    try {
      await uploadDocument(file);
      setFile(null);
      await loadDocuments();
    } catch (err) {
      console.error("Upload failed:", err);
      alert("Upload failed. Please try again.");
    } finally {
      setUploading(false);
    }
  };

  return (
    <div style={{ padding: 20, fontFamily: "Arial" }}>
      <h1>InsightDocs RAG App</h1>

      <input
        type="file"
        onChange={(e) => setFile(e.target.files?.[0] || null)}
      />
      <button onClick={handleUpload} style={{ marginLeft: "1rem" }} disabled={!file || uploading}>
        {uploading ? "Uploading..." : "Upload"}
      </button>

      <h2 style={{ marginTop: "2rem" }}>Documents</h2>
      <ul>
        {documents.map((doc) => (
          <li key={doc.id}>
            <strong>{doc.filename}</strong> -{" "}
            <span style={{
              color: doc.status === "INDEXED" ? "#4caf50" :
                     doc.status === "FAILED" ? "#f44336" :
                     doc.status === "PROCESSING" ? "#ff9800" : "#999"
            }}>
              {doc.status}
            </span>
          </li>
        ))}
      </ul>

      <div style={{ padding: 20 }}>
        <h1>Chat</h1>

        <input
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && ask()}
          style={{ width: "300px" }}
          placeholder="Ask a question about your documents..."
        />

        <button onClick={ask} disabled={asking || !query.trim()}>
          {asking ? "Thinking..." : "Ask"}
        </button>

        <h3>Answer:</h3>
        <p>{answer || (asking ? "Generating answer..." : "No answer yet")}</p>

        {sources.length > 0 && (
          <>
            <h4>Sources:</h4>
            <ul>
              {sources.map((s, idx) => (
                <li key={idx}>
                  <strong>Doc {s.document_id.substring(0, 8)}...</strong> (chunk {s.chunk_index}):{" "}
                  {s.content.substring(0, 150)}...
                </li>
              ))}
            </ul>
          </>
        )}
      </div>
    </div>
  );
}

export default App;