"use client";
import { useQuery } from "@tanstack/react-query";
import api from "@/lib/api";
import { useState } from "react";

export default function Page(){
 const [tab,setTab]=useState<any>(null)

 const {data:metrics}=useQuery({
  queryKey:["metrics"],
  queryFn:async()=> (await api.get("/metrics")).data
 })

 const {data:tabs=[]}=useQuery({
  queryKey:["tabs"],
  queryFn:async()=> (await api.get("/tabs")).data
 })

 const {data:listings=[]}=useQuery({
  queryKey:["listings",tab],
  queryFn:async()=>{
   return (await api.get(tab?`/listings?tab_id=${tab}`:"/listings")).data
  }
 })

 return(
 <div>

 <h1>Listings</h1>

 <div>Profit: ${metrics?.total_profit}</div>

 <button onClick={()=>api.post("/automation/run").then(()=>location.reload())}>
  Run Automation
 </button>

 <button onClick={()=>api.post("/arbitrage/run").then(()=>location.reload())}>
  Run Arbitrage
 </button>

 {tabs.map((t:any)=>(
  <button key={t.id} onClick={()=>setTab(t.id)}>{t.name}</button>
 ))}

 <button onClick={async()=>{
  const name=prompt("Tab name")
  await api.post("/tabs",{name})
  location.reload()
 }}>
  +Tab
 </button>

 {listings.map((l:any)=>(
  <div key={l.id}>
   {l.title} - ${l.price} | Profit: ${l.profit}
   <button onClick={async()=>{
    await api.delete(`/listings/${l.id}`)
    location.reload()
   }}>X</button>
  </div>
 ))}

 </div>
 )
}