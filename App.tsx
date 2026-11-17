import { useState } from "react";
import { Send, Sparkles, Orbit, Brain, Settings2 } from "lucide-react";

type Message = { role: "user" | "assistant"; content: string };
const API = "http://127.0.0.1:8000";

export default function App() {
  const [messages, setMessages] = useState<Message[]>([
    { role: "assistant", content: "I’m RAFAYEL. Your desktop and Android assistant is ready. What shall we work on?" }
  ]);
  const [input, setInput] = useState("");
  const [conversation, setConversation] = useState<string | undefined>();
  const [busy, setBusy] = useState(false);
  const [provider, setProvider] = useState("waiting for first reply");

  async function send() {
    const value = input.trim();
    if (!value || busy) return;
    setInput("");
    setMessages(m => [...m, { role: "user", content: value }]);
    setBusy(true);
    try {
      const response = await fetch(`${API}/api/chat`, {
        method: "POST", headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: value, conversation_id: conversation })
      });
      const data = await response.json();
      if (!response.ok) throw new Error(data.detail || "Backend request failed");
      setConversation(data.conversation_id);
      setProvider(data.provider);
      setMessages(m => [...m, { role: "assistant", content: data.reply }]);
    } catch (e) {
      setMessages(m => [...m, { role: "assistant", content: `Connection issue: ${e instanceof Error ? e.message : "Unknown error"}. Check that the RAFAYEL backend is running.` }]);
    } finally { setBusy(false); }
  }

  return <main className="shell">
    <aside className="sidebar">
      <div className="brand"><div className="brandOrb"><Orbit size={24}/></div><div><b>RAFAYEL</b><small>THE COSMIC INTELLIGENCE</small></div></div>
      <div className="sideItem active"><Sparkles size={17}/> New conversation</div>
      <div className="sideItem"><Brain size={17}/> Memory</div>
      <div className="sideItem"><Settings2 size={17}/> Settings</div>
      <div className="sideBottom"><span className="dot"/> HYBRID CORE <small>Cloud + Local fallback</small></div>
    </aside>
    <section className="main">
      <header><div><span className="eyebrow">PERSONAL INTELLIGENCE</span><h1>Beyond answers. Towards understanding.</h1></div><span className="status">● SYSTEM READY</span></header>
      <div className="orbStage"><div className="orbit orbitA"/><div className="orbit orbitB"/><div className="orb"><div className="orbCore"/></div><span className="orbLabel">R A F A Y E L</span></div>
      <div className="chat">
        {messages.map((m,i)=><div className={`bubble ${m.role}`} key={i}><label>{m.role === "user" ? "YOU" : "RAFAYEL"}</label><p>{m.content}</p></div>)}
        {busy && <div className="bubble assistant"><label>RAFAYEL</label><p className="typing">Thinking through it…</p></div>}
      </div>
      <div className="composer"><textarea value={input} onChange={e=>setInput(e.target.value)} onKeyDown={e=>{if(e.key==="Enter"&&!e.shiftKey){e.preventDefault();send();}}} placeholder="Talk to RAFAYEL…" rows={2}/><button onClick={send} disabled={busy || !input.trim()}><Send size={18}/></button></div>
      <footer>PROVIDER: {provider.toUpperCase()} <span>•</span> Emotional tone adapts to context <span>•</span> You stay in control</footer>
    </section>
  </main>;
}
