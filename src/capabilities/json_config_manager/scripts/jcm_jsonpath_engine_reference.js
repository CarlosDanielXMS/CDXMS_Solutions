// JCM JsonPath Engine v1 — referência de comportamento.
function pathGet(root, path) {
  if (!path || path === '$') return root;
  const normalized = String(path).replace(/^\$\.?/, '');
  const tokens = normalized.replace(/\[(\d+)\]/g, '.$1').split('.').filter(Boolean);
  let current = root;
  for (const token of tokens) {
    if (current == null || !(token in Object(current))) return undefined;
    current = current[token];
  }
  return current;
}
function deepMerge(base, patch, preserveExisting) {
  if (!base || typeof base !== 'object' || Array.isArray(base)) base = {};
  if (!patch || typeof patch !== 'object' || Array.isArray(patch)) return patch;
  const out = Object.assign({}, base);
  Object.keys(patch).forEach(function (key) {
    if (preserveExisting && key in out) return;
    out[key] = (patch[key] && typeof patch[key] === 'object' && !Array.isArray(patch[key]))
      ? deepMerge(out[key], patch[key], preserveExisting)
      : patch[key];
  });
  return out;
}
