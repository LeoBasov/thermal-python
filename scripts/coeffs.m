function[c1, c2] = coeffs(T1, T2, r1, r2);
c1 = (T2 - T1) / (log(r2 / r1));
c2 = T1 - c1 * log(r1);
endfunction