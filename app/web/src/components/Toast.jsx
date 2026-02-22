import { useEffect } from "react";
import "./Toast.css";

export default function Toast({ message, onClose }) {
  useEffect(() => {
    const t = setTimeout(onClose, 2500);
    return () => clearTimeout(t);
  }, [onClose]);

  return <div className="toast" role="status">{message}</div>;
}
