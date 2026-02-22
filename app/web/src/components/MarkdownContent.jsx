import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import "./MarkdownContent.css";

/**
 * Post-process assembled context text for clean rendering:
 * - Ensure section labels start on their own line
 * - Format constraint lists properly
 * - Add spacing between sections
 */
function ensureSectionBreaks(text) {
  if (!text || typeof text !== "string") return text;
  let out = text;

  // Split "Original: ... Clarified: ..." onto separate lines
  out = out.replace(/(\S)\s+(\*\*Clarified\*\*:\s*|Clarified:\s*)/gi, "$1\n\n**Clarified:** ");

  // Ensure constraint-style labels get their own paragraph
  out = out.replace(/(\S)\s+(Must include:?\s*)/gi, "$1\n\n$2");
  out = out.replace(/(\S)\s+(Must NOT include:?\s*)/gi, "$1\n\n$2");
  out = out.replace(/(\S)\s+(Format rules:?\s*)/gi, "$1\n\n$2");
  out = out.replace(/(\S)\s+(CONSTRAINTS:?\s*)/g, "$1\n\n$2");

  // Promote major section labels to markdown headers
  out = out.replace(/^(CONSTRAINTS):?\s*$/gm, "### Constraints");
  out = out.replace(/^(GUIDANCE):?\s*$/gm, "### Guidance");
  out = out.replace(/^(DIRECTIVE):?\s*$/gm, "### Directive");
  out = out.replace(/^(OUTPUT FORMAT):?\s*$/gm, "### Output Format");
  out = out.replace(/^(Follow these rules):?\s*$/gm, "### Rules");

  // Ensure **Bold Label**: lines get preceding blank line
  out = out.replace(/\n(\s*\*\*[^*]+\*\*:?\s*)/g, "\n\n$1");

  // Turn inline items after constraint labels into bulleted lists
  const listLabels = [/Must include:?\s*/i, /Must NOT include:?\s*/i, /Format rules:?\s*/i];
  for (const re of listLabels) {
    out = out.replace(
      new RegExp(`(${re.source})\\n([\\w_]+(?:\\n[\\w_]+)+)`, re.flags || "gi"),
      (match, prefix, items) => {
        const list = items
          .split("\n")
          .map((i) => i.trim())
          .filter(Boolean)
          .map((i) => `- ${i}`)
          .join("\n");
        return `${prefix}\n${list}`;
      }
    );
  }

  // Ensure numbered steps like "1. " get preceding blank line for proper list rendering
  out = out.replace(/([^\n])\n(\d+\.\s)/g, "$1\n\n$2");

  // Collapse excessive newlines
  out = out.replace(/\n{4,}/g, "\n\n\n");

  return out.trim();
}

export default function MarkdownContent({ content }) {
  if (!content) return null;
  const processed = ensureSectionBreaks(content);
  return (
    <div className="markdown-content">
      <ReactMarkdown remarkPlugins={[remarkGfm]}>{processed}</ReactMarkdown>
    </div>
  );
}
