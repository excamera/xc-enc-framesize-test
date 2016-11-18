#!/bin/bash
run_test()
{
  echo "Running test $3..."
  ./run_test.py $1 $2 output_$3.dat
  gnuplot -e "output_name='$3.png'" plot.gnu
}

echo "Downloading the test vectors..."
./test_vectors/vids/download.sh

echo "Running the tests..."
run_test test_vectors/vids/0.y4m test_vectors/targets/0.txt 0
run_test test_vectors/vids/1.y4m test_vectors/targets/0.txt 1
