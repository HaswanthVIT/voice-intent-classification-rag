import axios from "axios";

const API = axios.create({
  baseURL: "http://127.0.0.1:5000",
});

export const fetchCalls = async () => {
  const res = await API.get("/calls");
  return res.data;
};

export const fetchCall = async (callId) => {
  const res = await API.get(`/calls/${callId}`);
  return res.data;
};

// Upload file — returns { file_path }
export const uploadFile = async (file) => {
  const formData = new FormData();
  formData.append("file", file);
  const res = await API.post("/upload", formData, {
    headers: { "Content-Type": "multipart/form-data" },
  });
  return res.data;
};

// Run pipeline on uploaded file — returns { call_id, intent_class, status }
export const processFile = async (filePath) => {
  const res = await API.post("/process", { file_path: filePath });
  return res.data;
};