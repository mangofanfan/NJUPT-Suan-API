export function getGradientColor() {
  const h = Math.floor(Math.random() * 200 + 20) // 20-220
  const s = Math.floor(Math.random() * 20 + 80) // 70%-100% 饱和度
  const l = Math.floor(Math.random() * 30 + 60) // 60%-90% 亮度
  return `linear-gradient(45deg, hsl(${h}, ${s}%, ${l}%), hsl(${h}, ${s - 20}%, ${l + 10}%))`
}
