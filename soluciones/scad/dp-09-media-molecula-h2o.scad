// DP-09 · Media molécula de agua (imprimir dos y unir)
// Diseño e Impresión 3D en el aula · Pablo Moraga · CC BY-NC-ND 4.0
$fn = 64;
a = 52.25; L = 22;
intersection() {
  union() {
    sphere(d = 20);
    for (s = [-1, 1]) {
      p = [s * L * sin(a), -L * cos(a), 0];
      hull() { sphere(d = 4); translate(p) sphere(d = 4); }
      translate(p) sphere(d = 12);
    }
  }
  translate([-50, -50, 0]) cube([100, 100, 50]);
}
