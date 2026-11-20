// DP-08 · Ficha táctil en braille: AULA
// Diseño e Impresión 3D en el aula · Pablo Moraga · CC BY-NC-ND 4.0
$fn = 64;
$fn = 24;
cube([40, 30, 3]);
cells = [[1], [1,3,6], [1,2,3], [1]];   // A U L A
x0 = (40 - (3 * 6 + 2.5)) / 2;
function dot(n) = [ (n > 3 ? 2.5 : 0), [17.5, 15, 12.5][(n - 1) % 3] ];
for (c = [0:3]) for (n = cells[c]) translate([x0 + c * 6 + dot(n)[0], dot(n)[1], 3]) scale([1, 1, 0.8]) sphere(r = 0.75);
