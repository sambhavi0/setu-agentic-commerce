import { useState, useEffect } from "react";
import "./App.css";

const API_BASE = "http://127.0.0.1:8000";

function App() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [auditLog, setAuditLog] = useState([]);
  const [mandate, setMandate] = useState(null);

  const fetchAudit = async () => {
    try {
      const res = await fetch(`${API_BASE}/agent/audit`);
      const data = await res.json();
      setAuditLog(data.log || []);
    } catch (err) {
      console.error("Failed to fetch audit log", err);
    }
  };

  const fetchMandate = async () => {
    try {
      const res = await fetch(`${API_BASE}/agent/mandate`);
      const data = await res.json();
      setMandate(data);
    } catch (err) {
      console.error("Failed to fetch mandate", err);
    }
  };

  useEffect(() => {
    fetchAudit();
    fetchMandate();
  }, []);

  const sendMessage = async () => {
    if (!input.trim() || loading) return;
    const userMsg = input;
    setMessages((prev) => [...prev, { role: "user", text: userMsg }]);
    setInput("");
    setLoading(true);

    try {
      const res = await fetch(`${API_BASE}/agent/chat`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: userMsg }),
      });
      const data = await res.json();
      setMessages((prev) => [...prev, { role: "agent", text: data.reply }]);
    } catch (err) {
      setMessages((prev) => [
        ...prev,
        { role: "agent", text: "Error reaching the agent. Is the backend running?" },
      ]);
    } finally {
      setLoading(false);
      fetchAudit();
    }
  };

  const statusColor = (status) => {
    if (status === "approved") return "#2e7d32";
    if (status === "needs_confirmation") return "#f9a825";
    return "#c62828";
  };

  return (
    <div className="app">
      <div className="sidebar">
        <h2>Setu</h2>
        <p className="subtitle">Agent-readable commerce with a spending mandate</p>

        <div className="mandate-box">
          <h3>Active Mandate</h3>
          {mandate ? (
            <>
              <p>Max per transaction: ₹{mandate.max_transaction}</p>
              <p>Daily limit: ₹{mandate.daily_limit}</p>
              <p>Needs confirmation above: ₹{mandate.require_confirmation_above}</p>
              <p>Allowed categories: {mandate.allowed_categories.join(", ")}</p>
              <p className="muted">Expires: {new Date(mandate.expires_at).toLocaleDateString()}</p>
            </>
          ) : (
            <p className="muted">Loading mandate...</p>
          )}
        </div>

        <h3>Audit Trail</h3>
        <div className="audit-list">
          {auditLog.length === 0 && <p className="muted">No actions yet.</p>}
          {auditLog.slice().reverse().map((entry, i) => (
            <div key={i} className="audit-entry" style={{ borderLeftColor: statusColor(entry.decision) }}>
              <strong>{entry.decision}</strong>
              <p>{entry.product_id} × {entry.quantity}</p>
              <p className="reason">{entry.reason}</p>
            </div>
          ))}
        </div>
      </div>

      <div className="chat">
        <div className="chat-log">
          {messages.map((m, i) => (
            <div key={i} className={`bubble ${m.role}`}>
              {m.text}
            </div>
          ))}
          {loading && <div className="bubble agent">thinking...</div>}
        </div>
        <div className="chat-input">
          <input
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && sendMessage()}
            placeholder="Ask the buyer agent to purchase something..."
          />
          <button onClick={sendMessage} disabled={loading}>Send</button>
        </div>
      </div>
    </div>
  );
}

export default App;