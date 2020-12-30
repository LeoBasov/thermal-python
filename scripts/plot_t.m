function plot_t(T1, T2, r1, r2, n);
[ c1, c2 ] = coeffs(T1, T2, r1, r2);
r = linspace(r1, r2, n);
T = c1 * log(r) + c2;

plot(r, T);
endfunction