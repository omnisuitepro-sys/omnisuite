"use client";

import { useState } from "react";
import api from "@/lib/api";

export default function ScanPage() {
  const [files, setFiles] = useState<File[]>([]);
  const [results, setResults] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);

  const handleFiles = (e:any)=>{
    setFiles(Array.from(e.target.files));
  };

  const runScan = async ()=>{
    setLoading(true);
    const res:any[] = [];

    for(const file of files){
      const form = new FormData();
      form.append("file", file);

      const r = await api.post("/ai/scan", form);
      res.push(r.data);
    }

    setResults(res);
    setLoading(false);
  };

  return (
    <div>
      <h1>AI Scanner</h1>

      <input type="file" multiple onChange={handleFiles} />

      <button onClick={runScan}>
        {loading ? "Scanning..." : "Scan"}
      </button>

      {results.map((r,i)=>(
        <div key={i}>
          <h3>{r.product_name}</h3>

          <img src={r.image_url} width={150}/>

          <h4>Best Supplier:</h4>
          {r.profit_analysis && (
            <div>
              Cost: ${r.profit_analysis.best_cost} <br/>
              Sell: ${r.profit_analysis.recommended_price} <br/>
              Profit: ${r.profit_analysis.profit}
            </div>
          )}

          <h4>Suppliers:</h4>
          {r.suppliers.map((s:any,idx:number)=>(
            <div key={idx}>
              {s.title} - ${s.price}
            </div>
          ))}
        </div>
      ))}
    </div>
  );
}