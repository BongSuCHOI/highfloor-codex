#!/usr/bin/env node

import fs from "node:fs";

const [graphPath, outputPath] = process.argv.slice(2);
if (!graphPath || !outputPath) {
  process.stderr.write("usage: validate-graph.mjs <graph.json> <report.json>\n");
  process.exit(2);
}

const FILE_LEVEL_TYPES = new Set([
  "file", "config", "document", "service", "pipeline", "table",
  "schema", "resource", "endpoint",
]);

try {
  const graph = JSON.parse(fs.readFileSync(graphPath, "utf8"));
  const issues = [];
  const warnings = [];

  if (!Array.isArray(graph.nodes)) issues.push("graph.nodes is missing or not an array");
  if (!Array.isArray(graph.edges)) issues.push("graph.edges is missing or not an array");
  if (!Array.isArray(graph.layers)) issues.push("graph.layers is missing or not an array");
  if (!Array.isArray(graph.tour)) issues.push("graph.tour is missing or not an array");

  const nodes = Array.isArray(graph.nodes) ? graph.nodes : [];
  const edges = Array.isArray(graph.edges) ? graph.edges : [];
  const layers = Array.isArray(graph.layers) ? graph.layers : [];
  const tour = Array.isArray(graph.tour) ? graph.tour : [];
  const nodeIds = new Set();

  nodes.forEach((node, index) => {
    if (!node || typeof node !== "object") {
      issues.push(`Node[${index}] is not an object`);
      return;
    }
    for (const field of ["id", "type", "name", "summary"]) {
      if (typeof node[field] !== "string" || !node[field]) {
        issues.push(`Node[${index}] missing ${field}`);
      }
    }
    if (!Array.isArray(node.tags) || node.tags.length === 0) {
      issues.push(`Node[${index}] '${node.id ?? "<unknown>"}' missing tags`);
    }
    if (nodeIds.has(node.id)) issues.push(`Duplicate node ID '${node.id}'`);
    if (typeof node.id === "string") nodeIds.add(node.id);
  });

  edges.forEach((edge, index) => {
    if (!edge || typeof edge !== "object") {
      issues.push(`Edge[${index}] is not an object`);
      return;
    }
    if (!nodeIds.has(edge.source)) issues.push(`Edge[${index}] source '${edge.source}' not found`);
    if (!nodeIds.has(edge.target)) issues.push(`Edge[${index}] target '${edge.target}' not found`);
    if (typeof edge.type !== "string" || !edge.type) issues.push(`Edge[${index}] missing type`);
  });

  const layerAssignments = new Map();
  layers.forEach((layer, index) => {
    for (const field of ["id", "name", "description"]) {
      if (typeof layer?.[field] !== "string" || !layer[field]) {
        issues.push(`Layer[${index}] missing ${field}`);
      }
    }
    if (!Array.isArray(layer?.nodeIds)) {
      issues.push(`Layer[${index}] missing nodeIds`);
      return;
    }
    layer.nodeIds.forEach((id) => {
      if (!nodeIds.has(id)) issues.push(`Layer '${layer.id}' refs missing node '${id}'`);
      if (layerAssignments.has(id)) {
        issues.push(`Node '${id}' appears in multiple layers`);
      }
      layerAssignments.set(id, layer.id);
    });
  });

  nodes
    .filter((node) => FILE_LEVEL_TYPES.has(node.type))
    .forEach((node) => {
      if (!layerAssignments.has(node.id)) issues.push(`File node '${node.id}' not in any layer`);
    });

  tour.forEach((step, index) => {
    if (!Number.isInteger(step?.order)) issues.push(`Tour step[${index}] missing integer order`);
    for (const field of ["title", "description"]) {
      if (typeof step?.[field] !== "string" || !step[field]) {
        issues.push(`Tour step[${index}] missing ${field}`);
      }
    }
    if (!Array.isArray(step?.nodeIds)) {
      issues.push(`Tour step[${index}] missing nodeIds`);
      return;
    }
    step.nodeIds.forEach((id) => {
      if (!nodeIds.has(id)) issues.push(`Tour step[${index}] refs missing node '${id}'`);
    });
  });

  const connected = new Set(edges.flatMap((edge) => [edge.source, edge.target]));
  nodes.forEach((node) => {
    if (node.id && !connected.has(node.id)) warnings.push(`Node '${node.id}' has no edges`);
  });

  const countBy = (items, field) => items.reduce((counts, item) => {
    const key = item?.[field] ?? "unknown";
    counts[key] = (counts[key] ?? 0) + 1;
    return counts;
  }, {});

  const stats = {
    totalNodes: nodes.length,
    totalEdges: edges.length,
    totalLayers: layers.length,
    tourSteps: tour.length,
    nodeTypes: countBy(nodes, "type"),
    edgeTypes: countBy(edges, "type"),
  };

  fs.writeFileSync(outputPath, JSON.stringify({ issues, warnings, stats }, null, 2));
} catch (error) {
  process.stderr.write(`${error instanceof Error ? error.message : String(error)}\n`);
  process.exit(1);
}
