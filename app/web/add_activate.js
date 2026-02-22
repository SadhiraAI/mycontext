const fs = require("fs");
const p = fs.readFileSync("src/api/client.js", "utf8");
if (!p.includes("activateLicense")) {
  const insert = `

export async function activateLicense(key) {
  const res = await fetch(\`\${API_BASE}/license/activate\`, {
    method: "POST",
    headers: getHeaders(),
    body: JSON.stringify({ key }),
  });
  return handleResponse(res);
}`;
  fs.writeFileSync("src/api/client.js", p.trimEnd() + insert);
  console.log("Added activateLicense");
} else {
  console.log("activateLicense already present");
}
