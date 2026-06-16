
const ARTIFACT_ID = "json_config_manager";
const VERSION = "1.0.0";
const BASE_PATH = "/storage/emulated/0/Documents/CDXMS_Solutions";

function result(success, status, operation, message, data, error) {
  return JSON.stringify({
    schema_version: 1,
    namespace: "CDXMS",
    success: success === true,
    status: String(status || (success ? "success" : "error")),
    artifact_type: "capability",
    artifact_id: ARTIFACT_ID,
    operation: String(operation || ""),
    message: String(message || ""),
    data: data && typeof data === "object" && !Array.isArray(data) ? data : {},
    error: error || null,
    meta: {
      timestamp: new Date().toISOString(),
      source: "[CDXMS] Json Config Manager",
      version: VERSION,
      json_path_engine: "JCM JsonPath Engine v1"
    }
  });
}
function err(code, message, details, recoverable) {
  return { code: String(code || "UNKNOWN_ERROR"), message: String(message || "Erro desconhecido."), details: details || {}, recoverable: recoverable === true };
}
function fail(operation, code, message, details, recoverable, status) {
  return result(false, status || "error", operation, message, details && details.data ? details.data : {}, err(code, message, details || {}, recoverable));
}
function parseJson(value, name) {
  if (value === null || value === undefined || String(value).trim() === "") {
    throw { code: "INVALID_JSON", message: "JSON vazio em " + name + ".", details: { input: name } };
  }
  try { return JSON.parse(String(value)); }
  catch (e) { throw { code: "INVALID_JSON", message: "JSON inválido em " + name + ".", details: { input: name, reason: String(e.message || e) } }; }
}
function pretty(obj, enabled) { return JSON.stringify(obj, null, enabled ? 2 : 0); }
function isObj(v) { return v && typeof v === "object" && !Array.isArray(v); }
function normalizePath(raw, fallback) {
  let p = String(raw || fallback || "").trim();
  p = p.replace(/\\+/g, "/").replace(/\/+/g, "/");
  if (!p || p === ".") return "";
  if (!p.startsWith("/")) p = BASE_PATH + "/" + p;
  p = p.replace(/\/+/g, "/");
  if (p.endsWith("/") && p.length > 1) p = p.slice(0, -1);
  return p;
}
function safePath(path, allowFile) {
  if (!path) return false;
  if (!path.startsWith(BASE_PATH)) return false;
  if (path.indexOf("..") >= 0) return false;
  if (/[;`$<>|&\r\n]/.test(path)) return false;
  if (allowFile && !/\.json(\.bak)?$/i.test(path)) return false;
  return true;
}
function trimPath(p) { return String(p || "").trim(); }
function quoteString(s) { return '"' + String(s).replace(/\\/g, "\\\\").replace(/"/g, '\\"') + '"'; }
function literalToString(v) { return typeof v === "string" ? quoteString(v) : String(v); }
function splitTopLevel(s, sep) {
  const out = [];
  let buf = "", quote = null, esc = false, depth = 0;
  for (let i=0;i<s.length;i++) {
    const ch = s[i];
    if (esc) { buf += ch; esc = false; continue; }
    if (ch === "\\") { buf += ch; esc = true; continue; }
    if (quote) { buf += ch; if (ch === quote) quote = null; continue; }
    if (ch === "'" || ch === '"') { buf += ch; quote = ch; continue; }
    if (ch === "(" || ch === "[") { depth++; buf += ch; continue; }
    if (ch === ")" || ch === "]") { depth--; buf += ch; continue; }
    if (depth === 0 && s.substr(i, sep.length) === sep) { out.push(buf.trim()); buf = ""; i += sep.length-1; continue; }
    buf += ch;
  }
  if (buf.length || s.length) out.push(buf.trim());
  return out.filter(x => x !== "");
}
function unquote(s) {
  s = String(s || "").trim();
  if ((s[0] === '"' && s[s.length-1] === '"') || (s[0] === "'" && s[s.length-1] === "'")) {
    try { return JSON.parse(s[0] === "'" ? '"' + s.slice(1,-1).replace(/\\'/g, "'").replace(/"/g, '\\"') + '"' : s); }
    catch(e) { return s.slice(1,-1); }
  }
  return s;
}
function parseLiteral(s) {
  s = String(s || "").trim();
  if ((s[0] === '"' && s[s.length-1] === '"') || (s[0] === "'" && s[s.length-1] === "'")) return unquote(s);
  if (/^-?\d+(\.\d+)?$/.test(s)) return Number(s);
  if (s === "true") return true;
  if (s === "false") return false;
  if (s === "null") return null;
  return s;
}
function readIdentifier(path, i) {
  let start = i;
  while (i < path.length && path[i] !== "." && path[i] !== "[") i++;
  return { value: path.slice(start, i).trim(), index: i };
}
function readBracket(path, i) {
  let start = i + 1, quote = null, esc = false, depth = 0;
  i = start;
  for (; i<path.length; i++) {
    const ch = path[i];
    if (esc) { esc = false; continue; }
    if (ch === "\\") { esc = true; continue; }
    if (quote) { if (ch === quote) quote = null; continue; }
    if (ch === "'" || ch === '"') { quote = ch; continue; }
    if (ch === "(" || ch === "[") { depth++; continue; }
    if (ch === ")" || ch === "]") { if (depth > 0) { depth--; continue; } }
    if (ch === "]" && depth === 0) return { value: path.slice(start, i).trim(), index: i + 1 };
  }
  throw { code:"INVALID_JSON_PATH", message:"Json Path inválido: colchete não fechado.", details:{ json_path:path } };
}
function parseBracketToken(inner) {
  inner = inner.trim();
  if (inner === "*") return { type:"wildcard" };
  if (/^-?\d+$/.test(inner)) return { type:"index", index:Number(inner) };
  if (/^-?\d*:-?\d*(?::-?\d+)?$/.test(inner)) {
    const parts = inner.split(":");
    return { type:"slice", start: parts[0] === "" ? null : Number(parts[0]), end: parts[1] === "" ? null : Number(parts[1]), step: parts[2] ? Number(parts[2]) : 1 };
  }
  if (inner.indexOf(",") >= 0) {
    return { type:"union", items: splitTopLevel(inner, ",").map(x => /^-?\d+$/.test(x) ? Number(x) : unquote(x)) };
  }
  if (inner[0] === "?" && inner[1] === "(" && inner[inner.length-1] === ")") return { type:"filter", expr: inner.slice(2,-1).trim(), shortcut:false };
  // CDXMS shortcut: [id="x"], [metadata.id="x"], [enabled=true]
  const m = inner.match(/^([A-Za-z_$][\w$.-]*)\s*(==|=|!=|>=|<=|>|<)\s*(.+)$/);
  if (m) return { type:"filter", expr:"@." + m[1] + " " + (m[2] === "=" ? "==" : m[2]) + " " + m[3], shortcut:true };
  if ((inner[0] === '"' && inner[inner.length-1] === '"') || (inner[0] === "'" && inner[inner.length-1] === "'")) return { type:"child", key: unquote(inner) };
  return { type:"child", key: inner };
}
function parseJsonPath(path) {
  path = trimPath(path);
  if (!path || path === "$" || path === ".") return [];
  if (path[0] !== "$") path = "$" + (path[0] === "[" ? "" : ".") + path;
  let i = 0;
  const tokens = [];
  if (path[i] === "$") i++;
  while (i < path.length) {
    if (path.substr(i,2) === "..") {
      i += 2;
      if (path[i] === "*") { tokens.push({ type:"recursive", key:"*" }); i++; continue; }
      const r = readIdentifier(path, i);
      if (!r.value) throw { code:"INVALID_JSON_PATH", message:"Json Path inválido após '..'.", details:{ json_path:path } };
      tokens.push({ type:"recursive", key:r.value }); i = r.index; continue;
    }
    if (path[i] === ".") {
      i++;
      if (path[i] === "*") { tokens.push({ type:"wildcard" }); i++; continue; }
      const r = readIdentifier(path, i);
      if (!r.value) throw { code:"INVALID_JSON_PATH", message:"Json Path possui propriedade vazia.", details:{ json_path:path } };
      tokens.push({ type:"child", key:r.value }); i = r.index; continue;
    }
    if (path[i] === "[") {
      const b = readBracket(path, i);
      tokens.push(parseBracketToken(b.value)); i = b.index; continue;
    }
    throw { code:"INVALID_JSON_PATH", message:"Json Path possui token inesperado.", details:{ json_path:path, index:i } };
  }
  return tokens;
}
function normalizeJsonPath(path) {
  path = trimPath(path);
  if (!path || path === ".") return "$";
  if (path[0] !== "$") path = "$" + (path[0] === "[" ? "" : ".") + path;
  return path;
}
function getByPath(obj, path) {
  path = String(path || "").trim();
  if (!path || path === "@" || path === "$") return obj;
  path = path.replace(/^@\.?/, "").replace(/^\$\.?/, "");
  if (!path) return obj;
  const parts = path.split(".");
  let cur = obj;
  for (let i=0;i<parts.length;i++) {
    const k = parts[i];
    if (cur === null || cur === undefined) return undefined;
    if (Array.isArray(cur) && /^\d+$/.test(k)) cur = cur[Number(k)];
    else cur = cur[k];
  }
  return cur;
}
function compareValues(left, op, right) {
  if (op === "==" || op === "=") return left === right;
  if (op === "!=") return left !== right;
  if (op === ">") return left > right;
  if (op === "<") return left < right;
  if (op === ">=") return left >= right;
  if (op === "<=") return left <= right;
  return false;
}
function evalSingleFilter(item, expr) {
  expr = expr.trim();
  const m = expr.match(/^(@(?:\.[A-Za-z_$][\w$-]*)*|@)\s*(==|=|!=|>=|<=|>|<)\s*(.+)$/);
  if (m) return compareValues(getByPath(item, m[1]), m[2], parseLiteral(m[3]));
  const exists = expr.match(/^@(?:\.[A-Za-z_$][\w$-]*)+$/);
  if (exists) return !!getByPath(item, expr);
  return false;
}
function evalFilter(item, expr) {
  const orParts = splitTopLevel(expr, "||");
  for (let i=0;i<orParts.length;i++) {
    const andParts = splitTopLevel(orParts[i], "&&");
    let ok = true;
    for (let j=0;j<andParts.length;j++) if (!evalSingleFilter(item, andParts[j])) { ok = false; break; }
    if (ok) return true;
  }
  return false;
}
function childRef(ref, key) {
  const v = ref.value;
  if (v !== null && v !== undefined && Object.prototype.hasOwnProperty.call(Object(v), key)) return { parent:v, key:key, value:v[key], path: ref.path + (String(key).match(/^[A-Za-z_$][\w$]*$/) ? "." + key : "[" + quoteString(key) + "]") };
  return null;
}
function indexRef(ref, idx) {
  const v = ref.value;
  if (!Array.isArray(v)) return null;
  if (idx < 0) idx = v.length + idx;
  if (idx < 0 || idx >= v.length) return null;
  return { parent:v, key:idx, value:v[idx], path: ref.path + "[" + idx + "]" };
}
function descendants(ref, key, out) {
  const v = ref.value;
  if (v === null || typeof v !== "object") return;
  const keys = Array.isArray(v) ? v.map((_,i)=>i) : Object.keys(v);
  for (let i=0;i<keys.length;i++) {
    const k = keys[i];
    const child = { parent:v, key:k, value:v[k], path: ref.path + (typeof k === "number" ? "["+k+"]" : (String(k).match(/^[A-Za-z_$][\w$]*$/) ? "."+k : "["+quoteString(k)+"]")) };
    if (key === "*" || k === key) out.push(child);
    descendants(child, key, out);
  }
}
function evaluate(root, path) {
  const normalized = normalizeJsonPath(path);
  const tokens = parseJsonPath(path);
  let refs = [{ parent:null, key:null, value:root, path:"$" }];
  for (let t=0;t<tokens.length;t++) {
    const token = tokens[t];
    const next = [];
    for (let r=0;r<refs.length;r++) {
      const ref = refs[r];
      const v = ref.value;
      if (token.type === "child") { const c = childRef(ref, token.key); if (c) next.push(c); }
      else if (token.type === "index") { const c = indexRef(ref, token.index); if (c) next.push(c); }
      else if (token.type === "wildcard") {
        if (Array.isArray(v)) for (let i=0;i<v.length;i++) next.push({ parent:v, key:i, value:v[i], path:ref.path+"["+i+"]" });
        else if (v && typeof v === "object") Object.keys(v).forEach(k => next.push({ parent:v, key:k, value:v[k], path:ref.path+(k.match(/^[A-Za-z_$][\w$]*$/)?"."+k:"["+quoteString(k)+"]") }));
      }
      else if (token.type === "union") {
        token.items.forEach(it => { const c = typeof it === "number" ? indexRef(ref, it) : childRef(ref, it); if (c) next.push(c); });
      }
      else if (token.type === "slice") {
        if (Array.isArray(v)) {
          const len = v.length, step = token.step || 1;
          let start = token.start === null ? (step > 0 ? 0 : len-1) : (token.start < 0 ? len + token.start : token.start);
          let end = token.end === null ? (step > 0 ? len : -1) : (token.end < 0 ? len + token.end : token.end);
          for (let i=start; step > 0 ? i<end : i>end; i += step) { const c = indexRef(ref, i); if (c) next.push(c); }
        }
      }
      else if (token.type === "filter") {
        if (Array.isArray(v)) {
          for (let i=0;i<v.length;i++) {
            if (evalFilter(v[i], token.expr)) next.push({ parent:v, key:i, value:v[i], path:ref.path+"["+i+"]" });
          }
        } else if (v && typeof v === "object") {
          Object.keys(v).forEach(k => {
            if (evalFilter(v[k], token.expr)) next.push({ parent:v, key:k, value:v[k], path:ref.path+(k.match(/^[A-Za-z_$][\w$]*$/)?"."+k:"["+quoteString(k)+"]") });
          });
        }
      }
      else if (token.type === "recursive") descendants(ref, token.key, next);
    }
    refs = next;
  }
  return { json_path: trimPath(path) || "$", normalized_json_path: normalized, match_count: refs.length, found: refs.length > 0, refs: refs, values: refs.map(r => r.value), paths: refs.map(r => r.path) };
}
function tokenIsDeterministic(t) { return t.type === "child" || t.type === "index"; }
function canCreatePath(path) { return parseJsonPath(path).every(tokenIsDeterministic); }
function createPathAndSet(root, path, value) {
  const tokens = parseJsonPath(path);
  if (!tokens.length) return value;
  if (!tokens.every(tokenIsDeterministic)) throw { code:"JSON_PATH_CREATE_NOT_SUPPORTED", message:"Criação automática só é suportada para caminhos determinísticos sem filtro, wildcard, union, slice ou recursão.", details:{ json_path:path } };
  let obj = (root && typeof root === "object") ? root : {};
  let cur = obj;
  for (let i=0;i<tokens.length-1;i++) {
    const t = tokens[i], next = tokens[i+1];
    if (t.type === "child") {
      if (cur[t.key] === undefined || cur[t.key] === null || typeof cur[t.key] !== "object") cur[t.key] = next.type === "index" ? [] : {};
      cur = cur[t.key];
    } else if (t.type === "index") {
      if (!Array.isArray(cur)) throw { code:"JSON_PATH_TARGET_NOT_ARRAY", message:"O caminho esperava array para criação por índice.", details:{ json_path:path } };
      if (cur[t.index] === undefined || cur[t.index] === null || typeof cur[t.index] !== "object") cur[t.index] = next.type === "index" ? [] : {};
      cur = cur[t.index];
    }
  }
  const last = tokens[tokens.length-1];
  if (last.type === "child") cur[last.key] = value;
  else if (last.type === "index") {
    if (!Array.isArray(cur)) throw { code:"JSON_PATH_TARGET_NOT_ARRAY", message:"O caminho esperava array no último índice.", details:{ json_path:path } };
    cur[last.index] = value;
  }
  return obj;
}
function setAtJsonPath(root, path, value) {
  const p = trimPath(path);
  if (!p || p === "$" || p === ".") return { root:value, matched_path:"$", created:false };
  const q = evaluate(root, p);
  if (q.match_count > 1) throw { code:"JSON_PATH_AMBIGUOUS_MATCH", message:"O caminho informado encontrou mais de um item e a escrita foi bloqueada.", details:{ json_path:p, match_count:q.match_count, matches:q.paths } };
  if (q.match_count === 1) {
    const r = q.refs[0];
    if (r.parent === null) return { root:value, matched_path:"$", created:false };
    r.parent[r.key] = value;
    return { root:root, matched_path:r.path, created:false };
  }
  if (!canCreatePath(p)) throw { code:"JSON_PATH_NOT_FOUND", message:"Caminho JSON não encontrado e não é possível criá-lo automaticamente.", details:{ json_path:p } };
  return { root:createPathAndSet(root, p, value), matched_path:normalizeJsonPath(p), created:true };
}
function deepMerge(base, incoming, preserve) {
  if (!isObj(base) || !isObj(incoming)) return preserve ? base : incoming;
  const out = Array.isArray(base) ? base.slice() : { ...base };
  Object.keys(incoming).forEach(k => {
    if (isObj(out[k]) && isObj(incoming[k])) out[k] = deepMerge(out[k], incoming[k], preserve);
    else if (!(preserve && Object.prototype.hasOwnProperty.call(out, k))) out[k] = incoming[k];
  });
  return out;
}
function mergeAtJsonPath(root, path, incoming, strategy) {
  const p = trimPath(path);
  if (strategy === "replace") return setAtJsonPath(root, p, incoming);
  if (!isObj(incoming)) throw { code:"JSON_PATH_TARGET_NOT_OBJECT", message:"merge_json exige Value Json do tipo objeto quando a estratégia não é replace.", details:{ strategy:strategy } };
  const q = evaluate(root, p);
  if (q.match_count > 1) throw { code:"JSON_PATH_AMBIGUOUS_MATCH", message:"O caminho informado encontrou mais de um item e o merge foi bloqueado.", details:{ json_path:p || "$", match_count:q.match_count, matches:q.paths } };
  if (q.match_count === 0) {
    if (!p || p === "$" || p === ".") return { root: deepMerge({}, incoming, strategy === "preserve_existing"), matched_path:"$", created:true };
    if (!canCreatePath(p)) throw { code:"JSON_PATH_NOT_FOUND", message:"Caminho JSON não encontrado e não é possível criá-lo automaticamente para merge.", details:{ json_path:p } };
    return setAtJsonPath(root, p, incoming);
  }
  const current = q.refs[0].value;
  if (!isObj(current)) throw { code:"JSON_PATH_TARGET_NOT_OBJECT", message:"O alvo de merge_json precisa ser um objeto JSON.", details:{ json_path:p || "$", matched_path:q.paths[0], actual_type:Array.isArray(current)?"array":typeof current } };
  const merged = deepMerge(current, incoming, strategy === "preserve_existing");
  const r = q.refs[0];
  if (r.parent === null) return { root:merged, matched_path:"$", created:false };
  r.parent[r.key] = merged;
  return { root:root, matched_path:r.path, created:false };
}
function selectedData(filePath, jsonPath, q) {
  const one = q.match_count === 1 ? q.values[0] : null;
  return {
    file_path: filePath,
    json_path: jsonPath || "$",
    normalized_json_path: q.normalized_json_path,
    found: q.found,
    match_count: q.match_count,
    matched_paths: q.paths,
    value: one,
    values: q.values,
    content: q.match_count === 1 ? one : q.values
  };
}
function errorResult(operation, e, fallbackMessage) {
  const code = e && e.code ? e.code : "PROCESSING_FAILED";
  const msg = e && e.message ? e.message : (fallbackMessage || "Falha de processamento.");
  return result(false, code === "JSON_PATH_NOT_FOUND" ? "not_found" : "error", operation, msg, {}, err(code, msg, e && e.details ? e.details : {}, true));
}
