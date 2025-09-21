/**
 * Generate a color for a chunk based on its index
 * Uses a categorical color palette that cycles every 12 colors
 */

const CHUNK_COLORS = [
  '#e91e63', // Pink
  '#9c27b0', // Purple
  '#673ab7', // Deep Purple
  '#3f51b5', // Indigo
  '#2196f3', // Blue
  '#03a9f4', // Light Blue
  '#00bcd4', // Cyan
  '#009688', // Teal
  '#4caf50', // Green
  '#8bc34a', // Light Green
  '#ff9800', // Orange
  '#ff5722', // Deep Orange
];

export function getChunkColor(index) {
  return CHUNK_COLORS[index % CHUNK_COLORS.length];
}