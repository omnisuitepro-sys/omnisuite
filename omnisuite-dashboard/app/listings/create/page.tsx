"use client";
import { useState } from "react";
import api from "@/lib/api";

export default function Create(){
 const [title,setTitle]=useState("")
 const [price,setPrice]=useState("")
 const [cost,setCost]=useState("")

 return(
 <form onSubmit={async e=>{
  e.preventDefault()
  await api.post("/listings",{title,price:+price,cost:+cost})
  location.href="/listings"
 }}>
  <input placeholder="title" onChange={e=>setTitle(e.target.value)}/>
  <input placeholder="price" onChange={e=>setPrice(e.target.value)}/>
  <input placeholder="cost" onChange={e=>setCost(e.target.value)}/>
  <button>Create</button>
 </form>
 )
}