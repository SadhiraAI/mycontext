import { useState, useEffect, useCallback } from "react";
import * as api from "../api/client";

/**
 * Global hook to fetch the user's active provider + model.
 * Returns { provider, model, hasKey, loading, refresh }.
 *
 * Usage:
 *   const { provider, model, hasKey, refresh } = useActiveProvider();
 */
export default function useActiveProvider() {
  const [provider, setProvider] = useState(null);
  const [model, setModel] = useState(null);
  const [hasKey, setHasKey] = useState(false);
  const [loading, setLoading] = useState(true);

  const refresh = useCallback(() => {
    setLoading(true);
    api
      .getActiveProvider()
      .then((data) => {
        setProvider(data.provider || null);
        setModel(data.model || null);
        setHasKey(data.has_key || false);
      })
      .catch(() => {
        setProvider(null);
        setModel(null);
        setHasKey(false);
      })
      .finally(() => setLoading(false));
  }, []);

  useEffect(() => {
    refresh();
  }, [refresh]);

  return { provider, model, hasKey, loading, refresh };
}
