set xlabel 'Frame Number'
set ylabel 'Size'

set term png size 1280,720
set output output_name


set style line 1 pt 5
set style line 2 pt 7

plot input_name using 1:2 with linespoint t "xc-enc" ls 1, \
             "" using 1:3 with linespoint t "target" ls 2
