import axios from "axios";

const API = axios.create({
  baseURL: "http://127.0.0.1:5000",
});

export const fetchCalls = async () => {
  const res = await API.get("/calls");
  return res.data;
};