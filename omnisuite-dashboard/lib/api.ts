import axios from "axios";

const api = axios.create({
  baseURL: "https://omnisuite-api.onrender.com", // ✅ TEMP FIX
});

export default api;