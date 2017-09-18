set xlabel "res_num"
set ylabel "Peer_num"
set title "dphub_vs_phub"
set xrange[1:29116]
set yrange[1:700]
set xtics 1,2000,29116
set ytics 1,20,700
set term pdfcairo lw 2 font "Time_New_Roman,8"
set output 'tmp.pdf'
set style line 1 lw 2 lc rgb "F62217"
set style line 2 lw 2 lc rgb "D4A017"
set style line 3 lw 2 lc rgb "2B60DE"
plot "data1" u 4:1 smooth bezier w lp lc 3 lw 2 pt 0 ps 1 t "dphub_num","data1" u 4:2 smooth bezier w lp lc 4 lw 2 pt 0 ps 1 t "phub_num","data1" u 4:3 smooth bezier w lp lc 8 lw 2 pt 0 ps 1 t "repeat_num"
set output
