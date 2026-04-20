import { useEffect, useState } from "react";
import { listDocuments, uploadDocument } from "./api/documents";

function App() {
  const [file, setFile] = useState<File | null>(null);
  const [documents, setDocuments] = useState<any[]>([]);

  const loadDocuments = async () => {
    const data = await listDocuments();
    setDocuments(data);
  };

  useEffect(() => {
    loadDocuments();
  const interval = setInterval(loadDocuments, 3000);
  return () => clearInterval(interval);
  }, []);

  const handleUpload = async () => {
    if (!file) return;
    await uploadDocument(file);
    setFile(null);
    await loadDocuments();
  };

  return (
    <div style={{ padding: "2rem", fontFamily: "Arial" }}>
      <h1>Phase 2 - Document Upload</h1>

      <input
        type="file"
        onChange={(e) => setFile(e.target.files?.[0] || null)}
      />
      <button onClick={handleUpload} style={{ marginLeft: "1rem" }}>
        Upload
      </button>

      <h2 style={{ marginTop: "2rem" }}>Documents</h2>
      <ul>
        {documents.map((doc) => (
          <li key={doc.id}>
            <strong>{doc.filename}</strong> - {doc.status}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default App;